from unittest.mock import Mock, patch

from click.testing import CliRunner

from video_scene_extractor.cli import _resolve_relative_path, main
from video_scene_extractor.config import Config, OutputConfig


def test_cli_help_is_available():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--config" in result.output
    assert "--output-relative-to-video" in result.output


def test_resolve_relative_path_uses_video_directory_and_preserves_absolute_path(tmp_path):
    absolute_path = tmp_path / "absolute.pdf"

    assert _resolve_relative_path("output.pdf", tmp_path) == tmp_path / "output.pdf"
    assert _resolve_relative_path(str(absolute_path), tmp_path) == absolute_path


def test_config_can_resolve_output_paths_from_video_directory(tmp_path):
    video_path = tmp_path / "training.mp4"
    video_path.touch()
    config = Config(
        output=OutputConfig(
            output_dir="frames", relative_to_video=True, keep_images=True
        )
    )
    detector = Mock()
    detector.detect_scenes.return_value = [Mock()]
    extractor = Mock()
    extractor.extract_frames.return_value = [Mock()]
    generator = Mock()

    with (
        patch("video_scene_extractor.cli.load_config", return_value=config),
        patch("video_scene_extractor.cli.SceneDetector", return_value=detector),
        patch("video_scene_extractor.cli.FrameExtractor", return_value=extractor) as frame_extractor,
        patch("video_scene_extractor.cli.PDFGenerator", return_value=generator),
    ):
        result = CliRunner().invoke(main, [str(video_path), "-o", "scenes.pdf"])

    assert result.exit_code == 0
    frame_extractor.assert_called_once_with(
        output_dir=str(tmp_path / "frames"), image_format="jpg", quality=95
    )
    generator.create_pdf.assert_called_once_with(
        extractor.extract_frames.return_value,
        str(tmp_path / "scenes.pdf"),
        title="training",
    )
