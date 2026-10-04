[CmdletBinding()]
param(
    [string]$HostName = "ftp.itdks.tech",
    [int]$Port = 21,
    [string]$UserName = "u312639377.itd",
    [string]$RemoteRoot = ".",
    [string]$LocalRoot = "",
    [switch]$DryRun,
    [switch]$TestLogin,
    [switch]$NoTls
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$HostName = $HostName.Trim() -replace "^ftp://", ""
$HostName = $HostName.TrimEnd("/")
$RemoteRoot = $RemoteRoot.Trim().Trim("/")
if ([string]::IsNullOrWhiteSpace($LocalRoot)) {
    $LocalRoot = if ($PSScriptRoot) {
        $PSScriptRoot
    }
    else {
        Split-Path -Parent $MyInvocation.MyCommand.Path
    }
}
$LocalRootPath = (Resolve-Path -LiteralPath $LocalRoot).Path
$RootPrefix = $LocalRootPath.TrimEnd("\", "/") + [System.IO.Path]::DirectorySeparatorChar
$UseTls = -not $NoTls

$ParsedHostIp = $null
if ($UseTls -and [System.Net.IPAddress]::TryParse($HostName, [ref]$ParsedHostIp)) {
    throw @"
TLS certificate checks can fail when HostName is an IP address.

Use the FTP hostname instead:
  .\deploy-hostinger.cmd -HostName ftp.itdks.tech

Or, only if Hostinger requires plain FTP for this account, rerun with:
  .\deploy-hostinger.cmd -HostName $HostName -NoTls
"@
}

$ExcludedDirectories = @(
    ".git",
    ".claude",
    ".codex",
    ".cache",
    ".next",
    "node_modules",
    "dist",
    "build"
)

$ExcludedFiles = @(
    "deploy-hostinger.ps1",
    "README.md",
    "deploy-hostinger.cmd",
    "DEPLOY.md",
    "deploy-ready.zip",
    "stats-admin-qa.png"
)

$ExcludedPatterns = @(
    ".env",
    ".env.*",
    "*.log",
    "*.tmp",
    "*.bak"
)

function Test-IsExcluded {
    param(
        [string]$RelativePath
    )

    $parts = $RelativePath -split "/"
    foreach ($part in $parts) {
        if ($ExcludedDirectories -contains $part) {
            return $true
        }
    }

    $leaf = $parts[-1]
    if ($ExcludedFiles -contains $leaf) {
        return $true
    }

    foreach ($pattern in $ExcludedPatterns) {
        if ($leaf -like $pattern -or $RelativePath -like $pattern) {
            return $true
        }
    }

    return $false
}

function Get-UploadFiles {
    $items = New-Object System.Collections.Generic.List[object]

    Get-ChildItem -LiteralPath $LocalRootPath -Recurse -File -Force | ForEach-Object {
        $relativePath = $_.FullName.Substring($RootPrefix.Length).Replace("\", "/")

        if (-not (Test-IsExcluded -RelativePath $relativePath)) {
            $items.Add([pscustomobject]@{
                LocalPath = $_.FullName
                RelativePath = $relativePath
                RemotePath = "$RemoteRoot/$relativePath"
            }) | Out-Null
        }
    }

    return $items | Sort-Object RelativePath
}

function ConvertTo-FtpUri {
    param(
        [string]$RemotePath
    )

    $escapedPath = (($RemotePath -split "/") | ForEach-Object {
        [System.Uri]::EscapeDataString($_)
    }) -join "/"

    return "ftp://$($HostName):$Port/$escapedPath"
}

function Invoke-CurlUpload {
    param(
        [object]$Item
    )

    $uri = ConvertTo-FtpUri -RemotePath $Item.RemotePath
    $arguments = @(
        "--fail",
        "--show-error",
        "--silent",
        "--globoff",
        "--ftp-create-dirs",
        "--connect-timeout",
        "20",
        "--max-time",
        "180",
        "--user",
        "$UserName`:$script:Password",
        "--upload-file",
        $Item.LocalPath,
        $uri
    )

    if ($UseTls) {
        $arguments = @("--ssl-reqd") + $arguments
    }

    & $script:CurlPath @arguments
    if ($LASTEXITCODE -ne 0) {
        if ($LASTEXITCODE -eq 67) {
            throw @"
FTP login was rejected by Hostinger with 530 Access denied.

Check that the FTP username and FTP password match the exact FTP account in Hostinger.
You can test the alternate username you provided earlier with:
  .\deploy-hostinger.cmd -NoTls -TestLogin -UserName u312639377.ITD
"@
        }

        if ($UseTls -and $LASTEXITCODE -eq 60) {
            throw @"
Upload failed for $($Item.RelativePath) because the FTP server certificate did not match the hostname.

For this Hostinger FTP endpoint, rerun with plain FTP:
  .\deploy-hostinger.cmd -NoTls
"@
        }

        throw "Upload failed for $($Item.RelativePath) with curl exit code $LASTEXITCODE."
    }
}

function Invoke-CurlLoginTest {
    $uri = ConvertTo-FtpUri -RemotePath $RemoteRoot
    if (-not $uri.EndsWith("/")) {
        $uri = "$uri/"
    }

    $arguments = @(
        "--fail",
        "--show-error",
        "--silent",
        "--globoff",
        "--connect-timeout",
        "20",
        "--max-time",
        "60",
        "--user",
        "$UserName`:$script:Password",
        $uri
    )

    if ($UseTls) {
        $arguments = @("--ssl-reqd") + $arguments
    }

    & $script:CurlPath @arguments | Out-Host
    if ($LASTEXITCODE -eq 67) {
        throw @"
FTP login was rejected by Hostinger with 530 Access denied.

Try the other FTP username you shared:
  .\deploy-hostinger.cmd -NoTls -TestLogin -UserName u312639377.ITD

If that also fails, reset the FTP password in Hostinger for this exact FTP account, then set HOSTINGER_FTP_PASSWORD again with single quotes.
"@
    }

    if ($LASTEXITCODE -ne 0) {
        throw "FTP login test failed with curl exit code $LASTEXITCODE."
    }

    Write-Host "Login test passed for $UserName at ftp://$($HostName):$Port/$RemoteRoot"
}

if ([string]::IsNullOrWhiteSpace($RemoteRoot)) {
    throw "RemoteRoot cannot be empty."
}

$files = @(Get-UploadFiles)

if ($DryRun) {
    Write-Host "Dry run: $($files.Count) files would upload to ftp://$($HostName):$Port/$RemoteRoot"
    foreach ($file in $files) {
        Write-Host "  $($file.RelativePath)"
    }
    exit 0
}

$script:Password = $env:HOSTINGER_FTP_PASSWORD
if ([string]::IsNullOrWhiteSpace($script:Password)) {
    throw @'
Missing HOSTINGER_FTP_PASSWORD.

Set it for this PowerShell session, then run the deploy again:
  $env:HOSTINGER_FTP_PASSWORD = 'your-ftp-password'
  .\deploy-hostinger.cmd

Use single quotes if the password contains special characters like `$`.
'@
}

$script:CurlPath = (Get-Command curl.exe -ErrorAction Stop).Source

if ($TestLogin) {
    Write-Host "Testing FTP login for $UserName at ftp://$($HostName):$Port/$RemoteRoot"
    if ($UseTls) {
        Write-Host "Using FTP over TLS. If Hostinger shows a certificate/principal-name error, rerun with -NoTls."
    }
    else {
        Write-Host "Using plain FTP because -NoTls was provided."
    }
    Invoke-CurlLoginTest
    exit 0
}

Write-Host "Uploading $($files.Count) files to ftp://$($HostName):$Port/$RemoteRoot"
if ($UseTls) {
    Write-Host "Using FTP over TLS. If Hostinger shows a certificate/principal-name error, rerun with -NoTls."
}
else {
    Write-Host "Using plain FTP because -NoTls was provided."
}

$index = 0
foreach ($file in $files) {
    $index++
    Write-Host ("[{0}/{1}] {2}" -f $index, $files.Count, $file.RelativePath)
    Invoke-CurlUpload -Item $file
}

Write-Host "Done. Uploaded $($files.Count) files."
