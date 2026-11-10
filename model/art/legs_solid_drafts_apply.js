(() => {
  /* Solid leg draft G (2026-11-09). User: no separate feet (not even a wider greave at the bottom) and no machine
     showing at the back of the legs. So each leg is two iron blocks of one footprint, like a player's leg: a thigh
     block and a lower-leg block down to the ground, with a dark knee block inside both that shows as a 1 px band
     at the knee (and fills the gap when it bends). The lower leg rides the shin bone: the foot bone stays empty,
     so no pivot moves. Removes the rejected flush drafts F1/F2 first. Borrowed texels for the shape review only.
     Strip comments before risky_eval. */
  if (Project.name !== 'power_suit') return 'wrong project';
  if (Group.all.some(g => /^proto_legsG_/.test(g.name))) return 'abort, drafts exist';
  const tex = Texture.all[0], G = n => Group.all.find(g => g.name === n);
  const IRON = {north: [131, 96, 140, 102], east: [240, 21, 248, 27], south: [195, 92, 203, 98], west: [222, 92, 230, 98], up: [224, 29, 232, 21], down: [232, 21, 240, 29]};
  const KNEE = {north: [113, 96, 119, 100], east: [25, 97, 30, 101], south: [18, 97, 24, 101], west: [60, 98, 65, 102], up: [217, 37, 223, 42], down: [217, 37, 223, 42]};
  const P = [
    ['right_leg', 'thigh', 'lgG_thigh', [1, 13.125, -4], [10, 23.625, 4], IRON],
    ['right_shin', 'knee', 'lgG_knee', [2, 10.625, -3], [9, 14.625, 3], KNEE],
    ['right_shin', 'shin', 'lgG_shin', [1, -0.375, -4], [10, 12.125, 4], IRON]];
  const old = Group.all.filter(g => /^proto_legsF[12]_/.test(g.name));
  const oldCubes = old.flatMap(g => g.children.filter(c => c instanceof Cube));
  Undo.initEdit({outliner: true, elements: oldCubes, groups: old});
  oldCubes.forEach(c => c.remove()); old.forEach(g => g.remove());
  Undo.finishEdit('Remove flush leg drafts F1/F2');
  const made = [], groups = {};
  Undo.initEdit({outliner: true, elements: []});
  const group = (bone, part, s) => { const k = bone + part; if (groups[k]) return groups[k];
    const g = new Group({name: 'proto_legsG_' + part + '_' + s, origin: G(bone).origin.slice()}).addTo(G(bone)).init();
    g.visibility = false; return groups[k] = g; };
  const cube = (bone, part, s, name, from, to, uv, mirror) => {
    const faces = {};
    for (const [f, r] of Object.entries(uv)) faces[f] = {uv: mirror ? [r[2], r[1], r[0], r[3]] : r.slice(), texture: tex.uuid};
    if (mirror) { const e = faces.east; faces.east = faces.west; faces.west = e; }
    const c = new Cube({name: name + '_' + s, from, to, origin: G(bone).origin.slice(), box_uv: false, faces}).addTo(group(bone, part, s)).init();
    c.visibility = false; made.push(c); };
  for (const [bone, part, name, f, t, uv] of P) {
    cube(bone, part, 'r', name, f, t, uv, false);
    cube(bone.replace('right', 'left'), part, 'l', name, [-t[0], f[1], f[2]], [-f[0], t[1], t[2]], uv, true);
  }
  Undo.finishEdit('Solid leg draft G', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok ' + made.length + ', removed ' + oldCubes.length;
})()
