// Sweep a footless gait spec (k2.js footlessLegs) per parameter set: dry build, sampled at 120 fps, no upload.
// usage: node fsweep.mjs <spec.js> '[{...K.P overrides}, ...]'   (MODEL=file.bbmodel for a saved model)
// Columns (spec bone names; knee = bone flex incl. rest, + = bent):
//   knee      knee range, both legs, whole cycle      plantKnee  knee range while the leg is planted
//   pitch     the planted block's pitch range (deg, + = toe up / rolling on the heel, - = heel up / on the toe)
//   flat      share of the stance with the block within 3 deg of flat
//   thigh     thigh x range        err  worst IK error (px; > 0.05: a planted edge doesn't reach its ground point)
//   low       lowest point of the blocks' bottoms (< -0.05 sinks)      step / kink  biggest knee change / 2nd difference
import * as B from './bb.mjs';
import fs from 'node:fs';
const [file,cs='[{}]']=process.argv.slice(2);
let m;if(process.env.MODEL)m=JSON.parse(fs.readFileSync(process.env.MODEL,'utf8'));else{await B.connect();m=await B.model();}
for(const P of JSON.parse(cs)){const r=await B.build(file,m,{dry:true,K:{P}});const spec=r.spec,K=r.K,rig=K.rig,L=K.L;
  const N=Math.round(spec.length*120),R={knee:[999,-999],pk:[999,-999],pitch:[999,-999],thigh:[999,-999]};let low=99,step=0,kink=0,flat=0,planted=0;
  const prev={},pp={};K.DIAG.err=0;const ext=(a,v)=>{a[0]=Math.min(a[0],v);a[1]=Math.max(a[1],v);};
  for(let i=0;i<=N;i++){const Q=spec.sample(spec.length*i/N);const W=L.fk(rig,Q);
    for(const s of ['r','l']){const S=K.SIDE[s];const k=-(Q[S.shin].r[0]+rig.bones[S.shin].rest[0]);
      ext(R.knee,k);ext(R.thigh,Q[S.leg].r[0]+rig.bones[S.leg].rest[0]);low=Math.min(low,K.shinLow(Q,s));
      if(K.DIAG.edge[s]!=='swing'){planted++;ext(R.pk,k);const h=L.xf(W[S.shin],K.EDGE[s].heel),t=L.xf(W[S.shin],K.EDGE[s].toe);
        const p=Math.atan2(t[1]-h[1],Math.hypot(t[0]-h[0],t[2]-h[2]))*180/Math.PI;ext(R.pitch,p);if(Math.abs(p)<3)flat++;}
      if(prev[s]!=null){step=Math.max(step,Math.abs(k-prev[s]));if(pp[s]!=null)kink=Math.max(kink,Math.abs(k-2*prev[s]+pp[s]));pp[s]=prev[s];}prev[s]=k;}}
  const f=a=>a[0]>a[1]?'-':a.map(x=>x.toFixed(0)).join('..');
  console.log(JSON.stringify(P),'knee',f(R.knee),'plantKnee',f(R.pk),'pitch',f(R.pitch),'flat',(flat/Math.max(1,planted)).toFixed(2),'thigh',f(R.thigh),
    'err',K.DIAG.err.toFixed(2),'low',low.toFixed(2),'step',step.toFixed(1),'kink',kink.toFixed(1));}
