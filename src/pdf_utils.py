from fpdf import FPDF
import unicodedata


def sanitize_filename(nome: str) -> str:
    """Gera um nome de arquivo seguro removendo acentos e espacos."""
    nfkd = unicodedata.normalize("NFKD", nome)
    ascii_only = nfkd.encode("ASCII", "ignore").decode("ASCII")
    return "".join(c if c.isalnum() else "_" for c in ascii_only).lower()


def gerar_pdf(titulo: str, conteudo: str, caminho: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_title(titulo)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align='C')
    pdf.multi_cell(0, 10, txt=conteudo)
    pdf.output(caminho)
