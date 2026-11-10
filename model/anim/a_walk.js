// WALK v7 (2026-11-10, footless legs: the lower leg is one block down to the ground, no foot, user: like the player and
// other mobs). The planted block rolls without slipping: on its heel edge from the strike until it stands flat, then on
// its toe edge to toe-off (k2.js plantRoll / footlessLegs). The hips ride on the planted leg held at a 15 deg knee
// (legs.hip): highest over it, dropping into each double support. Stance 16 px (22 rolled the blocks 50 deg onto their
// toes), heel centre z 6, 1.0 s cycle, duty 0.62: 1.61 blocks/s. Upper body as v6, tool arm stabilized.
// v6 (booted legs, front ankle hinge, 22 px / 2.22 blocks/s) in a_walk_v6.js.
const {TAU,spring,addTo,pnoise}=K;
const O=Object.assign({T:1.0,beta:0.62,S:16,zc:6,H:2.6,clear:0.6,vm:0.45,kStance:15,hip:0,sway:1.5,kneeOut:0,roll:4.5,
  dip:0.4,jolt:1.0,arm:18,yaw:5},K.P||{});
const {T,beta,S,zc}=O;
const phR=t=>t/T, phL=t=>t/T+0.5;
const xr=Math.sign(K.rig.bones.right_leg.origin[0]);       // sway toward the stance leg
const swayX=t=>O.sway*xr*Math.sin(TAU*t/T);
// the hips ride on the planted leg (legs.hip: as high as the block's intended roll allows; highest over the planted leg)
const legs=K.footlessLegs({T,beta,S,zc,H:O.H,clear:O.clear,vm:O.vm,kStance:O.kStance,
  rootXZ:t=>[swayX(t),0,0],root:t=>[swayX(t),yHip(t)+dipY(t),0]});
const yHip=t=>legs.hip(t)+O.hip;
// weight acceptance: the planted knee gives a little after each heel strike (an impulse shaped dip, both feet)
const hit=u=>{u=((u%1)+1)%1;return u<0.06?Math.sin(Math.PI/2*u/0.06):Math.exp(-(u-0.06)/0.09);};
const dipY=t=>-O.dip*(hit(phR(t))+hit(phL(t)));
const yS=spring(yHip,{f:2.6,z:0.4,T,loop:true});
const rel=t=>yS(t)-yHip(t);
const n1=pnoise(41,T,0.3,[1,2,3]);
// footfall impulse (both heel strikes) through springs: torso pitch forward, the head nods after it, the free arm swings on
const imp=t=>hit(phR(t)-0.0)+hit(phL(t)-0.0);
const sT=spring(imp,{f:4,z:0.35,T,loop:true}),sH=spring(imp,{f:3,z:0.3,T,loop:true}),sA=spring(imp,{f:2.5,z:0.25,T,loop:true});
const jolt=t=>({t:sT(t),hs:sH(t),a:sA(t)-imp(t)});
// --- tool arm stabilizer (same block in a_walk.js / a_run.js; spec names: right_* = the live tool arm) -----------
// Holds the tool steady relative to the suit (it sits in the cockpit view): IK the upper arm so the elbow stays
// near its cycle-average position, and fix the forearm's world orientation.
// keepPos / keepRot = how much of the original bob/sway survives (0 = rigid mount).
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
const SAMPLE=stabilize(RAW,T);
return {name:'animation.marine.walk',length:T,loop:'loop',fps:30,tol:{r:0.05,p:0.01},speed:S/(beta*T)/16,
 sample(t){return SAMPLE(t);}};
function RAW(t){
  const P={},f=TAU*t/T,R=rel(t);
  addTo(P,'marine','p',[swayX(t),yHip(t)+dipY(t),0]);
  // footfall jolt: each heel strike shakes the upper body (springs of different stiffness: torso, head, tool arm)
  const J=jolt(t);
  // a heavy walk: the weight rolls over onto each planted leg (sway + the waist leaning over it, lagging a little),
  // the hips turn with the legs, the shoulders counter-turn, little pitch
  const by=O.yaw*Math.cos(f),bz=-O.roll*xr*Math.sin(f-0.35),bx=-0.6*Math.cos(2*f);
  addTo(P,'body','r',[bx,by,bz]);
  const ty=-5*Math.cos(f-0.25),tz=1.2*xr*Math.sin(f-0.6),tx=-0.8*Math.cos(2*f-0.6);
  addTo(P,'torso','r',[tx-1.2*O.jolt*J.t,ty,tz]);   // -x: the top pitches forward
  addTo(P,'head','r',[-(bx+tx)*0.8+O.jolt*(0.8*J.t-1.0*J.hs)+0.4*Math.cos(2*f-1.2)+n1(t),-(by+ty)*0.85,-(bz+tz)*0.7]);
  // tool arm steady, a little lag on the bob
  addTo(P,'right_arm','r',[2+1.5*Math.cos(2*f-1.0)+1.2*R,-(by+ty)*0.45,0]);
  addTo(P,'right_forearm','r',[1+1.8*Math.cos(2*f-1.6)+1.0*R,0,0]);
  addTo(P,'right_pad','p',[0,0,0]);
  // free arm swings opposite the left leg
  addTo(P,'left_arm','r',[O.arm*Math.cos(f-0.35)+O.jolt*1.5*J.a,0,0]);
  addTo(P,'left_forearm','r',[12+0.55*O.arm*Math.cos(f-0.9)+O.jolt*2*J.a,0,0]);
  // extra knee-out twist while loaded (0: the rest pose's 7 deg hip twist already points knees and toes out; the foot
  // must stay square to the shin, whose slot it sits in)
  for(const s of ['r','l']){const out=Math.sign(K.rig.bones[s==='r'?'right_leg':'left_leg'].origin[0]);
    const load=0.6+0.4*Math.cos(f-(s==='r'?0.9:0.9+Math.PI));addTo(P,s==='r'?'right_leg':'left_leg','r',[0,-out*O.kneeOut*load,0]);}
  legs(P,t);
  return P;}
