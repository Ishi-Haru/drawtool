from pathlib import Path
from drawtool import FigureRenderer

out = FigureRenderer(Path(__file__).parent / "example_config.json").render()
print("Wrote:", out)
