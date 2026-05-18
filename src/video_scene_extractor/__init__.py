# This file includes AI-generated code - Review and modify as needed

"""
Video Scene Extractor

Extract screenshots from training videos using scene detection and merge them into PDF.
"""

__version__ = "0.1.0"

from .detector import SceneDetector, SceneInfo
from .extractor import FrameExtractor, ImageInfo
from .pdf_generator import PDFGenerator

__all__ = [
    "SceneDetector",
    "SceneInfo",
    "FrameExtractor",
    "ImageInfo",
    "PDFGenerator",
]

# Made with Bob
