from pathlib import Path
from demo.demo import parse_doc

pdf = Path("sample.pdf")
out = Path("results") / pdf.stem
out.mkdir(parents=True, exist_ok=True)
parse_doc([pdf], str(out), lang="en", backend="pipeline", method="auto")
print("Done. Output saved to", out)
