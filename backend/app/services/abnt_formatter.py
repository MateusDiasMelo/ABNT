"""
ABNT Formatter Service - NBR 14724 e NBR 6023
Formatação automática de trabalhos acadêmicos.

Implementa todos os elementos obrigatórios e opcionais da NBR 14724:
- Elementos pré-textuais: capa, lombada, folha de rosto, errata, folha de aprovação,
  dedicatória, agradecimentos, epígrafe, resumos, listas, sumário
- Elementos textuais: introdução, desenvolvimento, conclusão
- Elementos pós-textuais: referências, glossário, apêndice, anexo, índice
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from typing import Optional, Dict, List
from dataclasses import dataclass, field
from datetime import datetime
import re


@dataclass
class DocumentMetadata:
    """Metadados do documento acadêmico seguindo NBR 14724."""

    # Elementos obrigatórios
    author: str = ""
    title: str = ""
    subtitle: Optional[str] = None
    institution: str = ""
    department: Optional[str] = None
    degree_type: str = ""  # Ex: "Trabalho de Conclusão de Curso", "Dissertação", "Tese"
    field_of_study: str = ""  # Ex: "Engenharia Biomédica"
    city: str = ""
    year: int = datetime.now().year

    # Elementos opcionais
    advisor: Optional[str] = None
    advisor_title: Optional[str] = "Prof. Dr."
    co_advisor: Optional[str] = None
    co_advisor_title: Optional[str] = "Prof. Dr."

    # Elementos pré-textuais opcionais
    dedication: Optional[str] = None
    acknowledgments: Optional[str] = None
    epigraph: Optional[str] = None
    epigraph_author: Optional[str] = None
    abstract_pt: Optional[str] = None
    keywords_pt: Optional[List[str]] = field(default_factory=list)
    abstract_en: Optional[str] = None
    keywords_en: Optional[List[str]] = field(default_factory=list)

    # Errata
    errata_items: Optional[List[Dict[str, str]]] = field(default_factory=list)
    # Formato: [{"folha": "32", "linha": "3", "onde_se_le": "estrágico", "leia_se": "estratégico"}]

    def get_complete_title(self) -> str:
        """Retorna título completo com subtítulo."""
        if self.subtitle:
            return f"{self.title}: {self.subtitle}"
        return self.title


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

    def __init__(self, doc: Document, metadata: Optional[DocumentMetadata] = None):
        """
        Inicializa o formatador ABNT.

        Args:
            doc: Documento python-docx para formatar
            metadata: Metadados do documento (opcional)
        """
        self.doc = doc
        self.metadata = metadata or DocumentMetadata()
        self.page_count = 0

    def format_document(self, include_pretextual: bool = False) -> Document:
        """
        Aplica todas as formatações ABNT ao documento.

        Args:
            include_pretextual: Se True, adiciona elementos pré-textuais (capa, folha de rosto, etc.)

        Returns:
            Documento formatado
        """
        self._setup_page_settings()
        self._setup_styles()

        # Adiciona elementos pré-textuais se solicitado
        if include_pretextual:
            self._add_pretextual_elements()

        # Formata o conteúdo existente
        self._format_paragraphs()
        self._format_headings()
        self._format_citations()
        self._format_references()

        # Formata elementos pós-textuais
        self._format_post_textual_elements()

        # Adiciona numeração de páginas (pula elementos pré-textuais)
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

    # ========== ELEMENTOS PRÉ-TEXTUAIS ==========

    def _add_pretextual_elements(self):
        """Adiciona todos os elementos pré-textuais ao documento."""
        # A ordem segue a NBR 14724
        self._create_cover_page()
        # Lombada não é criada em DOCX (é elemento físico da encadernação)
        self._create_title_page()

        if self.metadata.errata_items:
            self._create_errata_page()

        # Folha de aprovação (geralmente adicionada após a defesa)
        # self._create_approval_page()

        if self.metadata.dedication:
            self._create_dedication_page()

        if self.metadata.acknowledgments:
            self._create_acknowledgments_page()

        if self.metadata.epigraph:
            self._create_epigraph_page()

        if self.metadata.abstract_pt:
            self._create_abstract_page_pt()

        if self.metadata.abstract_en:
            self._create_abstract_page_en()

        # Listas (tabelas, abreviaturas, símbolos) são detectadas automaticamente
        self._create_lists()

        # Sumário é gerado automaticamente baseado nos títulos
        self._create_summary()

    def _create_cover_page(self):
        """
        Cria a capa (elemento obrigatório) seguindo NBR 14724.

        Elementos da capa:
        - Nome do autor (centralizado, parte superior)
        - Título (centralizado, meio da página)
        - Subtítulo (se houver)
        - Cidade (centralizado, parte inferior)
        - Ano (centralizado, parte inferior)
        """
        # Insere nova página no início
        self._insert_page_at_beginning()

        # Nome do autor (topo)
        p = self.doc.paragraphs[0]
        p.text = self.metadata.author.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(5)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Título (meio da página)
        p = self.doc.add_paragraph()
        p.text = self.metadata.title.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(8)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Subtítulo (se houver)
        if self.metadata.subtitle:
            p = self.doc.add_paragraph()
            p.text = self.metadata.subtitle
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_NORMAL

        # Cidade e ano (parte inferior)
        p = self.doc.add_paragraph()
        p.text = self.metadata.city.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(10)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        p = self.doc.add_paragraph()
        p.text = str(self.metadata.year)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Quebra de página
        self.doc.add_page_break()

    def _create_title_page(self):
        """
        Cria a folha de rosto (elemento obrigatório) seguindo NBR 14724.

        Elementos da folha de rosto:
        - Nome do autor
        - Título e subtítulo
        - Natureza do trabalho
        - Nome do orientador
        - Cidade e ano
        """
        # Nome do autor
        p = self.doc.add_paragraph()
        p.text = self.metadata.author.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(5)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Título
        p = self.doc.add_paragraph()
        p.text = self.metadata.title.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(6)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Subtítulo (se houver)
        if self.metadata.subtitle:
            p = self.doc.add_paragraph()
            p.text = self.metadata.subtitle
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_NORMAL

        # Natureza do trabalho (recuado à direita)
        p = self.doc.add_paragraph()
        natureza_text = f"{self.metadata.degree_type} para obtenção do título de graduação em {self.metadata.field_of_study}"
        if self.metadata.department:
            natureza_text += f" apresentado à {self.metadata.institution} – {self.metadata.department}."
        else:
            natureza_text += f" apresentado à {self.metadata.institution}."

        p.text = natureza_text
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Cm(3)
        p.paragraph_format.left_indent = Cm(8)  # Recuo à direita
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_PEQUENA

        # Orientador
        if self.metadata.advisor:
            p = self.doc.add_paragraph()
            p.text = f"Orientador: {self.metadata.advisor_title} {self.metadata.advisor}"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(8)
            p.paragraph_format.space_before = Pt(12)
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_PEQUENA

        # Co-orientador (se houver)
        if self.metadata.co_advisor:
            p = self.doc.add_paragraph()
            p.text = f"Co-orientador: {self.metadata.co_advisor_title} {self.metadata.co_advisor}"
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(8)
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_PEQUENA

        # Cidade e ano
        p = self.doc.add_paragraph()
        p.text = self.metadata.city.upper()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(6)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        p = self.doc.add_paragraph()
        p.text = str(self.metadata.year)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Quebra de página
        self.doc.add_page_break()

    def _create_errata_page(self):
        """
        Cria a página de errata (elemento opcional) seguindo NBR 14724.

        A errata deve conter:
        - Referência do trabalho
        - Tabela com: Folha, Linha, Onde se lê, Leia-se
        """
        if not self.metadata.errata_items:
            return

        # Título ERRATA
        p = self.doc.add_paragraph()
        p.text = "ERRATA"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Referência do trabalho
        p = self.doc.add_paragraph()
        ref_text = f"{self.metadata.author.upper()}. {self.metadata.title}"
        if self.metadata.subtitle:
            ref_text += f": {self.metadata.subtitle}"
        ref_text += f". {self.metadata.year}. {self.count_pages()} f. {self.metadata.degree_type}"
        if self.metadata.department:
            ref_text += f" ({self.metadata.field_of_study}) – {self.metadata.department}, {self.metadata.institution}, {self.metadata.city}."

        p.text = ref_text
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Cm(2)
        p.paragraph_format.space_after = Cm(1)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL

        # Tabela de errata
        table = self.doc.add_table(rows=1 + len(self.metadata.errata_items), cols=4)
        table.style = 'Table Grid'

        # Cabeçalho
        headers = table.rows[0].cells
        headers[0].text = "Folha"
        headers[1].text = "Linha"
        headers[2].text = "Onde se lê"
        headers[3].text = "Leia-se"

        for cell in headers:
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Itens da errata
        for i, item in enumerate(self.metadata.errata_items, start=1):
            row = table.rows[i].cells
            row[0].text = item.get("folha", "")
            row[1].text = item.get("linha", "")
            row[2].text = item.get("onde_se_le", "")
            row[3].text = item.get("leia_se", "")

            for cell in row:
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

        # Quebra de página
        self.doc.add_page_break()

    def _create_dedication_page(self):
        """Cria página de dedicatória (elemento opcional)."""
        if not self.metadata.dedication:
            return

        # Texto da dedicatória (posicionado na parte inferior direita)
        p = self.doc.add_paragraph()
        p.text = self.metadata.dedication
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_before = Cm(15)
        p.paragraph_format.right_indent = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.italic = True

        self.doc.add_page_break()

    def _create_acknowledgments_page(self):
        """Cria página de agradecimentos (elemento opcional)."""
        if not self.metadata.acknowledgments:
            return

        # Título
        p = self.doc.add_paragraph()
        p.text = "AGRADECIMENTOS"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Texto
        p = self.doc.add_paragraph()
        p.text = self.metadata.acknowledgments
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Cm(2)
        p.paragraph_format.line_spacing = self.ESPACAMENTO_NORMAL
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL

        self.doc.add_page_break()

    def _create_epigraph_page(self):
        """Cria página de epígrafe (elemento opcional)."""
        if not self.metadata.epigraph:
            return

        # Texto da epígrafe (posicionado na parte inferior direita)
        p = self.doc.add_paragraph()
        p.text = f'"{self.metadata.epigraph}"'
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_before = Cm(15)
        p.paragraph_format.right_indent = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_PEQUENA
            run.font.italic = True

        # Autor da epígrafe
        if self.metadata.epigraph_author:
            p = self.doc.add_paragraph()
            p.text = self.metadata.epigraph_author
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p.paragraph_format.right_indent = Cm(3)
            p.paragraph_format.space_before = Pt(6)
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_PEQUENA

        self.doc.add_page_break()

    def _create_abstract_page_pt(self):
        """Cria página de resumo em português (elemento obrigatório)."""
        if not self.metadata.abstract_pt:
            return

        # Título
        p = self.doc.add_paragraph()
        p.text = "RESUMO"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Texto do resumo
        p = self.doc.add_paragraph()
        p.text = self.metadata.abstract_pt
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Cm(2)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL

        # Palavras-chave
        if self.metadata.keywords_pt:
            p = self.doc.add_paragraph()
            p.text = f"Palavras-chave: {'. '.join(self.metadata.keywords_pt)}."
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(12)
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_NORMAL

        self.doc.add_page_break()

    def _create_abstract_page_en(self):
        """Cria página de resumo em inglês/abstract (elemento obrigatório)."""
        if not self.metadata.abstract_en:
            return

        # Título
        p = self.doc.add_paragraph()
        p.text = "ABSTRACT"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(3)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # Texto do abstract
        p = self.doc.add_paragraph()
        p.text = self.metadata.abstract_en
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Cm(2)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL

        # Keywords
        if self.metadata.keywords_en:
            p = self.doc.add_paragraph()
            p.text = f"Keywords: {'. '.join(self.metadata.keywords_en)}."
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(12)
            for run in p.runs:
                run.font.name = self.FONTE_PRINCIPAL
                run.font.size = self.TAMANHO_FONTE_NORMAL

        self.doc.add_page_break()

    def _create_lists(self):
        """
        Cria listas opcionais:
        - Lista de tabelas
        - Lista de figuras
        - Lista de abreviaturas e siglas
        - Lista de símbolos

        Essas listas são geradas automaticamente baseadas no conteúdo do documento.
        """
        # TODO: Implementar detecção automática de tabelas, figuras, abreviaturas e símbolos
        # Por enquanto, este método é um placeholder
        pass

    def _create_summary(self):
        """
        Cria o sumário (elemento obrigatório) automaticamente baseado nos títulos.

        O sumário lista todas as seções e subseções com suas respectivas páginas.
        """
        # Título SUMÁRIO
        p = self.doc.add_paragraph()
        p.text = "SUMÁRIO"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Cm(3)
        p.paragraph_format.space_after = Cm(2)
        for run in p.runs:
            run.font.name = self.FONTE_PRINCIPAL
            run.font.size = self.TAMANHO_FONTE_NORMAL
            run.font.bold = True

        # TODO: Gerar entradas do sumário automaticamente
        # Isso requer a detecção de todos os títulos (Heading 1, 2, 3, etc.)
        # e suas páginas correspondentes

        self.doc.add_page_break()

    # ========== ELEMENTOS PÓS-TEXTUAIS ==========

    def _format_post_textual_elements(self):
        """Formata todos os elementos pós-textuais do documento."""
        self._format_glossary()
        self._format_appendix()
        self._format_annex()
        self._format_index()

    def _format_glossary(self):
        """
        Formata o glossário (elemento opcional).

        O glossário contém definições de termos técnicos utilizados no trabalho,
        organizados em ordem alfabética.
        """
        in_glossary = False

        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip().upper()

            # Detecta início do glossário
            if text in ['GLOSSÁRIO', 'GLOSSARIO']:
                in_glossary = True
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.space_before = Cm(3)
                for run in paragraph.runs:
                    run.font.bold = True
                continue

            # Processa itens do glossário
            if in_glossary:
                # Verifica se é uma nova seção
                if paragraph.style.name.startswith('Heading'):
                    break

                # Formata entrada do glossário
                if paragraph.text.strip():
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                    paragraph.paragraph_format.space_after = Pt(6)
                    for run in paragraph.runs:
                        run.font.name = self.FONTE_PRINCIPAL
                        run.font.size = self.TAMANHO_FONTE_NORMAL

    def _format_appendix(self):
        """
        Formata apêndices (elemento opcional).

        Apêndices são textos ou documentos elaborados pelo próprio autor,
        que complementam o trabalho.
        """
        in_appendix = False

        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip().upper()

            # Detecta início de apêndice (APÊNDICE A, APÊNDICE B, etc.)
            if text.startswith('APÊNDICE') or text.startswith('APENDICE'):
                in_appendix = True
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.space_before = Cm(3)
                for run in paragraph.runs:
                    run.font.bold = True

    def _format_annex(self):
        """
        Formata anexos (elemento opcional).

        Anexos são textos ou documentos NÃO elaborados pelo autor,
        que servem de fundamentação, comprovação ou ilustração.
        """
        in_annex = False

        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip().upper()

            # Detecta início de anexo (ANEXO A, ANEXO B, etc.)
            if text.startswith('ANEXO'):
                in_annex = True
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.space_before = Cm(3)
                for run in paragraph.runs:
                    run.font.bold = True

    def _format_index(self):
        """
        Formata o índice (elemento opcional).

        O índice é uma lista detalhada dos assuntos, nomes, lugares,
        etc., com indicação das páginas onde aparecem.
        """
        in_index = False

        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip().upper()

            # Detecta início do índice
            if text in ['ÍNDICE', 'INDICE']:
                in_index = True
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                paragraph.paragraph_format.space_before = Cm(3)
                for run in paragraph.runs:
                    run.font.bold = True
                continue

            # Formata itens do índice
            if in_index:
                if paragraph.style.name.startswith('Heading'):
                    break

                if paragraph.text.strip():
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    for run in paragraph.runs:
                        run.font.name = self.FONTE_PRINCIPAL
                        run.font.size = self.TAMANHO_FONTE_PEQUENA

    # ========== MÉTODOS AUXILIARES ==========

    def _insert_page_at_beginning(self):
        """Insere uma nova página no início do documento."""
        # Cria um parágrafo vazio no início
        first_paragraph = self.doc.paragraphs[0]
        new_paragraph = first_paragraph.insert_paragraph_before()
        return new_paragraph
