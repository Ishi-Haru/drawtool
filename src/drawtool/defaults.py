"""Default configuration for text rendering."""

from pathlib import Path
from typing import List, Dict, Any, Literal


class TextDefaults:
    """Default text rendering settings."""

    # Font size (in pixels)
    FONT_SIZE: int = 32

    # Text color (hex format)
    FONT_COLOR: str = "#000000"

    # Text alpha/opacity (0-255, 255=opaque, 0=transparent)
    ALPHA: int = 255

    # Bold font (enabled/disabled)
    BOLD: bool = False

    # Text alignment within text box (left, center, right)
    TEXT_ALIGN: Literal["left", "center", "right"] = "left"

    # Text anchor point - vertical (top, middle, bottom)
    ANCHOR_VERTICAL: Literal["top", "middle", "bottom"] = "top"

    # Text anchor point - horizontal (left, center, right)
    ANCHOR_HORIZONTAL: Literal["left", "center", "right"] = "left"

    # Text rotation in degrees (clockwise)
    ROTATION: float = 0.0

    # Font family candidates (tried in order, first match is used)
    FONT_PATHS: List[Path] = [
        Path("C:/Windows/Fonts/times.ttf"),  # Windows
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),  # Linux
        Path("/Library/Fonts/Times New Roman.ttf"),  # macOS
    ]

    # Bold font family candidates
    BOLD_FONT_PATHS: List[Path] = [
        Path("C:/Windows/Fonts/timesbd.ttf"),  # Windows
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),  # Linux
        Path("/Library/Fonts/Times New Roman Bold.ttf"),  # macOS
    ]

    # Default font family name (for informational purposes)
    DEFAULT_FONT_FAMILY: str = "Times New Roman"

    @classmethod
    def get_defaults(cls) -> Dict[str, Any]:
        """Get all text defaults as a dictionary."""
        return {
            "size": cls.FONT_SIZE,
            "color": cls.FONT_COLOR,
            "alpha": cls.ALPHA,
            "family": cls.DEFAULT_FONT_FAMILY,
            "bold": cls.BOLD,
            "align": cls.TEXT_ALIGN,
            "anchor_v": cls.ANCHOR_VERTICAL,
            "anchor_h": cls.ANCHOR_HORIZONTAL,
            "rotation": cls.ROTATION,
        }
