# drawtool

PowerPointのように複数の画像やテキストを組み合わせて論文図を作成するPythonライブラリ。素材画像はファイルに埋め込まず、パス参照で合成します。

## 実装予定の機能
- **画像のトリミング機能**: 上下左右のトリミング長さを指定してその分だけトリミングする
- **四角形などのシンプルな図形を描画する**
- **プレビュー画像でエレメントの外形を表示するモードを追加**
- **選択範囲のみのレンダリング**

## 特徴

- **JSON設定ファイルで図を定義**: 再現可能で編集しやすい
- **外部アセット参照**: 画像ファイルを埋め込まず、パスで参照
- **レイヤーシステム**: 要素を階層的に管理
- **豊富なテキストスタイル**: フォント、色、回転、アンカー、グロー効果
- **画像変換**: スケール、回転、透明度、アンカーポイント

## インストール

```bash
# 開発モードでインストール
pip install -e .

# または通常のインストール
pip install .
```

## クイックスタート

### 基本的な使い方

```python
from drawtool.renderer import FigureRenderer

# JSON設定ファイルから図を生成
renderer = FigureRenderer("config.json")
output_path = renderer.render()
print(f"Generated: {output_path}")
```

### 最小限のJSON設定例

```json
{
  "canvas": {
    "width": 800,
    "height": 600,
    "background": "#FFFFFF"
  },
  "assets": {
    "base_dir": "./images"
  },
  "elements": [
    {
      "type": "image",
      "path": "photo.png",
      "x": 100,
      "y": 100,
      "scale": 1.0
    },
    {
      "type": "text",
      "text": "Hello, drawtool!",
      "x": 100,
      "y": 50,
      "font": {
        "size": 32,
        "color": "#000000"
      }
    }
  ]
}
```

## 主な機能

### 画像要素

```json
{
  "type": "image",
  "path": "sample.png",
  "x": 200,
  "y": 150,
  "scale": 0.8,
  "alpha": 200,
  "rotation": -15,
  "anchor_h": "center",
  "anchor_v": "middle"
}
```

- **scale**: 拡大縮小率（1.0 = 100%）
- **alpha**: 透明度（0-255、255 = 不透明）
- **rotation**: 回転角度（度数、時計回り）
- **anchor_h/v**: 原点位置（left/center/right, top/middle/bottom）

### テキスト要素

```json
{
  "type": "text",
  "text": "Sample Text",
  "x": 400,
  "y": 300,
  "font": {
    "size": 28,
    "color": "#FF0000",
    "alpha": 255,
    "bold": true,
    "align": "center",
    "anchor_h": "center",
    "anchor_v": "middle",
    "rotation": -30,
    "glow": {
      "color": "#FFFFFF",
      "radius": 10,
      "alpha": 200
    }
  }
}
```

- **align**: テキスト揃え（left/center/right）
- **anchor**: テキストの原点位置
- **rotation**: 回転角度
- **glow**: グロー（発光）効果

### レイヤーシステム

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

レイヤーは`order`の昇順で描画されます（小さいほど背面）。

## ドキュメント

- [Getting Started](docs/getting-started.md) - 詳細なチュートリアル
- [API Reference](docs/api-reference.md) - APIの完全なリファレンス
- [Config Schema](specs/config-schema.md) - JSON設定の仕様
- [Examples](docs/examples.md) - 実用的なサンプル集

## 例

`examples/`ディレクトリに完全な例があります：

```bash
cd examples
python make_example.py
# build/example.png が生成されます
```

## 要件

- Python >= 3.11
- Pillow >= 10.0.0

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## バージョン

現在のバージョン: **0.1.0**
