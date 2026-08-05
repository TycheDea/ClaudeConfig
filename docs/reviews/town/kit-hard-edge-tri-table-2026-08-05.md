# Town-kit triangle counts: beveled (git HEAD) vs hard-edge rebuild

Box bevel ruled dead (judge: 3/10 dark rebate trough vs. 9/10 artifact-free
hard edge, visually identical to a true chamfer at gameplay framing).
`make_box`'s `bmesh.ops.bevel` call and its `bevel`/`bevel_segments`
parameters were deleted; every kit piece was regenerated from a clean
Blender run. `reja_set` uses only curve-bevel wrought-iron bars (a distinct,
untouched mechanism), so its triangle count is unchanged.

| piece          | old tris (HEAD) | new tris (hard edge) | delta   |
|----------------|-----------------|-----------------------|---------|
| casa_small_a   | 4066            | 2578                  | -1488   |
| casa_small_b   | 4092            | 2700                  | -1392   |
| casa_two_story | 5768            | 3608                  | -2160   |
| casa_corner    | 7166            | 4382                  | -2784   |
| wall_segment   | 420             | 84                    | -336    |
| gate_arch      | 388             | 244                   | -144    |
| chapel         | 3413            | 2437                  | -976    |
| well_basin     | 244             | 100                   | -144    |
| reja_set       | 576             | 576                   | 0       |

Old counts read directly from the git-HEAD `content/models/props/<piece>/<piece>.gltf`
files (accessor index counts / 3, summed per primitive) before rebuild. New
counts read the same way from the rebuilt, installed files, and match
`target/kit-rebuild/raw/build_report.json`'s own `tris` field per type
(Blender's `mesh.calc_loop_triangles()` count) exactly.
