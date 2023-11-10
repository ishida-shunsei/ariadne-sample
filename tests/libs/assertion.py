from datetime import datetime
from ariadne.utils import convert_camel_case_to_snake

def assert_model_list(dicts: list[dict], models: list):
    assert len(dicts) == len(models), "Each length of dicts and modesl is different."
    for i in range(len(dicts)):
        assert_model(dicts[i], models[i])


def assert_model(dict_obj: dict, model):
    for camel_key, dict_value in dict_obj.items():
        # json 側の camel case の名前を snake case に変換
        snake_key = convert_camel_case_to_snake(camel_key)
        model_value = getattr(model, snake_key)
        if type(dict_value) is dict:
            assert_model(dict_value, model_value)
        else:
            if type(model_value) is datetime:
                model_value = model_value.isoformat()
            assert dict_value == model_value, f"Each Value for [{snake_key}] in dict and model is different. {dict_value} / {model_value}"
                