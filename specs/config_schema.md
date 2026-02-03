# Config Schema (v0.1)

## Required keys
- canvas.width (int > 0)
- canvas.height (int > 0)
- canvas.background (string, "#RRGGBB" or color name)
- elements (list)

## Element: image
- type: "image"
- path: string
- x,y: int
- scale: float (optional, default 1.0)

## Element: text
- type: "text"
- text: string
- x,y: int
- font.size/color optional
