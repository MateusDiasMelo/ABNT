# ABNT NBR 14724 - Elementos Implementados

Este documento descreve as funcionalidades implementadas para formatação completa de trabalhos acadêmicos seguindo a norma ABNT NBR 14724.

## 📋 Visão Geral

O formatador ABNT agora suporta todos os elementos obrigatórios e opcionais especificados na NBR 14724, incluindo:

- **Elementos pré-textuais**: Capa, folha de rosto, errata, dedicatória, agradecimentos, epígrafe, resumos, sumário
- **Elementos textuais**: Introdução, desenvolvimento, conclusão (formatação automática)
- **Elementos pós-textuais**: Referências, glossário, apêndice, anexo, índice

## 🎯 Elementos Pré-Textuais

### Obrigatórios

#### 1. Capa
Contém:
- Nome do autor (centralizado, parte superior)
- Título do trabalho (centralizado, meio da página)
- Subtítulo (se houver)
- Cidade da instituição
- Ano de depósito

#### 2. Folha de Rosto
Contém:
- Nome do autor
- Título e subtítulo
- Natureza do trabalho (tipo, objetivo, instituição, área)
- Nome do orientador e co-orientador (se houver)
- Cidade e ano

#### 3. Resumo na Língua Vernácula
- Texto do resumo em português
- Palavras-chave (3 a 5 palavras)

#### 4. Resumo em Língua Estrangeira (Abstract)
- Texto do resumo em inglês
- Keywords (3 a 5 palavras)

#### 5. Sumário
- Lista de todas as seções e subseções com respectivas páginas
- Gerado automaticamente baseado nos títulos do documento

### Opcionais

#### 1. Errata
Lista de correções do trabalho em formato de tabela:
- Folha
- Linha
- Onde se lê
- Leia-se

#### 2. Folha de Aprovação
Documento com assinaturas da banca examinadora (geralmente adicionado após a defesa)

#### 3. Dedicatória
Texto dedicado a alguém (posicionado na parte inferior direita da página)

#### 4. Agradecimentos
Texto de agradecimentos às pessoas que contribuíram para o trabalho

#### 5. Epígrafe
Citação seguida de autoria (posicionada na parte inferior direita da página)

#### 6. Listas
- Lista de tabelas
- Lista de ilustrações
- Lista de abreviaturas e siglas
- Lista de símbolos

## 📚 Elementos Textuais

A formatação automática é aplicada a:

### 1. Introdução
- Primeira seção principal do trabalho
- Apresenta o tema, objetivos, justificativa e metodologia

### 2. Desenvolvimento
- Corpo do trabalho
- Pode ser dividido em várias seções e subseções
- Revisão bibliográfica, metodologia, resultados

### 3. Conclusão
- Considerações finais do trabalho
- Retomada dos objetivos e principais resultados

### Formatação Aplicada

- **Fonte**: Times New Roman, tamanho 12
- **Espaçamento**: 1,5 entre linhas
- **Alinhamento**: Justificado
- **Recuo de parágrafo**: 1,25 cm
- **Títulos**: Negrito, numerados (1, 1.1, 1.1.1, etc.)

## 📖 Elementos Pós-Textuais

### Obrigatórios

#### 1. Referências
- Lista de todas as obras citadas no trabalho
- Formatação segundo NBR 6023
- Alinhamento à esquerda
- Espaçamento simples entre linhas
- Espaço simples em branco entre referências

### Opcionais

#### 1. Glossário
- Definições de termos técnicos utilizados
- Organizado em ordem alfabética

#### 2. Apêndice
- Textos ou documentos elaborados pelo autor
- Complementam o trabalho
- Identificados por letras maiúsculas (APÊNDICE A, APÊNDICE B, etc.)

#### 3. Anexo
- Textos ou documentos NÃO elaborados pelo autor
- Fundamentação, comprovação ou ilustração
- Identificados por letras maiúsculas (ANEXO A, ANEXO B, etc.)

#### 4. Índice
- Lista detalhada de assuntos, nomes, lugares
- Com indicação das páginas onde aparecem

## 🚀 Como Usar

### Opção 1: Via API (Recomendado para aplicações web)

```python
import requests

# 1. Upload do documento
with open('meu_trabalho.docx', 'rb') as f:
    response = requests.post('http://localhost:8000/api/upload', files={'file': f})
    file_id = response.json()['file_id']

# 2. Processar com elementos pré-textuais
metadata = {
    "author": "João da Silva",
    "title": "Título do Trabalho",
    "subtitle": "Subtítulo (opcional)",
    "institution": "Universidade Federal de São Paulo",
    "department": "Instituto de Ciência e Tecnologia",
    "degree_type": "Trabalho de Conclusão de Curso",
    "field_of_study": "Engenharia Biomédica",
    "city": "São José dos Campos",
    "year": 2024,
    "advisor": "Prof. Dr. José da Silva",
    "abstract_pt": "Texto do resumo em português...",
    "keywords_pt": ["Palavra1", "Palavra2", "Palavra3"],
    "abstract_en": "Abstract text in English...",
    "keywords_en": ["Keyword1", "Keyword2", "Keyword3"]
}

processing_request = {
    "include_pretextual": True,
    "metadata": metadata
}

response = requests.post(
    f'http://localhost:8000/api/process/{file_id}',
    json=processing_request
)

# 3. Download do documento formatado (após pagamento)
# ...
```

### Opção 2: Uso Direto no Python

```python
from docx import Document
from app.services.abnt_formatter import ABNTFormatter, DocumentMetadata

# Define metadados
metadata = DocumentMetadata(
    author="João da Silva",
    title="Título do Trabalho",
    institution="Universidade Federal de São Paulo",
    city="São Paulo",
    year=2024,
    advisor="Prof. Dr. José da Silva",
    abstract_pt="Resumo do trabalho...",
    keywords_pt=["Palavra1", "Palavra2"],
    # ... outros campos opcionais
)

# Carrega documento
doc = Document('meu_trabalho.docx')

# Aplica formatação ABNT com elementos pré-textuais
formatter = ABNTFormatter(doc, metadata=metadata)
formatted_doc = formatter.format_document(include_pretextual=True)

# Salva
formatted_doc.save('trabalho_formatado_abnt.docx')
```

### Opção 3: Apenas Formatação (Sem Elementos Pré-textuais)

```python
from docx import Document
from app.services.abnt_formatter import ABNTFormatter

doc = Document('meu_trabalho.docx')
formatter = ABNTFormatter(doc)
formatted_doc = formatter.format_document(include_pretextual=False)
formatted_doc.save('trabalho_formatado_simples.docx')
```

## 📐 Especificações Técnicas

### Configuração de Página

- **Papel**: A4 (21,0 cm × 29,7 cm)
- **Margens**:
  - Superior: 3,0 cm
  - Esquerda: 3,0 cm
  - Inferior: 2,0 cm
  - Direita: 2,0 cm

### Tipografia

- **Fonte principal**: Times New Roman
- **Fonte alternativa**: Arial
- **Tamanho normal**: 12 pt
- **Tamanho reduzido**: 10 pt (citações longas, notas de rodapé)

### Espaçamento

- **Texto normal**: 1,5 entre linhas
- **Citações longas**: Simples
- **Referências**: Simples entre linhas, espaço simples em branco entre itens
- **Títulos**: Espaçamento antes e depois

### Numeração

- **Páginas**: Números arábicos no canto superior direito
- **Início da contagem**: Folha de rosto
- **Início da numeração visível**: Primeira página da parte textual (Introdução)
- **Seções**: Numeração progressiva (1, 1.1, 1.1.1, etc.)

## ⚙️ Campos de Metadados Disponíveis

### Obrigatórios
- `author`: Nome completo do autor
- `title`: Título do trabalho
- `institution`: Nome da instituição
- `city`: Cidade
- `year`: Ano

### Recomendados
- `degree_type`: Tipo do trabalho ("Trabalho de Conclusão de Curso", "Dissertação", "Tese")
- `field_of_study`: Área de concentração ("Engenharia Biomédica", etc.)
- `advisor`: Nome do orientador
- `abstract_pt`: Resumo em português
- `keywords_pt`: Lista de palavras-chave em português
- `abstract_en`: Abstract em inglês
- `keywords_en`: Lista de keywords em inglês

### Opcionais
- `subtitle`: Subtítulo do trabalho
- `department`: Departamento ou instituto
- `advisor_title`: Título do orientador (padrão: "Prof. Dr.")
- `co_advisor`: Nome do co-orientador
- `co_advisor_title`: Título do co-orientador
- `dedication`: Texto de dedicatória
- `acknowledgments`: Texto de agradecimentos
- `epigraph`: Texto da epígrafe
- `epigraph_author`: Autor da epígrafe
- `errata_items`: Lista de erros a corrigir

### Formato de Errata

```python
errata_items = [
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
```

## 🧪 Testes

Para testar as novas funcionalidades, execute o exemplo:

```bash
cd backend
source venv/bin/activate
python example_abnt_usage.py
```

Este script criará dois documentos de exemplo:
1. **exemplo_trabalho_abnt.docx**: Documento completo com todos os elementos pré-textuais
2. **exemplo_simples_abnt.docx**: Documento com formatação básica apenas

## 📝 Notas Importantes

1. **Elementos pré-textuais** são adicionados APENAS quando `include_pretextual=True`
2. **Metadados** são opcionais - se não fornecidos, apenas a formatação básica é aplicada
3. A **numeração de páginas** pula os elementos pré-textuais (começa na Introdução)
4. **Listas** (tabelas, figuras, etc.) ainda precisam de implementação automática completa
5. **Sumário** será gerado automaticamente em versões futuras (atualmente é um placeholder)

## 🔄 Próximas Melhorias

- [ ] Geração automática do sumário com números de página
- [ ] Detecção automática de tabelas e figuras para listas
- [ ] Detecção automática de abreviaturas e siglas
- [ ] Folha de aprovação customizável
- [ ] Suporte para diferentes templates de universidades
- [ ] Validação mais rigorosa dos metadados
- [ ] Exportação para PDF mantendo a formatação

## 📚 Referências

- ABNT NBR 14724:2011 - Informação e documentação — Trabalhos acadêmicos — Apresentação
- ABNT NBR 6023:2018 - Informação e documentação — Referências — Elaboração
- ABNT NBR 6024:2012 - Informação e documentação — Numeração progressiva das seções de um documento — Apresentação
- ABNT NBR 6027:2012 - Informação e documentação — Sumário — Apresentação
- ABNT NBR 6028:2021 - Informação e documentação — Resumo, resenha e recensão — Apresentação

## 💡 Suporte

Para dúvidas ou problemas, consulte:
- README.md principal do projeto
- Exemplos em `backend/example_abnt_usage.py`
- Issues no GitHub

---

**Versão**: 2.0
**Data**: Dezembro 2024
**Implementação**: NBR 14724:2011 completa
