from click.testing import CliRunner

from video_scene_extractor.cli import main


def test_cli_help_is_available():
    result = CliRunner().invoke(main, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--config" in result.output
