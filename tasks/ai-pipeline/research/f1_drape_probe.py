"""F1 drape test: does MPFB2's MakeClothes fit + weight transfer hold on novel kitbash shells?

MPFB2's clothes path is not free-form nearest-surface. VertexMatch restricts its search to
basemesh faces inside the vertex group named on the clothes vertex, and interpolate_weights
then inherits skin weights barycentrically from the three matched basemesh verts. The probe
run showed the matchable vocabulary is coarse: one `body` group over the whole skin, plus
`helper-skirt` / `helper-tights` standoff cages. There is no helper cage for a cloak or a
pauldron, so those must bind to `body` -- i.e. to whatever body surface happens to be
nearest, with no way to declare intent.

That is the failure mode this test measures: a pauldron standing off the deltoid may inherit
upper-arm weights and swing with the arm instead of riding the shoulder.

Two shells, both authored as clean all-quad grids the way a kitbash parts library would emit
them, placed from MPFB joint-group centroids so the geometry is anatomically anchored rather
than hand-guessed:

  pauldron -- asymmetric spherical cap over the left shoulder, standing well off the deltoid
  cloak    -- flared back panel from the shoulders to below the knee

Reported per shell: MakeClothes validity, match-strategy histogram, the dominant bone the
transferred weights actually landed on, and the displacement under a 60 degrees arm raise.

Run headless (CPU only, no GPU):

    blender.exe -b --python f1_drape_probe.py
"""

import math
import sys
from collections import Counter

import bmesh
import bpy
from mathutils import Vector, kdtree


def resolve_mpfb():
    """MPFB2 installs as bl_ext.user_default.mpfb; a bare `import mpfb` fails."""
    for name, module in list(sys.modules.items()):
        if name.endswith(".mpfb") or name == "mpfb":
            return module
    raise RuntimeError("mpfb not loaded")


resolve_mpfb()
from bl_ext.user_default.mpfb.entities.clothes.mhclo import Mhclo  # noqa: E402
from bl_ext.user_default.mpfb.entities.objectproperties import GeneralObjectProperties  # noqa: E402
from bl_ext.user_default.mpfb.services.clothesservice import ClothesService  # noqa: E402
from bl_ext.user_default.mpfb.services.humanservice import HumanService  # noqa: E402
from bl_ext.user_default.mpfb.services.rigservice import RigService  # noqa: E402
from bl_ext.user_default.mpfb.services.targetservice import TargetService  # noqa: E402
from bl_ext.user_default.mpfb.entities.objectproperties import HumanObjectProperties  # noqa: E402


def skin_coords(basemesh):
    """Basemesh vertex positions in local space with macro targets applied.

    MPFB stores macro targets as shape keys, so `data.vertices` holds the pre-target shape --
    the very reason fit_clothes_to_human builds a from-mix key. Landmarks, standoff and match
    geometry must all read the same body or the numbers describe different ones.

    Full depsgraph evaluation is the wrong tool: create_human masks helper geometry with a
    Mask modifier, so the evaluated mesh loses vertices and no longer indexes alike.
    """
    key = basemesh.shape_key_add(name="probe_mix", from_mix=True)
    coords = [point.co.copy() for point in key.data]
    basemesh.shape_key_remove(key)
    return coords


def penetration(basemesh, coords):
    """Signed depth of each point inside the body surface, in metres (0 when outside).

    Nearest-vertex distance cannot detect penetration -- a point 5 cm inside scores the same
    as one 5 cm proud. Only the surface normal at the closest point gives the sign.
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    body = basemesh.evaluated_get(depsgraph)
    depths = []
    for point in coords:
        hit, location, normal, _ = body.closest_point_on_mesh(point)
        if not hit:
            depths.append(0.0)
            continue
        signed = (point - location).dot(normal)
        depths.append(-signed if signed < 0.0 else 0.0)
    return depths


def report_penetration(label, basemesh, coords):
    depths = penetration(basemesh, coords)
    inside = [d for d in depths if d > 0.0005]
    print("   %-12s inside body: %d/%d verts, max depth %.4f"
          % (label, len(inside), len(depths), max(depths) if depths else 0.0))


def push_outside(obj, basemesh, standoff):
    """Lift any vertex that starts inside the body out to `standoff` above the surface.

    A cap built around a joint centre is partly inside the body, because joints are interior
    points. Real parts sit on the skin, so authoring has to project onto it -- MPFB never
    will: it preserves whatever penetration it is handed.
    """
    depsgraph = bpy.context.evaluated_depsgraph_get()
    body = basemesh.evaluated_get(depsgraph)
    lifted = 0
    for vert in obj.data.vertices:
        hit, location, normal, _ = body.closest_point_on_mesh(vert.co)
        if hit and (vert.co - location).dot(normal) < standoff:
            vert.co = location + normal * standoff
            lifted += 1
    return lifted


def build_skin_tree(coords):
    tree = kdtree.KDTree(len(coords))
    for index, coord in enumerate(coords):
        tree.insert(coord, index)
    tree.balance()
    return tree


def group_centroid(obj, coords, group_name):
    idx = obj.vertex_groups[group_name].index
    total = Vector((0.0, 0.0, 0.0))
    count = 0
    for vert in obj.data.vertices:
        for group in vert.groups:
            if group.group == idx:
                total += coords[vert.index]
                count += 1
                break
    if not count:
        raise RuntimeError("empty group %s" % group_name)
    return total / count


def make_grid(name, u_segments, v_segments, place):
    """Build an all-quad grid and push each vertex through `place(u, v) -> Vector`.

    All-quad matters: mesh_is_valid_as_clothes rejects mixed tri/quad outright.
    """
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=u_segments, y_segments=v_segments, size=1.0)
    for vert in bm.verts:
        u = (vert.co.x + 1.0) / 2.0
        v = (vert.co.y + 1.0) / 2.0
        vert.co = place(u, v)
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def assign_all_to_group(obj, group_name):
    """Every vertex in exactly one group -- MakeClothes rejects zero or multiple."""
    group = obj.vertex_groups.new(name=group_name)
    group.add(range(len(obj.data.vertices)), 1.0, "REPLACE")


def dominant_bones(obj, bone_names, top=6):
    """Share of skinning weight per bone. The authoring group used for matching survives on
    the shell as an inert non-bone group and must be excluded or it skews every share."""
    weight_by_group = Counter()
    index_to_name = {g.index: g.name for g in obj.vertex_groups}
    for vert in obj.data.vertices:
        for group in vert.groups:
            name = index_to_name[group.group]
            if name in bone_names:
                weight_by_group[name] += group.weight
    total = sum(weight_by_group.values()) or 1.0
    return [(name, weight / total) for name, weight in weight_by_group.most_common(top)]


def evaluated_coords(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    coords = [obj.matrix_world @ vert.co for vert in mesh.vertices]
    evaluated.to_mesh_clear()
    return coords


def skinned_in_basemesh_space(obj, basemesh):
    """Deformed shell vertices expressed in basemesh local space, ready for closest_point_on_mesh."""
    depsgraph = bpy.context.evaluated_depsgraph_get()
    to_local = basemesh.matrix_world.inverted()
    return [to_local @ point for point in evaluated_coords(obj, depsgraph)]


print("\n" + "=" * 70)
print("F1 DRAPE TEST -- MPFB2 weight transfer onto novel kitbash shells")
print("=" * 70)

basemesh = HumanService.create_human()
rig = HumanService.add_builtin_rig(basemesh, "mixamo")

print("\nbasemesh: %d verts, object scale %s" % (len(basemesh.data.vertices), tuple(basemesh.scale)))
print("rig: %d bones" % len(rig.data.bones))

rest_skin = skin_coords(basemesh)
shoulder = group_centroid(basemesh, rest_skin, "joint-l-shoulder")
elbow = group_centroid(basemesh, rest_skin, "joint-l-elbow")
scapula = group_centroid(basemesh, rest_skin, "joint-l-scapula")
spine_top = group_centroid(basemesh, rest_skin, "joint-spine-4")
spine_low = group_centroid(basemesh, rest_skin, "joint-spine-1")
knee = group_centroid(basemesh, rest_skin, "joint-l-knee")

arm_span = (elbow - shoulder).length
print("\nlandmarks (basemesh local):")
print("  l-shoulder %s" % (tuple(round(c, 3) for c in shoulder),))
print("  l-elbow    %s  (shoulder->elbow %.3f)" % (tuple(round(c, 3) for c in elbow), arm_span))
print("  spine-4    %s" % (tuple(round(c, 3) for c in spine_top),))
print("  l-knee     %s" % (tuple(round(c, 3) for c in knee),))

# Pauldron: spherical cap centred on the shoulder joint, reaching ~70% of the way to the
# elbow and standing off the skin -- the silhouette a hand-modelled parts library would emit,
# and the one with no helper cage to bind to.
pauldron_radius = arm_span * 0.70


def pauldron_place(u, v):
    theta = (u - 0.5) * math.pi * 1.15
    phi = v * math.pi * 0.55
    return shoulder + Vector((
        -math.sin(phi) * math.cos(theta) * pauldron_radius * 1.25,
        math.sin(phi) * math.sin(theta) * pauldron_radius,
        math.cos(phi) * pauldron_radius * 0.85,
    ))


# Cloak: flared back panel, shoulders to below the knee, standing off the spine. The back
# plane is measured off the torso rather than guessed from a joint centroid -- joints sit on
# the body axis, not its surface.
torso_back = max(
    coord.y for coord in rest_skin
    if knee.z < coord.z < shoulder.z and abs(coord.x) < arm_span * 0.5
)
cloak_top = shoulder.z
cloak_bottom = knee.z - (shoulder.z - knee.z) * 0.12
cloak_back = torso_back + arm_span * 0.18
cloak_half_width = arm_span * 0.85
print("  torso back plane y=%.3f -> cloak at y=%.3f" % (torso_back, cloak_back))


def cloak_place(u, v):
    t = 1.0 - v
    flare = 1.0 + t * 0.85
    x = (u - 0.5) * 2.0 * cloak_half_width * flare
    bulge = math.cos((u - 0.5) * math.pi) * arm_span * 0.30 * (0.35 + t)
    return Vector((
        spine_top.x + x,
        cloak_back + bulge,
        cloak_top + (cloak_bottom - cloak_top) * t,
    ))


# The third shell is the same cloak bound to MPFB's `helper-skirt` standoff cage instead of
# the skin. The cage is the mechanism's own answer to loose geometry, so a shoulder cloak has
# to be tried against it before the skin result is called a verdict.
shells = [
    ("pauldron", make_grid("pauldron", 12, 10, pauldron_place), "body"),
    ("cloak", make_grid("cloak", 16, 20, cloak_place), "body"),
    ("cloak_caged", make_grid("cloak_caged", 16, 20, cloak_place), "helper-skirt"),
]

cage_z = [rest_skin[vert.index].z for vert in basemesh.data.vertices
          for group in vert.groups
          if basemesh.vertex_groups["helper-skirt"].index == group.group]
print("  helper-skirt cage: %d verts, z %.3f..%.3f (cloak spans %.3f..%.3f)"
      % (len(cage_z), min(cage_z), max(cage_z), cloak_bottom, cloak_top))

results = {}
mhclos = {}

skin_tree = build_skin_tree(rest_skin)

for label, obj, bind_group in shells:
    obj.scale = basemesh.scale
    lifted = push_outside(obj, basemesh, arm_span * 0.06)
    assign_all_to_group(obj, bind_group)

    print("\n" + "-" * 70)
    print("%s -- %d verts, %d faces, %d lifted clear of the skin at authoring"
          % (label, len(obj.data.vertices), len(obj.data.polygons), lifted))
    print("-" * 70)

    standoff = [skin_tree.find(vert.co)[2] for vert in obj.data.vertices]
    print("standoff from skin: min %.4f  mean %.4f  max %.4f (sampled)"
          % (min(standoff), sum(standoff) / len(standoff), max(standoff)))

    report = ClothesService.mesh_is_valid_as_clothes(obj, basemesh)
    print("valid as clothes: %s" % report["all_checks_ok"])
    for key in ("all_faces_same_type", "all_verts_have_min_one_vgroup",
                "all_verts_have_max_one_vgroup", "clothes_groups_exist_on_basemesh",
                "objs_same_scale"):
        print("   %-34s %s" % (key, report[key]))
    for warning in report["warnings"]:
        print("   WARNING: %s" % warning)
    if not report["all_checks_ok"]:
        print("   -> cannot proceed for %s" % label)
        continue

    mhclo = ClothesService.create_mhclo_from_clothes_matching(basemesh, obj)
    mhclo.clothes = obj
    mhclo.basename = "f1_%s" % label

    # Which body region did each shell vertex actually bind to? Map the matched basemesh
    # verts back through the rig's own weights to name the bone the shell will follow.
    bone_group_names = {b.name for b in rig.data.bones}
    index_to_name = {g.index: g.name for g in basemesh.vertex_groups}
    matched_bone_mass = Counter()
    for entry in mhclo.verts.values():
        for basemesh_vert_index, weight in zip(entry["verts"], entry["weights"]):
            for group in basemesh.data.vertices[basemesh_vert_index].groups:
                name = index_to_name[group.group]
                if name in bone_group_names:
                    matched_bone_mass[name] += group.weight * weight
    matched_total = sum(matched_bone_mass.values()) or 1.0
    print("matched basemesh region (top 5 by bone mass):")
    for name, mass in matched_bone_mass.most_common(5):
        print("   %-28s %5.1f%%" % (name, 100.0 * mass / matched_total))

    ClothesService.set_up_rigging(basemesh, obj, rig, mhclo,
                                  import_subrig=False, import_weights=False)

    print("transferred weights (top 5 vertex groups):")
    for name, share in dominant_bones(obj, bone_group_names, top=5):
        print("   %-28s %5.1f%%" % (name, 100.0 * share))
    print("penetration at rest:")
    report_penetration(label, basemesh, [v.co for v in obj.data.vertices])

    results[label] = obj
    mhclos[label] = mhclo

# Pose test: raise the left upper arm 60 degrees. A pauldron that inherited LeftArm weights
# swings with it; one riding LeftShoulder/Spine stays put. The cloak is the control -- it
# should barely move.
depsgraph = bpy.context.evaluated_depsgraph_get()
rest = {label: evaluated_coords(obj, depsgraph) for label, obj in results.items()}

bpy.context.view_layer.objects.active = rig
bpy.ops.object.mode_set(mode="POSE")
arm_bone = rig.pose.bones["mixamorig:LeftArm"]
arm_bone.rotation_mode = "XYZ"
arm_bone.rotation_euler.z = math.radians(60.0)
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.view_layer.update()

depsgraph = bpy.context.evaluated_depsgraph_get()

print("\n" + "=" * 70)
print("POSE TEST -- mixamorig:LeftArm raised 60 degrees")
print("=" * 70)
for label, obj in results.items():
    posed = evaluated_coords(obj, depsgraph)
    deltas = [(a - b).length for a, b in zip(posed, rest[label])]
    moved = sum(1 for d in deltas if d > arm_span * 0.02)
    print("%-10s max %.4f  mean %.4f  (%.0f%% of shoulder->elbow)  verts moved: %d/%d"
          % (label, max(deltas), sum(deltas) / len(deltas),
             100.0 * max(deltas) / arm_span, moved, len(deltas)))
    report_penetration(label, basemesh, skinned_in_basemesh_space(obj, basemesh))

# Conform test: the whole reason to pay the mhclo authoring cost is that one authored shell
# should re-fit across body shapes instead of being re-modelled per race. Push the body to
# heavy/muscular/tall, refit, and check the shells followed without poking through the skin.
for pose_bone in rig.pose.bones:
    pose_bone.rotation_euler = (0.0, 0.0, 0.0)
bpy.context.view_layer.update()

before_fit = {label: [v.co.copy() for v in obj.data.vertices] for label, obj in results.items()}

# create_mhclo_from_clothes_matching leaves offsets in MakeHuman's frame as (dx, dz, -dy);
# only Mhclo.load converts them back, as (d0, -d2, d1). So an mhclo handed straight to
# fit_clothes_to_human has its standoff rotated, while one written to disk and reloaded round
# trips exactly. Author through the file, which is what a real parts pipeline does anyway.
reference_scale = ClothesService.get_reference_scale(basemesh)
for label in list(mhclos):
    path = bpy.path.abspath("//f1_%s.mhclo" % label)
    mhclos[label].write_mhclo(path, also_export_obj=False, reference_scale=reference_scale)
    reloaded = Mhclo()
    reloaded.load(path)
    reloaded.clothes = results[label]
    mhclos[label] = reloaded

# Control: refit against the UNCHANGED body must be the identity. Until this reads ~0, no
# conform number below means anything.
print("\n" + "=" * 70)
print("CONTROL -- refit against the unchanged body (must be a no-op)")
print("=" * 70)
print("scale_factor = %s" % GeneralObjectProperties.get_value("scale_factor", entity_reference=basemesh))
for label, obj in results.items():
    ClothesService.fit_clothes_to_human(obj, basemesh, mhclo=mhclos[label], set_parent=False)
    drift = [(v.co - old).length for v, old in zip(obj.data.vertices, before_fit[label])]
    print("%-12s identity drift: mean %.4f max %.4f" % (label, sum(drift) / len(drift), max(drift)))

before_fit = {label: [v.co.copy() for v in obj.data.vertices] for label, obj in results.items()}

for name, value in (("weight", 0.95), ("muscle", 0.85), ("height", 0.9)):
    HumanObjectProperties.set_value(name, value, entity_reference=basemesh)
TargetService.reapply_macro_details(basemesh)
bpy.context.view_layer.update()

# The armature must follow the body too. Refitting only the shells leaves them skinned to a
# rig still sized for the old body, so their rest positions measure correct while everything
# the armature modifier actually displays is wrong.
RigService.refit_existing_armature(rig, basemesh)
bpy.context.view_layer.update()

for label, obj in results.items():
    ClothesService.fit_clothes_to_human(obj, basemesh, mhclo=mhclos[label], set_parent=False)
bpy.context.view_layer.update()

conform_skin = skin_coords(basemesh)
skin_tree = build_skin_tree(conform_skin)
print("body height %.3f -> %.3f" % (max(c.z for c in rest_skin), max(c.z for c in conform_skin)))

print("\n" + "=" * 70)
print("CONFORM TEST -- body pushed to weight 0.95 / muscle 0.85 / height 0.9, then refit")
print("=" * 70)
# Measure the skinned result, not the rest mesh. The armature modifier is what ships and what
# the viewport shows; rest-position standoff can look clean while the deformed shell is buried.
depsgraph = bpy.context.evaluated_depsgraph_get()
for label, obj in results.items():
    moved = [(v.co - old).length for v, old in zip(obj.data.vertices, before_fit[label])]
    rest_standoff = [skin_tree.find(v.co)[2] for v in obj.data.vertices]
    skinned = obj.evaluated_get(depsgraph)
    skinned_mesh = skinned.to_mesh()
    live_standoff = [skin_tree.find(v.co)[2] for v in skinned_mesh.vertices]
    buried = sum(1 for a, b in zip(skinned_mesh.vertices, obj.data.vertices)
                 if skin_tree.find(a.co)[2] < 0.5 * skin_tree.find(b.co)[2])
    skinned.to_mesh_clear()
    print("%-12s moved mean %.4f | rest standoff min %.4f mean %.4f | SKINNED min %.4f mean %.4f | collapsed %d/%d"
          % (label, sum(moved) / len(moved), min(rest_standoff),
             sum(rest_standoff) / len(rest_standoff), min(live_standoff),
             sum(live_standoff) / len(live_standoff), buried, len(rest_standoff)))
    report_penetration(label, basemesh, skinned_in_basemesh_space(obj, basemesh))

bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath("//f1_drape_test.blend"))
print("\nsaved f1_drape_test.blend")
