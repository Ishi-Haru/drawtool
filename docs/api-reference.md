# API Reference

drawtoolライブラリの完全なAPIリファレンスです。

## 目次

- [FigureRenderer](#figurerenderer)
- [設定型（Types）](#設定型types)
- [デフォルト値（Defaults）](#デフォルト値defaults)

---

## FigureRenderer

メインのレンダリングクラス。JSON設定ファイルから図を生成します。

### クラス定義

```python
from drawtool.renderer import FigureRenderer

@dataclass
class FigureRenderer:
    config_path: Path
```

### コンストラクタ

```python
FigureRenderer(config_path: str | Path)
```

**引数:**
- `config_path` (str | Path): JSON設定ファイルのパス

**例:**
```python
renderer = FigureRenderer("config.json")
renderer = FigureRenderer(Path("./config/figure.json"))
```

---

### render()

設定ファイルに基づいて図を生成し、画像ファイルとして保存します。

```python
def render(self, output_path: str | Path | None = None) -> Path
```

**引数:**
- `output_path` (str | Path | None, optional): 出力ファイルのパス。指定しない場合はJSON設定の`output.path`を使用

**戻り値:**
- `Path`: 生成された画像ファイルの絶対パス

**例外:**
- `FileNotFoundError`: 設定ファイルまたは画像アセットが見つからない場合
- `ValueError`: 設定ファイルの内容が不正な場合

**例:**
```python
# JSON設定のoutput.pathを使用
output = renderer.render()

# 出力パスを上書き
output = renderer.render("custom_output.png")
output = renderer.render(Path("./output/figure.png"))
```

---

## 設定型（Types）

JSON設定ファイルの構造を定義する型です（`drawtool.types`モジュール）。

### Config

最上位の設定オブジェクト。

```python
class Config(TypedDict, total=False):
    version: str
    output: OutputCfg
    canvas: CanvasCfg
    assets: AssetsCfg
    elements: List[Dict[str, Any]]
    layers: List[LayerCfg]
```

**フィールド:**
- `version` (str, optional): 設定ファイルのバージョン（例: "0.1"）
- `output` (OutputCfg, optional): 出力設定
- `canvas` (CanvasCfg, **必須**): キャンバス設定
- `assets` (AssetsCfg, optional): アセットディレクトリ設定
- `elements` (List, optional): 要素のリスト（レガシーモード）
- `layers` (List[LayerCfg], optional): レイヤーのリスト（推奨）

**注意:** `elements`または`layers`のいずれかが必須です。

---

### CanvasCfg

キャンバス（出力画像）の設定。

```python
class CanvasCfg(TypedDict):
    width: int
    height: int
    background: str  # "#RRGGBB"
```

**フィールド:**
- `width` (int, **必須**): 画像の幅（ピクセル）
- `height` (int, **必須**): 画像の高さ（ピクセル）
- `background` (str, **必須**): 背景色（16進数カラーコード、例: "#FFFFFF"）

**例:**
```json
{
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#F0F0F0"
  }
}
```

---

### OutputCfg

出力ファイルの設定。

```python
class OutputCfg(TypedDict, total=False):
    path: str
```

**フィールド:**
- `path` (str, optional): 出力ファイルのパス（JSON設定ファイルからの相対パス）
  - デフォルト: `"build/figure.png"`

**例:**
```json
{
  "output": {
    "path": "output/my_figure.png"
  }
}
```

---

### AssetsCfg

アセット（画像ファイル）のベースディレクトリ設定。

```python
class AssetsCfg(TypedDict, total=False):
    base_dir: str
```

**フィールド:**
- `base_dir` (str, optional): アセットのベースディレクトリ（JSON設定ファイルからの相対パス）
  - デフォルト: `""` (設定ファイルと同じディレクトリ)

**例:**
```json
{
  "assets": {
    "base_dir": "./images"
  }
}
```

---

### LayerCfg

レイヤーの設定。

```python
class LayerCfg(TypedDict, total=False):
    id: str
    order: int
    elements: List[Dict[str, Any]]
```

**フィールド:**
- `id` (str, optional): レイヤーの識別子
- `order` (int, optional): レイヤーの描画順序（小さい値が背面）
  - デフォルト: レイヤーのインデックス × 10
- `elements` (List, **必須**): レイヤー内の要素のリスト

**例:**
```json
{
  "layers": [
    {
      "id": "background",
      "order": 0,
      "elements": [...]
    },
    {
      "id": "foreground",
      "order": 10,
      "elements": [...]
    }
  ]
}
```

---

### BaseElementCfg

全ての要素の共通設定。

```python
class BaseElementCfg(TypedDict, total=False):
    type: ElementType  # "image" | "text"
    id: str
    x: int
    y: int
    z: int
```

**フィールド:**
- `type` (str, **必須**): 要素のタイプ（`"image"` または `"text"`）
- `id` (str, optional): 要素の識別子
- `x` (int, **必須**): X座標（ピクセル）
- `y` (int, **必須**): Y座標（ピクセル）
- `z` (int, optional): レイヤー内での描画順序（大きい値が前面）
  - デフォルト: `0`

---

### ImageElementCfg

画像要素の設定。

```python
class ImageElementCfg(BaseElementCfg, total=False):
    type: Literal["image"]
    path: str
    scale: float
    alpha: int
    rotation: float
    anchor_v: Literal["top", "middle", "bottom"]
    anchor_h: Literal["left", "center", "right"]
```

**フィールド:**
- `type` (str, **必須**): `"image"`
- `path` (str, **必須**): 画像ファイルのパス（`assets.base_dir`からの相対パス）
- `scale` (float, optional): 拡大縮小率
  - デフォルト: `1.0` (100%)
- `alpha` (int, optional): 透明度（0-255）
  - デフォルト: `255` (不透明)
- `rotation` (float, optional): 回転角度（度数、時計回り）
  - デフォルト: `0.0`
- `anchor_v` (str, optional): 垂直方向の原点位置（`"top"`, `"middle"`, `"bottom"`）
  - デフォルト: `"top"`
- `anchor_h` (str, optional): 水平方向の原点位置（`"left"`, `"center"`, `"right"`）
  - デフォルト: `"left"`

**例:**
```json
{
  "type": "image",
  "id": "photo1",
  "path": "sample.png",
  "x": 300,
  "y": 200,
  "scale": 0.8,
  "alpha": 200,
  "rotation": -15,
  "anchor_h": "center",
  "anchor_v": "middle"
}
```

---

### TextElementCfg

テキスト要素の設定。

```python
class TextElementCfg(BaseElementCfg, total=False):
    type: Literal["text"]
    text: str
    font: FontCfg
```

**フィールド:**
- `type` (str, **必須**): `"text"`
- `text` (str, **必須**): 表示するテキスト（改行は`\n`）
- `font` (FontCfg, optional): フォント設定

**例:**
```json
{
  "type": "text",
  "id": "title",
  "text": "My Figure",
  "x": 600,
  "y": 50,
  "font": {
    "size": 36,
    "color": "#000000",
    "bold": true
  }
}
```

---

### FontCfg

フォント（テキストスタイル）の設定。

```python
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
```

**フィールド:**
- `family` (str, optional): フォントファミリー名
  - デフォルト: `"Times New Roman"`
- `size` (int, optional): フォントサイズ（ピクセル）
  - デフォルト: `32`
- `color` (str, optional): テキスト色（16進数カラーコード）
  - デフォルト: `"#000000"` (黒)
- `alpha` (int, optional): 透明度（0-255）
  - デフォルト: `255` (不透明)
- `bold` (bool, optional): 太字
  - デフォルト: `false`
- `align` (str, optional): テキスト揃え（`"left"`, `"center"`, `"right"`）
  - デフォルト: `"left"`
- `anchor_v` (str, optional): 垂直方向の原点位置（`"top"`, `"middle"`, `"bottom"`）
  - デフォルト: `"top"`
- `anchor_h` (str, optional): 水平方向の原点位置（`"left"`, `"center"`, `"right"`）
  - デフォルト: `"left"`
- `rotation` (float, optional): 回転角度（度数、時計回り）
  - デフォルト: `0.0`
- `glow` (GlowCfg, optional): グロー（発光）効果

**例:**
```json
{
  "font": {
    "size": 36,
    "color": "#FF0000",
    "alpha": 255,
    "bold": true,
    "align": "center",
    "anchor_h": "center",
    "anchor_v": "middle",
    "rotation": -30
  }
}
```

---

### GlowCfg

グロー（発光）効果の設定。

```python
class GlowCfg(TypedDict, total=False):
    color: str
    radius: int
    alpha: int
```

**フィールド:**
- `color` (str, optional): グローの色（16進数カラーコード）
  - デフォルト: `"#FFFFFF"` (白)
- `radius` (int, optional): ぼかしの半径（ピクセル）
  - デフォルト: `10`
- `alpha` (int, optional): グローの透明度（0-255）
  - デフォルト: `200`

**例:**
```json
{
  "glow": {
    "color": "#FF0000",
    "radius": 15,
    "alpha": 255
  }
}
```

---

## デフォルト値（Defaults）

デフォルト設定を定義するクラスです（`drawtool.defaults`モジュール）。

### TextDefaults

テキスト要素のデフォルト設定。

```python
class TextDefaults:
    FONT_SIZE: int = 32
    FONT_COLOR: str = "#000000"
    ALPHA: int = 255
    BOLD: bool = False
    TEXT_ALIGN: Literal["left", "center", "right"] = "left"
    ANCHOR_VERTICAL: Literal["top", "middle", "bottom"] = "top"
    ANCHOR_HORIZONTAL: Literal["left", "center", "right"] = "left"
    ROTATION: float = 0.0
    DEFAULT_FONT_FAMILY: str = "Times New Roman"
    
    # システムフォントのパス（プラットフォーム別）
    FONT_PATHS: List[Path] = [
        Path("C:/Windows/Fonts/times.ttf"),  # Windows
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"),  # Linux
        Path("/Library/Fonts/Times New Roman.ttf"),  # macOS
    ]
    
    BOLD_FONT_PATHS: List[Path] = [
        Path("C:/Windows/Fonts/timesbd.ttf"),  # Windows
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),  # Linux
        Path("/Library/Fonts/Times New Roman Bold.ttf"),  # macOS
    ]
```

**メソッド:**

```python
@classmethod
def get_defaults(cls) -> Dict[str, Any]:
    """全てのデフォルト設定を辞書として取得"""
```

---

### ImageDefaults

画像要素のデフォルト設定。

```python
class ImageDefaults:
    ALPHA: int = 255
    ROTATION: float = 0.0
    ANCHOR_VERTICAL: Literal["top", "middle", "bottom"] = "top"
    ANCHOR_HORIZONTAL: Literal["left", "center", "right"] = "left"
```

**メソッド:**

```python
@classmethod
def get_defaults(cls) -> Dict[str, Any]:
    """全てのデフォルト設定を辞書として取得"""
```

---

## 内部メソッド

以下は`FigureRenderer`の内部メソッドです。通常は直接呼び出す必要はありませんが、カスタマイズやデバッグに役立ちます。

### _load_config()

```python
def _load_config(self) -> Dict[str, Any]
```

JSON設定ファイルを読み込みます。

**戻り値:** 設定の辞書

**例外:** `FileNotFoundError`

---

### _validate_config()

```python
def _validate_config(self, cfg: Dict[str, Any]) -> None
```

設定ファイルの妥当性を検証します。

**例外:** `ValueError` - 設定が不正な場合

---

### _create_canvas()

```python
def _create_canvas(self, cfg: Dict[str, Any]) -> Image.Image
```

空のキャンバス（PILイメージ）を作成します。

**戻り値:** RGBA形式のPIL Image

---

### _draw_image()

```python
def _draw_image(self, canvas: Image.Image, el: Dict[str, Any], base_dir: Path) -> None
```

画像要素をキャンバスに描画します。

---

### _draw_text()

```python
def _draw_text(self, draw: ImageDraw.ImageDraw, el: Dict[str, Any]) -> None
```

テキスト要素をキャンバスに描画します。

---

## 使用例

### 基本的な使い方

```python
from drawtool.renderer import FigureRenderer

# レンダラーを初期化
renderer = FigureRenderer("config.json")

# 図を生成
output = renderer.render()
print(f"Generated: {output}")
```

### 出力パスを上書き

```python
from pathlib import Path
from drawtool.renderer import FigureRenderer

renderer = FigureRenderer("config.json")
output = renderer.render(output_path=Path("custom_output.png"))
```

### プログラムから設定を生成

```python
import json
from pathlib import Path
from drawtool.renderer import FigureRenderer

# 設定を辞書として作成
config = {
    "canvas": {
        "width": 800,
        "height": 600,
        "background": "#FFFFFF"
    },
    "elements": [
        {
            "type": "text",
            "text": "Hello, drawtool!",
            "x": 400,
            "y": 300,
            "font": {
                "size": 48,
                "anchor_h": "center",
                "anchor_v": "middle"
            }
        }
    ]
}

# 一時ファイルに保存
config_path = Path("temp_config.json")
with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

# レンダリング
renderer = FigureRenderer(config_path)
output = renderer.render()
print(f"Generated: {output}")
```

### エラーハンドリング

```python
from drawtool.renderer import FigureRenderer

try:
    renderer = FigureRenderer("config.json")
    output = renderer.render()
    print(f"Success: {output}")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid configuration: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## 座標系と単位

### 座標系

- 原点は左上 (0, 0)
- X軸は右方向に増加
- Y軸は下方向に増加

```
(0,0) -----> X
  |
  |
  v
  Y
```

### 単位

- **座標 (x, y)**: ピクセル
- **フォントサイズ**: ピクセル
- **回転角度**: 度数（時計回り、0-360）
- **透明度 (alpha)**: 0-255（0=完全透明、255=不透明）
- **スケール**: 倍率（1.0 = 100%）

---

## パス解決のルール

### アセットパス

```
画像の絶対パス = (JSON設定ファイルのディレクトリ) / (assets.base_dir) / (要素のpath)
```

### 出力パス

```
出力の絶対パス = (JSON設定ファイルのディレクトリ) / (output.path)
```

または`render(output_path=...)`で上書き可能

---

## 次のステップ

- [Getting Started](getting-started.md) - 初心者向けチュートリアル
- [Config Schema](../specs/config-schema.md) - JSON設定の完全な仕様
- [Examples](examples.md) - 実用的なサンプル集
