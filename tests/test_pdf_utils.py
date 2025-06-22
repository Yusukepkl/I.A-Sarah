import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

import ia_sarah.core.adapters.services.pdf_utils as pdf_utils


def test_sanitize_filename():
    nome = "João da Silva 1/2"
    assert pdf_utils.sanitize_filename(nome) == "joao_da_silva_1_2"


def test_gerar_pdf(tmp_path):
    caminho = tmp_path / "out.pdf"
    pdf_utils.gerar_pdf("Titulo", "Conteudo", caminho)
    assert caminho.exists()
    assert caminho.stat().st_size > 0


def test_gerar_treino_pdf(tmp_path):
    caminho = tmp_path / "treino.pdf"
    exercicios = [{"nome": "Supino", "series": "3", "reps": "10", "peso": "20kg"}]
    pdf_utils.gerar_treino_pdf("Treino", exercicios, caminho)
    assert caminho.exists()
    assert caminho.stat().st_size > 0
