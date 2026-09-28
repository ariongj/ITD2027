# Hostinger Deployment

This folder can be deployed to Hostinger with `deploy-hostinger.ps1`.

## Current FTP target

- Host: `ftp.itdks.tech`
- FTP IP: `82.198.227.132`
- Port: `21`
- User: `u312639377.itd`
- Remote folder: `.`

This FTP account opens directly inside `/home/u312639377/domains/itdks.tech/public_html`, so the deploy path is `.`.

## Deploy

Set the FTP password only in the current PowerShell session:

```powershell
$env:HOSTINGER_FTP_PASSWORD = 'your-ftp-password'
```

Use single quotes. PowerShell changes passwords containing `$` when they are placed inside double quotes.

Preview what will upload:

```powershell
.\deploy-hostinger.cmd -DryRun
```

Test FTP login without uploading:

```powershell
.\deploy-hostinger.cmd -NoTls -TestLogin
```

Upload the website:

```powershell
.\deploy-hostinger.cmd
```

The script tries FTP over TLS first. If Hostinger rejects TLS for this FTP account, use plain FTP:

```powershell
.\deploy-hostinger.cmd -NoTls
```

If you see this error, use `-NoTls`:

```text
schannel: SNI or certificate check failed: SEC_E_WRONG_PRINCIPAL
```

If you see `530 Access denied`, Hostinger rejected the username or password. Try the other FTP username that was provided:

```powershell
.\deploy-hostinger.cmd -NoTls -TestLogin -UserName u312639377.ITD
```

Use `ftp.itdks.tech` for TLS. The IP `82.198.227.132` points to the same server, but TLS certificate checks can fail when connecting to the raw IP.

Recommended workflow: edit locally, test locally, then run the deploy script after the change is confirmed.

## Shared site data

Public contact details, the Formspree endpoint, booking URL, and asset versions are stored in `site.config.json`. After changing that file, regenerate the static pages with:

```powershell
node .\scripts\sync-site.mjs
```

The generated HTML remains ordinary static hosting output. The `scripts`, `tests`, `backups`, and `site.config.json` files are intentionally excluded from the public upload.

Before launch, sign in to Formspree and confirm that form `xpqypezj` delivers to `info@itdks.tech`. This recipient is configured in Formspree and cannot be verified from the website files.

## AI chat key

The website chat uses `/chat.php`, which reads the existing OpenAI key from the server as `OPENAI_API_KEY`.

Preferred setup: add `OPENAI_API_KEY` in the Hostinger/server environment. If the hosting plan does not expose environment variables, create a `.env` file manually on the server inside `public_html`:

```text
OPENAI_API_KEY=your-existing-key
ITD_OPENAI_MODEL=gpt-4.1-mini
```

The deploy script intentionally excludes `.env` files, so this secret is not uploaded from the local folder. `.htaccess` also blocks `.env` files from web access.

The chat stores only content-free diagnostic metadata for up to 14 days. Raw visitor and assistant message text is not retained in `stats/storage/chat.jsonl`.

By default, chat rate limiting uses the direct server address and ignores visitor-controlled forwarding headers. If the site is later placed behind a trusted reverse proxy, configure only that proxy's exact network ranges:

```text
ITD_TRUSTED_PROXY_CIDRS=192.0.2.10/32,2001:db8:1234::/48
```

Do not set this value to broad public ranges.
