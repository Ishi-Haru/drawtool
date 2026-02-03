from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from drawtool.defaults import TextDefaults, ImageDefaults


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

        # Get image settings
        scale = float(el.get("scale", 1.0))
        alpha = int(el.get("alpha", ImageDefaults.ALPHA))
        rotation = float(el.get("rotation", ImageDefaults.ROTATION))
        anchor_v = el.get("anchor_v", ImageDefaults.ANCHOR_VERTICAL)
        anchor_h = el.get("anchor_h", ImageDefaults.ANCHOR_HORIZONTAL)

        # Apply scale
        if scale != 1.0:
            new_w = max(1, int(img.width * scale))
            new_h = max(1, int(img.height * scale))
            img = img.resize((new_w, new_h), resample=Image.Resampling.LANCZOS)

        # Apply alpha if not fully opaque
        if alpha < 255:
            # Apply alpha channel multiplication
            alpha_factor = alpha / 255.0
            img_data = img.getdata()
            new_data = []
            for item in img_data:
                # item is (R, G, B, A)
                new_alpha = int(item[3] * alpha_factor)
                new_data.append((item[0], item[1], item[2], new_alpha))
            img.putdata(new_data)

        # Apply rotation if specified
        if rotation != 0:
            img = img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)

        # Calculate anchor offset
        offset_x, offset_y = self._calculate_anchor_offset(img.width, img.height, anchor_v, anchor_h)

        # Composite image at position with anchor offset
        x, y = int(el["x"]), int(el["y"])
        canvas.alpha_composite(img, dest=(x - offset_x, y - offset_y))

    def _draw_text(self, draw: ImageDraw.ImageDraw, el: Dict[str, Any]) -> None:
        x, y = int(el["x"]), int(el["y"])
        text = str(el["text"])

        font_cfg = el.get("font", {}) if isinstance(el.get("font", {}), dict) else {}
        size = int(font_cfg.get("size", TextDefaults.FONT_SIZE))
        color = font_cfg.get("color", TextDefaults.FONT_COLOR)
        alpha = int(font_cfg.get("alpha", TextDefaults.ALPHA))
        bold = bool(font_cfg.get("bold", TextDefaults.BOLD))
        align = font_cfg.get("align", TextDefaults.TEXT_ALIGN)
        anchor_v = font_cfg.get("anchor_v", TextDefaults.ANCHOR_VERTICAL)
        anchor_h = font_cfg.get("anchor_h", TextDefaults.ANCHOR_HORIZONTAL)
        rotation = float(font_cfg.get("rotation", TextDefaults.ROTATION))
        glow_cfg = font_cfg.get("glow", None) if isinstance(font_cfg.get("glow", {}), dict) else None

        # Convert color to RGBA format with alpha
        rgba_color = self._color_with_alpha(color, alpha)

        # Load TrueType font with specified size and bold setting
        font = self._load_font(size, bold)

        # Calculate anchor string for Pillow
        anchor_map_v = {"top": "a", "middle": "m", "bottom": "s"}
        anchor_map_h = {"left": "l", "center": "m", "right": "r"}
        anchor_str = anchor_map_h[anchor_h] + anchor_map_v[anchor_v]

        # If alpha is not fully opaque, rotation is used, or glow is enabled, render to temp image first
        needs_compositing = alpha < 255 or rotation != 0 or glow_cfg is not None

        # For multi-line text, handle alignment
        if "\n" in text:
            # Multi-line text with alignment
            if needs_compositing:
                # Render to a separate image first for alpha, rotation, or glow
                temp_img = self._render_text_to_image(text, font, rgba_color, align)
                
                # Apply glow effect if specified
                if glow_cfg:
                    temp_img = self._apply_glow(temp_img, glow_cfg)
                
                if rotation != 0:
                    temp_img = temp_img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
                
                # Calculate position based on anchor
                offset_x, offset_y = self._calculate_anchor_offset(temp_img.width, temp_img.height, anchor_v, anchor_h)
                draw._image.alpha_composite(temp_img, dest=(x - offset_x, y - offset_y))
            else:
                # Non-rotated fully opaque multi-line text - direct draw
                draw.multiline_text((x, y), text, fill=rgba_color, font=font, align=align, anchor=anchor_str)
        else:
            # Single-line text
            if needs_compositing:
                # Render to a separate image first for alpha, rotation, or glow
                temp_img = self._render_text_to_image(text, font, rgba_color, "left")
                
                # Apply glow effect if specified
                if glow_cfg:
                    temp_img = self._apply_glow(temp_img, glow_cfg)
                
                if rotation != 0:
                    temp_img = temp_img.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
                
                # Calculate position based on anchor
                offset_x, offset_y = self._calculate_anchor_offset(temp_img.width, temp_img.height, anchor_v, anchor_h)
                draw._image.alpha_composite(temp_img, dest=(x - offset_x, y - offset_y))
            else:
                # Non-rotated fully opaque single-line text - direct draw
                draw.text((x, y), text, fill=rgba_color, font=font, anchor=anchor_str)

    def _render_text_to_image(self, text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                               color: tuple[int, int, int, int], align: str) -> Image.Image:
        """Render text to a temporary image for rotation."""
        # Create a dummy draw to calculate text bounding box
        dummy_img = Image.new("RGBA", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        
        # Calculate text bounding box
        if "\n" in text:
            bbox = dummy_draw.multiline_textbbox((0, 0), text, font=font, align=align)
        else:
            bbox = dummy_draw.textbbox((0, 0), text, font=font)
        
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create temporary image with padding
        padding = 10
        temp_img = Image.new("RGBA", (text_width + padding * 2, text_height + padding * 2), (255, 255, 255, 0))
        temp_draw = ImageDraw.Draw(temp_img)
        
        # Draw text at the center of temp image
        if "\n" in text:
            temp_draw.multiline_text((padding - bbox[0], padding - bbox[1]), text, fill=color, font=font, align=align)
        else:
            temp_draw.text((padding - bbox[0], padding - bbox[1]), text, fill=color, font=font)
        
        # Crop to actual text size
        return temp_img.crop((padding, padding, padding + text_width, padding + text_height))

    def _apply_glow(self, text_img: Image.Image, glow_cfg: Dict[str, Any]) -> Image.Image:
        """Apply glow effect to text image."""
        glow_color = glow_cfg.get("color", "#FFFFFF")
        glow_radius = int(glow_cfg.get("radius", 10))
        glow_alpha = int(glow_cfg.get("alpha", 200))
        
        # Create a larger canvas to accommodate the glow
        margin = glow_radius * 3
        glow_width = text_img.width + margin * 2
        glow_height = text_img.height + margin * 2
        
        # Extract text alpha channel
        text_alpha = text_img.split()[3]
        
        # Create a grayscale mask from text alpha for blurring
        alpha_mask = Image.new("L", (glow_width, glow_height), 0)
        alpha_mask.paste(text_alpha, (margin, margin))
        
        # Apply Gaussian blur to create glow effect
        blurred_mask = alpha_mask.filter(ImageFilter.GaussianBlur(radius=glow_radius))
        
        # Create glow layer with the blurred mask
        glow_r, glow_g, glow_b, _ = self._color_with_alpha(glow_color, 255)
        glow_layer = Image.new("RGBA", (glow_width, glow_height), (0, 0, 0, 0))
        
        # Create glow color image and apply blurred mask with glow_alpha strength
        glow_colored = Image.new("RGB", (glow_width, glow_height), (glow_r, glow_g, glow_b))
        
        # Create the glow alpha channel by scaling blurred mask with glow_alpha
        glow_alpha_channel = Image.new("L", (glow_width, glow_height), 0)
        glow_alpha_data = []
        for pixel in blurred_mask.getdata():
            # Scale the blurred mask value to glow_alpha
            glow_alpha_data.append(int(pixel * glow_alpha / 255))
        glow_alpha_channel.putdata(glow_alpha_data)
        
        # Merge color with alpha channel
        glow_layer = Image.merge("RGBA", (glow_colored.split()[0], glow_colored.split()[1], glow_colored.split()[2], glow_alpha_channel))
        
        # Paste original text on top
        glow_layer.alpha_composite(text_img, dest=(margin, margin))
        
        return glow_layer

    def _color_with_alpha(self, color: str, alpha: int) -> tuple[int, int, int, int]:
        """Convert hex color to RGBA tuple with alpha channel."""
        # Remove '#' if present
        if color.startswith('#'):
            color = color[1:]
        
        # Parse RGB values
        if len(color) == 6:
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
        elif len(color) == 3:
            r = int(color[0] * 2, 16)
            g = int(color[1] * 2, 16)
            b = int(color[2] * 2, 16)
        else:
            # Fallback to black if invalid format
            r, g, b = 0, 0, 0
        
        # Clamp alpha to 0-255 range
        alpha = max(0, min(255, alpha))
        
        return (r, g, b, alpha)

    def _calculate_anchor_offset(self, width: int, height: int, anchor_v: str, anchor_h: str) -> tuple[int, int]:
        """Calculate offset based on anchor point."""
        offset_x = 0
        offset_y = 0
        
        # Horizontal offset
        if anchor_h == "center":
            offset_x = width // 2
        elif anchor_h == "right":
            offset_x = width
        
        # Vertical offset
        if anchor_v == "middle":
            offset_y = height // 2
        elif anchor_v == "bottom":
            offset_y = height
        
        return offset_x, offset_y

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
