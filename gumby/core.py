def stretch_segment_along_y(mesh, in_range, delta):
    import numpy as np
    height = mesh.v[:, 1]
    minval, maxval = in_range

    verts_in_range, = np.where((height >= minval) & (height <= maxval))
    verts_above, = np.where(height > maxval)

    above_minval = mesh.v[:, 1][verts_in_range] - minval
    mesh.v[:, 1][verts_in_range] += delta / (maxval - minval) * above_minval

    mesh.v[:, 1][verts_above] += delta

def stretch_segments_along_y(mesh, landmarks, segments):
    segments_from_floor_up = sorted(
        segments,
        key=lambda segm: landmarks[segm[0]][1])
    cumulative_delta = 0.
    for bottom, top, delta in segments:
        in_range = (
            landmarks[bottom][1] + cumulative_delta,
            landmarks[top][1] + cumulative_delta)
        stretch_segment_along_y(mesh=mesh, in_range=in_range, delta=delta)
        cumulative_delta += delta

def main():
    """
    python -m gumby.core
    """
    from lace.mesh import Mesh
    from lace.serialization import meshlab_pickedpoints
    from blmath.numerics import vx
    from .path import relative_to_project
    from .landmarks import print_landmarks

    original_mesh = Mesh(filename=relative_to_project('examples/vitra/vitra.obj'))
    # Fix crash in write_obj.
    del original_mesh.segm
    mesh = original_mesh.copy()

    landmarks = meshlab_pickedpoints.load(relative_to_project('examples/vitra/vitra.pp'))
    print_landmarks(landmarks, units='cm', precision=1)

    segments = [
        ('leg seam', 'knee bottom', 20),
        ('knee bottom', 'knee top', 10),
        ('knee top', 'leg top', 10),
        ('back middle', 'back top', 50),
    ]
    stretch_segments_along_y(mesh=mesh, landmarks=landmarks, segments=segments)

    mesh.show()
    original_mesh.show()

    mesh.write_obj('stretched.obj')

if __name__ == '__main__':
    main()
