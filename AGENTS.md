# Konfiguracja Gemini dla projektu JskToolBox

## Konfiguracja plików

Uwzględnij tylko pliki źródłowe Python i testy.

**files.include**

- `jsktoolbox/**/*.py`
- `tests/**/*.py`

Wyklucz katalogi wirtualnego środowiska, pamięć podręczną i inne pliki pomocnicze.

**files.exclude**

- `.venv/**`
- `.pytest_cache/**`
- `__pycache__/**`
- `dist/**`
- `*.egg-info/**`
- `examples/**`
- `examples/**/*`

## Instrukcje dotyczące zachowania

Sekcje poniżej opisują preferowane ustawienia dla agentów Gemini, Copilot, Codex i innych.

### Język i zarządzanie projektem

- `language`: `Python 3.10+`
- `project_management`: Projekt używa Poetry. Uruchamiaj narzędzia poprzez `poetry run <polecenie>` (np. `poetry run pytest`).

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
- **Konsystencja** - jednolity autor we wszystkich modułach: `Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>`

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

- Testy znajdują się w katalogu `tests/`.
- Klasy testowe dziedziczą po `unittest.TestCase`, a zestaw uruchamiaj przez `poetry run pytest`.
- Zapewnij pokrycie testami każdej nowej funkcjonalności.

### Dokumentacja API

- Pełna dokumentacja API jest generowana automatycznie za pomocą Sphinx.
- Przed rozpoczęciem pracy z biblioteką zawsze generuj świeżą dokumentację: `make docs` lub `poetry run python generate_docs.py`.
- Dostępne pliki dokumentacji:
  - `docs_api/build/html/index.html` - Kompletna dokumentacja HTML API
  - `api_structure.json` - Struktura API w formacie JSON (do parsowania)
  - `API_INDEX.md` - Szybki indeks modułów z przykładami importów
  - `PREFERRED_IMPORTS.md` - Mapa leniwych importów (preferowane wzorce)
  - `AI_AGENT_GUIDE.md` - Przewodnik integracji dla agentów AI
  - `EXAMPLES_FOR_AI.md` - Kompletne przykłady kodu
  - `AI_README.md` - Quick reference dla agentów AI
  - `DOKUMENTACJA_PL.md` - Instrukcja w języku polskim

### Wzorce architektury

#### Klasy bazowe z basetool

Wszystkie klasy z modułu `jsktoolbox.basetool` to klasy bazowe dla dziedziczenia. Kluczowe właściwości:

- **Brak własnego konstruktora** - nie wymagają wywołania `super().__init__()`
- **Dodają właściwości i metody** - rozszerzają API klas pochodnych
- **ThBaseObject dla wątków** - zawiera deklaracje wymagane dla threading.Thread
- Zamiast `class Worker(threading.Thread)` używaj: `class Worker(ThBaseObject, Thread)`

#### ReadOnlyClass - Immutable Keys

Zawsze używaj `ReadOnlyClass` dla kluczy słowników w BData:

```python
from jsktoolbox.attribtool import ReadOnlyClass

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

Zobacz `EXAMPLES_FOR_AI.md` dla szczegółów każdego wzorca.

#### BData - Typed Storage

Klasa `BData` zapewnia bezpieczny kontener słownikowy z kontrolą typów.

**Zasady (od 2024):**

1. **Rejestracja typów w setterach**: Używaj `set_default_type` w `_set_data()`
2. **Gettery bez rejestracji typu**: `_get_data()` nie używa `set_default_type` (przestarzałe)
3. **Typ raz ustawiony jest niezmienny**: Wymagane `_delete_data()` przed zmianą typu
4. **None zachowuje typ**: `set_default_type=None` nie zmienia istniejącego typu

**Preferowane metody:**

```python
# ✓ Zalecane - setter rejestruje typ
self._set_data("key", 42, set_default_type=int)  # Rejestruje typ int

# ✓ Zalecane - getter bez set_default_type
value = self._get_data("key", default_value=0)

# ✓ Aktualizacja z zachowaniem typu
self._set_data("key", 100, set_default_type=None)  # Zachowuje typ int

# ✗ Przestarzałe - _get_data z set_default_type
value = self._get_data("key", set_default_type=int, default_value=0)  # DeprecationWarning

# ✗ Możliwe, ale bez kontroli typów
value = self._data["key"]
self._data["key"] = 42
```

**Zmiana typu:**

```python
# ✗ BŁĄD - nie można zmienić typu bez usunięcia
self._set_data("key", "text", set_default_type=str)  # TypeError!

# ✓ Poprawnie - najpierw usuń, potem ustaw nowy typ
self._delete_data("key")  # Usuwa wartość I typ
self._set_data("key", "text", set_default_type=str)  # Nowy typ
```

**Dodatkowe metody:**

- `_copy_data(key)` - deep copy wartości
- `_delete_data(key)` - usuwa wartość i constraint typu
- `_clear_data(key)` - usuwa wartość, zachowuje constraint

#### Lazy Imports

Biblioteka wykorzystuje leniwe importy dla lepszej wydajności. Preferowane wzorce:

```python
# ✓ Zalecane (lazy loading z __init__.py)
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient
from jsktoolbox.netaddresstool import Address, Network

# ✗ Unikaj (działa, ale dłuższa forma)
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient
```

Sprawdź `__init__.py` w każdym module by poznać dostępne leniwe importy.

#### netaddresstool - Rozróżnienie IPv4/IPv6

Moduł rozróżnia klasy dla IPv4 i IPv6 z suffixem '6':

```python
# IPv4
from jsktoolbox.netaddresstool import Address, Netmask, Network

# IPv6 - z suffixem '6'
from jsktoolbox.netaddresstool import Address6, Prefix6, Network6

# ✗ BŁĄD - Address nie obsługuje IPv6
addr = Address("2001:db8::1/64")  # ValueError!

# ✗ BŁĄD - Address6 nie obsługuje prefiksu w adresie
addr = Address6("2001:db8::1/64")  # ValueError!

# ✓ Poprawnie - pojedynczy adres IPv6 bez prefiksu
addr = Address6("2001:db8::1")

# ✓ Poprawnie - sieć IPv6 z prefiksem
net = Network6("2001:db8::/64")
```

#### BClasses - Automatyczne właściwości

- `_c_name` - automatyczna property zwracająca `self.__class__.__name__`
- `_f_name` - automatyczna property zwracająca nazwę bieżącej metody
- **Nie deklaruj ich** jako zmiennych klasowych - przykryjesz automatykę

### Obsługa błędów

- Do zgłaszania wyjątków używaj mechanizmu `raise Raise.error(message, exception_type, class_name, frame)`.
- **WAŻNE:** `Raise.error()` **tworzy** wyjątek, ale go nie rzuca - zawsze używaj słowa kluczowego `raise`.

```python
import inspect
from jsktoolbox.raisetool import Raise

# ✓ Poprawnie
raise Raise.error(
    "Invalid value",
    ValueError,
    class_name=self._c_name,
    currentframe=inspect.currentframe()
)

# ✗ BŁĄD - wyjątek nie zostanie rzucony
Raise.error("Invalid value", ValueError)
```

### Ogólne zalecenia

- Odpowiadaj w języku polskim.
- Plik konfiguracyjny AGENTS.md uzupełniaj w języku polskim.
- Komentarze i dokumentację w repozytorium zapisuj po angielsku.
- Zachowuj zwięzłą, techniczną formę odpowiedzi zgodną z konwencjami projektu.
- Przy zmianach obejmujących wiele plików przedstaw plan i poproś o akceptację.
- **ZAWSZE aktualizuj CAŁĄ dokumentację** - nie tylko jeden plik.
- Przy aktualizacji dokumentacji sprawdzaj także:
  - **README.md** - Główny plik dokumentacji projektu (EN)
  - **docs/\*.md** - Moduł-specyficzne pliki w katalogu docs (EN)

### Checklist aktualizacji dokumentacji

**KOLEJNOŚĆ AKTUALIZACJI (OBOWIĄZKOWA):**

1. **NAJPIERW: Sprawdź i zaktualizuj docstringi** w kodzie źródłowym (EN)
2. **NASTĘPNIE: Regeneruj dokumentację API** - uruchom `make docs`
3. **NA KOŃCU: Zaktualizuj dokumentację Markdown** - wszystkie pliki `.md`

**ZASADA:** Jeśli polecenie nie wskazuje konkretnego modułu lub klasy, przeprowadź aktualizację **dla całego projektu**.

**Lista plików dokumentacji:**

- [ ] **Docstringi w kodzie** (EN) - **ZAWSZE NAJPIERW**
- [ ] **Dokumentacja API** (`make docs`) - **PO DOCSTRINGACH**
- [ ] **EXAMPLES_FOR_AI.md** - Przykłady kodu (EN)
- [ ] **AI_AGENT_GUIDE.md** - Przewodnik architektoniczny (EN)
- [ ] **AI_README.md** - Quick reference (EN)
- [ ] **DOKUMENTACJA_PL.md** - Instrukcja użytkowania (PL)
- [ ] **AGENTS.md** - Konfiguracja i ustalenia (PL)
- [ ] **README.md** - Główna dokumentacja projektu (EN)
- [ ] **docs/\*.md** - Dokumentacja modułów w katalogu docs (EN)
- [ ] **PREFERRED_IMPORTS.md** - Jeśli dodano nowe lenive importy

### Wzorce do sprawdzenia w dokumentacji

Upewnij się że wszystkie pliki dokumentacji zawierają:

1. **ReadOnlyClass** - Trzy wzorce (inside class, module level, public)
2. **Raise.error()** - Zawsze z `raise` keyword
3. **BClasses properties** - `_c_name` i `_f_name` NIE SĄ deklarowane
4. **Lazy imports** - Preferowane krótkie formy
5. **BData methods** - Nowe zasady (2024):
   - Typ rejestrowany TYLKO w `_set_data()` przez `set_default_type`
   - `_get_data()` NIE używa `set_default_type` (przestarzałe)
   - Typ raz ustawiony jest niezmienny (wymaga `_delete_data()` przed zmianą)
   - `set_default_type=None` zachowuje istniejący typ
6. **netaddresstool** - Rozróżnienie Address/Network i IPv4/IPv6

## Docstring Template

Docstringi tworzymy w języku angielskim według poniższych wzorców.

### Standardy formatowania

- **Author:** Dwie spacje po dwukropku - `Author:  `
- **Created:** Format YYYY-MM-DD (ISO 8601)
- **Konsystencja:** Jednolity autor - `Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>`

### Module-level Docstring

```python
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
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
_(A user-friendly paragraph explaining what this module helps the user accomplish. Focus on the "why" and the benefits, not just the technical function.)_

## Getting Started

_(Explanation of how to import and perform initial setup, if any.)_

```python
from [module_path] import [Class1, Class2]
```

---

## `[ClassName]` Class

**[Class Introduction]:**
_(A more detailed description of the class's role and responsibilities. Explain how its methods work together to provide a cohesive functionality.)_

### `[ClassName].[MethodName]()`

**[Detailed Description]:**
_(A full paragraph explaining the method's purpose, its specific behavior, and common use cases. This should be more descriptive than the docstring summary, focusing on practical application and scenarios.)_

**Signature:**

```python
[Full method signature]
```

- **Arguments:**
  - `arg1: type` - [Description of argument 1.]
- **Returns:**
  - `type` - [Description of the return value.]
- **Raises:**
  - `ExceptionType`: [Condition for raising.]

**Usage Example:**
_(A clear, well-commented code block demonstrating how to use the method effectively in a realistic scenario.)_

```python
# A clear and commented code example
result = ClassName.method_name(argument="value")
print(result)
```

---

_(Repeat for all public methods and classes)_
````
