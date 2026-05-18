# This file includes AI-generated code - Review and modify as needed

"""
PDF generation module for creating PDFs from extracted images.
"""

from typing import List
from pathlib import Path
import img2pdf
from PIL import Image

from .extractor import ImageInfo


class PDFGenerator:
    """
    Generate PDF from extracted images.
    
    Args:
        page_size: Page size ('A4', 'Letter', etc.)
        orientation: Page orientation ('portrait' or 'landscape')
        add_timestamp: Whether to add timestamp to images
    """
    
    def __init__(
        self,
        page_size: str = "A4",
        orientation: str = "landscape",
        add_timestamp: bool = True
    ):
        self.page_size = page_size.upper()
        self.orientation = orientation.lower()
        self.add_timestamp = add_timestamp
        
        # Validate orientation
        if self.orientation not in ["portrait", "landscape"]:
            raise ValueError(f"Invalid orientation: {orientation}. Must be 'portrait' or 'landscape'")
        
        # Define page sizes in points (1 point = 1/72 inch)
        self.page_sizes = {
            "A4": (595, 842),      # 210mm x 297mm
            "LETTER": (612, 792),  # 8.5" x 11"
            "A3": (842, 1191),     # 297mm x 420mm
            "LEGAL": (612, 1008),  # 8.5" x 14"
        }
        
        if self.page_size not in self.page_sizes:
            raise ValueError(f"Unsupported page size: {page_size}")
    
    def create_pdf(
        self,
        images: List[ImageInfo],
        output_path: str,
        title: str | None = None,
        metadata: dict | None = None
    ) -> None:
        """
        Create PDF from list of images.
        
        Args:
            images: List of ImageInfo objects (in chronological order)
            output_path: Path for output PDF file
            title: PDF title (optional)
            metadata: Additional PDF metadata (optional)
            
        Raises:
            ValueError: If no images provided or images don't exist
        """
        if not images:
            raise ValueError("No images provided")
        
        # Verify all image files exist
        image_paths = []
        for img_info in images:
            img_path = Path(img_info.file_path)
            if not img_path.exists():
                raise ValueError(f"Image file not found: {img_info.file_path}")
            image_paths.append(str(img_path))
        
        # Get page dimensions
        page_width, page_height = self.page_sizes[self.page_size]
        
        # Swap dimensions for landscape
        if self.orientation == "landscape":
            page_width, page_height = page_height, page_width
        
        # Create layout for img2pdf
        layout_fun = img2pdf.get_layout_fun(
            (page_width, page_height),
            fit=img2pdf.FitMode.into
        )
        
        # Prepare metadata
        pdf_metadata = {}
        if title:
            pdf_metadata["title"] = title
        if metadata:
            pdf_metadata.update(metadata)
        
        # Convert images to PDF
        try:
            with open(output_path, "wb") as f:
                f.write(
                    img2pdf.convert(
                        image_paths,
                        layout_fun=layout_fun,
                        **pdf_metadata
                    )
                )
        except Exception as e:
            raise ValueError(f"Failed to create PDF: {str(e)}")
    
    def add_timestamp_to_image(self, image_info: ImageInfo) -> None:
        """
        Add timestamp text to an image.
        
        Args:
            image_info: ImageInfo object containing image path and timestamp
        """
        if not self.add_timestamp:
            return
        
        from PIL import ImageDraw, ImageFont
        
        # Open image
        image = Image.open(image_info.file_path)
        draw = ImageDraw.Draw(image)
        
        # Format timestamp
        minutes = int(image_info.timestamp // 60)
        seconds = int(image_info.timestamp % 60)
        timestamp_text = f"Scene {image_info.scene_number} - {minutes:02d}:{seconds:02d}"
        
        # Try to use a nice font, fall back to default if not available
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position (bottom-right corner with padding)
        text_bbox = draw.textbbox((0, 0), timestamp_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        padding = 10
        x = image.width - text_width - padding
        y = image.height - text_height - padding
        
        # Draw background rectangle for better readability
        draw.rectangle(
            [x - 5, y - 5, x + text_width + 5, y + text_height + 5],
            fill=(0, 0, 0, 180)
        )
        
        # Draw text
        draw.text((x, y), timestamp_text, fill=(255, 255, 255), font=font)
        
        # Save image
        image.save(image_info.file_path)

# Made with Bob
