(() => {
  /* Leg drafts (2026-11-09): machine cores + iron plates, borrowed texels (pads, arms) for the shape review. The live
     drafts were then tweaked: lgA_thigh_plate top 21.125 (uv 7.5 rows), lgA_shin_guard bottom 5.625 (uv 6 rows), and
     lgB_thigh_plate (z to 2) / lgB_shin_guard (z to 1.5) copied from them. Strip comments before risky_eval. */
  if (Project.name !== 'power_suit') return 'wrong project';
  if (Group.all.some(g => /^proto_legsA_/.test(g.name))) return 'abort, drafts exist';
  const tex = Texture.all[0], G = n => Group.all.find(g => g.name === n);
  const P = [
    ['right_leg', 'thigh', 'lgA_thigh_core', [2, 10.625, -3], [9, 23.625, 3],
      {north: [113, 96, 120, 109], south: [18, 97, 25, 110], east: [25, 97, 31, 110], west: [60, 98, 66, 111], up: [198, 37, 205, 43], down: [198, 37, 205, 43]}],
    ['right_leg', 'thigh', 'lgA_thigh_plate', [1, 13.625, -4], [10, 21.125, 0],
      {north: [131, 96, 140, 104], south: [131, 96, 140, 104], east: [230, 98, 234, 106], west: [230, 98, 234, 106], up: [186, 88, 195, 92], down: [176, 93, 185, 97]}],
    ['right_shin', 'shin', 'lgA_shin_core', [2.5, 3.625, -2.5], [8.5, 14.625, 2.5],
      {north: [113, 96, 119, 107], south: [18, 97, 24, 108], east: [25, 97, 30, 108], west: [60, 98, 65, 109], up: [217, 37, 223, 42], down: [217, 37, 223, 42]}],
    ['right_shin', 'shin', 'lgA_shin_guard', [1, 5.625, -5], [10, 11.625, -1],
      {north: [131, 96, 140, 103], south: [131, 96, 140, 103], east: [230, 98, 234, 105], west: [230, 98, 234, 105], up: [186, 88, 195, 92], down: [176, 93, 185, 97]}],
    ['right_foot', 'foot', 'lgA_boot', [1, -0.375, -9], [10, 4.375, 4],
      {north: [131, 96, 140, 101], south: [131, 96, 140, 101], east: [230, 98, 240, 103], west: [230, 98, 240, 103], up: [186, 88, 195, 98], down: [176, 93, 185, 103]}],
    ['hips', 'hips', 'lgA_hip_plate', [0.25, 25.625, -5.5], [7.25, 28.625, 5.5],
      {north: [131, 96, 138, 99], south: [131, 96, 138, 99], east: [230, 98, 240, 101], west: [230, 98, 240, 101], up: [186, 88, 193, 98], down: [176, 93, 183, 103]}]];
  const made = [], groups = {};
  Undo.initEdit({outliner: true, elements: []});
  const group = (bone, part) => { const k = bone + part; if (groups[k]) return groups[k];
    const b = G(bone); const g = new Group({name: 'proto_legsA_' + part + (bone.startsWith('right') ? '_r' : bone.startsWith('left') ? '_l' : ''), origin: b.origin.slice()}).addTo(b).init();
    g.visibility = false; return groups[k] = g; };
  const cube = (bone, part, name, from, to, uv, mirror) => {
    const faces = {};
    for (const [f, r] of Object.entries(uv)) faces[f] = {uv: mirror ? [r[2], r[1], r[0], r[3]] : r.slice(), texture: tex.uuid};
    if (mirror) { const e = faces.east; faces.east = faces.west; faces.west = e; }
    const c = new Cube({name, from, to, origin: G(bone).origin.slice(), box_uv: false, faces}).addTo(group(bone, part)).init();
    c.visibility = false; made.push(c); };
  for (const [bone, part, name, f, t, uv] of P) {
    if (bone === 'hips') { cube(bone, part, name + '_r', f, t, uv, false); cube(bone, part, name + '_l', [-t[0], f[1], f[2]], [-f[0], t[1], t[2]], uv, true); continue; }
    cube(bone, part, name + '_r', f, t, uv, false);
    cube(bone.replace('right', 'left'), part, name + '_l', [-t[0], f[1], f[2]], [-f[0], t[1], t[2]], uv, true);
  }
  Undo.finishEdit('Leg block drafts A', {outliner: true, elements: made});
  Canvas.updateAll();
  return 'ok ' + made.length;
})()
