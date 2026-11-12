// Reload a generated .bbmodel into its own Blockbench tab (the review tab of the script-built workflow, SKILL.md §0).
// Codemode function body. Usage:
//   const SKILL = "/Users/ajac-zero/Developer/PowerSuits/.agents/skills/blockbench-mcp/scripts";
//   const src = (await tools.bash({command: `cat ${SKILL}/reload.js # ${Date.now()}`})).output;
//   const reload = new Function("tools", src)(tools);
//   await reload({file: "/tmp/frame/draft.bbmodel", name: "draft"});   // -> "tabs ... cur=draft cubes=27 ..."
// Why each step (2026-11-05/11 sessions):
// - closing the old tab is async: await it, or the new file loads into a half-closed project;
// - loading a file from the same path again can bring back the previous content: load a copy under a fresh path;
// - after loading, compare each texture with the file's and refresh it from the file if they differ (once a reload
//   kept the old texture);
// - never run the build that writes the file and this reload in parallel tool calls: the reload read a half-written
//   file and showed the previous draft.
// It only closes tabs whose name starts with `name`, never the user's other projects.
return async ({file, name = "draft"}) => {
  const ev = async code => (await tools.mcp__blockbench__risky_eval({code})).content[0].text;
  await ev(`(async () => { for (const p of ModelProject.all.filter(p => p.name.startsWith(${JSON.stringify(name)}))) { p.select(); await p.close(true); } return 1 })()`);
  const tag = Date.now() % 1000000;
  const copy = file.replace(/\.bbmodel$/, `_${tag}.bbmodel`);
  await tools.bash({command: `cp '${file}' '${copy}'`});
  await ev(`(() => { const f = ${JSON.stringify(copy)}; loadModelFile({content: require('fs').readFileSync(f, 'utf8'), path: f, name: ${JSON.stringify(name + '.bbmodel')}}); Project.name = ${JSON.stringify(name)}; return 1 })()`);
  return await ev(`(() => { const d = JSON.parse(require('fs').readFileSync(Project.save_path, 'utf8')); let fixed = 0;
    Texture.all.forEach((t, i) => { if (d.textures[i] && t.source !== d.textures[i].source) { t.fromDataURL(d.textures[i].source); fixed++ } });
    return 'tabs ' + ModelProject.all.map(p => p.name) + ' cur=' + Project.name + ' cubes=' + Cube.all.length + ' textures refreshed=' + fixed })()`);
};
