from pathlib import Path
from demo import parse_doc
from demo import parse_doc as _parse_doc

pdf_path = Path("demo/pdfs/demo1.pdf")
output_dir = Path("output_custom")
_parse_doc([pdf_path], output_dir, lang="en", backend="pipeline", method="auto")
print("Done — output in", output_dir)
