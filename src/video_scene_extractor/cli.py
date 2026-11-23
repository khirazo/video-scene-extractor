# This file includes AI-generated code - Review and modify as needed

"""
Command-line interface for video-scene-extractor.
"""

import sys
from pathlib import Path

import click
from tqdm import tqdm

from .config import load_config
from .detector import SceneDetector
from .extractor import FrameExtractor
from .pdf_generator import PDFGenerator


def _resolve_relative_path(path: str, base_dir: Path) -> Path:
    """Resolve a relative path from the supplied base directory."""
    path_obj = Path(path)
    return path_obj if path_obj.is_absolute() else base_dir / path_obj


@click.command()
@click.argument('input_video', type=click.Path(exists=True))
@click.option(
    '--config',
    type=click.Path(exists=True),
    help='Configuration file path (YAML)'
)
@click.option(
    '-o', '--output',
    default=None,
    help='Output PDF file path [default: output.pdf]'
)
@click.option(
    '--output-dir',
    default=None,
    help='Image output directory [default: ./frames]'
)
@click.option(
    '--output-relative-to-video',
    is_flag=True,
    default=None,
    help='Resolve relative output paths from the input video directory'
)
@click.option(
    '--keep-images',
    is_flag=True,
    default=None,
    help='Keep images after PDF generation'
)
@click.option(
    '-t', '--threshold',
    default=None,
    type=float,
    help='Scene detection threshold (0-100) [default: 17.0]'
)
@click.option(
    '--min-scene-len',
    default=None,
    type=int,
    help='Minimum scene length in frames [default: 15]'
)
@click.option(
    '--position',
    default=None,
    type=click.Choice(['start', 'middle', 'end']),
    help='Frame extraction position [default: start]'
)
@click.option(
    '--format',
    'image_format',
    default=None,
    type=click.Choice(['jpg', 'png']),
    help='Image format [default: jpg]'
)
@click.option(
    '--quality',
    default=None,
    type=click.IntRange(1, 100),
    help='JPEG quality (1-100) [default: 95]'
)
@click.option(
    '--max-width',
    default=None,
    type=int,
    help='Maximum width in pixels'
)
@click.option(
    '--max-height',
    default=None,
    type=int,
    help='Maximum height in pixels'
)
@click.option(
    '--page-size',
    default=None,
    type=click.Choice(['A4', 'Letter', 'A3', 'Legal'], case_sensitive=False),
    help='Page size [default: A4]'
)
@click.option(
    '--orientation',
    default=None,
    type=click.Choice(['portrait', 'landscape']),
    help='Page orientation [default: landscape]'
)
@click.option(
    '--no-timestamp',
    is_flag=True,
    default=None,
    help='Hide timestamp on images'
)
@click.option(
    '--title',
    default=None,
    help='PDF title'
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=None,
    help='Verbose output'
)
@click.version_option(version='0.1.0')
def main(
    input_video,
    config,
    output,
    output_dir,
    output_relative_to_video,
    keep_images,
    threshold,
    min_scene_len,
    position,
    image_format,
    quality,
    max_width,
    max_height,
    page_size,
    orientation,
    no_timestamp,
    title,
    verbose
):
    """
    Extract screenshots from training videos using scene detection and merge them into PDF.
    
    INPUT_VIDEO: Path to the input video file
    """
    try:
        # Load configuration file (auto-detect if not specified)
        cfg = load_config(config)
        
        # Determine config source for display
        if config:
            config_source = f"config file: {config}"
        else:
            # Check which config file was auto-detected
            cwd = Path.cwd()
            script_dir = Path(__file__).parent.parent.parent if not getattr(sys, 'frozen', False) else Path(sys.executable).parent
            
            if (cwd / "config.yaml").exists():
                config_source = f"config file: {cwd / 'config.yaml'} (auto-detected)"
            elif (cwd / "config.yml").exists():
                config_source = f"config file: {cwd / 'config.yml'} (auto-detected)"
            elif (script_dir / "config.yaml").exists():
                config_source = f"config file: {script_dir / 'config.yaml'} (auto-detected)"
            elif (script_dir / "config.yml").exists():
                config_source = f"config file: {script_dir / 'config.yml'} (auto-detected)"
            else:
                config_source = "default"
        
        # Track parameter sources for display
        param_sources = {}
        
        # Merge CLI arguments with config (CLI takes precedence)
        if threshold is not None:
            param_sources['threshold'] = 'CLI'
        else:
            threshold = cfg.detection.threshold
            param_sources['threshold'] = config_source
            
        if min_scene_len is not None:
            param_sources['min_scene_len'] = 'CLI'
        else:
            min_scene_len = cfg.detection.min_scene_len
            param_sources['min_scene_len'] = config_source
            
        if position is not None:
            param_sources['position'] = 'CLI'
        else:
            position = cfg.detection.position
            param_sources['position'] = config_source
            
        if image_format is not None:
            param_sources['format'] = 'CLI'
        else:
            image_format = cfg.image.format
            param_sources['format'] = config_source
            
        if quality is not None:
            param_sources['quality'] = 'CLI'
        else:
            quality = cfg.image.quality
            param_sources['quality'] = config_source
            
        if max_width is not None:
            param_sources['max_width'] = 'CLI'
        else:
            max_width = cfg.image.max_width
            param_sources['max_width'] = config_source if max_width else 'not set'
            
        if max_height is not None:
            param_sources['max_height'] = 'CLI'
        else:
            max_height = cfg.image.max_height
            param_sources['max_height'] = config_source if max_height else 'not set'
            
        if page_size is not None:
            param_sources['page_size'] = 'CLI'
        else:
            page_size = cfg.pdf.page_size
            param_sources['page_size'] = config_source
            
        if orientation is not None:
            param_sources['orientation'] = 'CLI'
        else:
            orientation = cfg.pdf.orientation
            param_sources['orientation'] = config_source
            
        if no_timestamp is not None:
            add_timestamp = not no_timestamp
            param_sources['add_timestamp'] = 'CLI'
        else:
            add_timestamp = cfg.pdf.add_timestamp
            param_sources['add_timestamp'] = config_source
            
        if output is not None:
            param_sources['output'] = 'CLI'
        else:
            output = "output.pdf"
            param_sources['output'] = 'default'
            
        if output_dir is not None:
            param_sources['output_dir'] = 'CLI'
        else:
            output_dir = cfg.output.output_dir
            param_sources['output_dir'] = config_source

        if output_relative_to_video is not None:
            param_sources['output_relative_to_video'] = 'CLI'
        else:
            output_relative_to_video = cfg.output.relative_to_video
            param_sources['output_relative_to_video'] = config_source
            
        if keep_images is not None:
            param_sources['keep_images'] = 'CLI'
        else:
            keep_images = cfg.output.keep_images
            param_sources['keep_images'] = config_source
            
        if verbose is not None:
            param_sources['verbose'] = 'CLI'
        else:
            verbose = cfg.output.verbose
            param_sources['verbose'] = config_source
        
        if output_relative_to_video:
            video_dir = Path(input_video).resolve().parent
            output = str(_resolve_relative_path(output, video_dir))
            output_dir = str(_resolve_relative_path(output_dir, video_dir))

        # Always print configuration summary
        click.echo("=" * 60)
        click.echo("Configuration Summary")
        click.echo("=" * 60)
        click.echo(f"Input video: {input_video}")
        click.echo(f"Output PDF: {output} (source: {param_sources['output']})")
        click.echo(f"Output directory: {output_dir} (source: {param_sources['output_dir']})")
        click.echo()
        click.echo("Scene Detection:")
        click.echo(f"  Threshold: {threshold} (source: {param_sources['threshold']})")
        click.echo(f"  Min scene length: {min_scene_len} frames (source: {param_sources['min_scene_len']})")
        click.echo(f"  Position: {position} (source: {param_sources['position']})")
        click.echo()
        click.echo("Image Settings:")
        click.echo(f"  Format: {image_format} (source: {param_sources['format']})")
        click.echo(f"  Quality: {quality} (source: {param_sources['quality']})")
        if max_width:
            click.echo(f"  Max width: {max_width}px (source: {param_sources['max_width']})")
        if max_height:
            click.echo(f"  Max height: {max_height}px (source: {param_sources['max_height']})")
        click.echo()
        click.echo("PDF Settings:")
        click.echo(f"  Page size: {page_size} (source: {param_sources['page_size']})")
        click.echo(f"  Orientation: {orientation} (source: {param_sources['orientation']})")
        click.echo(f"  Add timestamp: {add_timestamp} (source: {param_sources['add_timestamp']})")
        click.echo()
        click.echo("Output Settings:")
        click.echo(
            "  Resolve paths from video: "
            f"{output_relative_to_video} "
            f"(source: {param_sources['output_relative_to_video']})"
        )
        click.echo(f"  Keep images: {keep_images} (source: {param_sources['keep_images']})")
        click.echo(f"  Verbose: {verbose} (source: {param_sources['verbose']})")
        click.echo("=" * 60)
        click.echo()
        
        # Step 1: Detect scenes
        click.echo("Step 1/3: Detecting scenes...")
        detector = SceneDetector(threshold=threshold, min_scene_len=min_scene_len)
        
        with tqdm(total=1, desc="Scene detection", disable=not verbose) as pbar:
            scenes = detector.detect_scenes(input_video)
            pbar.update(1)
        
        if not scenes:
            click.echo("Warning: No scenes detected. Try lowering the threshold.", err=True)
            sys.exit(1)
        
        click.echo(f"  Detected {len(scenes)} scenes")
        
        # Step 2: Extract frames
        click.echo("Step 2/3: Extracting frames...")
        extractor = FrameExtractor(
            output_dir=output_dir,
            image_format=image_format,
            quality=quality
        )
        
        images = []
        with tqdm(total=len(scenes), desc="Frame extraction", disable=not verbose) as pbar:
            images = extractor.extract_frames(input_video, scenes, position=position)
            pbar.update(len(scenes))
        
        if not images:
            click.echo("Error: No frames extracted.", err=True)
            sys.exit(1)
        
        click.echo(f"  Extracted {len(images)} frames")
        
        # Resize images if specified
        if max_width or max_height:
            click.echo("  Resizing images...")
            with tqdm(total=len(images), desc="Resizing", disable=not verbose) as pbar:
                for img in images:
                    extractor.resize_image(img.file_path, max_width, max_height)
                    pbar.update(1)
        
        # Step 3: Generate PDF
        click.echo("Step 3/3: Generating PDF...")
        generator = PDFGenerator(
            page_size=page_size,
            orientation=orientation,
            add_timestamp=add_timestamp
        )
        
        # Add timestamps to images if enabled
        if add_timestamp:
            with tqdm(total=len(images), desc="Adding timestamps", disable=not verbose) as pbar:
                for img in images:
                    generator.add_timestamp_to_image(img)
                    pbar.update(1)
        
        # Create PDF
        with tqdm(total=1, desc="PDF generation", disable=not verbose) as pbar:
            generator.create_pdf(
                images,
                output,
                title=title or Path(input_video).stem
            )
            pbar.update(1)
        
        click.echo(f"  PDF created: {output}")
        
        # Clean up images if not keeping them
        if not keep_images:
            click.echo("  Cleaning up temporary images...")
            import shutil
            shutil.rmtree(output_dir)
        
        click.echo()
        click.echo("Done!")
        
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
