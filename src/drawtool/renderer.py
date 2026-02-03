from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

from drawtool.defaults import TextDefaults


@dataclass
class FigureRenderer:
    config_path: Path

    def __post_init__(self) -> None:
        self.config_path = Path(self.config_path)

    def render(self, output_path: str | Path | None = None) -> Path:
        cfg = self._load_config()
        self._validate_config(cfg)

        base_dir = self._assets_base_dir(cfg)
        canvas = self._create_canvas(cfg)
        draw = ImageDraw.Draw(canvas)

        # Get elements: use layers if available, otherwise fall back to elements
        all_elements = self._get_all_elements(cfg)

        # Draw elements (already sorted by layer order and element order)
        for el in all_elements:
            el_type = el["type"]
            if el_type == "image":
                self._draw_image(canvas, el, base_dir)
            elif el_type == "text":
                self._draw_text(draw, el)
            else:
                raise ValueError(f"Unknown element type: {el_type}")

        out = self._resolve_output_path(cfg, output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out)
        return out

    # ---------- config ----------
    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        with self.config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _validate_config(self, cfg: Dict[str, Any]) -> None:
        if "canvas" not in cfg:
            raise ValueError("Missing required key: canvas")
        for k in ("width", "height", "background"):
            if k not in cfg["canvas"]:
                raise ValueError(f"Missing required key: canvas.{k}")

        w, h = cfg["canvas"]["width"], cfg["canvas"]["height"]
        if not (isinstance(w, int) and w > 0 and isinstance(h, int) and h > 0):
            raise ValueError("canvas.width/height must be positive integers")

        # Check for either 'elements' or 'layers'
        has_elements = "elements" in cfg and isinstance(cfg["elements"], list)
        has_layers = "layers" in cfg and isinstance(cfg["layers"], list)

        if not has_elements and not has_layers:
            raise ValueError("Missing required key: elements or layers (list)")

        # Validate elements if present
        if has_elements:
            for i, el in enumerate(cfg["elements"]):
                self._validate_element(el, i, "elements")

        # Validate layers if present
        if has_layers:
            for layer_idx, layer in enumerate(cfg["layers"]):
                if "elements" not in layer or not isinstance(layer["elements"], list):
                    raise ValueError(f"layers[{layer_idx}] missing elements (list)")
                for el_idx, el in enumerate(layer["elements"]):
                    self._validate_element(el, el_idx, f"layers[{layer_idx}].elements")

    def _validate_element(self, el: Dict[str, Any], idx: int, path: str) -> None:
        """Validate a single element."""
        if "type" not in el:
            raise ValueError(f"{path}[{idx}] missing type")
        if "x" not in el or "y" not in el:
            raise ValueError(f"{path}[{idx}] missing x/y")
        if el["type"] == "image":
            if "path" not in el:
                raise ValueError(f"{path}[{idx}] image missing path")
            if "scale" in el and (not isinstance(el["scale"], (int, float)) or el["scale"] <= 0):
                raise ValueError(f"{path}[{idx}] image scale must be > 0")
        if el["type"] == "text":
            if "text" not in el:
                raise ValueError(f"{path}[{idx}] text missing text")

    def _assets_base_dir(self, cfg: Dict[str, Any]) -> Path:
        base_dir = cfg.get("assets", {}).get("base_dir", "")
        # base_dir is relative to config file directory
        return (self.config_path.parent / base_dir).resolve()

    def _resolve_output_path(self, cfg: Dict[str, Any], override: str | Path | None) -> Path:
        if override is not None:
            return Path(override)
        p = cfg.get("output", {}).get("path", "build/figure.png")
        return (self.config_path.parent / p).resolve()

    def _get_all_elements(self, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get all elements from either layers or elements, sorted by layer order then element order."""
        if "layers" in cfg and isinstance(cfg["layers"], list) and cfg["layers"]:
            # Use layers if available
            all_elements: List[Tuple[int, int, Dict[str, Any]]] = []
            for layer_idx, layer in enumerate(cfg["layers"]):
                layer_order = int(layer.get("order", layer_idx * 10))
                elements = layer.get("elements", [])
                for el_idx, el in enumerate(elements):
                    el_order = int(el.get("z", el_idx))
                    all_elements.append((layer_order, el_order, el))

            # Sort by layer_order first, then by el_order
            all_elements.sort(key=lambda x: (x[0], x[1]))
            return [el for _, _, el in all_elements]
        else:
            # Fall back to elements (legacy mode)
            return self._sorted_elements(cfg.get("elements", []))

    # ---------- rendering ----------
    def _create_canvas(self, cfg: Dict[str, Any]) -> Image.Image:
        c = cfg["canvas"]
        w, h = c["width"], c["height"]
        bg = c.get("background", "#FFFFFF")
        return Image.new("RGBA", (w, h), bg)

    def _sorted_elements(self, elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # if z exists, sort by z, else keep original order (stable)
        def key(el: Dict[str, Any]) -> Tuple[int, int]:
            z = el.get("z", 0)
            return (int(z), 0)

        # stable sort: Python sort is stable, so original order preserved within same z
        return sorted(elements, key=key)

    def _draw_image(self, canvas: Image.Image, el: Dict[str, Any], base_dir: Path) -> None:
        rel = el["path"]
        src_path = (base_dir / rel).resolve()
        if not src_path.exists():
            el_id = el.get("id", "?")
            raise FileNotFoundError(f"Image not found (id={el_id}): {src_path}")

        img = Image.open(src_path).convert("RGBA")

        scale = float(el.get("scale", 1.0))
        if scale != 1.0:
            new_w = max(1, int(img.width * scale))
            new_h = max(1, int(img.height * scale))
            img = img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)

        x, y = int(el["x"]), int(el["y"])
        canvas.alpha_composite(img, dest=(x, y))

    def _draw_text(self, draw: ImageDraw.ImageDraw, el: Dict[str, Any]) -> None:
        x, y = int(el["x"]), int(el["y"])
        text = str(el["text"])

        font_cfg = el.get("font", {}) if isinstance(el.get("font", {}), dict) else {}
        size = int(font_cfg.get("size", TextDefaults.FONT_SIZE))
        color = font_cfg.get("color", TextDefaults.FONT_COLOR)
        bold = bool(font_cfg.get("bold", TextDefaults.BOLD))

        # Load TrueType font with specified size and bold setting
        font = self._load_font(size, bold)

        draw.text((x, y), text, fill=color, font=font)

    def _load_font(self, size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Load a TrueType font with the specified size and bold setting."""
        # Choose font paths based on bold setting
        font_paths = TextDefaults.BOLD_FONT_PATHS if bold else TextDefaults.FONT_PATHS
        
        # Try to use system fonts from defaults
        for font_path in font_paths:
            if font_path.exists():
                try:
                    return ImageFont.truetype(str(font_path), size=size)
                except Exception:
                    continue

        # If bold font not found, try regular fonts
        if bold:
            for font_path in TextDefaults.FONT_PATHS:
                if font_path.exists():
                    try:
                        return ImageFont.truetype(str(font_path), size=size)
                    except Exception:
                        continue

        # Fallback to default font if no TrueType font is found
        return ImageFont.load_default()
