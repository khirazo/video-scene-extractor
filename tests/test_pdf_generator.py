from unittest.mock import Mock, patch

import pytest
from PIL import Image

from video_scene_extractor.extractor import ImageInfo
from video_scene_extractor.pdf_generator import PDFGenerator


def test_create_pdf_uses_landscape_layout_and_metadata(tmp_path):
    image_path = tmp_path / "scene.png"
    Image.new("RGB", (20, 10), color="white").save(image_path)
    output_path = tmp_path / "output.pdf"
    image = ImageInfo(str(image_path), 1, 0.0, 0, 20, 10)
    layout = Mock()

    with (
        patch("video_scene_extractor.pdf_generator.img2pdf.get_layout_fun", return_value=layout) as get_layout_fun,
        patch("video_scene_extractor.pdf_generator.img2pdf.convert", return_value=b"pdf") as convert,
    ):
        PDFGenerator(page_size="A4", orientation="landscape").create_pdf(
            [image], str(output_path), title="Scenes", metadata={"author": "Example"}
        )

    get_layout_fun.assert_called_once()
    assert get_layout_fun.call_args.args[0] == (842, 595)
    convert.assert_called_once_with(
        [str(image_path)], layout_fun=layout, title="Scenes", author="Example"
    )
    assert output_path.read_bytes() == b"pdf"


def test_create_pdf_rejects_empty_image_list(tmp_path):
    with pytest.raises(ValueError, match="No images provided"):
        PDFGenerator().create_pdf([], str(tmp_path / "output.pdf"))


def test_pdf_generator_rejects_invalid_page_size():
    with pytest.raises(ValueError, match="Unsupported page size"):
        PDFGenerator(page_size="B5")
