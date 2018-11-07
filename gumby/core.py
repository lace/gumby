from __future__ import print_function
import vx
import numpy as np

def stretch_segment_along_y(mesh, in_range, delta):
    height = mesh.v[:, 1]
    minval, maxval = in_range

    verts_in_range, = np.where((height >= minval) & (height <= maxval))
    verts_above, = np.where(height > maxval)

    above_minval = mesh.v[:, 1][verts_in_range] - minval
    mesh.v[:, 1][verts_in_range] += delta / (maxval - minval) * above_minval

    mesh.v[:, 1][verts_above] += delta


def stretch_segments_along_y(mesh, landmarks, segments):
    segments_from_floor_up = sorted(segments, key=lambda segm: landmarks[segm[0]][1])
    cumulative_delta = 0.0
    for bottom, top, delta in segments:
        in_range = (
            landmarks[bottom][1] + cumulative_delta,
            landmarks[top][1] + cumulative_delta,
        )
        stretch_segment_along_y(mesh=mesh, in_range=in_range, delta=delta)
        cumulative_delta += delta
    return mesh

def principal_components(coords):
    mean = np.mean(coords, axis=0)
    _, _, result = np.linalg.svd(coords - mean)
    return result

def major_axis(coords):
    return principal_components(coords)[0]

def project_to_line(points, point_on_line, direction):
    return point_on_line + vx.proj(points - point_on_line, direction)

def scalar_project_to_line(points, point_on_line, direction):
    return vx.sproj(points - point_on_line, direction)

def tug(mesh, groups, axis, reference_point, travel, tug_range, easing, anchor_point):
    # groups: later
    # anchor_point: later
    centroid = mesh.centroid

    proj_reference_point = project_to_line(reference_point, centroid, axis)
    proj_start = project_to_line(tug_range[0], centroid, axis)
    proj_end = project_to_line(tug_range[1], centroid, axis)

    sproj_reference_point = scalar_project_to_line(proj_reference_point, centroid, axis)
    sproj_start = scalar_project_to_line(proj_start, centroid, axis)
    sproj_end = scalar_project_to_line(proj_end, centroid, axis)

    if sproj_start > sproj_end:
        raise ValueError('Tug range is backwards relative to axis')
    if sproj_reference_point < sproj_start or sproj_reference_point > sproj_end:
        raise ValueError('Reference point is not within tug range')

    if isinstance(easing, tuple):
        [easing_attack, easing_decay] = easing
    else:
        easing_attack = easing_decay = easing

    def tweened_sproj(s):
        if s < sproj_start:
            return 0.0
        elif s < sproj_reference_point:
            t = (s - sproj_start) / (sproj_reference_point - sproj_start)
            return easing_attack(t)
        elif s == sproj_reference_point:
            return 1.0
        elif s > sproj_reference_point and s <= sproj_end:
            t = (s - sproj_end) / (sproj_reference_point - sproj_end)
            return easing_decay(t)
        else:
            return 0.0

    def dbg(s):
        print("tweened_sproj({}): {}".format(s, tweened_sproj(s)))

    for i in range(100):
        dbg(-i/100.)


    # dbg(sproj_start)
    # dbg(0.5*(sproj_reference_point + sproj_start))
    # dbg(sproj_reference_point)
    # dbg(0.5*(sproj_end + sproj_reference_point))
    # dbg(sproj_end)

    # import sys
    # sys.exit(1)

    # import pdb
    # pdb.set_trace()

    sproj_points = scalar_project_to_line(mesh.v, centroid, axis)
    travel_for_each_point = travel * np.array([tweened_sproj(s) for s in sproj_points])

    proj_points = project_to_line(mesh.v, centroid, axis)
    from_axis_to_points = mesh.v - proj_points

    mesh.v = mesh.v + travel_for_each_point.reshape(-1, 1) * from_axis_to_points

def main():
    """
    python -m gumby.core
    """
    import pytweening
    from lace.mesh import Mesh
    from .path import relative_to_project

    original_mesh = Mesh(filename=relative_to_project("examples/glass-bottle/glass_bottle.obj"))
    # Fix crash in write_obj.
    del original_mesh.vn
    del original_mesh.segm
    mesh = original_mesh.copy()

    tug(mesh=mesh,
        groups=None,
        axis=vx.basis.y,
        reference_point=np.array([0.0, 0.375, 0.0]),
        travel=0.25,
        tug_range=np.array([[0.0, 0.10, 0.0], [0.0, 0.65, 0.0]]),
        easing=pytweening.easeInOutSine,
        anchor_point=None)


    mesh.show()
    original_mesh.show()

    mesh.write_obj("tugged.obj")


if __name__ == "__main__":
    main()
