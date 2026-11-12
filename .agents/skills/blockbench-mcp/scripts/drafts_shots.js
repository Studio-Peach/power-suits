// Review sheets for a draft round: one labelled sheet per hidden proto_* option of the current tab, all from the
// same cameras (SKILL.md §0). Codemode function body. Usage:
//   const SKILL = "/Users/ajac-zero/Developer/PowerSuits/.agents/skills/blockbench-mcp/scripts";
//   const src = (await tools.bash({command: `cat ${SKILL}/drafts_shots.js # ${Date.now()}`})).output;
//   const draftShots = new Function("tools", "image", src)(tools, image);
//   const files = await draftShots({prefix: "/path/sheet_", views: [{name: "back3q", pos: [-30,34,40], target: [0,24,4]}]});
//   (then tools.read each file and image() it)
// The viewer is shared with the user: scene objects they added (a reference player, a second model) are hidden only
// for the renders and put back exactly as they were; the options' visibility goes back to "first option shown".
// View names must not contain spaces (shots.js writes files named after them).
return async ({prefix = "/private/tmp/shots/draft_", views} = {}) => {
  const SKILL = "/Users/ajac-zero/Developer/PowerSuits/.agents/skills/blockbench-mcp/scripts";
  const shots = new Function("tools", "image", (await tools.bash({command: `cat ${SKILL}/shots.js # ${Date.now()}`})).output)(tools, () => {});
  const ev = async code => (await tools.mcp__blockbench__risky_eval({code})).content[0].text;
  const names = JSON.parse(JSON.parse(await ev(`JSON.stringify(Group.all.filter(g => g.name.startsWith('proto_')).map(g => g.name))`)));
  const V = (name, pos, target, fov = 30) => ({name, pos, target, fov, w: 440, h: 500, size: 420});
  views = views || [V("back3q", [-30, 34, 40], [0, 24, 4]), V("back", [0, 26, 42], [0, 24, 4], 32), V("side", [44, 26, 8], [0, 24, 4], 32),
                    V("front3q", [40, 30, -50], [0, 22, 0]), V("tp", [0, 50, 95], [0, 22, 0], 34)];
  // hide what isn't the project's model (the user's extras), remember exactly what was visible
  await ev(`(() => { window.__hiddenForShots = scene.children.filter(o => o.visible && o.type === 'Object3D' && o !== Project.model_3d && o.children.length && !['outline_group', 'grid_group', 'lights'].includes(o.name)).map(o => o.uuid);
    window.__hiddenForShots.forEach(u => { scene.children.find(o => o.uuid === u).visible = false }); return 1 })()`);
  const out = [];
  try {
    for (const n of names.length ? names : ["(no drafts)"]) {
      if (names.length) await ev(`(() => { Group.all.filter(g => g.name.startsWith('proto_')).forEach(g => { const v = g.name == '${n}'; g.visibility = v; g.forEachChild(c => c.visibility = v) }); Canvas.updateVisibility(); return 1 })()`);
      const k = n.replace(/^proto_/, "").replace(/\W+/g, "_");
      const f = `${prefix}${k}_${Date.now() % 100000}.jpg`;
      await shots({views: views.map((v, i) => i ? v : {...v, name: `${k}__${v.name}`}), out: f});
      out.push(f);
    }
    if (names.length) await ev(`(() => { Group.all.filter(g => g.name.startsWith('proto_')).forEach((g, i) => { const v = i == 0; g.visibility = v; g.forEachChild(c => c.visibility = v) }); Canvas.updateVisibility(); return 1 })()`);
  } finally {
    await ev(`(() => { (window.__hiddenForShots || []).forEach(u => { const o = scene.children.find(o => o.uuid === u); if (o) o.visible = true }); return 1 })()`);
  }
  return out;
};
