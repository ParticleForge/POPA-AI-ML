import json
import os

import keras.saving.legacy.save
import numpy as np

from .models import get_keras_model


def clean_dict_helper(d):
    if isinstance(d, np.ndarray):
        return d.tolist()

    if isinstance(d, list):  # For those db functions which return list
        return [clean_dict_helper(x) for x in d]

    if isinstance(d, dict):
        for k, v in d.items():
            d.update({k: clean_dict_helper(v)})

    # return anything else, like a string or number
    return d


def save_model_architecture(model_name, model_dir, model):
    print(model.get_config())
    with open("{}/{}/{}_config.json".format(model_dir, model_name, model_name), "w") as f:
        config = clean_dict_helper(model.get_config())
        json.dump(config, f)


def save_model_weights(model_name, model_dir, model):
    for layer in model.layers:
        print("Type:", type(layer.get_weights()))
        print("Layer name:", layer.name)

        weight_format = {"layer_name": layer.name}

        all_weights = []
        for index, weights in enumerate(layer.get_weights()):
            all_weights.append({"weight_no": index + 1, "shard_no": 1, "values": weights.tolist()})

        weight_format['weights'] = all_weights
        with open("{}/{}/weights/{}.json".format(model_dir, model_name, layer.name), "w") as f:
            json.dump([weight_format], f)


def save_model_by_name(model_name):
    os.makedirs(model_name, exist_ok=True)
    os.makedirs(os.path.join(model_name, "weights"), exist_ok=True)

    model = get_keras_model(model_name)

    save_model_weights(model_name, model)
    save_model_architecture(model_name, model)


def save_model(model_name, model_dir, model_path):
    os.makedirs(os.path.join(model_dir, model_name), exist_ok=True)
    os.makedirs(os.path.join(model_dir, model_name, "weights"), exist_ok=True)

    model = keras.models.load_model(model_path)

    save_model_weights(model_name, model_dir, model)
    save_model_architecture(model_name, model_dir, model)
