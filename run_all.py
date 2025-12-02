"""
Обрабатывает все PDF в demo/pdfs_testset/
Сохраняет результаты и краткую сводку в results/
"""
import os
import time
import json
import csv
from pathlib import Path

# импортируем основной парсер из demo
try:
    from demo.demo import parse_doc
except Exception as e:
    raise RuntimeError(
        "Cannot import parse_doc from demo.demo. "
        "Run this script from the repo root and ensure mineru installed in editable mode "
        "(python -m pip install -e '.[core]')"
    ) from e

# psutil используется для замера RSS-памяти процесса
try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    PSUTIL_AVAILABLE = False

ROOT = Path.cwd()
INPUT_DIR = ROOT / "demo" / "pdfs_testset"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(exist_ok=True)

PDFS = sorted(INPUT_DIR.glob("*.pdf"))
if not PDFS:
    print("No pdfs found in", INPUT_DIR)
    raise SystemExit(1)

summary = []

for pdf_path in PDFS:
    name = pdf_path.stem
    out_dir = RESULTS_DIR / name
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== Processing {name} ===")

    # измерения памяти до запуска
    proc = psutil.Process(os.getpid()) if PSUTIL_AVAILABLE else None
    before_rss = proc.memory_info().rss if proc else None

    t0 = time.perf_counter()
    try:
        parse_doc([pdf_path], str(out_dir), lang="en", backend="pipeline", method="auto")
        success = True
        error = None
    except Exception as e:
        success = False
        error = str(e)
        print("Error during parse_doc:", error)
    t1 = time.perf_counter()

    after_rss = proc.memory_info().rss if proc else None

    # найти сгенерированные пути (если они есть)
    md_path = None
    middle_json_path = None

    cand = list(out_dir.rglob("*_middle.json"))
    if cand:
        middle_json_path = cand[0]

    md_cands = list(out_dir.rglob("*.md"))
    if md_cands:
        md_path = md_cands[0]

    entry = {
        "stem": name,
        "success": success,
        "error": error,
        "time_s": t1 - t0,
        "rss_before_bytes": before_rss,
        "rss_after_bytes": after_rss,
        "md_path": str(md_path) if md_path else None,
        "middle_json_path": str(middle_json_path) if middle_json_path else None,
    }
    summary.append(entry)

    with open(out_dir / "run_meta.json", "w", encoding="utf-8") as f:
        json.dump(entry, f, ensure_ascii=False, indent=2)

with open(RESULTS_DIR / "summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

csv_path = RESULTS_DIR / "summary.csv"
keys = ["stem", "success", "error", "time_s", "rss_before_bytes", "rss_after_bytes", "md_path", "middle_json_path"]
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=keys)
    writer.writeheader()
    for s in summary:
        writer.writerow({k: s.get(k) for k in keys})

print("\nAll done. Summary saved to", RESULTS_DIR)
