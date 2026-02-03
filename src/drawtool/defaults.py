"""Default configuration for text rendering."""

from pathlib import Path
from typing import List, Dict, Any


class TextDefaults:
    """Default text rendering settings."""

    # Font size (in pixels)
    FONT_SIZE: int = 32

    # Text color (hex format)
    FONT_COLOR: str = "#000000"

    # Bold font (enabled/disabled)
    BOLD: bool = False

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
            "family": cls.DEFAULT_FONT_FAMILY,
            "bold": cls.BOLD,
        }
