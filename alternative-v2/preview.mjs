import http from 'node:http';
import {readFile, stat} from 'node:fs/promises';
import {resolve, dirname, extname, sep} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)), 'site');
const port=8790;
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.png':'image/png','.webp':'image/webp','.txt':'text/plain; charset=utf-8','.ttf':'font/ttf','.svg':'image/svg+xml'};
http.createServer(async(req,res)=>{
 const headers={'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','X-Robots-Tag':'noindex, nofollow','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self'; connect-src https://formspree.io; form-action https://formspree.io; frame-ancestors 'none'; base-uri 'none'"};
 try {
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,headers);return res.end();}
  let pathname=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(pathname==='/')pathname='/index.html';
  const path=resolve(root,'.'+pathname);
  if(!path.startsWith(root+sep)||pathname.split('/').some(s=>s.startsWith('.'))||!mime[extname(path)])throw Error('Forbidden');
  await stat(path);
  res.writeHead(200,{...headers,'Content-Type':mime[extname(path)]});
  res.end(req.method==='HEAD'?undefined:await readFile(path));
 }catch{
  res.writeHead(404,{...headers,'Content-Type':'text/html; charset=utf-8'});
  res.end(req.method==='HEAD'?undefined:await readFile(resolve(root,'404.html')));
 }
}).listen(port,'127.0.0.1',()=>console.log('IT Department alternative preview: http://127.0.0.1:'+port));

