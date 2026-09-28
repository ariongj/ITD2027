[CmdletBinding()]
param([string]$ReleaseName = "ITD-Hostinger-SEO-Mobile-2026-09-08", [switch]$TrackingPatch)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
if ($ReleaseName -notmatch '^[A-Za-z0-9-]+$') { throw "Use a simple release name." }
$archive = Join-Path $root "$ReleaseName.zip"
$stage = Join-Path $root "deploy-ready-$ReleaseName"
if ((Test-Path -LiteralPath $archive) -or (Test-Path -LiteralPath $stage)) { throw "Release already exists; use a new name to preserve it." }
$publicNames = @(".htaccess", "robots.txt", "sitemap.xml", "llms.txt", "llms-full.txt", "site.webmanifest")
$files = @(Get-ChildItem -LiteralPath $root -File -Force | Where-Object {
    $_.Name -in $publicNames -or $_.Extension -in @(".html", ".css", ".js", ".php") -or $_.Name -like "logo-*.png" -or $_.Name -like "logo-*.webp"
})
if ($TrackingPatch) {
    # Upgrade-only: never overwrite production credentials, PHP or collected data.
    $trackingFiles = @("app.js", "app-lite.js", "app.min.js", "app-lite.min.js", "analytics-config.js", "analytics.js", "analytics.min.js", "consent.js")
    $files = @(Get-ChildItem -LiteralPath $root -File | Where-Object { $_.Extension -eq ".html" -or $_.Name -in $trackingFiles })
} else {
$files += @(Get-ChildItem -LiteralPath (Join-Path $root "assets") -Recurse -File | Where-Object {
    $_.FullName -notmatch '[\\/]creative[\\/].*\.(?:png|jpg)$'
})
$files += @(Get-ChildItem -LiteralPath (Join-Path $root "stats") -File -Force)
$files += Get-Item -LiteralPath (Join-Path $root "stats\storage\.htaccess") -Force
}
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$null = New-Item -ItemType Directory -Path $stage
$zip = [System.IO.Compression.ZipFile]::Open($archive, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in ($files | Sort-Object FullName)) {
        $relative = $file.FullName.Substring($root.Length + 1)
        if ($relative -match '(?:^|[\\/])\.env|\.(?:zip|log|jsonl|bak)$|[\\/]storage[\\/](?!\.htaccess$)') { throw "Private file rejected: $relative" }
        $destination = Join-Path $stage $relative
        $null = New-Item -ItemType Directory -Path (Split-Path -Parent $destination) -Force
        Copy-Item -LiteralPath $file.FullName -Destination $destination
        $entry = [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $destination, $relative.Replace("\", "/"), [System.IO.Compression.CompressionLevel]::Optimal)
        # Normal public-file mode for Linux shared hosting (0644).
        $entry.ExternalAttributes = (0x81A4 -shl 16)
    }
} finally { $zip.Dispose() }
# .NET on Windows marks entries as DOS even when Unix modes are supplied.
# Set the creator OS in each central-directory record so Linux unzip honors 0644.
$zipBytes = [System.IO.File]::ReadAllBytes($archive)
$endOffset = $zipBytes.Length - 22
if ([BitConverter]::ToUInt32($zipBytes, $endOffset) -ne 0x06054b50) { throw "Unexpected ZIP end record." }
$entryCount = [BitConverter]::ToUInt16($zipBytes, $endOffset + 10)
$centralOffset = [int][BitConverter]::ToUInt32($zipBytes, $endOffset + 16)
for ($i = 0; $i -lt $entryCount; $i++) {
    if ([BitConverter]::ToUInt32($zipBytes, $centralOffset) -ne 0x02014b50) { throw "Invalid ZIP central directory." }
    $zipBytes[($centralOffset + 5)] = 3
    $centralOffset += 46 + [BitConverter]::ToUInt16($zipBytes, $centralOffset + 28) + [BitConverter]::ToUInt16($zipBytes, $centralOffset + 30) + [BitConverter]::ToUInt16($zipBytes, $centralOffset + 32)
}
if ($centralOffset -ne $endOffset) { throw "Unexpected ZIP directory length." }
[System.IO.File]::WriteAllBytes($archive, $zipBytes)
$hash = (Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash
Write-Output "Packaged $($files.Count) files."
Write-Output "Archive: $archive"
Write-Output "Preview: $stage"
Write-Output "SHA256: $hash"
