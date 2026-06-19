from __future__ import annotations

import io
from pathlib import Path
from textwrap import wrap

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
PDF_ROOT = ROOT / "manuals" / "pdf"

NAVY = colors.HexColor("#10203A")
NAVY_2 = colors.HexColor("#152B4C")
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#647086")
BLUE = colors.HexColor("#2C74B8")
GOLD = colors.HexColor("#C89B3C")
PAPER = colors.HexColor("#F7F9FC")
LINE = colors.HexColor("#D8DEE8")


MANUALS = {
    "lotq-0001-exponents-logarithms-compounding-for-quant-research-manual.pdf": {
        "id": "LOTQ-0001",
        "title": "Exponents, Logarithms, and Compounding",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Growth, decay, returns, logs, and compounding for quant research systems.",
    },
    "lotq-0002-quant-arithmetic-ratios-log-returns-manual.pdf": {
        "id": "LOTQ-0002",
        "title": "Arithmetic, Ratios, and Log Returns",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Convert prices into ratios, returns, cumulative paths, and research-ready series.",
    },
    "lotq-0003-quant-calculus-foundations-market-models-manual.pdf": {
        "id": "LOTQ-0003",
        "title": "Calculus Foundations for Market Models",
        "category": "Calculus",
        "difficulty": "Beginner",
        "subtitle": "Derivatives, integrals, optimization, sensitivity, and continuous-growth intuition.",
    },
    "lotq-0004-quant-derivatives-rates-sensitivity-manual.pdf": {
        "id": "LOTQ-0004",
        "title": "Derivatives, Rates of Change, and Sensitivity",
        "category": "Calculus",
        "difficulty": "Intermediate",
        "subtitle": "Local change, gradients, Greeks, marginal risk, and robustness diagnostics.",
    },
    "lotq-0005-functions-graphs-transformations-field-guide.pdf": {
        "id": "LOTQ-0005",
        "title": "Functions, Graphs, and Transformations",
        "category": "Functions",
        "difficulty": "Beginner",
        "subtitle": "Function behavior, graph transformations, feature maps, and quant pipeline intuition.",
    },
    "lotq-0006-quant-sequences-series-financial-growth-manual.pdf": {
        "id": "LOTQ-0006",
        "title": "Sequences, Series, and Financial Growth",
        "category": "Core Math",
        "difficulty": "Beginner",
        "subtitle": "Ordered values, summed values, compounding, discounting, and equity-curve mechanics.",
    },
    "lotq-0007-quant-integrals-accumulation-expected-value-manual.pdf": {
        "id": "LOTQ-0007",
        "title": "Integrals, Accumulation, and Expected Value",
        "category": "Calculus",
        "difficulty": "Intermediate",
        "subtitle": "Accumulation, discounting, scenario weighting, expected value, and numeric methods.",
    },
    "lotq-0008-functions-expanded-field-guide-intermediate.pdf": {
        "id": "LOTQ-0008",
        "title": "Functions Expanded Field Guide",
        "category": "Functions",
        "difficulty": "Intermediate",
        "subtitle": "Function families, formulas, graph behavior, research uses, and common traps.",
    },
    "lotq-0009-algebra-foundations-for-quant-research-manual.pdf": {
        "id": "LOTQ-0009",
        "title": "Algebra Foundations for Quant Research",
        "category": "Algebra",
        "difficulty": "Beginner",
        "subtitle": "Variables, equations, constraints, scaling, PnL formulas, and formula debugging.",
    },
    "lotq-0010-quant-linear-algebra-foundations-for-quant-research-manual.pdf": {
        "id": "LOTQ-0010",
        "title": "Linear Algebra Foundations for Quant Research",
        "category": "Linear Algebra",
        "difficulty": "Beginner",
        "subtitle": "Vectors, matrices, covariance, regression geometry, PCA, and implementation hazards.",
    },
    "lotq-0011-quant-vectors-matrices-factor-models-manual.pdf": {
        "id": "LOTQ-0011",
        "title": "Vectors, Matrices, and Factor Models",
        "category": "Linear Algebra",
        "difficulty": "Intermediate",
        "subtitle": "Exposure vectors, return matrices, factor models, risk decompositions, and attribution.",
    },
}


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, width_chars: int, font: str, size: int, leading: int) -> float:
    c.setFont(font, size)
    for line in wrap(text, width_chars):
        c.drawString(x, y, line)
        y -= leading
    return y


def make_cover(meta: dict[str, str], width: float, height: float) -> bytes:
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    margin = 48
    c.setFillColor(NAVY)
    c.roundRect(margin, height - 292, width - 2 * margin, 232, 14, fill=1, stroke=0)
    c.setFillColor(NAVY_2)
    c.roundRect(margin + 14, height - 326, width - 2 * margin - 28, 44, 10, fill=1, stroke=0)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 9)
    eyebrow = f"{meta['id']} / {meta['category'].upper()} / {meta['difficulty'].upper()} / FIELD GUIDE"
    c.drawString(margin + 22, height - 92, eyebrow)

    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(margin + 22, height - 108, margin + 132, height - 108)

    y = height - 148
    c.setFillColor(colors.white)
    for line in wrap(meta["title"], 28):
        c.setFont("Helvetica-Bold", 30)
        c.drawString(margin + 22, y, line)
        y -= 36

    c.setFillColor(colors.HexColor("#DDE8F6"))
    y = draw_wrapped(c, meta["subtitle"], margin + 22, height - 262, 78, "Helvetica", 10, 14)

    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 28, height - 313, "Library of the Quant")
    c.setFont("Helvetica", 9)
    c.drawRightString(width - margin - 28, height - 313, "Educational reference manual")

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, height - 350, "Manual Profile")
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(margin, height - 360, width - margin, height - 360)

    profile = [
        ("Library ID", meta["id"]),
        ("Category", meta["category"]),
        ("Difficulty", meta["difficulty"]),
        ("Format", "Single-column field-guide manual"),
        ("Use", "Study, lookup, and research-system reference"),
    ]
    y = height - 392
    for label, value in profile:
        c.setFillColor(MUTED)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(margin, y, label.upper())
        c.setFillColor(INK)
        c.setFont("Helvetica", 11)
        c.drawString(margin + 110, y, value)
        y -= 26

    c.setFillColor(colors.HexColor("#E9EEF7"))
    c.roundRect(margin, 126, width - 2 * margin, 92, 10, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 18, 188, "Educational Use Only")
    c.setFont("Helvetica", 9)
    disclaimer = (
        "This manual is educational material for quant research study. It is not financial advice, "
        "not a trading recommendation, and not a guarantee of correctness or live trading usefulness."
    )
    draw_wrapped(c, disclaimer, margin + 18, 170, 88, "Helvetica", 9, 12)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(margin, 54, f"Library of the Quant - {meta['title']}")
    c.drawRightString(width - margin, 54, meta["id"])
    c.showPage()
    c.save()
    packet.seek(0)
    return packet.read()


def normalize_pdf(pdf: Path) -> None:
    meta = MANUALS[pdf.name]
    reader = PdfReader(str(pdf))
    writer = PdfWriter()
    width = float(reader.pages[0].mediabox.width)
    height = float(reader.pages[0].mediabox.height)

    cover_reader = PdfReader(io.BytesIO(make_cover(meta, width, height)))
    writer.add_page(cover_reader.pages[0])

    for page in reader.pages[1:]:
        writer.add_page(page)

    tmp = pdf.with_suffix(".normalized.tmp.pdf")
    with tmp.open("wb") as fh:
        writer.write(fh)
    tmp.replace(pdf)


def main() -> None:
    for pdf in sorted(PDF_ROOT.rglob("*.pdf")):
        if pdf.name not in MANUALS:
            raise SystemExit(f"Missing metadata for {pdf}")
        normalize_pdf(pdf)
        print(f"normalized {pdf.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
