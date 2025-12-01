"""
ABNT Formatter Service - NBR 14724 e NBR 6023
Formatação automática de trabalhos acadêmicos.
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import Optional, Dict, List
import re


class ABNTFormatter:
    """Formatador de documentos seguindo normas ABNT."""

    # Constantes ABNT NBR 14724
    MARGEM_SUPERIOR = Cm(3.0)
    MARGEM_INFERIOR = Cm(2.0)
    MARGEM_ESQUERDA = Cm(3.0)
    MARGEM_DIREITA = Cm(2.0)

    FONTE_PRINCIPAL = "Times New Roman"
    FONTE_ALTERNATIVA = "Arial"

    TAMANHO_FONTE_NORMAL = Pt(12)
    TAMANHO_FONTE_PEQUENA = Pt(10)

    ESPACAMENTO_NORMAL = 1.5
    ESPACAMENTO_SIMPLES = 1.0

    RECUO_PARAGRAFO = Cm(1.25)
    RECUO_CITACAO_LONGA = Cm(4.0)

    def __init__(self, doc: Document):
        """
        Inicializa o formatador ABNT.

        Args:
            doc: Documento python-docx para formatar
        """
        self.doc = doc
        self.page_count = 0

    def format_document(self) -> Document:
        """
        Aplica todas as formatações ABNT ao documento.

        Returns:
            Documento formatado
        """
        self._setup_page_settings()
        self._setup_styles()
        self._format_paragraphs()
        self._format_headings()
        self._format_citations()
        self._format_references()
        self._add_page_numbers()

        return self.doc

    def _setup_page_settings(self):
        """Configura as margens e tamanho da página (A4)."""
        sections = self.doc.sections

        for section in sections:
            # Tamanho A4
            section.page_height = Cm(29.7)
            section.page_width = Cm(21.0)

            # Margens ABNT
            section.top_margin = self.MARGEM_SUPERIOR
            section.bottom_margin = self.MARGEM_INFERIOR
            section.left_margin = self.MARGEM_ESQUERDA
            section.right_margin = self.MARGEM_DIREITA

    def _setup_styles(self):
        """Configura os estilos do documento."""
        styles = self.doc.styles

        # Estilo Normal (corpo do texto)
        try:
            normal_style = styles['Normal']
        except KeyError:
            normal_style = styles.add_style('Normal', WD_STYLE_TYPE.PARAGRAPH)

        normal_font = normal_style.font
        normal_font.name = self.FONTE_PRINCIPAL
        normal_font.size = self.TAMANHO_FONTE_NORMAL

        normal_paragraph = normal_style.paragraph_format
        normal_paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        normal_paragraph.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        normal_paragraph.line_spacing = self.ESPACAMENTO_NORMAL
        normal_paragraph.first_line_indent = self.RECUO_PARAGRAFO
        normal_paragraph.space_before = Pt(0)
        normal_paragraph.space_after = Pt(0)

        # Estilo para citações longas
        try:
            quote_style = styles['Quote']
        except KeyError:
            quote_style = styles.add_style('Quote', WD_STYLE_TYPE.PARAGRAPH)

        quote_font = quote_style.font
        quote_font.name = self.FONTE_PRINCIPAL
        quote_font.size = self.TAMANHO_FONTE_PEQUENA

        quote_paragraph = quote_style.paragraph_format
        quote_paragraph.left_indent = self.RECUO_CITACAO_LONGA
        quote_paragraph.line_spacing_rule = WD_LINE_SPACING.SINGLE
        quote_paragraph.space_before = Pt(6)
        quote_paragraph.space_after = Pt(6)

        # Estilos de título
        self._setup_heading_styles()

    def _setup_heading_styles(self):
        """Configura estilos de títulos (seções)."""
        styles = self.doc.styles

        for i in range(1, 6):  # Heading 1 a Heading 5
            style_name = f'Heading {i}'
            try:
                heading_style = styles[style_name]
            except KeyError:
                heading_style = styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)

            heading_font = heading_style.font
            heading_font.name = self.FONTE_PRINCIPAL
            heading_font.size = self.TAMANHO_FONTE_NORMAL
            heading_font.bold = True
            heading_font.color.rgb = RGBColor(0, 0, 0)

            heading_paragraph = heading_style.paragraph_format
            heading_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            heading_paragraph.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
            heading_paragraph.line_spacing = self.ESPACAMENTO_NORMAL
            heading_paragraph.space_before = Pt(12)
            heading_paragraph.space_after = Pt(6)
            heading_paragraph.keep_with_next = True

    def _format_paragraphs(self):
        """Formata todos os parágrafos do documento."""
        for paragraph in self.doc.paragraphs:
            # Ignora parágrafos vazios
            if not paragraph.text.strip():
                continue

            # Aplica formatação se não for título
            if not paragraph.style.name.startswith('Heading'):
                paragraph.style = 'Normal'

                # Verifica se é citação longa (mais de 3 linhas ou > 300 caracteres)
                if self._is_long_citation(paragraph.text):
                    paragraph.style = 'Quote'

    def _is_long_citation(self, text: str) -> bool:
        """
        Verifica se o texto é uma citação longa.

        Args:
            text: Texto do parágrafo

        Returns:
            True se for citação longa
        """
        # Critérios: mais de 300 caracteres OU contém padrões de citação
        citation_patterns = [
            r'\([A-Z]+,\s*\d{4},\s*p\.\s*\d+\)',  # (AUTOR, 2020, p. 10)
            r'segundo\s+[A-Z]',  # segundo Fulano
            r'de acordo com\s+[A-Z]',  # de acordo com Fulano
            r'conforme\s+[A-Z]',  # conforme Fulano
        ]

        is_citation_pattern = any(re.search(pattern, text, re.IGNORECASE) for pattern in citation_patterns)
        is_long = len(text) > 300

        return is_citation_pattern and is_long

    def _format_headings(self):
        """Formata e numera os títulos das seções."""
        section_counters = [0, 0, 0, 0, 0]  # Contadores para até 5 níveis

        for paragraph in self.doc.paragraphs:
            if paragraph.style.name.startswith('Heading'):
                level = int(paragraph.style.name.split()[-1]) - 1

                # Incrementa contador do nível atual
                section_counters[level] += 1

                # Zera contadores de níveis inferiores
                for i in range(level + 1, 5):
                    section_counters[i] = 0

                # Gera numeração (ex: 1.2.3)
                numbering = '.'.join(str(section_counters[i]) for i in range(level + 1) if section_counters[i] > 0)

                # Remove numeração existente
                text = re.sub(r'^\d+(\.\d+)*\s*', '', paragraph.text)

                # Adiciona nova numeração
                paragraph.text = f"{numbering} {text}"

                # Remove ponto final se existir
                if paragraph.text.endswith('.'):
                    paragraph.text = paragraph.text[:-1]

    def _format_citations(self):
        """Formata citações diretas e indiretas."""
        for paragraph in self.doc.paragraphs:
            text = paragraph.text

            # Identifica citações diretas entre aspas
            if '"' in text or '"' in text or '"' in text:
                # Normaliza aspas
                text = text.replace('"', '"').replace('"', '"')

                # Se for longa, aplica estilo Quote
                if len(text) > 300:
                    paragraph.style = 'Quote'

    def _format_references(self):
        """Formata a seção de referências (NBR 6023)."""
        in_references = False
        reference_paragraphs = []

        # Identifica a seção de referências
        for i, paragraph in enumerate(self.doc.paragraphs):
            text = paragraph.text.strip().upper()

            if text in ['REFERÊNCIAS', 'REFERENCIAS', 'REFERÊNCIAS BIBLIOGRÁFICAS']:
                in_references = True
                continue

            if in_references:
                if paragraph.style.name.startswith('Heading'):
                    break  # Nova seção começou

                if paragraph.text.strip():
                    reference_paragraphs.append(paragraph)

        # Formata referências
        for paragraph in reference_paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            paragraph.paragraph_format.space_after = Pt(12)  # Espaço simples entre referências
            paragraph.paragraph_format.first_line_indent = Cm(0)  # Sem recuo

            # Fonte tamanho 12
            for run in paragraph.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_NORMAL

    def _add_page_numbers(self):
        """Adiciona numeração de páginas no canto superior direito."""
        for section in self.doc.sections:
            # Cria header se não existir
            header = section.header

            # Remove conteúdo existente
            for paragraph in header.paragraphs:
                paragraph.clear()

            # Adiciona parágrafo para numeração
            paragraph = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

            # Adiciona campo de numeração
            run = paragraph.add_run()
            fldChar1 = OxmlElement('w:fldChar')
            fldChar1.set(qn('w:fldCharType'), 'begin')

            instrText = OxmlElement('w:instrText')
            instrText.set(qn('xml:space'), 'preserve')
            instrText.text = "PAGE"

            fldChar2 = OxmlElement('w:fldChar')
            fldChar2.set(qn('w:fldCharType'), 'end')

            run._r.append(fldChar1)
            run._r.append(instrText)
            run._r.append(fldChar2)

            # Formata numeração
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_PEQUENA

    def count_pages(self) -> int:
        """
        Estima o número de páginas do documento.

        Returns:
            Número estimado de páginas
        """
        # Estimativa baseada em caracteres por página A4
        # Aproximadamente 1800 caracteres por página com formatação ABNT
        total_chars = sum(len(p.text) for p in self.doc.paragraphs)
        estimated_pages = max(1, round(total_chars / 1800))

        self.page_count = estimated_pages
        return estimated_pages

    def get_document_info(self) -> Dict:
        """
        Retorna informações do documento formatado.

        Returns:
            Dicionário com informações
        """
        return {
            "total_paragraphs": len(self.doc.paragraphs),
            "total_tables": len(self.doc.tables),
            "estimated_pages": self.count_pages(),
            "has_references": self._has_references_section(),
        }

    def _has_references_section(self) -> bool:
        """Verifica se o documento possui seção de referências."""
        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip().upper()
            if text in ['REFERÊNCIAS', 'REFERENCIAS', 'REFERÊNCIAS BIBLIOGRÁFICAS']:
                return True
        return False
