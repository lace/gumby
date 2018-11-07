class Recipe(object):
    def __init__(self, recipe):
        """
        example recipe:

        mesh: examples/vitra/vitra.obj
        landmarks: examples/vitra/vitra.pp
        segments:
          - ['leg seam', 'knee bottom', 20]
          - ['knee bottom', 'knee top', 10]
          - ['knee top', 'leg top', 10]
          - ['back middle', 'back top', 50]
        """
        self.mesh_path = recipe["mesh"]
        self.landmarks_path = recipe["landmarks"]
        self.segments = recipe["segments"]

    @classmethod
    def load(cls, recipe_path):
        import yaml

        with open(recipe_path, "r") as f:
            recipe_data = yaml.load(f)
        return Recipe(recipe_data)

    @property
    def source_mesh(self):
        from lace.mesh import Mesh

        mesh = Mesh(filename=self.mesh_path)
        # Fix crash in write_obj.
        del mesh.segm
        return mesh

    @property
    def landmarks(self):
        from lace.serialization import meshlab_pickedpoints

        return meshlab_pickedpoints.load(self.landmarks_path)

    def run(self):
        from .core import stretch_segments_along_y

        return stretch_segments_along_y(
            mesh=self.source_mesh, landmarks=self.landmarks, segments=self.segments
        )


def main():
    """
    python -m gumby.recipe
    """
    from .path import relative_to_project

    recipe = Recipe.load(relative_to_project("examples/vitra/vitra.yml"))
    result = recipe.run()
    result.write_obj("stretched.obj")
    result.show()


if __name__ == "__main__":
    main()
