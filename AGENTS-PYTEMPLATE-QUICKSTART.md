# Quick Start - AGENTS-PYTEMPLATE.md

## Metoda 1: Użycie skryptu automatycznego (zalecane)

```bash
# Z katalogu JskToolBox uruchom skrypt:
./tools/setup-agents-config.sh

# Odpowiedz na pytania:
# - Project Name: MyAwesomeProject
# - Package Name: myproject
# - Author Name: Jan Kowalski
# - Author Email: jan@example.com
# - Python Version: 3.11+ (lub Enter dla domyślnej)
# - Test Directory: tests (lub Enter)
# - Docs Directory: docs (lub Enter)
# - Examples Directory: examples (lub Enter)
# - Output directory: /path/to/your/project

# Skrypt utworzy plik AGENTS.md z wypełnionymi wartościami
```

## Metoda 2: Ręczna konfiguracja

### Krok 1: Skopiuj szablon

```bash
cp /path/to/JskToolBox/AGENTS-PYTEMPLATE.md /path/to/your/project/AGENTS.md
cd /path/to/your/project
```

### Krok 2: Zamień zmienne (Linux/macOS)

```bash
# Zamień wszystkie zmienne jedną komendą:
sed -i 's/{PROJECT_NAME}/MyAwesomeProject/g' AGENTS.md && \
sed -i 's/{PACKAGE_NAME}/myproject/g' AGENTS.md && \
sed -i 's/{AUTHOR_NAME}/Jan Kowalski/g' AGENTS.md && \
sed -i 's/{AUTHOR_EMAIL}/jan@example.com/g' AGENTS.md && \
sed -i 's/{PYTHON_VERSION}/3.11+/g' AGENTS.md && \
sed -i 's/{TEST_DIR}/tests/g' AGENTS.md && \
sed -i 's/{DOCS_DIR}/docs/g' AGENTS.md && \
sed -i 's/{EXAMPLES_DIR}/examples/g' AGENTS.md && \
sed -i "s/2024-XX-XX/$(date +%Y-%m-%d)/g" AGENTS.md
```

### Krok 2b: Zamień zmienne (Windows PowerShell)

```powershell
# Zamień wszystkie zmienne:
(Get-Content AGENTS.md) -replace '{PROJECT_NAME}', 'MyAwesomeProject' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{PACKAGE_NAME}', 'myproject' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{AUTHOR_NAME}', 'Jan Kowalski' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{AUTHOR_EMAIL}', 'jan@example.com' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{PYTHON_VERSION}', '3.11+' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{TEST_DIR}', 'tests' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{DOCS_DIR}', 'docs' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '{EXAMPLES_DIR}', 'examples' |
  Set-Content AGENTS.md
(Get-Content AGENTS.md) -replace '2024-XX-XX', (Get-Date -Format 'yyyy-MM-dd') |
  Set-Content AGENTS.md
```

### Krok 3: Dostosuj plik

1. Otwórz `AGENTS.md` w edytorze
2. Usuń sekcję komentarza na początku (między `<!--` a `-->`)
3. Przejrzyj i dostosuj sekcje do swojego projektu
4. Zapisz i commituj

```bash
git add AGENTS.md
git commit -m "docs: add AI agent configuration"
```

## Metoda 3: Ręczna edycja w IDE

1. Otwórz `AGENTS-PYTEMPLATE.md` w swoim IDE
2. Użyj funkcji Find & Replace (Ctrl+H / Cmd+H):
   - Zamień `{PROJECT_NAME}` → `MyAwesomeProject`
   - Zamień `{PACKAGE_NAME}` → `myproject`
   - Zamień `{AUTHOR_NAME}` → `Jan Kowalski`
   - Zamień `{AUTHOR_EMAIL}` → `jan@example.com`
   - Zamień `{PYTHON_VERSION}` → `3.11+`
   - Zamień `{TEST_DIR}` → `tests`
   - Zamień `{DOCS_DIR}` → `docs`
   - Zamień `{EXAMPLES_DIR}` → `examples`
   - Zamień `2024-XX-XX` → dzisiejsza data w formacie YYYY-MM-DD
3. Zapisz jako `AGENTS.md` w swoim projekcie
4. Usuń sekcję komentarza na początku
5. Dostosuj i commituj

## Szybkie dostosowania po utworzeniu

### Jeśli NIE używasz JskToolBox

Usuń lub zakomentuj sekcję "Użycie JskToolBox":

```bash
# Znajdź linię "#### Użycie JskToolBox (jeśli dotyczy)"
# i usuń całą sekcję aż do następnego głównego nagłówka
```

### Jeśli używasz innego test frameworka

W sekcji "Testowanie" zamień:

```markdown
- Klasy testowe dziedziczą po `unittest.TestCase`
```

na:

```markdown
- Używamy pytest fixtures i test functions
```

### Jeśli używasz innych narzędzi

Zaktualizuj sekcję "Narzędzia Development" według swoich potrzeb.

## Weryfikacja

Po skonfigurowaniu sprawdź czy:

- [ ] Wszystkie zmienne `{...}` zostały zastąpione
- [ ] Sekcja komentarza na początku została usunięta
- [ ] Ścieżki do katalogów są poprawne
- [ ] Dane autora są prawidłowe
- [ ] Sekcje nieużywane zostały usunięte lub zakomentowane
- [ ] Plik jest w głównym katalogu projektu jako `AGENTS.md`

## Testowanie z agentem AI

Po skonfigurowaniu przetestuj działanie z agentem AI:

1. Otwórz projekt w IDE z włączonym agentem AI
2. Zapytaj: "Jaki jest styl kodowania w tym projekcie?"
3. Agent powinien odpowiedzieć zgodnie z konfiguracją w AGENTS.md

## Pomoc

Jeśli masz problemy:

1. Przeczytaj pełny `AGENTS-PYTEMPLATE-README.md`
2. Sprawdź oryginalny `AGENTS.md` w projekcie JskToolBox jako przykład
3. Otwórz issue w repozytorium JskToolBox
