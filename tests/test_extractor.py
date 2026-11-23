import pytest
from PIL import Image

from video_scene_extractor.detector import SceneInfo
from video_scene_extractor.extractor import FrameExtractor


@pytest.mark.parametrize(
    ("position", "expected_frame"),
    [("start", 10), ("middle", 20), ("end", 29)],
)
def test_get_frame_number_uses_requested_scene_position(tmp_path, position, expected_frame):
    extractor = FrameExtractor(output_dir=tmp_path)
    scene = SceneInfo(1, 1.0, 3.0, 10, 30)

    assert extractor._get_frame_number(scene, position) == expected_frame


def test_resize_image_preserves_aspect_ratio_and_does_not_enlarge(tmp_path):
    image_path = tmp_path / "image.png"
    Image.new("RGB", (400, 200), color="white").save(image_path)
    extractor = FrameExtractor(output_dir=tmp_path, image_format="png")

    extractor.resize_image(str(image_path), max_width=100, max_height=100)

    assert Image.open(image_path).size == (100, 50)

    extractor.resize_image(str(image_path), max_width=200)

    assert Image.open(image_path).size == (100, 50)


def test_frame_extractor_rejects_unsupported_image_format(tmp_path):
    with pytest.raises(ValueError, match="Unsupported image format"):
        FrameExtractor(output_dir=tmp_path, image_format="gif")
