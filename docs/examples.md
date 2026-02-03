# Examples

drawtoolの実用的な使用例集です。

## 目次

1. [基本的な図](#基本的な図)
2. [研究図の作成](#研究図の作成)
3. [複数の写真を配置](#複数の写真を配置)
4. [回転とアンカー](#回転とアンカー)
5. [透明度を使った重ね合わせ](#透明度を使った重ね合わせ)
6. [グロー効果でタイトル](#グロー効果でタイトル)
7. [レイヤーで複雑な図を管理](#レイヤーで複雑な図を管理)
8. [プログラムから設定を生成](#プログラムから設定を生成)

---

## 基本的な図

シンプルなテキストと背景色だけの図。

### config.json

```json
{
  "canvas": {
    "width": 800,
    "height": 600,
    "background": "#E8F4F8"
  },
  "output": {
    "path": "output/simple.png"
  },
  "elements": [
    {
      "type": "text",
      "text": "Hello, drawtool!",
      "x": 400,
      "y": 300,
      "font": {
        "size": 48,
        "color": "#2C3E50",
        "bold": true,
        "anchor_h": "center",
        "anchor_v": "middle"
      }
    }
  ]
}
```

### render.py

```python
from drawtool.renderer import FigureRenderer

renderer = FigureRenderer("config.json")
output = renderer.render()
print(f"Generated: {output}")
```

---

## 研究図の作成

論文用の比較図（Before/After）。

### config.json

```json
{
  "canvas": {
    "width": 1200,
    "height": 600,
    "background": "#FFFFFF"
  },
  "assets": {
    "base_dir": "./images"
  },
  "output": {
    "path": "output/comparison.png"
  },
  "elements": [
    {
      "type": "text",
      "text": "Experimental Results",
      "x": 600,
      "y": 30,
      "font": {
        "size": 36,
        "color": "#000000",
        "bold": true,
        "anchor_h": "center"
      }
    },
    {
      "type": "image",
      "path": "before.png",
      "x": 150,
      "y": 150,
      "scale": 0.8
    },
    {
      "type": "text",
      "text": "(a) Before",
      "x": 150,
      "y": 550,
      "font": {
        "size": 24,
        "color": "#333333"
      }
    },
    {
      "type": "image",
      "path": "after.png",
      "x": 750,
      "y": 150,
      "scale": 0.8
    },
    {
      "type": "text",
      "text": "(b) After",
      "x": 750,
      "y": 550,
      "font": {
        "size": 24,
        "color": "#333333"
      }
    }
  ]
}
```

**ポイント:**
- タイトルを中央揃えで配置
- 2つの画像を左右に配置
- 各画像にキャプションを追加

---

## 複数の写真を配置

グリッドレイアウトで複数の写真を整列。

### config.json

```json
{
  "canvas": {
    "width": 1000,
    "height": 800,
    "background": "#F5F5F5"
  },
  "assets": {
    "base_dir": "./photos"
  },
  "output": {
    "path": "output/grid.png"
  },
  "elements": [
    {"type": "image", "path": "photo1.jpg", "x": 50, "y": 50, "scale": 0.4},
    {"type": "image", "path": "photo2.jpg", "x": 550, "y": 50, "scale": 0.4},
    {"type": "image", "path": "photo3.jpg", "x": 50, "y": 450, "scale": 0.4},
    {"type": "image", "path": "photo4.jpg", "x": 550, "y": 450, "scale": 0.4},
    
    {"type": "text", "text": "Sample 1", "x": 50, "y": 20, "font": {"size": 20}},
    {"type": "text", "text": "Sample 2", "x": 550, "y": 20, "font": {"size": 20}},
    {"type": "text", "text": "Sample 3", "x": 50, "y": 420, "font": {"size": 20}},
    {"type": "text", "text": "Sample 4", "x": 550, "y": 420, "font": {"size": 20}}
  ]
}
```

### Pythonでグリッドを自動生成

```python
import json
from drawtool.renderer import FigureRenderer

# グリッド設定
cols = 2
rows = 2
cell_width = 500
cell_height = 400
margin = 50

# 設定を生成
config = {
    "canvas": {
        "width": cols * cell_width,
        "height": rows * cell_height,
        "background": "#F5F5F5"
    },
    "assets": {"base_dir": "./photos"},
    "output": {"path": "output/grid.png"},
    "elements": []
}

# 画像とラベルを追加
for row in range(rows):
    for col in range(cols):
        idx = row * cols + col + 1
        x = col * cell_width + margin
        y = row * cell_height + margin
        
        # 画像
        config["elements"].append({
            "type": "image",
            "path": f"photo{idx}.jpg",
            "x": x,
            "y": y + 30,
            "scale": 0.4
        })
        
        # ラベル
        config["elements"].append({
            "type": "text",
            "text": f"Sample {idx}",
            "x": x,
            "y": y,
            "font": {"size": 20}
        })

# JSONに保存
with open("grid_config.json", "w") as f:
    json.dump(config, f, indent=2)

# レンダリング
renderer = FigureRenderer("grid_config.json")
output = renderer.render()
print(f"Generated: {output}")
```

---

## 回転とアンカー

画像とテキストを回転させて配置。

### config.json

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
      "path": "arrow.png",
      "x": 400,
      "y": 300,
      "scale": 1.0,
      "rotation": 45,
      "anchor_h": "center",
      "anchor_v": "middle"
    },
    {
      "type": "text",
      "text": "Rotated Text",
      "x": 400,
      "y": 500,
      "font": {
        "size": 32,
        "color": "#FF0000",
        "rotation": -30,
        "anchor_h": "center",
        "anchor_v": "middle"
      }
    }
  ]
}
```

**ポイント:**
- `anchor_h: "center"`と`anchor_v: "middle"`で中心を原点に
- `rotation`で回転（時計回り、度数）
- 回転は原点中心に行われる

---

## 透明度を使った重ね合わせ

半透明のウォーターマークを追加。

### config.json

```json
{
  "canvas": {
    "width": 1000,
    "height": 800,
    "background": "#FFFFFF"
  },
  "assets": {
    "base_dir": "./images"
  },
  "layers": [
    {
      "id": "main",
      "order": 0,
      "elements": [
        {
          "type": "image",
          "path": "main_photo.jpg",
          "x": 0,
          "y": 0,
          "scale": 1.0
        }
      ]
    },
    {
      "id": "watermark",
      "order": 10,
      "elements": [
        {
          "type": "image",
          "path": "logo.png",
          "x": 500,
          "y": 400,
          "scale": 0.5,
          "alpha": 100,
          "anchor_h": "center",
          "anchor_v": "middle"
        },
        {
          "type": "text",
          "text": "© 2026 My Lab",
          "x": 950,
          "y": 750,
          "font": {
            "size": 18,
            "color": "#888888",
            "alpha": 150,
            "anchor_h": "right",
            "anchor_v": "bottom"
          }
        }
      ]
    }
  ]
}
```

**ポイント:**
- `alpha`で透明度を調整（0-255）
- レイヤーで前景/背景を明確に分離
- ウォーターマークは控えめに（alpha=100）

---

## グロー効果でタイトル

目立つタイトルをグロー効果で作成。

### config.json

```json
{
  "canvas": {
    "width": 1200,
    "height": 200,
    "background": "#1A1A2E"
  },
  "elements": [
    {
      "type": "text",
      "text": "RESEARCH TITLE",
      "x": 600,
      "y": 100,
      "font": {
        "size": 64,
        "color": "#FFFFFF",
        "bold": true,
        "anchor_h": "center",
        "anchor_v": "middle",
        "glow": {
          "color": "#00D9FF",
          "radius": 20,
          "alpha": 255
        }
      }
    }
  ]
}
```

**ポイント:**
- 暗い背景でグロー効果が映える
- `glow.radius`でぼかしの強さを調整
- `glow.color`でグローの色を指定

---

## レイヤーで複雑な図を管理

多数の要素をレイヤーで整理。

### config.json

```json
{
  "canvas": {
    "width": 1400,
    "height": 1000,
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
          "path": "background.png",
          "x": 0,
          "y": 0,
          "scale": 1.0
        }
      ]
    },
    {
      "id": "diagrams",
      "order": 10,
      "elements": [
        {"type": "image", "path": "diagram1.png", "x": 100, "y": 200, "scale": 0.8},
        {"type": "image", "path": "diagram2.png", "x": 700, "y": 200, "scale": 0.8},
        {"type": "image", "path": "diagram3.png", "x": 100, "y": 600, "scale": 0.8},
        {"type": "image", "path": "diagram4.png", "x": 700, "y": 600, "scale": 0.8}
      ]
    },
    {
      "id": "labels",
      "order": 20,
      "elements": [
        {"type": "text", "text": "(a)", "x": 100, "y": 170, "font": {"size": 24, "bold": true}},
        {"type": "text", "text": "(b)", "x": 700, "y": 170, "font": {"size": 24, "bold": true}},
        {"type": "text", "text": "(c)", "x": 100, "y": 570, "font": {"size": 24, "bold": true}},
        {"type": "text", "text": "(d)", "x": 700, "y": 570, "font": {"size": 24, "bold": true}}
      ]
    },
    {
      "id": "annotations",
      "order": 30,
      "elements": [
        {
          "type": "image",
          "path": "arrow.png",
          "x": 550,
          "y": 350,
          "scale": 0.5,
          "rotation": 0,
          "anchor_h": "center",
          "anchor_v": "middle"
        },
        {
          "type": "text",
          "text": "Process",
          "x": 550,
          "y": 400,
          "font": {
            "size": 20,
            "color": "#FF0000",
            "anchor_h": "center"
          }
        }
      ]
    },
    {
      "id": "title",
      "order": 40,
      "elements": [
        {
          "type": "text",
          "text": "Figure 1: System Architecture",
          "x": 700,
          "y": 50,
          "font": {
            "size": 36,
            "color": "#000000",
            "bold": true,
            "anchor_h": "center"
          }
        }
      ]
    }
  ]
}
```

**ポイント:**
- レイヤーで役割ごとに要素を分類
- `order`で描画順序を明確に管理
- 修正時は該当レイヤーだけ編集すればOK

---

## プログラムから設定を生成

Pythonコードで動的に設定を生成。

### generate_timeline.py

```python
import json
from pathlib import Path
from drawtool.renderer import FigureRenderer

def create_timeline(events):
    """タイムラインの図を生成"""
    width = 1200
    height = 200 + len(events) * 100
    
    config = {
        "canvas": {
            "width": width,
            "height": height,
            "background": "#F9F9F9"
        },
        "elements": [
            {
                "type": "text",
                "text": "Project Timeline",
                "x": width // 2,
                "y": 50,
                "font": {
                    "size": 40,
                    "bold": True,
                    "anchor_h": "center"
                }
            }
        ]
    }
    
    # タイムラインを描画
    y_start = 150
    x_line = 200
    
    for i, event in enumerate(events):
        y = y_start + i * 100
        
        # 線
        config["elements"].append({
            "type": "text",
            "text": "│",
            "x": x_line,
            "y": y - 20,
            "font": {"size": 40, "color": "#3498DB"}
        })
        
        # 点
        config["elements"].append({
            "type": "text",
            "text": "●",
            "x": x_line,
            "y": y,
            "font": {"size": 30, "color": "#E74C3C", "anchor_h": "center"}
        })
        
        # イベント名
        config["elements"].append({
            "type": "text",
            "text": event["name"],
            "x": x_line + 50,
            "y": y - 10,
            "font": {"size": 24, "bold": True}
        })
        
        # 日付
        config["elements"].append({
            "type": "text",
            "text": event["date"],
            "x": x_line + 50,
            "y": y + 20,
            "font": {"size": 18, "color": "#7F8C8D"}
        })
    
    return config

# イベントデータ
events = [
    {"name": "Project Start", "date": "2026-01-01"},
    {"name": "Phase 1 Complete", "date": "2026-03-15"},
    {"name": "Review Meeting", "date": "2026-04-01"},
    {"name": "Phase 2 Complete", "date": "2026-06-30"},
    {"name": "Final Presentation", "date": "2026-08-01"},
]

# 設定を生成
config = create_timeline(events)

# JSONに保存
config_path = Path("timeline_config.json")
with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# レンダリング
renderer = FigureRenderer(config_path)
output = renderer.render("timeline.png")
print(f"Timeline generated: {output}")
```

**ポイント:**
- Pythonで設定を動的に生成
- データ駆動で図を作成
- 繰り返し処理で要素を追加

---

## データ駆動の実験結果図

CSVからデータを読み込んで図を生成。

### generate_results.py

```python
import json
import csv
from pathlib import Path
from drawtool.renderer import FigureRenderer

def load_results(csv_path):
    """CSVから実験結果を読み込み"""
    results = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            results.append({
                "method": row["method"],
                "image": row["image"],
                "accuracy": float(row["accuracy"])
            })
    return results

def create_results_figure(results):
    """実験結果の図を生成"""
    cols = len(results)
    cell_width = 300
    cell_height = 400
    margin = 50
    
    width = cols * cell_width + margin * 2
    height = cell_height + margin * 2 + 100
    
    config = {
        "canvas": {
            "width": width,
            "height": height,
            "background": "#FFFFFF"
        },
        "assets": {"base_dir": "./results"},
        "elements": [
            {
                "type": "text",
                "text": "Experimental Results",
                "x": width // 2,
                "y": 30,
                "font": {
                    "size": 36,
                    "bold": True,
                    "anchor_h": "center"
                }
            }
        ]
    }
    
    for i, result in enumerate(results):
        x = margin + i * cell_width
        y = 100
        
        # 結果画像
        config["elements"].append({
            "type": "image",
            "path": result["image"],
            "x": x,
            "y": y,
            "scale": 0.8
        })
        
        # 手法名
        config["elements"].append({
            "type": "text",
            "text": result["method"],
            "x": x + cell_width // 2,
            "y": y + 330,
            "font": {
                "size": 20,
                "bold": True,
                "anchor_h": "center"
            }
        })
        
        # 精度
        accuracy_text = f"Acc: {result['accuracy']:.1%}"
        color = "#27AE60" if result["accuracy"] >= 0.9 else "#E67E22"
        config["elements"].append({
            "type": "text",
            "text": accuracy_text,
            "x": x + cell_width // 2,
            "y": y + 360,
            "font": {
                "size": 18,
                "color": color,
                "anchor_h": "center"
            }
        })
    
    return config

# CSVから読み込み
results = load_results("results.csv")

# 設定を生成
config = create_results_figure(results)

# レンダリング
config_path = Path("results_config.json")
with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

renderer = FigureRenderer(config_path)
output = renderer.render("results.png")
print(f"Results figure generated: {output}")
```

### results.csv

```csv
method,image,accuracy
Baseline,baseline.png,0.75
Method A,method_a.png,0.88
Method B,method_b.png,0.92
Proposed,proposed.png,0.95
```

**ポイント:**
- CSVからデータを読み込み
- 精度に応じて色を変更（条件分岐）
- 完全にデータ駆動で図を生成

---

## まとめ

これらの例は以下のように組み合わせて使えます：

1. **シンプルな図**: 基本的な要素配置
2. **研究図**: Before/After比較
3. **グリッド**: 複数画像の整列
4. **回転**: ダイナミックな配置
5. **透明度**: 重ね合わせ効果
6. **グロー**: 目立つタイトル
7. **レイヤー**: 複雑な図の管理
8. **プログラム生成**: 動的な図の作成

詳細は以下のドキュメントを参照してください：

- [Getting Started](getting-started.md)
- [API Reference](api-reference.md)
- [Config Schema](../specs/config-schema.md)
