# AGENTS-PYTEMPLATE.md - Instrukcja użycia

## Cel

`AGENTS-PYTEMPLATE.md` to szablon pliku konfiguracyjnego dla agentów AI (Gemini, Copilot, Claude, etc.) przeznaczony dla nowych projektów Python.

## Jak używać

### 1. Skopiuj szablon do swojego projektu

```bash
cp AGENTS-PYTEMPLATE.md /path/to/your/project/AGENTS.md
```

### 2. Zamień zmienne konfiguracyjne

Otwórz plik `AGENTS.md` i zamień wszystkie zmienne w nawiasach klamrowych `{VARIABLE}` na właściwe wartości dla swojego projektu:

#### Wymagane zmienne:

- `{PROJECT_NAME}` - Nazwa projektu (np. "MyAwesomeProject")
- `{PACKAGE_NAME}` - Nazwa pakietu Python (np. "myproject")
- `{AUTHOR_NAME}` - Imię i nazwisko autora (np. "Jan Kowalski")
- `{AUTHOR_EMAIL}` - Email autora (np. "jan@example.com")
- `{PYTHON_VERSION}` - Minimalna wersja Python (np. "3.10+", "3.11+")

#### Opcjonalne zmienne (mają wartości domyślne):

- `{TEST_DIR}` - Katalog z testami (domyślnie "tests")
- `{DOCS_DIR}` - Katalog z dokumentacją (domyślnie "docs")
- `{EXAMPLES_DIR}` - Katalog z przykładami (usuń jeśli nie masz)

### 3. Przykład szybkiej zamiany (Linux/macOS)

```bash
cd /path/to/your/project

# Zamiana zmiennych za pomocą sed
sed -i 's/{PROJECT_NAME}/MyAwesomeProject/g' AGENTS.md
sed -i 's/{PACKAGE_NAME}/myproject/g' AGENTS.md
sed -i 's/{AUTHOR_NAME}/Jan Kowalski/g' AGENTS.md
sed -i 's/{AUTHOR_EMAIL}/jan@example.com/g' AGENTS.md
sed -i 's/{PYTHON_VERSION}/3.11+/g' AGENTS.md
sed -i 's/{TEST_DIR}/tests/g' AGENTS.md
sed -i 's/{DOCS_DIR}/docs/g' AGENTS.md
sed -i 's/{EXAMPLES_DIR}/examples/g' AGENTS.md
```

### 4. Dostosuj sekcje do swojego projektu

Po zamianie zmiennych przejrzyj plik i:

1. **Usuń sekcję komentarza** na początku pliku (marked z `<!-- -->`)
2. **Dostosuj sekcję "Użycie JskToolBox"** - jeśli nie używasz JskToolBox, usuń lub zmodyfikuj tę sekcję
3. **Uzupełnij sekcję "Projekt-specyficzne zasady"** - dodaj własne wzorce i konwencje
4. **Zaktualizuj sekcję "Kontakt i zasoby"** - dodaj linki do repozytorium, dokumentacji, itp.
5. **Usuń/zmodyfikuj nieużywane sekcje** - np. jeśli nie masz katalogu `examples/`

### 5. Commituj do repozytorium

```bash
git add AGENTS.md
git commit -m "docs: add AI agent configuration"
```

## Struktura szablonu

Szablon zawiera następujące sekcje:

1. **Konfiguracja plików** - Include/exclude patterns dla agentów AI
2. **Język i zarządzanie projektem** - Python, Poetry, Git
3. **Styl kodowania** - Black, PEP 8, type hints
4. **Standardy Docstringów** - Format i wymagania
5. **Testowanie** - Pytest, unittest, pokrycie
6. **Dokumentacja** - Struktura i generowanie
7. **Wzorce architektury** - JskToolBox best practices (opcjonalne)
8. **Docstring Templates** - Gotowe szablony
9. **Markdown Documentation Template** - Format dokumentacji
10. **Git Workflow** - Branch naming, commit messages
11. **Narzędzia Development** - Poetry, formatowanie, testy
12. **Projekt-specyficzne zasady** - Sekcja do wypełnienia
13. **Kontakt i zasoby** - Linki i informacje

## Kompatybilność z agentami AI

Szablon jest kompatybilny z następującymi agentami AI:

- ✅ GitHub Copilot
- ✅ Google Gemini
- ✅ Claude (Anthropic)
- ✅ OpenAI Codex
- ✅ Inne agenty wspierające Markdown configuration files

## Wskazówki

### Dla projektów bez JskToolBox

Jeśli nie używasz biblioteki JskToolBox, usuń lub zmodyfikuj sekcję "Użycie JskToolBox":

```bash
# Edytuj AGENTS.md i usuń sekcję:
# #### Użycie JskToolBox (jeśli dotyczy)
# ... cała sekcja do końca ...
```

### Dla projektów z własną biblioteką bazową

Zastąp sekcję "Użycie JskToolBox" własną sekcją z wzorcami z twojej biblioteki:

```markdown
#### Użycie MyLibrary

Projekt wykorzystuje bibliotekę `mylibrary` jako fundament. Kluczowe wzorce:

[...]
```

### Dla projektów z dokumentacją Sphinx

Dodaj do sekcji "Dokumentacja":

```markdown
- Dokumentacja API generowana przez Sphinx: `make docs`
- Output: `docs/_build/html/index.html`
- Regeneruj przed commitowaniem zmian w API
```

### Dla projektów z MkDocs

Dodaj do sekcji "Dokumentacja":

```markdown
- Dokumentacja generowana przez MkDocs: `mkdocs build`
- Development server: `mkdocs serve`
- Output: `site/`
```

## Przykłady projektów

Przykłady projektów używających tego szablonu:

- **JskToolBox** - Oryginalny projekt z pełną konfiguracją
- _(Dodaj swoje projekty tutaj)_

## Changelog szablonu

### v1.0.0 (2024-XX-XX)

- Initial release
- Bazuje na JskToolBox AGENTS.md best practices
- Obsługa Python 3.10+
- Poetry, Black, Pytest
- JskToolBox integration (optional)

## Licencja

Ten szablon jest dostępny jako część projektu JskToolBox.

## Kontakt

W razie pytań lub sugestii dotyczących szablonu, skontaktuj się z maintainerem projektu JskToolBox.
