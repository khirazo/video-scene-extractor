# This file includes AI-generated code - Review and modify as needed

"""
Scene detection module using PySceneDetect.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List

from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector


@dataclass
class SceneInfo:
    """Information about a detected scene."""
    
    scene_number: int
    start_time: float  # seconds
    end_time: float    # seconds
    start_frame: int
    end_frame: int


class SceneDetector:
    """
    Detect scene changes in videos using PySceneDetect.
    
    Args:
        threshold: Scene detection threshold (0-255, default 27.0)
                  Higher values = detect only major changes
        min_scene_len: Minimum scene length in frames (default 15)
    """
    
    def __init__(self, threshold: float = 27.0, min_scene_len: int = 15):
        self.threshold = threshold
        self.min_scene_len = min_scene_len
    
    def detect_scenes(self, video_path: str) -> List[SceneInfo]:
        """
        Detect scenes in a video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of SceneInfo objects containing scene information
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video file is invalid
        """
        video_path_obj = Path(video_path)
        if not video_path_obj.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Open video
        video = open_video(str(video_path_obj))
        
        # Initialize scene manager
        scene_manager = SceneManager()
        
        # Add content detector with specified threshold
        scene_manager.add_detector(
            ContentDetector(
                threshold=self.threshold,
                min_scene_len=self.min_scene_len
            )
        )
        
        # Detect scenes
        scene_manager.detect_scenes(video)
        
        # Get scene list
        scene_list = scene_manager.get_scene_list()
        
        # Convert to SceneInfo objects
        scenes = []
        for i, (start_time, end_time) in enumerate(scene_list):
            scenes.append(SceneInfo(
                scene_number=i + 1,
                start_time=start_time.get_seconds(),
                end_time=end_time.get_seconds(),
                start_frame=start_time.get_frames(),
                end_frame=end_time.get_frames()
            ))
        
        return scenes
    
    def get_scene_frames(self, video_path: str) -> List[int]:
        """
        Get frame numbers where scene changes occur.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            List of frame numbers
        """
        scenes = self.detect_scenes(video_path)
        return [scene.start_frame for scene in scenes]

# Made with Bob
