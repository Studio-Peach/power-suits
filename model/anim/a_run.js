// RUN v9 (2026-11-10, footless legs: the lower leg is one block down to the ground, like a player's). The v8 drive kept:
// a 0.7 s stride with flight, the suit sinking into each planted leg after the footfall (sink, sinkAt) and driving up
// through the push-off, a rise in flight (fly), the heel kicking up early in the swing (up) and the swing pawing back
// at the strike (paw). The planted block rolls heel -> toe without slipping (k2.js footlessLegs, as the walk v7); the
// hips come from the planted leg at a kStance knee instead of v8's reach. Upper body as v8.
// v8 (booted legs, front ankle hinge) in a_run_v8.js.
const {TAU,spring,addTo,pnoise,smooth,clamp,lerp}=K;
const O=Object.assign({T:0.7,beta:0.32,S:20,zc:4,H:4,up:0.4,wide:0.5,kick:1,paw:0.4,clear:0.5,kStance:20,
  lean:-11,arm:14,armF:6,toolPump:true,armZ:-5,elbow:70,fly:1.5,sink:1,sinkAt:0.25,waistLean:true},K.P||{});
const {T,beta,S,zc}=O;
const phR=t=>t/T, phL=t=>t/T+0.5;            // right heel strike at t=0, left at T/2
const flightBump=t=>{let v=0;for(const s of ['r','l']){const ph=(((s==='r'?phR(t):phL(t))%1)+1)%1;if(ph>=beta&&ph<0.5){v=Math.max(v,Math.sin(Math.PI*(ph-beta)/(0.5-beta)));}}return v;};
// O.sink: the suit sinks into each planted leg (lowest at O.sinkAt of the stance, then driving back up through the
// push-off): the knee loads up under the weight and extends through the shove
const stanceSink=t=>{let v=0;for(const s of ['r','l']){const ph=(((s==='r'?phR(t):phL(t))%1)+1)%1;if(ph<beta){const u=ph/beta,a=O.sinkAt??0.4;
  v=Math.max(v,u<a?Math.sin(Math.PI/2*u/a):Math.cos(Math.PI/2*(u-a)/(1-a)));}}return v;};
const sinkS=spring(t=>stanceSink(t),{f:3.5,z:0.5,T,loop:true});
const legs=K.footlessLegs({T,beta,S,zc,H:O.H,clear:O.clear,kick:O.kick,paw:O.paw,up:O.up,wide:O.wide,kStance:O.kStance,
  rootXZ:t=>[0.45*Math.sin(TAU*t/T),0,0],root:t=>[0.45*Math.sin(TAU*t/T),yHip(t),0]});
// hips: held up by the planted leg (legs.hip, bridged through the flight), + a rise in flight, - the sink after a footfall
const yHip=t=>legs.hip(t)+O.fly*flightBump(t)-(O.sink||0)*sinkS(t);
const yS=spring(yHip,{f:3.2,z:0.3,T,loop:true});
const rel=t=>yS(t)-yHip(t);
// footfall jolt: an impulse at each strike through a stiff spring (torso/head/arms take it with different lags)
const imp=t=>{let v=0;for(const t0 of [0,T/2,T,-T/2]){const d=t-t0;if(d>=0&&d<T/2)v+=d<0.015?d/0.015:Math.exp(-(d-0.015)/0.05);}return v;};
const jolt=spring(imp,{f:6,z:0.35,T,loop:true});
const n1=pnoise(21,T,0.4,[1,2,3]);
// --- tool arm stabilizer (same block in a_walk.js / a_run.js; spec names: right_* = the live tool arm) -----------
// IK the upper arm so the elbow stays near its cycle-average position, and fix the forearm's world orientation.
// keepPos / keepRot = how much of the original bob/sway survives (0 = rigid mount). The cockpit shows a viewmodel,
// so in a sprint the tool arm may pump (third person only).
function stabilize(raw,T,{keepPos=0.25,keepRot=0.15,N=30}={}){
  const L=K.L,rig=K.rig,EL=rig.bones.right_forearm.origin;let ref=null;
  const fwd=P=>{const W=L.fk(rig,P);return {E:L.xf(W.right_arm,EL),R:W.right_forearm.R};};
  const mean=()=>{const acc={};for(let i=0;i<N;i++){const P=raw(T*i/N);
    for(const b in P)for(const ch in P[b]){const v=P[b][ch];if(!Array.isArray(v))continue;
      const a=((acc[b]=acc[b]||{})[ch]=acc[b][ch]||[0,0,0]);v.forEach((x,j)=>a[j]+=x/N);}}return fwd(acc);};
  return t=>{const P=raw(t);if(!ref)ref=mean();const cur=fwd(P);
    const E=L.add(ref.E,L.sc(L.sub(cur.E,ref.E),keepPos));
    const e0=L.euler(ref.R),e1=L.euler(cur.R);
    const R=L.rot(e0.map((v,i)=>v+K.wrapDeg(e1[i]-v)*keepRot));
    K.ik(P,[['right_arm',0],['right_arm',1],['right_arm',2]],'right_arm',EL,E,{iters:30,damp:0.01});
    K.orient(P,'right_forearm',R);
    return P;};
}
// ---
// v8 (user): the tool arm pumps like the hand arm (same short swing, opposite phase) instead of being held steady:
// shots leave from the pilot's eye and the cockpit draws its own viewmodel, so its third-person pose never aims
const SAMPLE=O.toolPump?RAW:stabilize(RAW,T,{keepPos:0.6,keepRot:0.5});
return {name:'animation.marine.run',length:T,loop:'loop',fps:60,tol:{r:0.04,p:0.01},
 sample(t){return SAMPLE(t);}};
function RAW(t){
  const P={},f=TAU*t/T,R=rel(t),J=jolt(t);
  addTo(P,'marine','p',[0.45*Math.sin(f),yHip(t),0]);
  // lean into the run from the waist; the hips twist with the legs, the shoulders against them
  const by=8*Math.cos(f),bz=3*Math.sin(f),bx=O.lean-1.5*Math.cos(2*f-0.4)-2.5*J;
  const ty=-14*Math.cos(f-0.2),tz=-4*Math.sin(f-0.2),tx=-4-1.5*Math.cos(2*f-1.0)-2*J;
  // waistLean (2026-10-18, space-marine chest): the forward lean pivots at the waist (torso, y 27.125) instead of the
  // hip axis (body, y 22.625): leaning from 4.5 px lower swung the abdomen ~2 px out in front of the static belt
  // (the hip hoods). Same angles; the body keeps only its twist and roll.
  addTo(P,'body','r',[O.waistLean?0:bx,by,bz]);
  addTo(P,'torso','r',[O.waistLean?tx+bx:tx,ty,tz]);
  addTo(P,'head','r',[-(bx+tx)*0.85-3+1.5*Math.cos(2*f-1.6)+3.5*J+n1(t),-(by+ty)*0.8,-(bz+tz)*0.6]);
  // tool arm: heavy, pumps a little against the free arm, jolts on impact
  if(O.toolPump){addTo(P,'right_arm','r',[10-O.arm*Math.cos(f-0.35)+2.5*R+4*J,-(by+ty)*0.3,0]);
    addTo(P,'right_forearm','r',[8-O.armF*Math.cos(f-0.9)+2*R+5*J,0,0]);}
  else{addTo(P,'right_arm','r',[10-12*Math.cos(f-0.35)+3*Math.cos(2*f-1.2)+2.5*R+4*J,-(by+ty)*0.3,0]);
    addTo(P,'right_forearm','r',[8+3*Math.cos(2*f-1.8)+2*R+5*J,0,0]);}
  // free arm pumps opposite the left leg, elbow bent ~90 (v8: a short, heavy pump, arm 14 / armF 6: the old 44 / 22
  // swung the fist 17 px against the tool arm's steady 2.6, user: 'jarring'); held 5 deg out from the body and the elbow
  // at 70 so the driving thigh passes under the forearm (it came up 1 px into it)
  addTo(P,'left_arm','r',[(O.armX??-4)+O.arm*Math.cos(f-0.35),0,O.armZ??0]);
  addTo(P,'left_forearm','r',[(O.elbow??62)+O.armF*Math.cos(f-0.9),0,0]);
  legs(P,t);
  return P;}
