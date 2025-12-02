"""
Exemplo de uso do ABNTFormatter com elementos pré-textuais e pós-textuais.

Este exemplo demonstra como criar um documento acadêmico completo seguindo
as normas ABNT NBR 14724, incluindo todos os elementos obrigatórios e opcionais.
"""

from docx import Document
from app.services.abnt_formatter import ABNTFormatter, DocumentMetadata


def create_complete_academic_document():
    """
    Cria um documento acadêmico completo com todos os elementos ABNT.
    """

    # Define os metadados do documento
    metadata = DocumentMetadata(
        # Elementos obrigatórios
        author="João da Silva Santos",
        title="Análise de Algoritmos de Machine Learning para Diagnóstico Médico",
        subtitle="Um Estudo de Caso em Cardiologia",
        institution="Universidade Federal de São Paulo",
        department="Instituto de Ciência e Tecnologia",
        degree_type="Trabalho de Conclusão de Curso",
        field_of_study="Engenharia Biomédica",
        city="São José dos Campos",
        year=2024,

        # Orientação
        advisor="José da Silva",
        advisor_title="Prof. Dr.",

        # Elementos opcionais
        dedication="Dedico este trabalho aos meus pais, pelo apoio incondicional durante toda a jornada acadêmica.",

        acknowledgments=(
            "Agradeço primeiramente a Deus, por me dar força e saúde para concluir este trabalho. "
            "Ao meu orientador, Prof. Dr. José da Silva, pela paciência e dedicação em todas as etapas deste projeto. "
            "Aos meus colegas de curso, pelo companheirismo e apoio mútuo. "
            "À minha família, pelo suporte emocional e financeiro que tornou possível esta conquista."
        ),

        epigraph="A ciência nunca resolve um problema sem criar pelo menos outros dez.",
        epigraph_author="George Bernard Shaw",

        # Resumo em português
        abstract_pt=(
            "Este trabalho apresenta uma análise comparativa de algoritmos de machine learning "
            "aplicados ao diagnóstico de doenças cardiovasculares. Foram avaliados cinco algoritmos "
            "diferentes: Random Forest, Support Vector Machines, Redes Neurais Artificiais, "
            "k-Nearest Neighbors e Naive Bayes. Os experimentos foram realizados utilizando "
            "a base de dados UCI Heart Disease Dataset, contendo 303 registros de pacientes. "
            "Os resultados demonstraram que o algoritmo Random Forest obteve a melhor performance, "
            "com acurácia de 87,3%, seguido por Support Vector Machines com 85,1%. "
            "Conclui-se que técnicas de machine learning podem auxiliar significativamente "
            "profissionais de saúde no diagnóstico precoce de doenças cardiovasculares, "
            "potencialmente salvando vidas através da detecção antecipada."
        ),
        keywords_pt=[
            "Machine Learning",
            "Diagnóstico Médico",
            "Doenças Cardiovasculares",
            "Random Forest",
            "Inteligência Artificial"
        ],

        # Abstract em inglês
        abstract_en=(
            "This work presents a comparative analysis of machine learning algorithms "
            "applied to cardiovascular disease diagnosis. Five different algorithms were evaluated: "
            "Random Forest, Support Vector Machines, Artificial Neural Networks, "
            "k-Nearest Neighbors, and Naive Bayes. Experiments were conducted using "
            "the UCI Heart Disease Dataset, containing 303 patient records. "
            "Results showed that the Random Forest algorithm achieved the best performance "
            "with 87.3% accuracy, followed by Support Vector Machines with 85.1%. "
            "It is concluded that machine learning techniques can significantly assist "
            "healthcare professionals in early diagnosis of cardiovascular diseases, "
            "potentially saving lives through early detection."
        ),
        keywords_en=[
            "Machine Learning",
            "Medical Diagnosis",
            "Cardiovascular Diseases",
            "Random Forest",
            "Artificial Intelligence"
        ],

        # Errata (exemplo)
        errata_items=[
            {
                "folha": "32",
                "linha": "3",
                "onde_se_le": "estrágico",
                "leia_se": "estratégico"
            },
            {
                "folha": "45",
                "linha": "12",
                "onde_se_le": "obedece",
                "leia_se": "obedecem"
            }
        ]
    )

    # Cria um novo documento
    doc = Document()

    # Adiciona conteúdo do trabalho (exemplo simplificado)
    # Introdução
    doc.add_heading('Introdução', level=1)
    doc.add_paragraph(
        'A utilização de técnicas de inteligência artificial na área médica tem crescido '
        'exponencialmente nos últimos anos. Este trabalho investiga a aplicação de algoritmos '
        'de machine learning para o diagnóstico de doenças cardiovasculares...'
    )

    # Desenvolvimento
    doc.add_heading('Desenvolvimento', level=1)

    doc.add_heading('Revisão Bibliográfica', level=2)
    doc.add_paragraph(
        'Segundo Silva (2020, p. 45), "os algoritmos de machine learning têm demonstrado '
        'resultados promissores na área médica, especialmente no diagnóstico precoce de doenças".'
    )

    doc.add_heading('Metodologia', level=2)
    doc.add_paragraph(
        'A metodologia adotada neste trabalho consiste em cinco etapas principais: '
        '(1) coleta e preparação dos dados; (2) seleção de features; (3) treinamento dos modelos; '
        '(4) avaliação de desempenho; (5) análise comparativa dos resultados.'
    )

    doc.add_heading('Resultados', level=2)
    doc.add_paragraph(
        'Os experimentos realizados demonstraram que o algoritmo Random Forest obteve '
        'o melhor desempenho, com acurácia de 87,3%. A Tabela 1 apresenta os resultados '
        'completos de todos os algoritmos avaliados.'
    )

    # Conclusão
    doc.add_heading('Conclusão', level=1)
    doc.add_paragraph(
        'Este trabalho apresentou uma análise comparativa de algoritmos de machine learning '
        'para diagnóstico de doenças cardiovasculares. Os resultados obtidos demonstram que '
        'estas técnicas podem auxiliar significativamente profissionais de saúde, '
        'potencialmente salvando vidas através da detecção precoce.'
    )

    # Referências
    doc.add_heading('REFERÊNCIAS', level=1)
    doc.add_paragraph(
        'SILVA, J. A. Machine Learning aplicado à medicina. São Paulo: Editora Saúde, 2020.'
    )
    doc.add_paragraph(
        'SANTOS, M. P.; OLIVEIRA, R. T. Diagnóstico assistido por computador: '
        'uma revisão sistemática. Revista Brasileira de Engenharia Biomédica, v. 35, n. 2, '
        'p. 123-145, 2019.'
    )

    # Apêndice
    doc.add_heading('APÊNDICE A – Código-fonte dos algoritmos', level=1)
    doc.add_paragraph(
        'Este apêndice contém o código-fonte completo dos algoritmos implementados...'
    )

    # Anexo
    doc.add_heading('ANEXO A – Aprovação do Comitê de Ética', level=1)
    doc.add_paragraph(
        'Documento de aprovação do Comitê de Ética em Pesquisa...'
    )

    # Aplica formatação ABNT com elementos pré-textuais
    formatter = ABNTFormatter(doc, metadata=metadata)
    formatted_doc = formatter.format_document(include_pretextual=True)

    # Salva o documento formatado
    output_path = '/home/user/ABNT/backend/exemplo_trabalho_abnt.docx'
    formatted_doc.save(output_path)

    # Exibe informações
    info = formatter.get_document_info()
    print(f"✅ Documento criado com sucesso!")
    print(f"📄 Arquivo: {output_path}")
    print(f"📊 Estatísticas:")
    print(f"   - Parágrafos: {info['total_paragraphs']}")
    print(f"   - Tabelas: {info['total_tables']}")
    print(f"   - Páginas estimadas: {info['estimated_pages']}")
    print(f"   - Possui referências: {'Sim' if info['has_references'] else 'Não'}")
    print(f"\n📋 Elementos pré-textuais incluídos:")
    print(f"   ✓ Capa")
    print(f"   ✓ Folha de rosto")
    print(f"   ✓ Errata")
    print(f"   ✓ Dedicatória")
    print(f"   ✓ Agradecimentos")
    print(f"   ✓ Epígrafe")
    print(f"   ✓ Resumo (PT)")
    print(f"   ✓ Abstract (EN)")
    print(f"   ✓ Sumário")

    return formatted_doc


def create_simple_document():
    """
    Cria um documento simples sem elementos pré-textuais (apenas formatação).
    """

    # Cria documento com conteúdo básico
    doc = Document()
    doc.add_heading('Introdução', level=1)
    doc.add_paragraph('Este é um texto de exemplo...')

    doc.add_heading('Desenvolvimento', level=1)
    doc.add_paragraph('Conteúdo do desenvolvimento...')

    doc.add_heading('Conclusão', level=1)
    doc.add_paragraph('Conclusão do trabalho...')

    doc.add_heading('REFERÊNCIAS', level=1)
    doc.add_paragraph('AUTOR, A. Título do livro. Cidade: Editora, 2020.')

    # Aplica apenas formatação básica (sem elementos pré-textuais)
    formatter = ABNTFormatter(doc)
    formatted_doc = formatter.format_document(include_pretextual=False)

    # Salva
    output_path = '/home/user/ABNT/backend/exemplo_simples_abnt.docx'
    formatted_doc.save(output_path)

    print(f"✅ Documento simples criado: {output_path}")

    return formatted_doc


if __name__ == '__main__':
    print("=" * 60)
    print("Exemplo 1: Documento completo com elementos pré-textuais")
    print("=" * 60)
    create_complete_academic_document()

    print("\n" + "=" * 60)
    print("Exemplo 2: Documento simples (apenas formatação)")
    print("=" * 60)
    create_simple_document()

    print("\n✨ Exemplos criados com sucesso!")
