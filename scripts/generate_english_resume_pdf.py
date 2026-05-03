from pathlib import Path

from generate_resume_pdfs import ChromePDF, html_to_pdf


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "resume" / "resume_zhibi_liu_en.html"
OUTPUT = ROOT / "resume" / "resume_zhibi_liu_en.pdf"


def build_pdf() -> None:
    chrome = ChromePDF()
    try:
        html_to_pdf(chrome, HTML, OUTPUT)
        print(OUTPUT)
    finally:
        chrome.close()


if __name__ == "__main__":
    build_pdf()
