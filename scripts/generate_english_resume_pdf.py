from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
VENV_SITE_PACKAGES = ROOT / ".venv" / "Lib" / "site-packages"
if VENV_SITE_PACKAGES.exists():
    sys.path.insert(0, str(VENV_SITE_PACKAGES))

from fpdf import FPDF


OUTPUT = ROOT / "resume" / "resume_zhibi_liu_en.pdf"

INK = (28, 38, 51)
MUTED = (86, 105, 122)
BLUE = (36, 73, 105)
PALE_BLUE = (246, 251, 255)
BORDER = (219, 232, 243)


class ResumePDF(FPDF):
    def header(self) -> None:
        return None

    def footer(self) -> None:
        return None


def set_rgb(pdf: ResumePDF, color: tuple[int, int, int]) -> None:
    pdf.set_text_color(*color)


def fill_rgb(pdf: ResumePDF, color: tuple[int, int, int]) -> None:
    pdf.set_fill_color(*color)


def draw_page_background(pdf: ResumePDF) -> None:
    fill_rgb(pdf, (245, 248, 251))
    pdf.rect(0, 0, 210, 297, style="F")
    fill_rgb(pdf, (255, 255, 255))
    pdf.rect(10, 6, 190, 285, style="F")
    fill_rgb(pdf, (239, 246, 252))
    pdf.rect(10, 6, 190, 28, style="F")
    fill_rgb(pdf, (255, 255, 255))
    pdf.rect(10, 27, 190, 264, style="F")


def section(pdf: ResumePDF, title: str) -> None:
    pdf.ln(2.0)
    y = pdf.get_y()
    fill_rgb(pdf, (121, 184, 232))
    pdf.ellipse(13, y + 1.4, 2.1, 2.1, style="F")
    pdf.set_draw_color(214, 226, 237)
    pdf.line(41, y + 2.5, 198, y + 2.5)
    pdf.set_xy(18, y)
    pdf.set_font("Helvetica", "B", 8.9)
    set_rgb(pdf, BLUE)
    pdf.cell(0, 5.1, title.upper(), ln=1)
    set_rgb(pdf, INK)


def entry_header(pdf: ResumePDF, title: str, subtitle: str, dates: str) -> None:
    pdf.set_font("Helvetica", "B", 9.25)
    set_rgb(pdf, (24, 42, 60))
    pdf.cell(138, 4.35, title, ln=0)
    pdf.set_font("Helvetica", "", 8.15)
    set_rgb(pdf, (103, 128, 152))
    pdf.cell(0, 4.35, dates, align="R", ln=1)
    if subtitle:
        pdf.set_font("Helvetica", "", 8.45)
        set_rgb(pdf, (96, 114, 131))
        pdf.cell(0, 3.75, subtitle, ln=1)
    set_rgb(pdf, INK)


def bullet(pdf: ResumePDF, text: str, line_height: float = 3.55) -> None:
    x = pdf.get_x()
    pdf.set_font("Helvetica", "", 7.9)
    set_rgb(pdf, (36, 54, 72))
    pdf.cell(3.4, line_height, "-", ln=0)
    pdf.multi_cell(0, line_height, text)
    pdf.set_x(x)


def skill_box(pdf: ResumePDF, label: str, body: str) -> None:
    x = pdf.get_x()
    y = pdf.get_y()
    box_w = 187
    box_h = 8.9
    fill_rgb(pdf, PALE_BLUE)
    pdf.set_draw_color(*BORDER)
    pdf.rect(x, y, box_w, box_h, style="DF")
    pdf.set_xy(x + 2, y + 1.1)
    pdf.set_font("Helvetica", "B", 7.65)
    set_rgb(pdf, (33, 70, 102))
    pdf.cell(38, 3.2, label, ln=0)
    pdf.set_font("Helvetica", "", 7.75)
    set_rgb(pdf, (51, 69, 87))
    pdf.multi_cell(box_w - 42, 3.2, body)
    pdf.set_xy(x, y + box_h + 1.0)


def build_pdf() -> None:
    pdf = ResumePDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(12, 8, 12)
    pdf.add_page()
    draw_page_background(pdf)
    pdf.set_xy(13, 10)

    pdf.set_font("Helvetica", "B", 21.5)
    set_rgb(pdf, (23, 50, 74))
    pdf.cell(118, 8.3, "Zhibi Liu", ln=0)
    pdf.set_font("Helvetica", "", 8.35)
    set_rgb(pdf, MUTED)
    pdf.cell(0, 4.1, "15921101277 | billoutsider414@outlook.com", align="R", ln=1)
    pdf.set_x(13)
    pdf.set_font("Helvetica", "B", 8.65)
    set_rgb(pdf, (78, 100, 119))
    pdf.cell(118, 4.0, "Senior Data Specialist | SQL, Python, PyTorch, Data Quality, NLP", ln=0)
    pdf.set_font("Helvetica", "", 8.25)
    pdf.cell(0, 4.0, "Shanghai, China", align="R", ln=1)

    pdf.set_y(23.5)
    pdf.set_x(13)
    pdf.set_font("Helvetica", "", 8.25)
    set_rgb(pdf, (41, 55, 72))
    pdf.multi_cell(
        184,
        3.8,
        "Data specialist with hands-on experience in e-commerce data processing, data quality optimization, "
        "SQL-based investigation, rule iteration, sample screening, and workflow tooling. Experienced across "
        "data analysis, machine learning, and natural language processing scenarios, with a track record of "
        "translating business requirements into reliable data operations and lightweight internal tools.",
    )
    pdf.set_draw_color(216, 227, 237)
    pdf.line(13, 39.5, 197, 39.5)
    pdf.set_y(41)

    section(pdf, "Education")
    entry_header(pdf, "The University of Texas at Austin", "Bachelor of Science in Mathematics | GPA: 3.6 / 4.0", "Aug 2018 - May 2022")

    section(pdf, "Experience")
    entry_header(pdf, "NielsenIQ, Shanghai Branch", "Senior Data Specialist", "Dec 2024 - Present")
    bullet(pdf, "Supported multi-dimensional data requests from client-facing teams by extracting, cleaning, and validating large datasets with SQL, enabling configuration impact analysis and before/after comparisons for product classification results.")
    bullet(pdf, "Investigated bad cases in a BERT + rules product classification workflow, explained data quality issues to clients, and converted recurring error patterns into SQL / PL-SQL correction rules deployed in HUE and Oracle pipelines.")
    bullet(pdf, "Reduced final delivery error rate from approximately 20% to below 10% through iterative issue diagnosis, rule refinement, and structured validation.")
    bullet(pdf, "Designed a high-risk sample screening approach using locally deployed BERT vectorization in PyTorch, delivering 140,000+ candidate samples from three years of historical data for manual validation, supplemental labeling, and future model retraining.")
    bullet(pdf, "Built a lightweight Streamlit + Oracle productivity tool to streamline Excel ingestion, ad hoc data pulls, configuration lookup, and result comparison workflows.")

    pdf.ln(0.6)
    entry_header(pdf, "Shanghai Xuankai Business Consulting Co., Ltd.", "Business Analyst", "Nov 2022 - Nov 2024")
    bullet(pdf, "Participated in market research projects for luxury goods and sports footwear/apparel brands, covering questionnaire data processing, desk research, and consumer and market information analysis.")
    bullet(pdf, "Synthesized research findings into client-facing insights, prepared presentation materials, and supported proposal communication to translate research outputs into business recommendations.")

    section(pdf, "Projects")
    entry_header(pdf, "Multimodal LLM Validation for Product Attribute Recognition", "", "Feb 2026 - Present")
    bullet(pdf, "Designed batch concurrent API calling scripts and iterated prompts to evaluate multimodal model feasibility for product attribute recognition where text-only workflows were insufficient.")
    bullet(pdf, "Identified generalizable attributes such as specifications and packaging type as stronger candidates for practical implementation and complex sample triage.")

    pdf.ln(0.6)
    entry_header(pdf, "OCR + Model Number Matching Automation", "", "Aug 2025 - Dec 2025")
    bullet(pdf, "Used PaddleOCR to extract product model information for electronics and durable goods catalog maintenance, then combined field cleaning and brand naming rule analysis to improve matching and code-linking efficiency.")
    bullet(pdf, "Derived brand/model naming rules for products that could not be directly matched, focusing manual review on out-of-rule samples.")

    section(pdf, "Skills")
    skill_box(pdf, "Data Analysis", "Python (Pandas, NumPy, Scikit-learn, PyTorch), SQL, R")
    skill_box(pdf, "Data Platforms", "Hadoop ecosystem (HDFS, HUE, SparkSQL), Oracle, MySQL, Power BI, Streamlit")
    skill_box(pdf, "AI Tools", "Cursor, GitHub Copilot, Claude Code; practical experience with Qwen and Doubao API calls")
    skill_box(pdf, "Office", "Microsoft 365 (Excel, PowerPoint, Word), Power Automate")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
