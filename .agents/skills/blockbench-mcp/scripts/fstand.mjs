// Footless legs in any spec (dry build, 60 fps): per leg the knee flex range, the planted block's pitch range (+ toe up)
// and the lowest point of the blocks' bottoms. usage: node fstand.mjs spec.js ['{"P":{...},"MODE":"..."}']
import * as B from './bb.mjs';
await B.connect();const m=await B.model();
const [file,kj='{}']=process.argv.slice(2);
const r=await B.build(file,m,{dry:true,K:JSON.parse(kj)});const spec=r.spec,K=r.K,rig=K.rig,L=K.L;
const N=Math.max(2,Math.round(spec.length*60)),R={};let low=99,lowT=0;
for(let i=0;i<=N;i++){const t=spec.length*i/N,Q=spec.sample(t),W=L.fk(rig,Q);
  for(const s of ['r','l']){const S=K.SIDE[s],k=-(((Q[S.shin]||{}).r||[0])[0]+rig.bones[S.shin].rest[0]);
    const h=L.xf(W[S.shin],K.EDGE[s].heel),to=L.xf(W[S.shin],K.EDGE[s].toe),p=Math.atan2(to[1]-h[1],Math.hypot(to[0]-h[0],to[2]-h[2]))*180/Math.PI;
    const o=R[s]=R[s]||{k:[999,-999],p:[999,-999]};o.k=[Math.min(o.k[0],k),Math.max(o.k[1],k)];
    if(Math.min(h[1],to[1])<0.3)o.p=[Math.min(o.p[0],p),Math.max(o.p[1],p)];
    const lo=K.shinLow(Q,s);if(lo<low){low=lo;lowT=t;}}}
const f=a=>a[0]>a[1]?'-':a.map(x=>x.toFixed(0)).join('..');
console.log(file.split('/').pop(),kj,'R knee',f(R.r.k),'pitch',f(R.r.p),'| L knee',f(R.l.k),'pitch',f(R.l.p),'| low',low.toFixed(2),'@',lowT.toFixed(2));
