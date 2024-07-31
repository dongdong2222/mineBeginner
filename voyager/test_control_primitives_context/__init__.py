import pkg_resources
import os
import voyager.utils as U


def load_test_control_primitives_context(primitive_names=None):
    package_path = pkg_resources.resource_filename("voyager", "")
    if primitive_names is None:
        primitive_names = [
            primitive[:-3]
            for primitive in os.listdir(f"{package_path}/test_control_primitives_context")
            if primitive.endswith(".js")
        ]
    primitives = [
        U.load_text(f"{package_path}/test_control_primitives_context/{primitive_name}.js")
        for primitive_name in primitive_names
    ]
    return primitives

if __name__ == "__main__":
    import os
