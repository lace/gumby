import lacecore
import numpy as np


def stretch_segment_along_y(mesh, in_range, delta):
    height = mesh.v[:, 1]
    minval, maxval = in_range

    (verts_in_range,) = np.where((height >= minval) & (height <= maxval))
    (verts_above,) = np.where(height > maxval)

    above_minval = mesh.v[:, 1][verts_in_range] - minval

    new_v = np.copy(mesh.v)

    new_v[:, 1][verts_in_range] += delta / (maxval - minval) * above_minval

    new_v[:, 1][verts_above] += delta

    return lacecore.Mesh(v=new_v, f=mesh.f)


def stretch_segments_along_y(mesh, landmarks, segments):
    segments_from_floor_up = sorted(segments, key=lambda segm: landmarks[segm[0]][1])

    working_mesh = mesh
    cumulative_delta = 0.0
    for bottom, top, delta in segments_from_floor_up:
        in_range = (
            landmarks[bottom][1] + cumulative_delta,
            landmarks[top][1] + cumulative_delta,
        )
        working_mesh = stretch_segment_along_y(
            mesh=working_mesh, in_range=in_range, delta=delta
        )
        cumulative_delta += delta
    return working_mesh


def main():
    """
    python3 -m gumby.core
    """
    import meshlab_pickedpoints
    from .path import relative_to_project
    from .landmarks import print_landmarks

    original_mesh = lacecore.load_obj(
        relative_to_project("examples/vitra/vitra.obj"), triangulate=True
    )

    landmarks = meshlab_pickedpoints.load(
        relative_to_project("examples/vitra/vitra.pp")
    )
    print_landmarks(landmarks, units="cm", precision=1)

    segments = [
        ("leg seam", "knee bottom", 20),
        ("knee bottom", "knee top", 10),
        ("knee top", "leg top", 10),
        ("back middle", "back top", 50),
    ]
    stretched = stretch_segments_along_y(
        mesh=original_mesh, landmarks=landmarks, segments=segments
    )

    stretched.write_obj("stretched.obj")


if __name__ == "__main__":
    main()
