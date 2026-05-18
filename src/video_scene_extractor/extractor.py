# This file includes AI-generated code - Review and modify as needed

"""
Frame extraction module for extracting images from video scenes.
"""

from dataclasses import dataclass
from typing import List
from pathlib import Path
import cv2
from PIL import Image

from .detector import SceneInfo


@dataclass
class ImageInfo:
    """Information about an extracted image."""
    
    file_path: str
    scene_number: int
    timestamp: float  # seconds
    frame_number: int
    width: int
    height: int


class FrameExtractor:
    """
    Extract frames from video at scene change points.
    
    Args:
        output_dir: Directory to save extracted images
        image_format: Image format ('jpg' or 'png')
        quality: JPEG quality (1-100, only for jpg format)
    """
    
    def __init__(
        self,
        output_dir: str = "./frames",
        image_format: str = "jpg",
        quality: int = 95
    ):
        self.output_dir = Path(output_dir)
        self.image_format = image_format.lower()
        self.quality = quality
        
        # Validate format
        if self.image_format not in ["jpg", "png"]:
            raise ValueError(f"Unsupported image format: {image_format}")
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_frames(
        self,
        video_path: str,
        scenes: List[SceneInfo],
        position: str = "start"
    ) -> List[ImageInfo]:
        """
        Extract frames from video at scene positions.
        
        Args:
            video_path: Path to the video file
            scenes: List of SceneInfo objects
            position: Position to extract frame from ('start', 'middle', or 'end')
            
        Returns:
            List of ImageInfo objects for extracted images
            
        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If position is invalid
        """
        video_path_obj = Path(video_path)
        if not video_path_obj.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        if position not in ["start", "middle", "end"]:
            raise ValueError(f"Invalid position: {position}. Must be 'start', 'middle', or 'end'")
        
        # Open video
        cap = cv2.VideoCapture(str(video_path_obj))
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")
        
        images = []
        
        try:
            for scene in scenes:
                # Calculate frame number based on position
                frame_number = self._get_frame_number(scene, position)
                
                # Set video position to the frame
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
                
                # Read frame
                ret, frame = cap.read()
                if not ret:
                    print(f"Warning: Failed to read frame {frame_number} for scene {scene.scene_number}")
                    continue
                
                # Save frame
                image_path = self._save_frame(frame, scene.scene_number)
                
                # Create ImageInfo
                height, width = frame.shape[:2]
                images.append(ImageInfo(
                    file_path=str(image_path),
                    scene_number=scene.scene_number,
                    timestamp=scene.start_time if position == "start" else 
                             (scene.start_time + scene.end_time) / 2 if position == "middle" else
                             scene.end_time,
                    frame_number=frame_number,
                    width=width,
                    height=height
                ))
        
        finally:
            cap.release()
        
        return images
    
    def _get_frame_number(self, scene: SceneInfo, position: str) -> int:
        """Calculate frame number based on position in scene."""
        if position == "start":
            return scene.start_frame
        elif position == "middle":
            return (scene.start_frame + scene.end_frame) // 2
        else:  # end
            return scene.end_frame - 1  # -1 to avoid going to next scene
    
    def _save_frame(self, frame, scene_number: int) -> Path:
        """Save frame to file."""
        # Generate filename
        filename = f"scene_{scene_number:04d}.{self.image_format}"
        output_path = self.output_dir / filename
        
        # Convert BGR to RGB (OpenCV uses BGR)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Save using PIL for better quality control
        image = Image.fromarray(frame_rgb)
        
        if self.image_format == "jpg":
            image.save(output_path, "JPEG", quality=self.quality, optimize=True)
        else:  # png
            image.save(output_path, "PNG", optimize=True)
        
        return output_path
    
    def resize_image(
        self,
        image_path: str,
        max_width: int | None = None,
        max_height: int | None = None
    ) -> None:
        """
        Resize image while maintaining aspect ratio.
        
        Args:
            image_path: Path to the image file
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
        """
        if max_width is None and max_height is None:
            return
        
        image = Image.open(image_path)
        width, height = image.size
        
        # Calculate new size maintaining aspect ratio
        if max_width and max_height:
            ratio = min(max_width / width, max_height / height)
        elif max_width:
            ratio = max_width / width
        else:  # max_height
            ratio = max_height / height
        
        if ratio < 1:  # Only resize if image is larger
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save resized image
            if self.image_format == "jpg":
                image.save(image_path, "JPEG", quality=self.quality, optimize=True)
            else:
                image.save(image_path, "PNG", optimize=True)

# Made with Bob
