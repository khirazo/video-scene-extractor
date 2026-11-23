from copy import deepcopy

import pytest

from video_scene_extractor.config import Config, DetectionConfig, ImageConfig, PDFConfig


def test_config_from_dict_round_trips_and_preserves_input():
    data = {
        "detection": {"threshold": 24.5, "min_scene_len": 12, "position": "middle"},
        "image": {"format": "png", "quality": 80, "max_width": 1920},
        "pdf": {
            "page_size": "LETTER",
            "orientation": "portrait",
            "title": "Training",
            "metadata": {"author": "Example Author"},
        },
        "output": {
            "output_dir": "captures",
            "relative_to_video": True,
            "keep_images": True,
            "verbose": True,
        },
    }
    original_data = deepcopy(data)

    config = Config.from_dict(data)

    assert config.to_dict() == {
        "detection": {"threshold": 24.5, "min_scene_len": 12, "position": "middle"},
        "image": {"format": "png", "quality": 80, "max_width": 1920, "max_height": None},
        "pdf": {
            "page_size": "LETTER",
            "orientation": "portrait",
            "add_timestamp": True,
            "title": "Training",
            "metadata": {
                "author": "Example Author",
                "subject": "Video Scene Extraction",
                "keywords": "video, screenshot, training",
            },
        },
        "output": {
            "output_dir": "captures",
            "relative_to_video": True,
            "keep_images": True,
            "verbose": True,
        },
    }
    assert data == original_data


@pytest.mark.parametrize(
    ("config", "message"),
    [
        (DetectionConfig(threshold=101), "threshold must be between 0 and 100"),
        (ImageConfig(quality=0), "quality must be between 1 and 100"),
        (PDFConfig(orientation="diagonal"), "orientation must be 'portrait' or 'landscape'"),
    ],
)
def test_config_validation_rejects_invalid_values(config, message):
    with pytest.raises(ValueError, match=message):
        config.validate()


def test_config_from_yaml_loads_empty_file_as_defaults(tmp_path):
    config_path = tmp_path / "config.yaml"
    config_path.write_text("", encoding="utf-8")

    config = Config.from_yaml(config_path)

    assert config == Config()
