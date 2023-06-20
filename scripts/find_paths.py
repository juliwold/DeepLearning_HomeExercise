import os
import re

def path_to_project(model_dir, model_name):
    """Find path to project

    Args:
        model_dir (str): Directory containing models.
        model_name (str): Name of model.

    Returns:
        str: Path to project
    """
    annotations = extract_annotations(model_name)
    project = os.path.join(model_dir, annotations, model_name)

    return project


def path_to_model(model_dir, model_name):
    """Find path to best model weights

    Args:
        model_dir (str): Directory containing models.
        model_name (str): Name of model.

    Returns:
        str: Path to best model weights.
    """
    model_path = os.path.join(
        path_to_project(model_dir, model_name), "weights", "best.pt"
    )

    return model_path


def extract_annotations(model_name):
    """Extracts annotation set used

    Args:
        model_name (str): Name of model.

    Returns:
        str: Annotation set.
    """
    anno_pattern = ".*_annotations"
    annotations = re.match(anno_pattern, model_name)[0]

    return annotations
