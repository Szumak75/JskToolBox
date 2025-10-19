# Konfiguracja AI dla projektu {PROJECT_NAME}

<!--
SZABLON KONFIGURACJI DLA PROJEKTÓW PYTHON
==========================================
Instrukcja użycia:
1. Skopiuj ten plik do głównego katalogu swojego projektu jako AGENTS.md
2. Zamień wszystkie zmienne w nawiasach klamrowych {VARIABLE} na właściwe wartości
3. Dostosuj sekcje do specyfiki swojego projektu
4. Usuń tę sekcję komentarza

ZMIENNE KONFIGURACYJNE:
- {PROJECT_NAME}           - Nazwa projektu (np. "MyAwesomeProject")
- {PACKAGE_NAME}           - Nazwa pakietu Python (np. "myproject")
- {AUTHOR_NAME}            - Imię i nazwisko autora (np. "Jan Kowalski")
- {AUTHOR_EMAIL}           - Email autora (np. "jan@example.com")
- {PYTHON_VERSION}         - Minimalna wersja Python (np. "3.10+", "3.11+")
- {TEST_DIR}               - Katalog z testami (domyślnie "tests")
- {DOCS_DIR}               - Katalog z dokumentacją (domyślnie "docs")
- {EXAMPLES_DIR}           - Katalog z przykładami (opcjonalny)
-->

## Konfiguracja plików

Uwzględnij tylko pliki źródłowe Python i testy.

**files.include**

- `{PACKAGE_NAME}/**/*.py`
- `{TEST_DIR}/**/*.py`

Wyklucz katalogi wirtualnego środowiska, pamięć podręczną i inne pliki pomocnicze.

**files.exclude**

- `.venv/**`
- `venv/**`
- `.pytest_cache/**`
- `__pycache__/**`
- `dist/**`
- `build/**`
- `*.egg-info/**`
- `.git/**`
- `{EXAMPLES_DIR}/**` # Usuń jeśli chcesz uwzględnić przykłady

## Instrukcje dotyczące zachowania

Sekcje poniżej opisują preferowane ustawienia dla agentów AI (Gemini, Copilot, Claude, itp.).

### Język i zarządzanie projektem

- `language`: `Python {PYTHON_VERSION}`
- `project_management`: Projekt używa Poetry. Uruchamiaj narzędzia poprzez `poetry run <polecenie>` (np. `poetry run pytest`).
- `version_control`: Git

### Styl kodowania

- Formatuj kod przy użyciu `black`; po zmianach wykonaj `poetry run black .`.
- Pliki Markdown formatuj przy użyciu `prettier`; uruchamiaj `poetry run prettier --write <ścieżka>`.
- Przestrzegaj PEP 8 i waliduj styl poleceniem `poetry run pycodestyle`.
- Dodawaj adnotacje typów do nowych funkcji i metod.
- Preferuj pojedyncze cudzysłowy, chyba że podwójne są wymagane.

#### Standardy Docstringów

**Wymagania bezwzględne:**

- **Język angielski** - wszystkie docstringi w języku angielskim
- **Format modułu** - `Author:  ` (dwie spacje po dwukropku), `Created: YYYY-MM-DD`, `Purpose: `
- **Format funkcji/metod** - krótkie streszczenie, opcjonalne sekcje `### Arguments`, `### Returns`, `### Raises`
- **Konsystencja** - jednolity autor we wszystkich modułach: `{AUTHOR_NAME} --<{AUTHOR_EMAIL}>`

**Sekcja `### Arguments:` - kiedy wymagana:**

- **ZAWSZE dla metod z parametrami** (oprócz `self`/`cls`)
- **WYJĄTEK:** comparatory (`__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`, `__ne__`) - NIE wymagają
- **ZAWSZE dla setterów** - properties z parametrem value/arg
- **NIGDY dla getterów** - properties bez parametrów
- **ZAWSZE dla `__init__`** jeśli ma parametry
- **ZAWSZE dla pozostałych metod magicznych** z parametrami (`__setitem__`, `__getitem__`, etc.)

**Sekcje opcjonalne:**

- `### Returns` - **opcjonalna** dla metod `-> None` (setterzy, `__init__`)
- `### Raises` - **opcjonalna**, tylko gdy metoda faktycznie rzuca wyjątki

**Uwaga:** Pliki `__init__.py` mogą mieć uproszczone docstringi bez pełnej struktury Author/Created/Purpose.

### Testowanie

- Testy znajdują się w katalogu `{TEST_DIR}/`.
- Klasy testowe dziedziczą po `unittest.TestCase`, a zestaw uruchamiaj przez `poetry run pytest`.
- Zapewnij pokrycie testami każdej nowej funkcjonalności.
- Uruchamiaj testy przed commitem: `poetry run pytest`
- Sprawdzaj pokrycie testami: `poetry run pytest --cov={PACKAGE_NAME}`

### Dokumentacja

<!-- Dostosuj tę sekcję do swojego projektu -->

- Główny plik dokumentacji: `README.md` (w języku angielskim)
- Dokumentacja użytkownika: `{DOCS_DIR}/` (opcjonalnie)
- Dokumentacja API: Generowana automatycznie (np. Sphinx, MkDocs)
- Przykłady użycia: `{EXAMPLES_DIR}/` lub `examples/` (opcjonalnie)

### Wzorce architektury

#### Użycie JskToolBox (jeśli dotyczy)

Projekt wykorzystuje bibliotekę `jsktoolbox` jako fundament. Kluczowe wzorce:

##### Klasy bazowe z basetool

Wszystkie klasy z modułu `jsktoolbox.basetool` to klasy bazowe dla dziedziczenia:

- **Brak własnego konstruktora** - nie wymagają wywołania `super().__init__()`
- **Dodają właściwości i metody** - rozszerzają API klas pochodnych
- **ThBaseObject dla wątków** - zawiera deklaracje wymagane dla threading.Thread
- Zamiast `class Worker(threading.Thread)` używaj: `class Worker(ThBaseObject, Thread)`

##### ReadOnlyClass - Immutable Keys

Zawsze używaj `ReadOnlyClass` dla kluczy słowników w BData:

```python
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.basetool import BData

# Wzorzec 1: Klucze wewnątrz klasy (zakres klasy)
class MyClass(BData):
    class _Keys(object, metaclass=ReadOnlyClass):
        DATA: str = "data"

# Wzorzec 2: Klucze na poziomie modułu (współdzielone w module)
class _Keys(object, metaclass=ReadOnlyClass):
    CONFIG: str = "config"

# Wzorzec 3: Klucze publiczne (całe projekty)
class ProjectKeys(object, metaclass=ReadOnlyClass):
    APP_NAME: str = "app_name"
```

Zobacz dokumentację JskToolBox dla szczegółów każdego wzorca.

##### BData - Typed Storage

Klasa `BData` zapewnia bezpieczny kontener słownikowy z kontrolą typów.

**Zasady (od 2024):**

1. **Rejestracja typów w setterach**: Używaj `set_default_type` w `_set_data()`
2. **Gettery bez rejestracji typu**: `_get_data()` nie używa `set_default_type` (przestarzałe)
3. **Typ raz ustawiony jest niezmienny**: Wymagane `_delete_data()` przed zmianą typu
4. **None zachowuje typ**: `set_default_type=None` nie zmienia istniejącego typu
5. **Typy złożone**: Obsługa `Optional[T]`, `Dict[K, V]`, `List[T]`, `Union`, zagnieżdżenia

**Preferowane metody:**

```python
# ✓ Zalecane - setter rejestruje typ
self._set_data("key", 42, set_default_type=int)

# ✓ Zalecane - getter bez set_default_type
value = self._get_data("key", default_value=0)

# ✓ Aktualizacja z zachowaniem typu, typ zmiennej jest sprawdzany, rzuca TypeError przy niezgodności
self._set_data("key", 100)
```

**Typy złożone:**

```python
from typing import Optional, Dict, List

# ✓ Optional - akceptuje wartość lub None
self._set_data("key", "text", set_default_type=Optional[str])

# ✓ Dict z typami - weryfikuje klucze i wartości
self._set_data("config", {"a": 1}, set_default_type=Dict[str, int])

# ✓ List z typem - weryfikuje wszystkie elementy
self._set_data("items", ["a", "b"], set_default_type=List[str])
```

**Dodatkowe metody:**

- `_copy_data(key)` - deep copy wartości
- `_delete_data(key)` - usuwa wartość i constraint typu
- `_clear_data(key)` - usuwa wartość, zachowuje constraint

##### Lazy Imports

Biblioteka wykorzystuje leniwe importy dla lepszej wydajności. Preferowane wzorce:

```python
# ✓ Zalecane (lazy loading z __init__.py)
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient
from jsktoolbox.netaddresstool import Address, Network

# ✗ Unikaj (działa, ale dłuższa forma)
from jsktoolbox.configtool.main import Config
```

Sprawdź `__init__.py` w każdym module by poznać dostępne leniwe importy.

##### Obsługa błędów

Do zgłaszania wyjątków używaj mechanizmu `raise Raise.error()`:

```python
from inspect import currentframe
from jsktoolbox.raisetool import Raise

# ✓ Poprawnie
raise Raise.error(
    "Invalid value",
    ValueError,
    class_name=self._c_name,
    currentframe=currentframe()
)

# ✗ BŁĄD - wyjątek nie zostanie rzucony
Raise.error("Invalid value", ValueError)
```

**WAŻNE:** `Raise.error()` **tworzy** wyjątek, ale go nie rzuca - zawsze używaj słowa kluczowego `raise`.

### Ogólne zalecenia

- Odpowiadaj w języku polskim (lub języku użytkownika).
- Komentarze i dokumentację w repozytorium zapisuj po angielsku.
- Zachowuj zwięzłą, techniczną formę odpowiedzi zgodną z konwencjami projektu.
- Przy zmianach obejmujących wiele plików przedstaw plan i poproś o akceptację.
- **ZAWSZE aktualizuj dokumentację** po zmianach w kodzie.

### Checklist aktualizacji dokumentacji

**KOLEJNOŚĆ AKTUALIZACJI (OBOWIĄZKOWA):**

1. **NAJPIERW: Sprawdź i zaktualizuj docstringi** w kodzie źródłowym (EN)
2. **NASTĘPNIE: Regeneruj dokumentację API** - uruchom `make docs` lub generator dokumentacji
3. **NA KOŃCU: Zaktualizuj dokumentację Markdown** - wszystkie pliki `.md`

**ZASADA:** Jeśli polecenie nie wskazuje konkretnego modułu lub klasy, przeprowadź aktualizację **dla całego projektu**.

**Lista plików dokumentacji:**

- [ ] **Docstringi w kodzie** (EN) - **ZAWSZE NAJPIERW**
- [ ] **Dokumentacja API** (automatyczna) - **PO DOCSTRINGACH**
- [ ] **README.md** - Główna dokumentacja projektu (EN)
- [ ] **{DOCS_DIR}/\*.md** - Dokumentacja użytkownika (jeśli istnieje)
- [ ] **CHANGELOG.md** - Historia zmian (jeśli istnieje)

### Wzorce do sprawdzenia w dokumentacji

Upewnij się że wszystkie pliki dokumentacji zawierają:

1. **ReadOnlyClass** - Trzy wzorce (inside class, module level, public) - jeśli używasz JskToolBox
2. **Raise.error()** - Zawsze z `raise` keyword - jeśli używasz JskToolBox
3. **BClasses properties** - `_c_name` i `_f_name` NIE SĄ deklarowane - jeśli używasz JskToolBox
4. **Lazy imports** - Preferowane krótkie formy - jeśli używasz JskToolBox
5. **BData methods** - Nowe zasady (2024) - jeśli używasz JskToolBox:
   - Typ rejestrowany TYLKO w `_set_data()` przez `set_default_type`
   - `_get_data()` NIE używa `set_default_type` (przestarzałe)
   - Typ raz ustawiony jest niezmienny (wymaga `_delete_data()` przed zmianą)
   - `set_default_type=None` zachowuje istniejący typ
   - **Typy złożone**: Obsługa `Optional[T]`, `Dict[K, V]`, `List[T]`, `Union`, zagnieżdżenia

## Docstring Template

Docstringi tworzymy w języku angielskim według poniższych wzorców.

### Standardy formatowania

- **Author:** Dwie spacje po dwukropku - `Author:  `
- **Created:** Format YYYY-MM-DD (ISO 8601)
- **Konsystencja:** Jednolity autor - `{AUTHOR_NAME} --<{AUTHOR_EMAIL}>`

### Module-level Docstring

```python
"""
Author:  {AUTHOR_NAME} --<{AUTHOR_EMAIL}>
Created: YYYY-MM-DD

Purpose: Short, one-line summary of the module's purpose.

[Optional: More detailed description of the module's functionality,
its components, and how they fit into the larger project.]
"""
```

**Uwaga:** Pliki `__init__.py` mogą mieć uproszczone docstringi bez pełnej struktury.

### Class-level Docstring

```python
"""Short, one-line summary of the class's purpose.

[Optional: More detailed description of the class's responsibilities,
design choices, and its role (e.g., utility, data structure).]
"""
```

### Function/Method-level Docstring

```python
"""Short, one-line summary of what the function does.

[Optional: More detailed explanation of the function's logic,
its use cases, or any important algorithms used.]

### Arguments:
* arg1: type - Description of the first argument.
* arg2: Optional[type] - Description of the second, optional argument. Defaults to DefaultValue.

### Returns:
type - Description of the returned value.
# Dla metod zwracających None (setterzy, __init__):
# Pomiń całą sekcję Returns lub: "None - <krótki opis działania>"

### Raises:
* ExceptionType: Description of the condition that causes this exception to be raised.
# Sekcja opcjonalna - tylko gdy metoda rzuca wyjątki
"""
```

**Zasady sekcji:**

- `### Arguments:` - **WYMAGANA** gdy metoda ma parametry (oprócz `self`/`cls`)
  - **WYJĄTEK:** Metody magiczne comparatory (`__lt__`, `__le__`, `__gt__`, `__ge__`, `__eq__`, `__ne__`) - sekcja NIE JEST wymagana
  - **Settery** (`set_*`, `add_*`, `update_*`, itp.) - sekcja **WYMAGANA**
- `### Returns:` - **WYMAGANA** dla getterów (`get_*`, `is_*`, `has_*`, `@property`)
- `### Returns:` - **OPCJONALNA** dla metod `-> None`, jeśli dodana: `None - opis`
- `### Raises:` - **OPCJONALNA**, tylko gdy metoda faktycznie rzuca wyjątki
- Wszystkie sekcje **bez spacji przed dwukropkiem** - `### Arguments:` nie `### Arguments :`

## Markdown Documentation Template

Szablon dla dokumentacji `.md`, z naciskiem na czytelność, kontekst i przykłady.

````markdown
# [Module Name] Module

**Source:** `[path/to/module.py]`

**[High-Level Introduction]:**
_(A user-friendly paragraph explaining what this module helps the user accomplish.)_

## Getting Started

_(Explanation of how to import and perform initial setup, if any.)_

```python
from {PACKAGE_NAME}.module import Class1, Class2
```

---

## `[ClassName]` Class

**[Class Introduction]:**
_(Description of the class's role and responsibilities.)_

### `[ClassName].[MethodName]()`

**[Detailed Description]:**
_(Full paragraph explaining the method's purpose and use cases.)_

**Signature:**

```python
[Full method signature]
```

- **Arguments:**
  - `arg1: type` - [Description]
- **Returns:**
  - `type` - [Description]
- **Raises:**
  - `ExceptionType`: [Condition]

**Usage Example:**

```python
# Clear, commented example
result = ClassName.method_name(argument="value")
print(result)
```

---
````

## Git Workflow

### Branch Naming Convention

<!-- Dostosuj do swojej konwencji -->

- `main` / `master` - produkcja
- `develop` - rozwój
- `feature/nazwa-funkcji` - nowe funkcjonalności
- `bugfix/nazwa-bledu` - poprawki błędów
- `hotfix/nazwa-poprawki` - pilne poprawki produkcyjne

### Commit Messages

Format: `<type>: <subject>`

Types:

- `feat` - nowa funkcjonalność
- `fix` - poprawka błędu
- `docs` - zmiany w dokumentacji
- `style` - formatowanie, brakujące średniki, itp.
- `refactor` - refaktoryzacja kodu
- `test` - dodanie/modyfikacja testów
- `chore` - zmiany w narzędziach, konfiguracji

Przykłady:

- `feat: add user authentication`
- `fix: correct data validation in form`
- `docs: update README with installation instructions`

## Narzędzia Development

### Poetry Commands

```bash
# Instalacja zależności
poetry install

# Dodanie nowej zależności
poetry add package-name
poetry add --group dev package-name  # dev dependency

# Aktualizacja zależności
poetry update

# Uruchomienie komend w virtualenv
poetry run python script.py
poetry run pytest
poetry run black .
```

### Formatowanie i Linting

```bash
# Formatowanie kodu
poetry run black .
poetry run black {PACKAGE_NAME}/ {TEST_DIR}/

# Sprawdzanie stylu
poetry run pycodestyle {PACKAGE_NAME}/

# Type checking (jeśli używasz mypy)
poetry run mypy {PACKAGE_NAME}/
```

### Testowanie

```bash
# Uruchomienie wszystkich testów
poetry run pytest

# Uruchomienie z pokryciem
poetry run pytest --cov={PACKAGE_NAME}

# Uruchomienie konkretnego testu
poetry run pytest {TEST_DIR}/test_module.py::TestClass::test_method

# Verbose mode
poetry run pytest -v
```

## Projekt-specyficzne zasady

<!--
SEKCJA DO DOSTOSOWANIA
======================
Dodaj tutaj specyficzne zasady i wzorce dla swojego projektu:
- Specyficzna architektura (MVC, Clean Architecture, etc.)
- Własne klasy bazowe i mixiny
- Konwencje nazewnictwa specyficzne dla domeny
- Integracje z zewnętrznymi API
- Polityki bezpieczeństwa
- etc.
-->

### Przykład: Własne wzorce

```python
# Dodaj swoje własne przykłady i wzorce tutaj
```

## Kontakt i zasoby

<!-- Dostosuj do swojego projektu -->

- **Repository:** https://github.com/username/{PROJECT_NAME}
- **Documentation:** https://username.github.io/{PROJECT_NAME}
- **Issue Tracker:** https://github.com/username/{PROJECT_NAME}/issues
- **Maintainer:** {AUTHOR_NAME} <{AUTHOR_EMAIL}>

## Changelog

<!-- Prowadź historię zmian w tym pliku konfiguracyjnym -->

### 2024-XX-XX

- Initial configuration based on AGENTS-PYTEMPLATE.md

---

**Wersja szablonu:** 1.0.0  
**Data utworzenia:** 2024-XX-XX  
**Bazuje na:** JskToolBox AGENTS.md best practices
