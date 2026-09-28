// Local UI preview only. PHP endpoints deliberately remain unavailable.
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { resolve, extname, sep } from "node:path";
const root = resolve(process.argv[2] || ".");
const port = 8787;
const types = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".xml": "application/xml", ".txt": "text/plain", ".webmanifest": "application/manifest+json", ".woff2": "font/woff2" };
createServer(async (req, res) => {
  try {
    const path = decodeURIComponent(new URL(req.url, "http://localhost").pathname);
    if (path.endsWith(".php")) {
      res.writeHead(503, { "Content-Type": "application/json" });
      return res.end(JSON.stringify({ error: "PHP endpoints are unavailable in this local UI preview." }));
    }
    const route = path === "/" ? "/index.html" : path === "/en" || path === "/de" ? `/index-${path.slice(1)}.html` : path;
    const target = resolve(root, `.${extname(route) ? route : `${route}.html`}`);
    if (!target.startsWith(root + sep) || /[\\/]\.|[\\/](?:scripts|tests|stats|backups|deploy-ready)/i.test(target.slice(root.length)) || !types[extname(target)]) throw new Error("Private path");
    await stat(target);
    res.writeHead(200, { "Content-Type": types[extname(target)], "Cache-Control": "no-store" });
    res.end(await readFile(target));
  } catch {
    res.writeHead(404, { "Content-Type": "text/html; charset=utf-8" });
    res.end(await readFile(resolve(root, "404.html")));
  }
}).listen(port, "127.0.0.1", () => console.log(`ITD UI preview: http://127.0.0.1:${port} (${root})`));
