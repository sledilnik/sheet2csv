# REVERSE_ENGINEERING_REPORT — sheet2csv

## A. Diagnóstico geral

### Arquitetura identificada
Biblioteca Python para exportar dados do Google Sheets para CSV via API do Google Sheets v4. Arquitetura simples:

- `sheet2csv/__init__.py`: módulo principal com funções `fetch_sheet()`, `sheet2dict()`, `sheet2csv()`, `parse_date()`, `serial2date()`, `decimal2time()`, `find_duplicates()`
- `sheet2csv/__main__.py`: ponto de entrada CLI (estava vazio antes da correção)
- `setup.py`: arquivo de empacotamento (estava vazio antes da correção)
- `setup.cfg`: metadados do pacote (nome, versão, dependências, classifiers)
- `requirements_dev.txt`: dependências de desenvolvimento (nose, black, ipython)
- `tests/test_basic.py`: testes que requerem `GOOGLE_API_KEY` do ambiente
- `.github/workflows/test.yml`: CI que roda testes no push/PR para master
- `.gitignore`: padrão Python

### Tecnologias e dependências
- Python >=3.6
- Dependências de runtime: google-api-python-client, google-auth-httplib2, google-auth-oauthlib, python-dateutil
- Dependências de dev: nose (depreciado), black, ipython
- Pacote publicado no PyPI (versão 1.0.7)

### Estado de manutenção
Último commit ativo. Repositório: https://github.com/sledilnik/sheet2csv. Branch default: master.

### Mecanismos de testes existentes
`tests/test_basic.py` com 4 testes ativos (test_fetch, test_sheet_rows, test_sheet_rows_labels, test_sheet_cols, test_sheet_cols_labels). Todos requerem `GOOGLE_API_KEY` do ambiente. Não é possível executar sem chave válida.

### Limitações da investigação
- Não é possível executar testes sem GOOGLE_API_KEY
- Não há dados de exemplo incluídos no repositório

## B. Problemas encontrados

| ID | Título | Severidade | Status | Localização |
|----|--------|------------|--------|-------------|
| REA-sheet2csv-001 | setup.py vazio (setup() sem argumentos) | P3 | CONFIRMADO | `setup.py` |
| REA-sheet2csv-002 | __main__.py vazio (sem CLI) | P3 | CONFIRMADO | `sheet2csv/__main__.py` |
| REA-sheet2csv-003 | test.yml usa actions/checkout@v6 (inexistente) | P2 | CONFIRMADO | `.github/workflows/test.yml:20` |
| REA-sheet2csv-004 | requirements_dev.txt usa nose (depreciado) | P3 | CONFIRMADO | `requirements_dev.txt` |

### Detalhes dos problemas confirmados

**REA-sheet2csv-001 (P3, CONFIRMADO)**: `setup.py` contém apenas `from setuptools import setup` seguido de `setup()` sem argumentos. Isso significa que o pacote não tem metadados, versão, dependências nem entry points definidos no setup.py (estão apenas no setup.cfg).

Evidência: `setup.py` tem apenas 2 linhas.

**REA-sheet2csv-002 (P3, CONFIRMADO)**: `sheet2csv/__main__.py` está vazio (0 bytes). Não é possível executar `python -m sheet2csv` como CLI.

Evidência: `__main__.py` tem 0 linhas de conteúdo.

**REA-sheet2csv-003 (P2, CONFIRMADO)**: `.github/workflows/test.yml:20` usa `actions/checkout@v6` e `actions/setup-python@v6`, que não existem (o máximo atual é checkout@v4 e setup-python@v5). A CI falharia ao tentar executar.

Evidência: `test.yml` linhas 20-24.

**REA-sheet2csv-004 (P3, CONFIRMADO)**: `requirements_dev.txt` lista `nose`, que é uma biblioteca de testes depreciada e não mantida.

Evidência: `requirements_dev.txt` linha 1.

## C. Problemas recorrentes
Nenhum problema recorrente público encontrado.

## D. Erros não documentados
Todos os itens da seção B são problemas não documentados anteriormente.

## E. Performance
Não há operações de performance sensíveis (exportação de dados de planilha via API).

## F. Melhorias técnicas
- Preencher setup.py com metadados completos (REA-sheet2csv-001, implementado)
- Adicionar CLI ao __main__.py (REA-sheet2csv-002, implementado)
- Corrigir versões das actions do GitHub no test.yml (REA-sheet2csv-003, implementado)
- Substituir nose por pytest em requirements_dev.txt (REA-sheet2csv-004, implementado)

## G. Plano de execução
Todas as correções são independentes e de baixo risco, implementadas em um único PR.

## H. Resultado esperado
Pacote Python corretamente empacotado, CLI funcional, CI executável, dependências de dev atualizadas.

**Ferramentas usadas:** git, gh, PowerShell, Python 3.12 (py_compile), inspeção estática.  
**Limitação:** Testes não executados (requerem GOOGLE_API_KEY).  
**Ambiente:** Windows, PowerShell 5.1, `C:\Users\User\audit-repos\sheet2csv` (clone do upstream, branch master).
