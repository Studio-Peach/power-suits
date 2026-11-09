(() => {
  /* Machine base + armour sets (2026-11-09, user: a copper set is planned): every armour piece sits in a group named
     <set>_<part> inside the bone that moves it, every machine piece in a frame_<part> group, so a renderer can show one
     set's groups and hide the others (like the helmet styles). New groups take their bone's pivot: nothing moves. */
  if (Project.name !== 'power_suit') return 'wrong project';
  const G = n => Group.all.find(g => g.name === n), C = n => Cube.all.find(c => c.name === n);
  const PLAN = [
    ['torso_armor', 'iron_torso', ['bp_plate', 'abd_plate', 'neck_guard', 'collar_r', 'collar_l']],
    ['right_pad', 'iron_pad_r', ['pad_r']], ['left_pad', 'iron_pad_l', ['pad_l']],
    ['right_forearm', 'iron_gauntlet_r', ['forearm_r', 'fist_r']], ['left_forearm', 'iron_gauntlet_l', ['forearm_l']],
    ['right_arm', 'frame_arm_r', ['upper_arm_r']], ['left_arm', 'frame_arm_l', ['upper_arm_l']],
    ['right_forearm', 'frame_forearm_r', ['forearm_inner_r']], ['left_forearm', 'frame_forearm_l', ['forearm_inner_l']]];
  const miss = PLAN.flatMap(([b, g, cs]) => [G(b) ? null : b, G(g) ? 'exists ' + g : null, ...cs.map(c => C(c) ? null : c)]).filter(Boolean);
  if (miss.length) return 'abort: ' + miss.join(',');
  const cubes = PLAN.flatMap(p => p[2].map(C));
  Undo.initEdit({outliner: true, elements: cubes});
  for (const [b, g, cs] of PLAN) {
    const bone = G(b), grp = new Group({name: g, origin: bone.origin.slice()}).addTo(bone).init();
    cs.forEach(n => C(n).addTo(grp));
  }
  const empty = ['chest_parts', 'collar_parts', 'waist_parts'].map(G).filter(g => g && !g.children.length);
  empty.forEach(g => g.remove());
  Undo.finishEdit('Group armour (iron_*) and machine (frame_*) pieces', {outliner: true, elements: cubes});
  Canvas.updateAll();
  return 'ok, removed empty ' + empty.map(g => g.name).join(',');
})()
