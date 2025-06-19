from fpdf import FPDF


def gerar_pdf(titulo: str, conteudo: str, caminho: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=titulo, ln=True, align='C')
    pdf.multi_cell(0, 10, txt=conteudo)
    pdf.output(caminho)
