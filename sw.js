/* Offline support. New version: change VERSION (done automatically by the build). */
const VERSION='20261113-1811';const CACHE='sprak-'+VERSION;
const FILES=['./','./index.html','./manifest.webmanifest','./icon-192.png','./icon-512.png','./icon-maskable-512.png','./apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k!=='sprak-audio').map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET')return;
  if(r.mode==='navigate'||r.url.endsWith('/index.html')){ /* network first: always newest version when online */
    e.respondWith(fetch(r).then(res=>{const cp=res.clone();caches.open(CACHE).then(c=>c.put('./index.html',cp));return res}).catch(()=>caches.match('./index.html')));return}
  if(r.url.indexOf('/audio/')>=0&&r.url.slice(-4)==='.mp3'){ /* audio: cache after first play */
    e.respondWith(caches.open('sprak-audio').then(c=>c.match(r).then(m=>m||fetch(r).then(res=>{if(res.ok)c.put(r,res.clone());return res}))));return}
  e.respondWith(caches.match(r).then(m=>m||fetch(r)))});
