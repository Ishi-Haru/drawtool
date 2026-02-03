# Config Schema (v0.1)

drawtoolのJSON設定ファイルの完全な仕様です。

## 目次

1. [最上位構造](#最上位構造)
2. [canvas（必須）](#canvas必須)
3. [output（オプション）](#outputオプション)
4. [assets（オプション）](#assetsオプション)
5. [elements（レガシー）](#elementsレガシー)
6. [layers（推奨）](#layers推奨)
7. [画像要素](#画像要素)
8. [テキスト要素](#テキスト要素)
9. [フォント設定](#フォント設定)
10. [グロー効果](#グロー効果)

---

## 最上位構造

```json
{
  "version": "0.1",
  "output": {...},
  "canvas": {...},
  "assets": {...},
  "elements": [...],  // または
  "layers": [...]     // layers使用を推奨
}
```

### フィールド

| フィールド | 型 | 必須 | 説明 |
|----------|-----|-----|-----|
| `version` | string | ❌ | 設定ファイルのバージョン（例: "0.1"） |
| `output` | object | ❌ | 出力ファイルの設定 |
| `canvas` | object | ✅ | キャンバス（画像）の設定 |
| `assets` | object | ❌ | アセットディレクトリの設定 |
| `elements` | array | ✅* | 要素のリスト（レガシーモード） |
| `layers` | array | ✅* | レイヤーのリスト（推奨） |

**注意:** `elements`または`layers`のいずれか一方が必須です。両方指定した場合は`layers`が優先されます。

---

## canvas（必須）

キャンバス（出力画像）のサイズと背景色を定義します。

```json
{
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#FFFFFF"
  }
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `width` | integer | ✅ | - | 画像の幅（ピクセル、> 0） |
| `height` | integer | ✅ | - | 画像の高さ（ピクセル、> 0） |
| `background` | string | ✅ | - | 背景色（16進数カラーコード） |

**background の形式:**
- 6桁: `"#RRGGBB"` (例: `"#FFFFFF"`)
- 3桁: `"#RGB"` (例: `"#FFF"`)

---

## output（オプション）

出力ファイルのパスを指定します。

```json
{
  "output": {
    "path": "build/figure.png"
  }
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `path` | string | ❌ | `"build/figure.png"` | 出力ファイルのパス（JSON設定ファイルからの相対パス） |

**パス解決:**
```
絶対パス = (JSON設定ファイルのディレクトリ) / (output.path)
```

`render(output_path=...)`メソッドで上書き可能です。

---

## assets（オプション）

画像アセットのベースディレクトリを指定します。

```json
{
  "assets": {
    "base_dir": "./images"
  }
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `base_dir` | string | ❌ | `""` | アセットのベースディレクトリ（JSON設定ファイルからの相対パス） |

**パス解決:**
```
画像の絶対パス = (JSON設定ファイルのディレクトリ) / (assets.base_dir) / (要素のpath)
```

---

## elements（レガシー）

要素を直接配列で指定する方法です（レガシーモード）。

```json
{
  "elements": [
    {"type": "image", "path": "img1.png", "x": 100, "y": 100},
    {"type": "text", "text": "Hello", "x": 200, "y": 50}
  ]
}
```

要素は配列の順番で描画されます。`z`フィールドで順序を制御可能です。

**推奨:** 複雑な図では`layers`の使用を推奨します。

---

## layers（推奨）

要素をレイヤーごとにグループ化します。

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

### レイヤーのフィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `id` | string | ❌ | - | レイヤーの識別子 |
| `order` | integer | ❌ | `index * 10` | レイヤーの描画順序（小さい値が背面） |
| `elements` | array | ✅ | - | レイヤー内の要素のリスト |

**描画順序:**
1. `order`の昇順でレイヤーを描画
2. 同じ`order`内では、配列の順番で描画
3. 各要素に`z`を指定すると、レイヤー内での順序を制御可能

---

## 画像要素

画像ファイルをキャンバスに配置します。

```json
{
  "type": "image",
  "id": "photo1",
  "path": "sample.png",
  "x": 300,
  "y": 200,
  "z": 0,
  "scale": 0.8,
  "alpha": 200,
  "rotation": -15,
  "anchor_h": "center",
  "anchor_v": "middle"
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `type` | string | ✅ | - | `"image"` |
| `id` | string | ❌ | - | 要素の識別子（デバッグ用） |
| `path` | string | ✅ | - | 画像ファイルのパス（`assets.base_dir`からの相対パス） |
| `x` | integer | ✅ | - | X座標（ピクセル） |
| `y` | integer | ✅ | - | Y座標（ピクセル） |
| `z` | integer | ❌ | `0` | レイヤー内での描画順序（大きい値が前面） |
| `scale` | float | ❌ | `1.0` | 拡大縮小率（1.0 = 100%、> 0） |
| `alpha` | integer | ❌ | `255` | 透明度（0-255、255 = 不透明） |
| `rotation` | float | ❌ | `0.0` | 回転角度（度数、時計回り） |
| `anchor_v` | string | ❌ | `"top"` | 垂直方向の原点位置（`"top"`, `"middle"`, `"bottom"`) |
| `anchor_h` | string | ❌ | `"left"` | 水平方向の原点位置（`"left"`, `"center"`, `"right"`) |

### 画像の配置

`(x, y)`は画像の原点位置を表します。原点は`anchor_h`と`anchor_v`で指定します。

```
anchor_h: "left"     anchor_h: "center"   anchor_h: "right"
anchor_v: "top"      anchor_v: "middle"   anchor_v: "bottom"

(x,y)               
  ┌─────┐              ┌─────┐                ┌─────┐
  │     │              │ (x,y)                │     │(x,y)
  │     │              │     │                │     │
  └─────┘              └─────┘                └─────┘
```

### スケールと回転

1. まずスケールを適用
2. 次に回転を適用（原点中心）
3. 最後に`(x, y)`に配置

---

## テキスト要素

テキストをキャンバスに描画します。

```json
{
  "type": "text",
  "id": "title",
  "text": "Hello\nWorld",
  "x": 400,
  "y": 300,
  "z": 1,
  "font": {...}
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `type` | string | ✅ | - | `"text"` |
| `id` | string | ❌ | - | 要素の識別子（デバッグ用） |
| `text` | string | ✅ | - | 表示するテキスト（`\n`で改行） |
| `x` | integer | ✅ | - | X座標（ピクセル） |
| `y` | integer | ✅ | - | Y座標（ピクセル） |
| `z` | integer | ❌ | `0` | レイヤー内での描画順序（大きい値が前面） |
| `font` | object | ❌ | デフォルト設定 | フォント設定（後述） |

### 改行

テキスト内で`\n`を使用すると改行されます。

```json
{
  "text": "1行目\n2行目\n3行目"
}
```

---

## フォント設定

テキストのスタイルを定義します。

```json
{
  "font": {
    "family": "Times New Roman",
    "size": 36,
    "color": "#FF0000",
    "alpha": 255,
    "bold": true,
    "align": "center",
    "anchor_v": "middle",
    "anchor_h": "center",
    "rotation": -30,
    "glow": {...}
  }
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `family` | string | ❌ | `"Times New Roman"` | フォントファミリー名 |
| `size` | integer | ❌ | `32` | フォントサイズ（ピクセル） |
| `color` | string | ❌ | `"#000000"` | テキスト色（16進数カラーコード） |
| `alpha` | integer | ❌ | `255` | 透明度（0-255、255 = 不透明） |
| `bold` | boolean | ❌ | `false` | 太字 |
| `align` | string | ❌ | `"left"` | テキスト揃え（`"left"`, `"center"`, `"right"`） |
| `anchor_v` | string | ❌ | `"top"` | 垂直方向の原点位置（`"top"`, `"middle"`, `"bottom"`） |
| `anchor_h` | string | ❌ | `"left"` | 水平方向の原点位置（`"left"`, `"center"`, `"right"`） |
| `rotation` | float | ❌ | `0.0` | 回転角度（度数、時計回り） |
| `glow` | object | ❌ | なし | グロー（発光）効果（後述） |

### align vs anchor

- **align**: 複数行テキストの各行の揃え方
- **anchor**: テキストボックス全体の原点位置

```json
// 中央揃え + 中央配置
{
  "text": "1行目\n2行目",
  "x": 600,
  "y": 400,
  "font": {
    "align": "center",      // 各行を中央揃え
    "anchor_h": "center",   // (600, 400)を中心に配置
    "anchor_v": "middle"
  }
}
```

### テキストの配置

`(x, y)`はテキストボックスの原点位置を表します。

```
anchor_h: "left"     anchor_h: "center"   anchor_h: "right"
anchor_v: "top"      anchor_v: "middle"   anchor_v: "bottom"

(x,y)Text                 Text                    Text(x,y)
                         (x,y)
```

---

## グロー効果

テキストに発光（グロー）効果を追加します。

```json
{
  "glow": {
    "color": "#FF0000",
    "radius": 15,
    "alpha": 255
  }
}
```

### フィールド

| フィールド | 型 | 必須 | デフォルト | 説明 |
|----------|-----|-----|-----------|-----|
| `color` | string | ❌ | `"#FFFFFF"` | グローの色（16進数カラーコード） |
| `radius` | integer | ❌ | `10` | ぼかしの半径（ピクセル） |
| `alpha` | integer | ❌ | `200` | グローの透明度（0-255） |

**注意:** グロー効果は処理が重いため、多用すると描画が遅くなります。

---

## 完全な例

```json
{
  "version": "0.1",
  "output": {
    "path": "output/figure.png"
  },
  "canvas": {
    "width": 1200,
    "height": 800,
    "background": "#F5F5F5"
  },
  "assets": {
    "base_dir": "./images"
  },
  "layers": [
    {
      "id": "background",
      "order": 0,
      "elements": [
        {
          "type": "image",
          "id": "bg",
          "path": "background.png",
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
          "id": "photo1",
          "path": "photo1.jpg",
          "x": 100,
          "y": 100,
          "scale": 0.8,
          "z": 0
        },
        {
          "type": "image",
          "id": "photo2",
          "path": "photo2.jpg",
          "x": 600,
          "y": 100,
          "scale": 0.8,
          "z": 0,
          "alpha": 200,
          "rotation": 15,
          "anchor_h": "center",
          "anchor_v": "middle"
        }
      ]
    },
    {
      "id": "labels",
      "order": 20,
      "elements": [
        {
          "type": "text",
          "id": "title",
          "text": "My Research Figure",
          "x": 600,
          "y": 50,
          "z": 0,
          "font": {
            "size": 48,
            "color": "#333333",
            "bold": true,
            "anchor_h": "center",
            "glow": {
              "color": "#FFFFFF",
              "radius": 10,
              "alpha": 200
            }
          }
        },
        {
          "type": "text",
          "id": "label1",
          "text": "Before",
          "x": 100,
          "y": 80,
          "z": 1,
          "font": {
            "size": 24,
            "color": "#FF0000"
          }
        },
        {
          "type": "text",
          "id": "label2",
          "text": "After",
          "x": 600,
          "y": 80,
          "z": 1,
          "font": {
            "size": 24,
            "color": "#00AA00"
          }
        }
      ]
    }
  ]
}
```

---

## バリデーション

設定ファイルは以下の条件を満たす必要があります：

### 必須チェック
- ✅ `canvas`が存在する
- ✅ `canvas.width`が正の整数
- ✅ `canvas.height`が正の整数
- ✅ `canvas.background`が文字列
- ✅ `elements`または`layers`のいずれかが存在する

### 要素チェック
- ✅ `type`が`"image"`または`"text"`
- ✅ `x`と`y`が存在する
- ✅ 画像要素には`path`が必要
- ✅ テキスト要素には`text`が必要
- ✅ `scale`は正の数値（> 0）

---

## 次のステップ

- [Getting Started](../docs/getting-started.md) - チュートリアル
- [API Reference](../docs/api-reference.md) - API詳細
- [Examples](../docs/examples.md) - サンプル集
