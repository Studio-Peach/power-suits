// walk_back = the walk played backwards (backing up, SuitAnimator): the walk spec baked, its keys mirrored in time
// (t -> length - t; Catmull-Rom curves stay the same curves) and uploaded as animation.marine.walk_back.
// usage (repo root, Blockbench open): node model/anim/walk_back.mjs     Re-run whenever the walk is re-baked.
import * as B from '../../.agents/skills/blockbench-mcp/scripts/bb.mjs';
await B.connect();
const m=await B.model();
const r=await B.build('model/anim/a_walk.js',m,{dry:true});
const L=r.spec.length,rev=chs=>chs.map(c=>({...c,keys:c.keys.map(k=>({...k,time:+(L-k.time).toFixed(6)})).sort((a,b)=>a.time-b.time)}));
const up=new Function(B.src('up.js'))();
const out=await up(B.tools,{name:'animation.marine.walk_back',length:L,loop:'loop',channels:rev(r.live(r.b.channels)),steps:[]});
console.log(JSON.stringify(out));
