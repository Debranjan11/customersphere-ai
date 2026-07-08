import json
from pathlib import Path


LABEL_PATH = Path(
    "model_registry/segmentation/label_mapping.json"
)


def save_label_mapping(mapping):

    LABEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        LABEL_PATH,
        "w"
    ) as file:

        json.dump(
            mapping,
            file,
            indent=4
        )


def load_label_mapping():

    with open(
        LABEL_PATH,
        "r"
    ) as file:

        return json.load(file)