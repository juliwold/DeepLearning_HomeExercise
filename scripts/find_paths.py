import os


def path_to_project(model_dir, model_name):
    """Find path to project

    Args:
        model_dir (str): Directory containing models.
        model_name (str): Name of model.

    Returns:
        str: Path to project
    """
    if "my_annotations" in model_name:
        sub_dir = "my_annotations"
    else:
        sub_dir = "all_annotations"
    project = os.path.join(model_dir, sub_dir, model_name)

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
