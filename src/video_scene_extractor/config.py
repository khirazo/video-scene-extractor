# This file includes AI-generated code - Review and modify as needed

"""
Configuration management module for loading and validating settings.
"""

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class DetectionConfig:
    """Scene detection configuration."""
    threshold: float = 17.0
    min_scene_len: int = 15
    position: str = "start"
    
    def validate(self) -> None:
        """Validate detection configuration."""
        if not 0 <= self.threshold <= 100:
            raise ValueError(f"threshold must be between 0 and 100, got {self.threshold}")
        if self.min_scene_len < 1:
            raise ValueError(f"min_scene_len must be >= 1, got {self.min_scene_len}")
        if self.position not in ["start", "middle", "end"]:
            raise ValueError(f"position must be 'start', 'middle', or 'end', got {self.position}")


@dataclass
class ImageConfig:
    """Image extraction configuration."""
    format: str = "jpg"
    quality: int = 95
    max_width: int | None = None
    max_height: int | None = None
    
    def validate(self) -> None:
        """Validate image configuration."""
        if self.format not in ["jpg", "png"]:
            raise ValueError(f"format must be 'jpg' or 'png', got {self.format}")
        if not 1 <= self.quality <= 100:
            raise ValueError(f"quality must be between 1 and 100, got {self.quality}")
        if self.max_width is not None and self.max_width < 1:
            raise ValueError(f"max_width must be >= 1, got {self.max_width}")
        if self.max_height is not None and self.max_height < 1:
            raise ValueError(f"max_height must be >= 1, got {self.max_height}")


@dataclass
class PDFMetadata:
    """PDF metadata configuration."""
    author: str | None = None
    subject: str = "Video Scene Extraction"
    keywords: str = "video, screenshot, training"


@dataclass
class PDFConfig:
    """PDF generation configuration."""
    page_size: str = "A4"
    orientation: str = "landscape"
    add_timestamp: bool = True
    title: str | None = None
    metadata: PDFMetadata = field(default_factory=PDFMetadata)
    
    def validate(self) -> None:
        """Validate PDF configuration."""
        valid_sizes = ["A4", "LETTER", "A3", "LEGAL"]
        if self.page_size.upper() not in valid_sizes:
            raise ValueError(f"page_size must be one of {valid_sizes}, got {self.page_size}")
        if self.orientation not in ["portrait", "landscape"]:
            raise ValueError(f"orientation must be 'portrait' or 'landscape', got {self.orientation}")


@dataclass
class OutputConfig:
    """Output configuration."""
    output_dir: str = "./frames"
    keep_images: bool = False
    verbose: bool = False
    
    def validate(self) -> None:
        """Validate output configuration."""
        # No specific validation needed for now
        pass


@dataclass
class Config:
    """Main configuration class."""
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    image: ImageConfig = field(default_factory=ImageConfig)
    pdf: PDFConfig = field(default_factory=PDFConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    
    def validate(self) -> None:
        """Validate all configuration sections."""
        self.detection.validate()
        self.image.validate()
        self.pdf.validate()
        self.output.validate()
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Config":
        """
        Create Config from dictionary.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            Config instance
        """
        detection_data = data.get("detection", {})
        image_data = data.get("image", {})
        pdf_data = data.get("pdf", {})
        output_data = data.get("output", {})
        
        # Handle PDF metadata separately
        pdf_metadata_data = pdf_data.pop("metadata", {})
        pdf_metadata = PDFMetadata(**pdf_metadata_data)
        
        config = cls(
            detection=DetectionConfig(**detection_data),
            image=ImageConfig(**image_data),
            pdf=PDFConfig(**pdf_data, metadata=pdf_metadata),
            output=OutputConfig(**output_data)
        )
        
        config.validate()
        return config
    
    @classmethod
    def from_yaml(cls, yaml_path: str | Path) -> "Config":
        """
        Load configuration from YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            Config instance
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        yaml_path = Path(yaml_path)
        
        if not yaml_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {yaml_path}")
        
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data is None:
                data = {}
            
            return cls.from_dict(data)
        
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
        except Exception as e:
            raise ValueError(f"Error loading configuration: {e}")
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Configuration dictionary
        """
        return {
            "detection": {
                "threshold": self.detection.threshold,
                "min_scene_len": self.detection.min_scene_len,
                "position": self.detection.position,
            },
            "image": {
                "format": self.image.format,
                "quality": self.image.quality,
                "max_width": self.image.max_width,
                "max_height": self.image.max_height,
            },
            "pdf": {
                "page_size": self.pdf.page_size,
                "orientation": self.pdf.orientation,
                "add_timestamp": self.pdf.add_timestamp,
                "title": self.pdf.title,
                "metadata": {
                    "author": self.pdf.metadata.author,
                    "subject": self.pdf.metadata.subject,
                    "keywords": self.pdf.metadata.keywords,
                },
            },
            "output": {
                "output_dir": self.output.output_dir,
                "keep_images": self.output.keep_images,
                "verbose": self.output.verbose,
            },
        }


def load_config(config_path: str | Path | None = None) -> Config:
    """
    Load configuration from file or return default.
    
    Searches for config.yaml in the following order:
    1. Specified config_path (if provided)
    2. Current working directory
    3. Script/project root directory
    
    Args:
        config_path: Path to configuration file (optional)
        
    Returns:
        Config instance
    """
    if config_path is None:
        # Build list of paths to search
        search_paths = []
        
        # 1. Current working directory
        search_paths.extend([
            Path.cwd() / "config.yaml",
            Path.cwd() / "config.yml",
        ])
        
        # 2. Script/project root directory
        # Resolve the project root from the installed package location
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            script_dir = Path(sys.executable).parent
        else:
            # Running as Python script
            # Go up from src/video_scene_extractor to project root
            script_dir = Path(__file__).parent.parent.parent
        
        search_paths.extend([
            script_dir / "config.yaml",
            script_dir / "config.yml",
        ])
        
        # Try each path
        for path in search_paths:
            if path.exists():
                return Config.from_yaml(path)
        
        # Return default configuration
        return Config()
    
    return Config.from_yaml(config_path)

# Made with Bob
