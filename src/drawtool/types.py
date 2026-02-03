from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional, TypedDict, List, Dict, Any


ElementType = Literal["image", "text"]


class CanvasCfg(TypedDict):
    width: int
    height: int
    background: str  # "#RRGGBB"


class OutputCfg(TypedDict, total=False):
    path: str


class AssetsCfg(TypedDict, total=False):
    base_dir: str


class GlowCfg(TypedDict, total=False):
    color: str
    radius: int
    alpha: int


class FontCfg(TypedDict, total=False):
    family: str
    size: int
    color: str
    alpha: int
    bold: bool
    align: Literal["left", "center", "right"]
    anchor_v: Literal["top", "middle", "bottom"]
    anchor_h: Literal["left", "center", "right"]
    rotation: float
    glow: GlowCfg


class BaseElementCfg(TypedDict, total=False):
    type: ElementType
    id: str
    x: int
    y: int
    z: int


class ImageElementCfg(BaseElementCfg, total=False):
    type: Literal["image"]
    path: str
    scale: float
    alpha: int
    rotation: float
    anchor_v: Literal["top", "middle", "bottom"]
    anchor_h: Literal["left", "center", "right"]


class TextElementCfg(BaseElementCfg, total=False):
    type: Literal["text"]
    text: str
    font: FontCfg


class LayerCfg(TypedDict, total=False):
    id: str
    order: int
    elements: List[Dict[str, Any]]


class Config(TypedDict, total=False):
    version: str
    output: OutputCfg
    canvas: CanvasCfg
    assets: AssetsCfg
    elements: List[Dict[str, Any]]
    layers: List[LayerCfg]
