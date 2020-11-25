class Recipe(object):
    def __init__(self, recipe):
        """
        example recipe:

        mesh: examples/vitra/vitra.obj
        triangulate: false
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
        self.triangulate = recipe.get("triangulate", False)

    @classmethod
    def load(cls, recipe_path):
        import yaml

        with open(recipe_path, "r") as f:
            recipe_data = yaml.safe_load(f)
        return Recipe(recipe_data)

    @property
    def source_mesh(self):
        import lacecore

        return lacecore.load_obj(self.mesh_path, triangulate=self.triangulate)

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
    python3 -m gumby.recipe
    """
    from .path import relative_to_project

    recipe = Recipe.load(relative_to_project("examples/vitra/vitra.yml"))
    result = recipe.run()
    out_mesh = "stretched.obj"
    result.write_obj(out_mesh)
    print(f"Wrote {out_mesh}")


if __name__ == "__main__":
    main()
