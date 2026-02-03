# Getting Started with drawtool

このガイドでは、drawtoolの基本的な使い方を学びます。

## 目次

1. [インストール](#インストール)
2. [最初の図を作成](#最初の図を作成)
3. [画像を追加](#画像を追加)
4. [テキストをカスタマイズ](#テキストをカスタマイズ)
5. [レイヤーを使う](#レイヤーを使う)
6. [高度な機能](#高度な機能)

## インストール

### 前提条件

- Python 3.11以上
- pip

### インストール手順

```bash
# リポジトリをクローン
git clone <repository-url>
cd drawtool

# 開発モードでインストール
pip install -e .
```

インストールが成功したか確認：

```bash
python -c "from drawtool.renderer import FigureRenderer; print('OK')"
```

## 最初の図を作成

### ステップ1: JSON設定ファイルを作成

`my_first_figure.json`を作成：

```json
{
  "canvas": {
    "width": 800,
    "height": 600,
    "background": "#F0F0F0"
  },
  "output": {
    "path": "output/my_figure.png"
  },
  "elements": [
    {
      "type": "text",
      "text": "My First Figure",
      "x": 400,
      "y": 300,
      "font": {
        "size": 48,
        "color": "#333333",
        "anchor_h": "center",
        "anchor_v": "middle"
      }
    }
  ]
}
```

### ステップ2: Pythonスクリプトで実行

`render_figure.py`を作成：

```python
from drawtool.renderer import FigureRenderer

renderer = FigureRenderer("my_first_figure.json")
output = renderer.render()
print(f"図を生成しました: {output}")
```

実行：

```bash
python render_figure.py
```

`output/my_figure.png`が生成されます！

## 画像を追加

### ステップ1: アセットディレクトリを設定

プロジェクト構造：

```
my_project/
├── assets/
│   ├── photo1.png
│   └── photo2.jpg
├── config.json
└── render.py
```

### ステップ2: JSON設定に画像を追加

```json
{
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#FFFFFF"
  },
  "assets": {
    "base_dir": "./assets"
  },
  "output": {
    "path": "output/figure_with_images.png"
  },
  "elements": [
    {
      "type": "image",
      "id": "photo1",
      "path": "photo1.png",
      "x": 100,
      "y": 100,
      "scale": 1.0
    },
    {
      "type": "image",
      "id": "photo2",
      "path": "photo2.jpg",
      "x": 600,
      "y": 100,
      "scale": 0.8
    },
    {
      "type": "text",
      "text": "Photo 1",
      "x": 100,
      "y": 50,
      "font": {
        "size": 24,
        "color": "#000000"
      }
    },
    {
      "type": "text",
      "text": "Photo 2",
      "x": 600,
      "y": 50,
      "font": {
        "size": 24,
        "color": "#000000"
      }
    }
  ]
}
```

### 画像のスケーリング

```json
{
  "type": "image",
  "path": "large_image.png",
  "x": 100,
  "y": 100,
  "scale": 0.5  // 50%に縮小
}
```

## テキストをカスタマイズ

### フォントサイズと色

```json
{
  "type": "text",
  "text": "カラフルなテキスト",
  "x": 200,
  "y": 100,
  "font": {
    "size": 36,
    "color": "#FF6600",
    "bold": true
  }
}
```

### テキストの配置

```json
{
  "type": "text",
  "text": "中央揃え",
  "x": 400,
  "y": 200,
  "font": {
    "size": 32,
    "align": "center",      // left, center, right
    "anchor_h": "center",   // left, center, right
    "anchor_v": "middle"    // top, middle, bottom
  }
}
```

- **align**: 複数行テキストの揃え方
- **anchor_h/v**: テキストボックスの原点位置

### 複数行テキスト

```json
{
  "type": "text",
  "text": "1行目\n2行目\n3行目",
  "x": 100,
  "y": 100,
  "font": {
    "size": 24,
    "align": "center"  // 各行を中央揃え
  }
}
```

### テキストの回転

```json
{
  "type": "text",
  "text": "回転したテキスト",
  "x": 400,
  "y": 300,
  "font": {
    "size": 28,
    "rotation": -45  // 度数（反時計回り45度）
  }
}
```

### 透明度

```json
{
  "type": "text",
  "text": "半透明テキスト",
  "x": 200,
  "y": 200,
  "font": {
    "size": 32,
    "color": "#FF0000",
    "alpha": 128  // 0-255（255=不透明、0=完全透明）
  }
}
```

### グロー効果

```json
{
  "type": "text",
  "text": "光るテキスト",
  "x": 400,
  "y": 300,
  "font": {
    "size": 40,
    "color": "#FFFFFF",
    "bold": true,
    "glow": {
      "color": "#FF0000",
      "radius": 15,
      "alpha": 255
    }
  }
}
```

## レイヤーを使う

レイヤーシステムを使うと、要素をグループ化して管理できます。

### 基本的なレイヤー構造

```json
{
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#FFFFFF"
  },
  "assets": {
    "base_dir": "./assets"
  },
  "layers": [
    {
      "id": "background",
      "order": 0,
      "elements": [
        {
          "type": "image",
          "path": "bg.png",
          "x": 0,
          "y": 0,
          "scale": 1.0
        }
      ]
    },
    {
      "id": "photos",
      "order": 10,
      "elements": [
        {
          "type": "image",
          "path": "photo1.png",
          "x": 100,
          "y": 100,
          "scale": 0.8
        },
        {
          "type": "image",
          "path": "photo2.png",
          "x": 600,
          "y": 100,
          "scale": 0.8
        }
      ]
    },
    {
      "id": "labels",
      "order": 20,
      "elements": [
        {
          "type": "text",
          "text": "Label 1",
          "x": 100,
          "y": 50,
          "font": {"size": 24}
        },
        {
          "type": "text",
          "text": "Label 2",
          "x": 600,
          "y": 50,
          "font": {"size": 24}
        }
      ]
    }
  ]
}
```

### レイヤーの順序

- `order`の小さい値から順に描画（0 → 10 → 20）
- 同じ`order`内では、`elements`配列の順番で描画
- 各要素に`z`を指定すると、レイヤー内での順序を制御可能

```json
{
  "id": "layer1",
  "order": 10,
  "elements": [
    {"type": "image", "z": 0, ...},  // 最背面
    {"type": "image", "z": 1, ...},  // 中間
    {"type": "text", "z": 2, ...}    // 最前面
  ]
}
```

## 高度な機能

### 画像の回転と原点

```json
{
  "type": "image",
  "path": "arrow.png",
  "x": 400,
  "y": 300,
  "scale": 1.0,
  "rotation": -45,        // 反時計回り45度
  "anchor_h": "center",   // 回転の中心を画像中央に
  "anchor_v": "middle"
}
```

### 画像の透明度

```json
{
  "type": "image",
  "path": "watermark.png",
  "x": 100,
  "y": 100,
  "scale": 1.0,
  "alpha": 100  // 半透明なウォーターマーク
}
```

### プログラムから出力パスを指定

```python
from drawtool.renderer import FigureRenderer

renderer = FigureRenderer("config.json")

# JSON設定のoutput.pathを上書き
output = renderer.render(output_path="custom_output.png")
print(f"Generated: {output}")
```

### 相対パスの解決

- `assets.base_dir`: JSON設定ファイルからの相対パス
- `output.path`: JSON設定ファイルからの相対パス
- 画像の`path`: `base_dir`からの相対パス

例：

```
project/
├── config/
│   └── figure.json      # assets.base_dir: "../images"
├── images/
│   └── photo.png        # path: "photo.png"
└── output/
    └── result.png       # output.path: "../output/result.png"
```

## 次のステップ

- [API Reference](api-reference.md) - 全APIの詳細
- [Config Schema](../specs/config-schema.md) - JSON設定の完全な仕様
- [Examples](examples.md) - 実用的なサンプル集

## トラブルシューティング

### エラー: "Image not found"

画像のパスが正しいか確認：

```json
{
  "assets": {
    "base_dir": "./assets"  // JSON設定ファイルからの相対パス
  },
  "elements": [
    {
      "type": "image",
      "path": "photo.png"  // base_dirからの相対パス
    }
  ]
}
```

実際のファイル構造：
```
project/
├── config.json
└── assets/
    └── photo.png
```

### エラー: "Missing required key"

必須フィールドが不足しています：

- `canvas.width`
- `canvas.height`
- `canvas.background`
- `elements` または `layers`

### フォントが見つからない

デフォルトではシステムフォントを使用します。カスタムフォントを使いたい場合は、`src/drawtool/defaults.py`の`FONT_PATHS`を編集してください。
