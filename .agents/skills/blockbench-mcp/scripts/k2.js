// kit part 2: legs, feet, gait
const SIDE={r:{leg:'right_leg',shin:'right_shin',foot:'right_foot'},l:{leg:'left_leg',shin:'left_shin',foot:'left_foot'}};
const FOOT={},FOOTLESS={};
for(const s of ['r','l']){const fb=rig.bones[SIDE[s].foot];const pts=[];
  // Footless legs (Power Suits since 2026-11-10: the lower leg is one block down to the ground, like a player's): an
  // empty foot bone stands for the shin's bottom. Its "foot" is the shin's lowest cubes, valid while the ankle is locked
  // at 0 (kit.json "ankle": [0, 0]; the foot's rest rotation must be 0, so the foot frame equals the shin's).
  let cubes=fb.cubes;FOOTLESS[s]=!cubes.length&&!rig.order.some(k=>rig.bones[k].parent===SIDE[s].foot&&rig.bones[k].cubes.length);
  if(FOOTLESS[s]){const bot=c=>Math.min(c.from[1],c.to[1])-(c.inflate||0);
    // the shin's cubes, including those in its sub-groups (armour / frame groups: same pivot, never rotated), not the foot's
    const own=[],grab=n=>{own.push(...rig.bones[n].cubes);rig.order.filter(k=>rig.bones[k].parent===n&&k!==SIDE[s].foot).forEach(grab);};
    grab(SIDE[s].shin);const lo=Math.min(...own.map(bot));cubes=own.filter(c=>bot(c)<lo+0.5);}
  cubes.forEach(c=>cubeCorners(c).forEach(p=>pts.push(sub(p,fb.origin))));
  // heel / toe edges: the cube named *sole*, else the foot cubes' bounding box (a boot whose sole is painted on)
  let sole=cubes.find(c=>/(^|_)sole/.test(c.name));
  if(!sole){const lo=[1e9,1e9,1e9],hi=[-1e9,-1e9,-1e9];cubes.forEach(c=>cubeCorners(c).forEach(p=>{for(let i=0;i<3;i++){lo[i]=Math.min(lo[i],p[i]);hi[i]=Math.max(hi[i],p[i]);}}));sole={from:lo,to:hi};}
  const cx=(sole.from[0]+sole.to[0])/2-fb.origin[0];const y=sole.from[1]-fb.origin[1];
  FOOT[s]={pts,heel:[cx,y,sole.to[2]-fb.origin[2]],toe:[cx,y,sole.from[2]-fb.origin[2]]};}
function minY(s,R){let m=1e9;for(const p of FOOT[s].pts){const y=mv(R,p)[1];if(y<m)m=y;}return m;}
const footR=(yaw,pitch=0,roll=0)=>mm(ry(yaw),mm(rx(pitch),rz(roll)));
const REST=(()=>{const W=fk(rig,{});const o={};for(const s of ['r','l']){const f=SIDE[s].foot;
  o[s]={pivot:xf(W[f],rig.bones[f].origin),yaw:euler(W[f].R)[1]};}return o;})();
// pivot of a flat foot standing on ground (y=0) at x,z
const flatPivot=(s,x,z,yaw)=>[x,-minY(s,footR(yaw)),z];
// plant: put foot pivot at world point with world rotation Rw (IK on thigh x,z + shin x)
const WARM={};
function plantRaw(pose,s,pivot,Rw){const S=SIDE[s];
  pose[S.foot]=pose[S.foot]||{};pose[S.foot].r=[0,0,0];
  if(WARM[s]){if(!(pose[S.leg]&&pose[S.leg].r))setTo(pose,S.leg,'r',WARM[s][0]);if(!(pose[S.shin]&&pose[S.shin].r))setTo(pose,S.shin,'r',WARM[s][1]);}
  let err=ik(pose,[[S.leg,0],[S.leg,2],[S.shin,0]],S.foot,rig.bones[S.foot].origin,pivot,{iters:40});
  // two knee solutions reach the same pivot, mirrored about flex = -offset (pivot line straight). The solver follows
  // its warm start; when that would bend the knee backward (flex < KNEE_FLOOR) it takes the mirrored one. With the
  // pivot in front of the shin's axis (offset < 0) the straight-legged stance is the lower solution, the swing needs
  // the upper one (it slid into hyperextension otherwise); a pivot behind the axis only ever has the upper one valid.
  const kOff=kneeOff(s)*180/PI,flex=()=>-(pose[S.shin].r[0]+rig.bones[S.shin].rest[0]);
  if(flex()<OPT.kneeFloor){const k=Math.max(-2*kOff-flex(),OPT.kneeFloor+5);setTo(pose,S.shin,'r',[-k-rig.bones[S.shin].rest[0],0,0]);
    err=ik(pose,[[S.leg,0],[S.leg,2],[S.shin,0]],S.foot,rig.bones[S.foot].origin,pivot,{iters:60});}
  WARM[s]=[pose[S.leg].r.slice(),pose[S.shin].r.slice()];
  orient(pose,S.foot,Rw);
  // squared foot: no twist against the shin, a little roll (+-4: the slot's play) to keep the sole flat
  if(OPT.square){const rr=rig.bones[S.foot].rest;pose[S.foot].r[1]=-rr[1];pose[S.foot].r[2]=clamp(pose[S.foot].r[2]+rr[2],-4,4)-rr[2];
    // the squared foot follows the shin's roll, so one sole edge can dip under a target set for a level foot (0.2 px
    // on a toed-out, swaying walk): lift the foot until its lowest corner is back on the ground (y 0)
    if(!OPT.lifting){const lo=footLow(pose,s);if(lo<-0.005&&pivot[1]+minY(s,Rw)<0.05){OPT.lifting=true;
      try{return plantRaw(pose,s,[pivot[0],pivot[1]-lo,pivot[2]],Rw);}finally{OPT.lifting=false;}}}}
  return err;}
// Ankle bend limits (degrees, foot X rotation incl. its rest, + = toes up toward the shin; null = free). A rig whose
// ankle is hidden inside a boot (Power Suits' stompers: -25..+30) can't bend the foot far against the shin: plant() then rolls the foot instead,
// about its lowest edge while it touches the ground (the contact point doesn't slip), lifting it if it would dig in.
const OPT={ankle:null,square:false,kneeFloor:2};
// the least knee flex plant() accepts (deg). A boot hinged in front of the shin's axis (offset -22.6 on Power Suits'
// v10 legs) has a straighter solution below -offset that flips back and forth with the bent one near full stretch
// (knee jumps of 30-47 deg in a frame): such rigs set the floor at -offset (kit.json "kneeFloor") and stay bent.
function setKneeFloor(d){OPT.kneeFloor=d;}   // ankle: [min, max] degrees or null (free); square: the ankle only bends (pitch)
function setAnkleLimit(d){OPT.ankle=Array.isArray(d)?d:[-d,d];}
// A foot that sits in a slot of the shin (Power Suits' boots) can't twist or roll against it: plant() then keeps the
// foot's Y/Z at zero total (square to the shin) and only bends it; the sole follows the shin's small yaw/roll.
function setAnkleSquare(b){OPT.square=!!b;}
function plant(pose,s,pivot,Rw){const S=SIDE[s];
  // footless legs (the foot bone empty, FOOT = the shin's bottom): the foot pose a spec asks for becomes the block's
  // ground contact. On the ground: rolled about its heel (toe up) or toe (heel up) as the requested pitch says, from
  // the flat position that implies, planted without slipping (plantRoll). In the air: the ankle pivot (a point of the
  // shin) goes to the target, the block's pitch follows the leg.
  if(FOOTLESS[s]){const o=rig.bones[S.foot].origin,pitch=euler(Rw)[0],yaw=euler(Rw)[1];
    if(pivot[1]+minY(s,Rw)>=0.05){pose[S.foot]=pose[S.foot]||{};pose[S.foot].r=[0,0,0];return reachPt(pose,s,o,pivot);}
    const e=pitch>=0?'heel':'toe',ew=add(pivot,mv(Rw,sub(EDGE[s][e],o)));
    const flat=mv(footR(yaw),sub(EDGE[s].heel,EDGE[s][e]));const gh=[ew[0]+flat[0],Math.max(0,ew[1]),ew[2]+flat[2]];
    return plantRoll(pose,s,gh,yaw,e).err;}
  if(!OPT.ankle)return plantRaw(pose,s,pivot,Rw);
  const warm=WARM[s]&&WARM[s].map(a=>a.slice()),[lo0,hi0]=OPT.ankle;
  const contact=pivot[1]+minY(s,Rw)<0.05;
  // the foot turned by d degrees (+ = toe up) about the edge that ends up lowest, which stays put while in contact
  const at=d=>{const R=mm(Rw,rx(d));let pv=pivot;
    if(d){let best=null,by=1e9;for(const p of FOOT[s].pts){const y=mv(R,p)[1];if(y<by){by=y;best=p;}}
      if(contact)pv=sub(add(pivot,mv(Rw,best)),mv(R,best));else if(pivot[1]+by<0)pv=[pivot[0],-by,pivot[2]];}
    if(warm){const y=pose[S.leg]&&pose[S.leg].r?pose[S.leg].r[1]:warm[0][1];setTo(pose,S.leg,'r',[warm[0][0],y,warm[0][2]]);setTo(pose,S.shin,'r',warm[1]);}   // keep a thigh twist the spec set
    const err=plantRaw(pose,s,pv,R);return {err,x:pose[S.foot].r[0]+rig.bones[S.foot].rest[0]};};
  const ok=r=>r.x>=lo0-0.05&&r.x<=hi0+0.05;
  let r=at(0);if(ok(r))return r.err;
  // a locked ankle (footless legs: the "foot" is the shin's own bottom): the window is too narrow for the 2 deg scan
  // below, so find the roll that puts the ankle at the lock by a sign change + bisection (the block rolls on an edge)
  if(hi0-lo0<0.2){const tgt=(lo0+hi0)/2,g=d=>at(d).x-tgt,s0=Math.sign(r.x-tgt);let a=0,b=null;
    for(const dir of [s0>0?-1:1,s0>0?1:-1]){for(let d=1;d<=90;d+=1){if(Math.sign(g(dir*d))!==s0){a=dir*(d-1);b=dir*d;break;}}if(b!==null)break;}
    if(b===null){r=at(0);pose[S.foot].r[0]=tgt-rig.bones[S.foot].rest[0];return r.err;}
    for(let i=0;i<22;i++){const m=(a+b)/2;if(Math.sign(g(m))===s0)a=m;else b=m;}
    return at(b).err;}
  // the smallest roll that brings the ankle back within its limit (scan, then bisect)
  const dir=r.x>hi0?-1:1;let lo=0,hi=null;
  for(let d=2;d<=80;d+=2){if(ok(at(dir*d))){hi=d;break;}lo=d;}
  if(hi===null){r=at(0);pose[S.foot].r[0]=clamp(r.x,lo0,hi0)-rig.bones[S.foot].rest[0];return r.err;}
  for(let i=0;i<8;i++){const mid=(lo+hi)/2;if(ok(at(dir*mid)))hi=mid;else lo=mid;}
  return at(dir*hi).err;}
// foot rolled about heel (pitch>0, toe up) or toe (pitch<0) around a flat reference pivot
function rolled(s,flatPv,yaw,pitch,roll=0){
  const R0=footR(yaw),R=footR(yaw,pitch,roll);
  if(Math.abs(pitch)<1e-6)return {pivot:flatPv,R};
  const c=pitch>0?FOOT[s].heel:FOOT[s].toe;
  const cw=add(flatPv,mv(R0,c));
  return {pivot:sub(cw,mv(R,c)),R};}
// gait foot: ph in [0,1), 0 = heel strike; stance [0,beta), swing [beta,1)
// G: {x,zc,S,beta,H,yaw,strike,toe,hang,rin,rout,vm}
function gaitFoot(s,ph,G){
  const {x,zc,S,beta,H,yaw,strike=10,toe=22,hang=-14,rin=0.14,rout=0.22,vm=0.4}=G;
  ph=((ph%1)+1)%1;
  const zf=zc-S/2,zb=zc+S/2;
  const stance=u=>{const z=zf+(zb-zf)*u;const fp=flatPivot(s,x,z,yaw);
    let p=0; if(u<rin)p=strike*(1-smooth(u/rin)); else if(u>1-rout)p=-toe*smooth((u-(1-rout))/rout);
    return rolled(s,fp,yaw,p);};
  if(ph<beta)return stance(ph/beta);
  const u=(ph-beta)/(1-beta);
  const A=stance(1),B=stance(0);
  // pitch through swing: toe-off -> hang -> strike
  const pitch=u<0.4?lerp(-toe,hang,smooth(u/0.4)):lerp(hang,strike,smooth((u-0.4)/0.6));
  const R=footR(yaw,pitch);
  // horizontal: hermite with ground-speed matched end velocities (body frame: +z)
  const T=1-beta, v=(zb-zf)/beta*T*vm; // dz/du at ends
  const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u;
  const z=h00*A.pivot[2]+h10*v+h01*B.pivot[2]+h11*v;
  const clear=H*Math.pow(Math.sin(PI*u),0.9);
  // height: lowest point at clearance, blended with stance endpoint heights near ends
  let y=clear-minY(s,R);
  const yA=A.pivot[1],yB=B.pivot[1];
  const w0=1-smooth(u/0.15),w1=smooth((u-0.85)/0.15);
  y=Math.max(y, w0*yA+(1-w0)*y); y=Math.max(y,w1*yB+(1-w1)*y);
  return {pivot:[x,y,z],R};
}
// sample a pose's lowest point of all foot cubes (diagnostics)
function footLow(pose,s){const W=fk(rig,pose);const f=SIDE[s].foot;let m=1e9;
  for(const p of FOOT[s].pts){const w=xf(W[f],add(p,rig.bones[f].origin));if(w[1]<m)m=w[1];}return m;}
// whole-body lowest point (for death/ground contact)
function bodyLow(pose){const W=fk(rig,pose);let m=1e9;
  for(const n of rig.order){if(n==='muzzle_flash'||n==='grenade')continue;for(const c of rig.bones[n].cubes)for(const p of cubeCorners(c)){const y=xf(W[n],p)[1];if(y<m)m=y;}}return m;}
// leg length hip pivot -> ankle pivot with the knee bent kneeDeg (thigh/shin lengths from the rig). kneeDeg is the
// bone's flex (-(shin x rotation incl. rest)), not the angle between the pivot lines: an ankle pivot behind the knee
// (Power Suits' boot hinges at its heel, 4 px back) makes the pivot line lean back ~19 deg at a straight bone, and
// treating the two as equal let reachHip hyperextend the knee by that much.
// An ankle pivot IN FRONT of the shin's axis (a boot hinged at the shin's front edge) gives a negative offset: the
// pivot line is straightest with the knee bent by -offset, and a straighter knee bends the pivot line the other way
// (the length only depends on |flex + offset|; plantRaw picks which knee).
function kneeOff(s){const S=SIDE[s],h=rig.bones[S.leg].origin,k=rig.bones[S.shin].origin,a=rig.bones[S.foot].origin;
  const u=sub(k,h),v=sub(a,k);return -Math.atan2(u[1]*v[2]-u[2]*v[1],u[1]*v[1]+u[2]*v[2]);}   // radians; legs hang down
function legLen(s,kneeDeg){const S=SIDE[s],h=rig.bones[S.leg].origin,k=rig.bones[S.shin].origin,a=rig.bones[S.foot].origin;
  const A=len(sub(k,h)),B=len(sub(a,k));
  const g=kneeDeg*PI/180+kneeOff(s);return Math.sqrt(A*A+B*B+2*A*B*Math.cos(g));}
// Hip height (root 'p' y offset) a gait can afford: as high as the planted feet allow with the knees bent at least
// kmin degrees. The raw limit has sharp dips (double support), so it is eroded (min over +-2w of the cycle) and then
// box-blurred twice (+-w each): every blurred value only averages limits taken within reach of its own time, so the
// curve never asks more of a leg than kmin, yet stays smooth and close under the limit (a Fourier low-pass had to be
// shifted down by its worst overshoot, which sank the whole curve). feet: [t => ({s, pivot, contact})] (contact = the
// foot carries weight); sway/dz(t) = root x/z offset. Samples without contact (flight) are bridged. cap = highest
// allowed offset. Returns t => y offset (periodic, linear between N samples).
function reachHip(T,feet,{kmin=10,N=240,w=0.05,cap=1e9,sway=()=>0,dz=()=>0}={}){
  const raw=[];
  for(let i=0;i<N;i++){const t=T*i/N;let best=NaN;
    for(const f of feet){const r=f(t);if(!r.contact)continue;const hp=rig.bones[SIDE[r.s].leg].origin;
      const dx=r.pivot[0]-(hp[0]+sway(t)),dzz=r.pivot[2]-(hp[2]+dz(t)),L=legLen(r.s,kmin);
      const y=r.pivot[1]+Math.sqrt(Math.max(0,L*L-dx*dx-dzz*dzz))-hp[1];if(!(best<=y))best=y;}
    raw.push(Math.min(best,cap));}
  const idx=raw.map((v,i)=>isNaN(v)?-1:i).filter(i=>i>=0);if(!idx.length)throw new Error('reachHip: no contact');
  const fill=raw.map((v,i)=>{if(!isNaN(v))return v;let a=i,b=i;while(isNaN(raw[((a%N)+N)%N]))a--;while(isNaN(raw[b%N]))b++;
    const va=raw[((a%N)+N)%N],vb=raw[b%N];return va+(vb-va)*(i-a)/(b-a);});
  const R=Math.max(1,Math.round(w*N)),at=(a,i)=>a[((i%N)+N)%N];
  const ero=fill.map((_,i)=>{let m=1e9;for(let k=-2*R;k<=2*R;k++)m=Math.min(m,at(fill,i+k));return m;});
  const blur=a=>a.map((_,i)=>{let s=0;for(let k=-R;k<=R;k++)s+=at(a,i+k);return s/(2*R+1);});
  const y=blur(blur(ero));
  return t=>{const u=((t/T)%1+1)%1*N,i=Math.floor(u),f=u-i;return at(y,i)*(1-f)+at(y,i+1)*f;};}
// ---- Footless legs (Power Suits since 2026-11-10: the lower leg is one block down to the ground, like a player's).
// The foot bone is empty and stays locked (r = 0): the shin's bottom is the foot. Its heel / toe edges come from FOOT
// (the shin's lowest cubes). In stance the block rolls without slipping: on its heel edge while its toe is up, then on
// its toe edge; nothing else decides the lower leg's pitch, so hip height and stride shape the roll.
const EDGE={};for(const s of ['r','l']){const o=rig.bones[SIDE[s].foot].origin;EDGE[s]={heel:add(FOOT[s].heel,o),toe:add(FOOT[s].toe,o)};}
// IK (thigh x, z + shin x) putting a point of the shin (model coords) on a world target, on the knee's bent solution
function reachPt(pose,s,pt,target){const S=SIDE[s];
  pose[S.foot]=pose[S.foot]||{};pose[S.foot].r=[0,0,0];
  if(WARM[s]){const y=pose[S.leg]&&pose[S.leg].r?pose[S.leg].r[1]:WARM[s][0][1];setTo(pose,S.leg,'r',[WARM[s][0][0],y,WARM[s][0][2]]);setTo(pose,S.shin,'r',WARM[s][1]);}
  let err=ik(pose,[[S.leg,0],[S.leg,2],[S.shin,0]],S.shin,pt,target,{iters:50});
  const h=rig.bones[S.leg].origin,k=rig.bones[S.shin].origin,u=sub(k,h),v=sub(pt,k);
  const kOff=-Math.atan2(u[1]*v[2]-u[2]*v[1],u[1]*v[1]+u[2]*v[2])*180/PI,flex=()=>-(pose[S.shin].r[0]+rig.bones[S.shin].rest[0]);
  if(flex()<OPT.kneeFloor){const kk=Math.max(-2*kOff-flex(),OPT.kneeFloor+5);setTo(pose,S.shin,'r',[-kk-rig.bones[S.shin].rest[0],0,0]);
    err=ik(pose,[[S.leg,0],[S.leg,2],[S.shin,0]],S.shin,pt,target,{iters:70});}
  // out of reach (a jump's hips rising off planted blocks): the solver straightens the leg along hip-knee-point, which
  // for a point off the shin's axis bends the knee backward; hold the knee at the floor and aim the thigh instead
  if(flex()<OPT.kneeFloor){setTo(pose,S.shin,'r',[-OPT.kneeFloor-rig.bones[S.shin].rest[0],0,0]);
    err=ik(pose,[[S.leg,0],[S.leg,2]],S.shin,pt,target,{iters:50});}
  WARM[s]=[pose[S.leg].r.slice(),pose[S.shin].r.slice()];return err;}
const edgeW=(pose,s,e)=>xf(fk(rig,pose)[SIDE[s].shin],EDGE[s][e]);
// the toe's ground point for a heel ground point (foot flat, turned by yaw)
const toeOf=(s,gh,yaw)=>add(gh,mv(footR(yaw),sub(EDGE[s].toe,EDGE[s].heel)));
// stance: the block stands on its heel (at gh) or on its toe (at its ground point): `pref` first (footlessLegs passes the
// edge that holds the hip higher at the planned knee bend), the other if pref can't reach or would put the other edge
// under the ground; if neither works, the closer. Then lifted until its lowest corner is on the ground (a rolled or
// toed-out block dips a corner).
function plantRoll(pose,s,gh,yaw,pref='heel'){const warm=WARM[s]&&WARM[s].map(a=>a.slice()),S=SIDE[s];
  const other=e=>e==='heel'?'toe':'heel',gp=e=>e==='heel'?gh:toeOf(s,gh,yaw);
  const tryE=(e,lift=0)=>{if(warm)WARM[s]=warm.map(a=>a.slice());const g=gp(e);const err=reachPt(pose,s,EDGE[s][e],[g[0],g[1]+lift,g[2]]);
    return {err,edge:e,ok:err<0.05&&edgeW(pose,s,other(e))[1]>=g[1]+lift-1e-3,r:[pose[S.leg].r.slice(),pose[S.shin].r.slice(),WARM[s]]};};
  const set=r=>{pose[S.leg].r=r.r[0];pose[S.shin].r=r.r[1];WARM[s]=r.r[2];return r;};
  let a=tryE(pref);if(!a.ok){const b=tryE(other(pref));a=b.ok||b.err<a.err?b:a;}set(a);
  const lo=shinLow(pose,s);if(lo<gh[1]-0.01){const b=tryE(a.edge,gh[1]-lo);if(b.err<0.05)set(b);}
  return {err:a.err,edge:a.edge};}
// lowest point of the shin's bottom cubes (FOOT) in a pose
const shinLow=(pose,s)=>footLow(pose,s);
// Gait legs for footless rigs: plants both legs into a pose whose root offset is already set. G: {T, beta, S (stance
// travel, px), zc (the heel's stance centre z), H (swing lift of the moving edge), clear (least height of the block's
// bottom in mid-swing, as a fraction of H), vm (swing end speed vs ground speed), kStance (knee flex of a planted leg,
// deg), root: t => root 'p' offset, rootXZ: t => its x / z part (sway, known before the height)}. Phase 0 = right heel
// strike, left = right + 0.5. Swing shape: kick / paw (end speeds, default vm), up (lift peak, 0.5), wide (0.9).
// legs.hip(t) is the root height a planted leg holds up with its knee at kStance: a rigid leg standing on the block's
// heel or toe edge, whichever holds the hip higher (standing on the other would put this one under the ground; both touch
// when it's flat), so
// the block rocks heel -> toe under it like a rocker; in double support the lower of the two legs, lightly blurred (w).
// Stance: plantRoll on ground points moving back at ground speed (heel strike at zc - S/2). Swing: the point IK'd slides
// from the toe (toe-off) to the heel (strike) along a Hermite path lifted by H sin(pi u)^0.9, raised further wherever
// the bottom would dip below clear*H*sin(pi u). DIAG records the worst IK error and which edge carries each leg.
const DIAG={err:0,edge:{}};
function footlessLegs(G){
  const {T,beta,S,zc,H,clear=0.6,vm=0.45,kick=vm,paw=vm,up=0.5,wide=0.9,kStance=10,w=0.015,N=240,root,rootXZ=root}=G,zf=zc-S/2,Tsw=(1-beta)*T,v=S/(beta*T);
  const R0=fk(rig,{}),X={},YAW={};
  for(const s of ['r','l']){X[s]=xf(R0[SIDE[s].shin],EDGE[s].heel)[0];YAW[s]=REST[s].yaw;}
  const ph=(s,t)=>((((t/T)+(s==='l'?0.5:0))%1)+1)%1;
  const gh=(s,u)=>[X[s],0,zf+S*u];
  // hip -> edge distance of a leg bent kStance (thigh straight down in model space, the shin turned back by the flex)
  const Leff=(s,e)=>{const H0=rig.bones[SIDE[s].leg].origin,K0=rig.bones[SIDE[s].shin].origin;
    return len(add(sub(K0,H0),mv(rx(-(kStance)),sub(EDGE[s][e],K0))));};
  const LE={r:{heel:Leff('r','heel'),toe:Leff('r','toe')},l:{heel:Leff('l','heel'),toe:Leff('l','toe')}};
  const HP={r:rig.bones[SIDE.r.leg].origin,l:rig.bones[SIDE.l.leg].origin};
  // the root height a planted leg holds up at kStance, and the edge it stands on (max: the edge it stands on holds the
  // hip higher; standing on the other would put this one under the ground)
  const stand=(s,t)=>{const rt=rootXZ(t),h=add(HP[s],[rt[0],0,rt[2]]),g=gh(s,ph(s,t)/beta);
    const yOf=(e,pt)=>{const d2=(pt[0]-h[0])**2+(pt[2]-h[2])**2;return pt[1]+Math.sqrt(Math.max(0,LE[s][e]**2-d2))-HP[s][1];};
    const yh=yOf('heel',g),yt=yOf('toe',toeOf(s,g,YAW[s]));return yh>=yt?{y:yh,edge:'heel'}:{y:yt,edge:'toe'};};
  const raw=[];
  for(let i=0;i<N;i++){const t=T*i/N;let best=NaN;
    for(const s of ['r','l']){if(ph(s,t)>=beta)continue;const y=stand(s,t).y;if(!(best<=y))best=y;}
    raw.push(best);}
  const fill=raw.map((v,i)=>{if(!isNaN(v))return v;let a=i,b=i;while(isNaN(raw[((a%N)+N)%N]))a--;while(isNaN(raw[b%N]))b++;
    const va=raw[((a%N)+N)%N],vb=raw[b%N];return va+(vb-va)*(i-a)/(b-a);});
  const Rw=Math.max(1,Math.round(w*N)),at=(a,i)=>a[((i%N)+N)%N];
  const blur=a=>a.map((_,i)=>{let s=0;for(let k=-Rw;k<=Rw;k++)s+=at(a,i+k);return s/(2*Rw+1);});
  const HY=blur(blur(fill));
  const END={};
  const toeEnd=s=>{if(END[s])return END[s];const tEnd=((beta-(s==='l'?0.5:0))%1+1)%1*T;
    const P={marine:{p:root(tEnd)}};const wm=WARM[s]&&WARM[s].map(a=>a.slice());plantRoll(P,s,gh(s,1),YAW[s]);if(wm)WARM[s]=wm;
    return END[s]=edgeW(P,s,'toe');};
  function legs(P,t){
    for(const s of ['r','l']){const p=ph(s,t);
      if(p<beta){const r=plantRoll(P,s,gh(s,p/beta),YAW[s],stand(s,t).edge);DIAG.err=Math.max(DIAG.err,r.err);DIAG.edge[s]=r.edge;continue;}
      DIAG.edge[s]='swing';
      const u=(p-beta)/(1-beta),A=toeEnd(s),B=gh(s,0);
      const q=add(sc(EDGE[s].toe,1-smooth(u)),sc(EDGE[s].heel,smooth(u)));
      // kick / paw: the swing's speed back at toe-off / at the strike vs ground speed; up: where the lift peaks (a run's
      // heel kick peaks early); wide: the lift's exponent
      const h00=2*u*u*u-3*u*u+1,h10=u*u*u-2*u*u+u,h01=-2*u*u*u+3*u*u,h11=u*u*u-u*u,uw=up===0.5?u:Math.pow(u,Math.log(0.5)/Math.log(up));
      const tg=[lerp(A[0],B[0],u),lerp(A[1],B[1],smooth(u))+H*Math.pow(Math.sin(PI*uw),wide),h00*A[2]+h10*v*Tsw*kick+h01*B[2]+h11*v*Tsw*paw];
      let err=reachPt(P,s,q,tg);
      for(let i=0;i<3;i++){const need=clear*H*Math.sin(PI*u)-shinLow(P,s);if(need<=0.01)break;tg[1]+=need;err=reachPt(P,s,q,tg);}
      DIAG.err=Math.max(DIAG.err,err);}}
  legs.hip=t=>{const x=((t/T)%1+1)%1*N,i=Math.floor(x),f=x-i;return at(HY,i)*(1-f)+at(HY,i+1)*f;};
  return legs;}
// Footless standing poses: a block stays flat only with its shin upright, so a lowered root (a crouch, a breath) has to
// sit back for the thighs to reach the knees: squat(P) adds the root z (+ = back) that keeps both blocks flat at their
// rest stance for the root height P already has (the mean of what each leg needs; nothing if the legs can't reach).
// Call it before plant() in standing specs (a no-op on rigs with feet). A spec's own z offset stays on top.
function squat(P){if(!FOOTLESS.r)return 0;const rt=(P.marine&&P.marine.p)||[0,0,0];let n=0,z=0;
  for(const s of ['r','l']){const S=SIDE[s],o=rig.bones[S.foot].origin,pv=flatPivot(s,REST[s].pivot[0],REST[s].pivot[2],REST[s].yaw);
    const k=add(pv,mv(footR(REST[s].yaw),sub(rig.bones[S.shin].origin,o))),h=add(rig.bones[S.leg].origin,[rt[0],rt[1],0]);
    const TL=len(sub(rig.bones[S.shin].origin,rig.bones[S.leg].origin)),dy=h[1]-k[1],dx=h[0]-k[0],q=TL*TL-dy*dy-dx*dx;
    if(q<0)continue;z+=k[2]+Math.sqrt(q)-rig.bones[S.leg].origin[2];n++;}
  if(n)addTo(P,'marine','p',[0,0,z/n]);return n?z/n:0;}

