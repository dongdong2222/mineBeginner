import sys

from voyager import Voyager
from voyager import CustomVoyager

print(f'sys.path: {sys.path}')



# voyager = Voyager(
#     # azure_login=azure_login,
#     openai_api_key=openai_api_key,
#     skill_library_dir="./skill_library/trial1",
#     ckpt_dir="ckpt",
#     mc_port=60777,
# )

param_dict = {
    # 'openai_api_key': openai_api_key,
    'skill_library_dir': "./skill_library/trial1",
    "ckpt_dir": "ckpt",
    "mc_port": 50159,

    "developer_model_name" : "gpt-3.5-turbo",
    "developer_template" : 0,
    "patroller_model_name": "gpt-3.5-turbo",
    "patroller_template" : 0,
    "evaluator_model_name": "gpt-3.5-turbo",
    "evaluator_template" : 0,
    "openai_api_request_timeout": 120,
}
custom_voyager = CustomVoyager(**param_dict)

#strat lifelong learning
# voyager.learn()
custom_voyager.learn()


