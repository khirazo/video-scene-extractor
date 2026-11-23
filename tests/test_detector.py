from unittest.mock import Mock, patch

import pytest

from video_scene_extractor.detector import SceneDetector, SceneInfo


class FakeTimecode:
    def __init__(self, seconds, frame):
        self.seconds = seconds
        self.frame = frame

    def get_seconds(self):
        return self.seconds

    def get_frames(self):
        return self.frame


def test_detect_scenes_converts_scenedetect_results(tmp_path):
    video_path = tmp_path / "input.mp4"
    video_path.touch()
    video = Mock()
    scene_manager = Mock()
    scene_manager.get_scene_list.return_value = [
        (FakeTimecode(0.0, 0), FakeTimecode(2.5, 75)),
        (FakeTimecode(2.5, 75), FakeTimecode(5.0, 150)),
    ]

    with (
        patch("video_scene_extractor.detector.open_video", return_value=video) as open_video,
        patch("video_scene_extractor.detector.SceneManager", return_value=scene_manager),
        patch("video_scene_extractor.detector.ContentDetector") as content_detector,
    ):
        scenes = SceneDetector(threshold=20.0, min_scene_len=10).detect_scenes(str(video_path))

    open_video.assert_called_once_with(str(video_path))
    content_detector.assert_called_once_with(threshold=20.0, min_scene_len=10)
    scene_manager.add_detector.assert_called_once_with(content_detector.return_value)
    scene_manager.detect_scenes.assert_called_once_with(video)
    assert scenes == [
        SceneInfo(1, 0.0, 2.5, 0, 75),
        SceneInfo(2, 2.5, 5.0, 75, 150),
    ]


def test_detect_scenes_rejects_missing_video(tmp_path):
    with pytest.raises(FileNotFoundError, match="Video file not found"):
        SceneDetector().detect_scenes(str(tmp_path / "missing.mp4"))


def test_get_scene_frames_returns_scene_start_frames():
    detector = SceneDetector()
    detector.detect_scenes = Mock(
        return_value=[
            SceneInfo(1, 0.0, 1.0, 0, 30),
            SceneInfo(2, 1.0, 2.0, 30, 60),
        ]
    )

    assert detector.get_scene_frames("input.mp4") == [0, 30]
