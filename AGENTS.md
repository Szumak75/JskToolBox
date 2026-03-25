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

- `language`: `Python 3.10-3.13` (fully compatible)
- `project_management`: Projekt używa Poetry. Uruchamiaj narzędzia poprzez `poetry run <polecenie>` (np. `poetry run pytest`).

**Python 3.13 Compatibility:** Projekt jest w pełni kompatybilny z Python 3.13, który wprowadził zmiany w module `threading` (`_thread._ThreadHandle` zamiast `LockType` dla thread handles). Kompatybilność wsteczna z Python 3.10-3.12 jest zachowana.

### Styl kodowania

- Formatuj kod przy użyciu `black`; po zmianach wykonaj `poetry run black .`.
- Pliki Markdown formatuj przy użyciu `prettier`; uruchamiaj `poetry run prettier --write <ścieżka>`.
- Przestrzegaj PEP 8 i waliduj styl poleceniem `poetry run pycodestyle`.
- Dodawaj adnotacje typów do nowych funkcji, metod, właściwości i stałych klasowych.
- Preferuj pojedyncze cudzysłowy, chyba że podwójne są wymagane.

#### Struktura klas

**Wymagania bezwzględne:**

1. Kod klasy musi być podzielony na sekcje oddzielone separatorami.
2. Separator musi mieć format `# #[SECTION NAME]#####...` i długość `80` znaków.
3. Metody i właściwości w każdej sekcji muszą być posortowane alfabetycznie.
4. Wszystkie metody i właściwości muszą posiadać pełne typowanie.

**Wymagana kolejność sekcji:**

1. `CONSTANTS`
2. `CONSTRUCTOR`
3. `PUBLIC PROPERTIES`
4. `PROTECTED PROPERTIES`
5. `PRIVATE PROPERTIES`
6. `PUBLIC METHODS`
7. `PROTECTED METHODS`
8. `PRIVATE METHODS`
9. `STATIC/CLASS METHODS`
10. `EOF`

**Doprecyzowanie `EOF`:**

- `EOF` oznacza wyłącznie ostatnią linię pliku modułu.
- Nie dodawaj sekcji `EOF` na końcu każdej klasy.
- W pliku może istnieć tylko jeden znacznik `# #[EOF]...` i powinien znajdować się na końcu modułu.

**Przykład separatora:**

```python
# #[PUBLIC METHODS]####################################################################
```

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

### Wersjonowanie projektu

Projekt stosuje Semantic Versioning w formacie `X.Y.Z` (`MAJOR.MINOR.PATCH`).

**Wymagania bezwzględne:**

1. Zmiany w kodzie projektu wymagają aktualizacji wersji zgodnie z Semantic Versioning.
2. Zmiany obejmujące wyłącznie dokumentację projektową lub developerską nie wymagają zmiany wersji.
3. Przy zwiększeniu `Y` (`MINOR`) należy zresetować `Z` do `0`.
4. Przy zwiększeniu `X` (`MAJOR`) należy zresetować `Y` i `Z` do `0`.

**Znaczenie numerów wersji:**

- `X` (`MAJOR`) - breaking changes, incompatible API changes.
- `Y` (`MINOR`) - new features, backward-compatible additions.
- `Z` (`PATCH`) - bug fixes, small improvements, refactoring.

**Przykłady:**

```text
Current: 0.2.3
- Bug fix       -> 0.2.4
- New feature   -> 0.3.0
- Breaking API  -> 1.0.0
```

**Zmiany dokumentacyjne i pozakodowe:**

- Zmiany wyłącznie w dokumentacji projektowej, dokumentacji developerskiej, planach prac lub zasadach repozytorium nie wymagają podniesienia wersji.
- Takie zmiany nadal należy odnotować w odpowiedniej sekcji `CHANGELOG.md`.
- Jeśli zmiana łączy modyfikację kodu i dokumentacji, obowiązuje versioning wynikający ze zmiany kodu.

**Pliki do aktualizacji przy zmianie wersji:**

1. `pyproject.toml`
2. `jsktoolbox/__init__.py`

**Checklist wersjonowania:**

- [ ] Określ, czy zmiana obejmuje kod czy wyłącznie dokumentację / metadane developerskie
- [ ] Jeśli zmiana obejmuje kod: określ typ zmiany `MAJOR`, `MINOR`, `PATCH`
- [ ] Jeśli zmiana obejmuje kod: zaktualizuj obie wersje tak, aby były zgodne
- [ ] Zawsze dopisz zmianę do właściwej sekcji `CHANGELOG.md`
- [ ] Jeśli zmiana obejmuje kod: przygotuj commit message `chore: bump version to X.Y.Z`
- [ ] Jeśli zmiana obejmuje kod: przygotuj tag `git tag vX.Y.Z`

### Changelog

Plik `CHANGELOG.md` zawiera szczegółową historię zmian projektu zgodnie z Semantic Versioning, z podziałem na typy zmian i odniesieniami do commitów lub pull requestów.

**Format wpisów:**

```text
<type>: <subject>
```

**Dozwolone typy:**

- `feat` - nowa funkcjonalność
- `fix` - poprawka błędu
- `docs` - zmiany w dokumentacji
- `style` - formatowanie i podobne poprawki niesemantyczne
- `refactor` - refaktoryzacja kodu
- `test` - dodanie lub modyfikacja testów
- `chore` - zmiany w narzędziach i konfiguracji

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

Wszystkie klasy z modułu `jsktoolbox.basetool` to klasy typu mixin dla dziedziczenia. Kluczowe właściwości:

- **Brak własnego konstruktora** - nie wymagają wywołania `super().__init__()`
- **Dodają właściwości i metody** - rozszerzają API klas pochodnych
- **ThBaseObject dla wątków** - zawiera deklaracje wymagane dla threading.Thread
- Zamiast `class Worker(threading.Thread)` używaj: `class Worker(ThBaseObject, Thread)`

#### ReadOnlyClass - Immutable Keys

Celem jest minimalizacja błędów literówek w nazwach kluczy słowników `BData`. Docelowo wszystkie stałe klucze słownikowe powinny być definiowane przez `ReadOnlyClass`.

**Dobór wzorca:**

| Zasięg | Wzorzec | Nazwa klasy | Lokalizacja |
| --- | --- | --- | --- |
| Jedna klasa | `__Keys` | `__Keys` | wewnątrz klasy |
| Cały moduł | `_Keys` | `_Keys` | nagłówek modułu |
| Cały projekt | publiczna klasa `NazwaKeys` | `NazwaKeys` | dedykowany publiczny moduł z kluczami |

**Reguła decyzji:**

```text
Klucz używany tylko w jednej klasie? -> __Keys
Klucz współdzielony przez klasy w module? -> _Keys
Klucz współdzielony w całym projekcie? -> NazwaKeys w publicznym module z kluczami
```

**Wzorzec 1: Private `__Keys`**

Używaj, gdy klucze są wykorzystywane wyłącznie przez jedną klasę.

```python
from jsktoolbox.attribtool import ReadOnlyClass
from typing import Optional

class MyClass(BData):
    class __Keys(object, metaclass=ReadOnlyClass):
        COUNT: str = '__count__'
        DATA: str = '__data__'

    def __init__(self) -> None:
        self._set_data(
            key=self.__Keys.DATA,
            value=None,
            set_default_type=Optional[str],
        )
```

Python stosuje tu name mangling: `self.__Keys` przechodzi do `self._NazwaKlasy__Keys`, co eliminuje przysłanianie między klasami dziedziczącymi lub mixinami.

**Wzorzec 2: Module-Level `_Keys`**

Używaj, gdy kilka klas w tym samym module współdzieli te same klucze.

```python
class _Keys(object, metaclass=ReadOnlyClass):
    CONFIG: str = '__config__'
    STATE: str = '__state__'

class ClassA(BData):
    def setup(self) -> None:
        self._set_data(key=_Keys.CONFIG, value={}, set_default_type=dict)

class ClassB(BData):
    def get_state(self) -> Optional[str]:
        return self._get_data(key=_Keys.STATE)
```

**Wzorzec 3: Project-Wide `NazwaKeys`**

Używaj, gdy klucze są współdzielone celowo w całym projekcie. Lokalizacja nie jest sztywna: zwykle umieszcza się je w katalogu modułu, którego dotyczą, w `keys.py` lub w kilku plikach `*_keys.py`. Jeśli w projekcie istnieje jeden wspólny publiczny moduł kluczy, powinien być łatwo dostępny bez szukania.

```python
class ResponseDbQueryStatusKeys(object, metaclass=ReadOnlyClass):
    ERROR: str = 'error'
    OK: str = 'ok'
```

Zobacz `EXAMPLES_FOR_AI.md` dla szczegółów każdego wzorca.

#### BData - Typed Storage

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
self._set_data("key", 42, set_default_type=int)  # Rejestruje typ int

# ✓ Zalecane - getter bez set_default_type
value = self._get_data("key", default_value=0)

# ✓ Aktualizacja z zachowaniem typu, wcześniej zarejestrowany typ jest sprawdzany i rzuca TypeError przy niezgodności
self._set_data("key", 100)  # Zachowuje typ int

# ✗ Przestarzałe - _get_data z set_default_type
value = self._get_data("key", set_default_type=int, default_value=0)  # DeprecationWarning

# ✗ Możliwe, ale bez kontroli typów
self._set_data("key2", 7, set_default_type=None)  # Nie rejestruje typu, nie używa kontroli typu aż do momentu zmiany tej decyzji dla klucza "key2" w kolejnym przypisaniu

# ✗ Możliwe, ale bez kontroli typów
value = self._data["key"]
self._data["key"] = 42
```

**Typy złożone (nowość 2024):**

```python
from typing import Optional, Dict, List

# ✓ Optional - akceptuje wartość lub None
self._set_data("key", "text", set_default_type=Optional[str])
self._set_data("key", None, set_default_type=None)  # Valid

# ✓ Dict z typami - weryfikuje klucze i wartości
self._set_data("config", {"a": 1, "b": 2}, set_default_type=Dict[str, int])

# ✓ List z typem - weryfikuje wszystkie elementy
self._set_data("items", ["a", "b"], set_default_type=List[str])

# ✓ Zagnieżdżone typy - rekursywna walidacja
self._set_data("data", [{"a": 1}], set_default_type=List[Dict[str, int]])

# ✓ Optional List - lista lub None
self._set_data("maybe", ["x"], set_default_type=Optional[List[str]])
self._set_data("maybe", None, set_default_type=None)  # Valid
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

**Obsługa `Optional[T]` w getterach:**

`_get_data(key)` semantycznie zwraca `Optional[T]`. Jeśli getter ma zwracać ścisły typ `T`, należy jawnie obsłużyć `None`.

```python
from inspect import currentframe
from typing import Optional

@property
def my_property(self) -> int:
    value: Optional[int] = self._get_data(key=self._Keys.MY_KEY)
    if value is None:
        raise Raise.error(
            'Value for MY_KEY is None',
            ValueError,
            self._c_name,
            currentframe(),
        )
    return value
```

Można również użyć `default_value`, jeśli logika inicjalizacji tego wymaga.

```python
from typing import Optional

@property
def my_property(self) -> str:
    value: Optional[str] = self._get_data(
        key=self._Keys.MY_KEY,
        default_value='abc',
    )
    if value is None:
        return ''
    return value
```

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
- [ ] **CHANGELOG.md** - Historia zmian projektu
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
   - **Typy złożone**: Obsługa `Optional[T]`, `Dict[K, V]`, `List[T]`, `Union`, zagnieżdżenia (2024)
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
