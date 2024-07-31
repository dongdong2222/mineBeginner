import pkg_resources
import os
import voyager.utils as U


def load_test_control_primitives(primitive_names=None):
    package_path = pkg_resources.resource_filename("voyager", "")
    if primitive_names is None:
        primitive_names = [ #경로에 있는 .js파일만
            primitives[:-3]
            for primitives in os.listdir(f"{package_path}/test_control_primitives")
            if primitives.endswith(".js")
        ]
    primitives = [ # primitive_name에 해당하는 파일 내용 list 형태로 로드하기
        U.load_text(f"{package_path}/test_control_primitives/{primitive_name}.js")
        for primitive_name in primitive_names
    ]
    return primitives
