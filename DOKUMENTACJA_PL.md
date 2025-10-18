# Dokumentacja JskToolBox - Instrukcja w języku polskim

## Przegląd

JskToolBox to biblioteka Python zawierająca zestawy klas pomocniczych do różnych operacji. Projekt zawiera kompletną dokumentację API zoptymalizowaną dla agentów AI.

**Ważne**: Biblioteka używa **leniwych importów** dla wydajności. Zawsze używaj preferowanej, krótszej składni:

```python
# ✓ PREFEROWANE (leniwe ładowanie)
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerClient

# ✗ UNIKAJ (działa ale dłuższe)
from jsktoolbox.configtool.main import Config
from jsktoolbox.logstool.logs import LoggerClient
```

Zobacz `PREFERRED_IMPORTS.md` dla pełnej listy leniwych importów.

## Szybki start

### Instalacja zależności

```bash
poetry install
```

### Generowanie dokumentacji

```bash
# Najprostszy sposób - używając Make
make docs

# Lub bezpośrednio
poetry run python generate_docs.py

# Otwórz dokumentację w przeglądarce
make docs-open
```

## Wygenerowane pliki dokumentacji

Po uruchomieniu `make docs` otrzymujesz:

### 1. Dokumentacja HTML (Sphinx)
- **Lokalizacja**: `docs_api/build/html/index.html`
- **Przeznaczenie**: Pełna dokumentacja API z cross-referencingiem
- **Dla kogo**: Programiści, agenty AI potrzebujące szczegółów

### 2. JSON API Structure
- **Lokalizacja**: `api_structure.json`
- **Przeznaczenie**: Struktura API w formacie JSON do parsowania
- **Dla kogo**: Agenty AI, narzędzia automatyzujące

### 3. Markdown Index
- **Lokalizacja**: `API_INDEX.md`
- **Przeznaczenie**: Szybki indeks modułów z przykładami importów
- **Dla kogo**: Szybkie odniesienie, quick reference

### 4. Przewodnik dla agentów AI
- **Lokalizacja**: `AI_AGENT_GUIDE.md`
- **Przeznaczenie**: Szczegółowy przewodnik integracji
- **Dla kogo**: Agenty AI rozpoczynające pracę z biblioteką

### 5. Przykłady kodu
- **Lokalizacja**: `EXAMPLES_FOR_AI.md`
- **Przeznaczenie**: Kompletne przykłady użycia
- **Dla kogo**: Nauka wzorców programowania

### 6. Szybki przewodnik
- **Lokalizacja**: `AI_README.md`
- **Przeznaczenie**: Quick reference dla agentów AI
- **Dla kogo**: Szybki dostęp do najważniejszych informacji

### 7. Mapa leniwych importów
- **Lokalizacja**: `PREFERRED_IMPORTS.md`
- **Przeznaczenie**: Preferowane składnie importów
- **Dla kogo**: Programiści, agenty AI szukające najlepszych praktyk

## Kluczowe ustalenia architektury

### ReadOnlyClass - Wzorce immutable keys

**Zawsze używaj** `ReadOnlyClass` dla kluczy słowników w BData:

```python
from jsktoolbox.attribtool import ReadOnlyClass

# Wzorzec 1: Klucze w klasie (zakres klasy)
class MyClass(BData):
    class _Keys(object, metaclass=ReadOnlyClass):
        DATA: str = "data"

# Wzorzec 2: Klucze na poziomie modułu (współdzielone)
class _Keys(object, metaclass=ReadOnlyClass):
    CONFIG: str = "config"

# Wzorzec 3: Klucze publiczne (cały projekt)
class ProjectKeys(object, metaclass=ReadOnlyClass):
    APP_NAME: str = "app_name"
```

**Dlaczego?** Zapobiega przypadkowej modyfikacji kluczy.

### BClasses - Automatyczne właściwości

**NIE DEKLARUJ** tych właściwości - są automatyczne:
- `_c_name` - zwraca `self.__class__.__name__` automatycznie
- `_f_name` - zwraca nazwę bieżącej metody

```python
class MyClass(BData):
    # ✗ BŁĄD - przykrywa automatyczną property
    # _c_name: str = "MyClass"
    
    def method(self):
        # ✓ POPRAWNIE - używa automatycznej property
        print(f"Class: {self._c_name}")  # "MyClass"
        print(f"Method: {self._f_name}")  # "method"
```

### Raise.error() - Prawidłowe użycie

**WAŻNE**: `Raise.error()` **tworzy** wyjątek ale go NIE RZUCA!

```python
from jsktoolbox.raisetool import Raise
from inspect import currentframe

# ✓ POPRAWNIE - z 'raise'
raise Raise.error(
    "Error message",
    ValueError,
    self.__class__.__name__,
    currentframe()
)

# ✗ BŁĄD - bez 'raise' nie rzuci wyjątku
Raise.error("Error message", ValueError, ...)  # Tylko tworzy, nie rzuca!
```

### BData - Metody dostępu

**Preferuj metody** zamiast bezpośredniego dostępu:

```python
# ✓ PREFEROWANE - z kontrolą typów
self._set_data(key=self._Keys.DATA, value="test", set_default_type=str)
value = self._get_data(key=self._Keys.DATA, set_default_type=str)

# ✗ DZIAŁA ALE BEZ KONTROLI TYPÓW
self._data[self._Keys.DATA] = "test"  # Brak walidacji typu
```

### netaddresstool - Poprawne API

**Rozróżniaj** klasy dla IPv4 i IPv6:

```python
# IPv4
from jsktoolbox.netaddresstool import Address, Network

addr = Address("192.168.1.100")       # Pojedynczy adres
net = Network("192.168.1.0/24")       # Sieć z maską

# IPv6
from jsktoolbox.netaddresstool import Address6, Network6

addr6 = Address6("2001:db8::1")      # Pojedynczy adres IPv6
net6 = Network6("2001:db8::/64")     # Sieć IPv6 z prefiksem
```

### Threading - Architektura

```python
import threading
from jsktoolbox.basetool import ThBaseObject
from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass

class MyThread(threading.Thread, ThBaseObject, NoDynamicAttributes):
    # _c_name jest automatyczne - NIE DEKLARUJ!
    
    class _Keys(object, metaclass=ReadOnlyClass):
        DATA: str = "data"
    
    def __init__(self):
        # Używa automatycznej property _c_name
        threading.Thread.__init__(self, name=self._c_name)
        self._stop_event = threading.Event()
        
        # BData storage z immutable keys
        self._set_data(
            key=self._Keys.DATA,
            value="initial",
            set_default_type=str
        )
```

## Struktura projektu

```
JskToolBox/
├── jsktoolbox/              # Kod źródłowy biblioteki
│   ├── attribtool/
│   ├── basetool/
│   ├── configtool/
│   └── ...
├── tests/                   # Testy jednostkowe
├── docs/                    # Dokumentacja markdown modułów
├── docs_api/                # Dokumentacja Sphinx API
│   ├── source/             # Źródła dokumentacji
│   └── build/              # Wygenerowana dokumentacja
├── examples/                # Przykłady użycia
├── generate_docs.py         # Skrypt generujący dokumentację
├── Makefile                 # Polecenia make
├── AI_AGENT_GUIDE.md       # Przewodnik dla AI
├── EXAMPLES_FOR_AI.md      # Przykłady dla AI
├── AI_README.md            # Quick reference dla AI
└── pyproject.toml          # Konfiguracja projektu
```

## Dostępne polecenia Make

```bash
make help           # Wyświetl pomoc
make docs           # Wygeneruj całą dokumentację
make docs-clean     # Usuń wygenerowaną dokumentację
make docs-open      # Generuj i otwórz w przeglądarce
make test           # Uruchom testy
make lint           # Uruchom lintery
make format         # Formatuj kod (black)
make install        # Zainstaluj zależności
```

## Dla agentów AI

### Priorytet konsultacji dokumentacji

Gdy agent AI pracuje z biblioteką, powinien konsultować dokumentację w tej kolejności:

1. **`API_INDEX.md`** - Znalezienie modułu i składni importu
2. **`AI_AGENT_GUIDE.md`** - Zrozumienie architektury
3. **`EXAMPLES_FOR_AI.md`** - Zobaczenie wzorców użycia
4. **`docs_api/build/html/`** - Pełna dokumentacja API
5. **`api_structure.json`** - Programatyczny dostęp do struktury

### Typowe zadania

| Zadanie | Plik dokumentacji |
|---------|-------------------|
| Szukam modułu do obsługi logowania | `API_INDEX.md` → logstool |
| Jak używać konfiguracji? | `EXAMPLES_FOR_AI.md` → Configuration Management |
| Jakie parametry ma funkcja X? | `docs_api/build/html/` → Moduł → Funkcja |
| Jak stworzyć wątek? | `EXAMPLES_FOR_AI.md` → Threading |
| Pełny przykład aplikacji | `EXAMPLES_FOR_AI.md` → Complete Application |

## Regeneracja dokumentacji

Po zmianach w kodzie źródłowym:

```bash
# Wyczyść starą dokumentację
make docs-clean

# Wygeneruj nową
make docs

# Sprawdź w przeglądarce
make docs-open
```

## Integracja z venv

Jeśli agent AI pracuje w środowisku venv:

```bash
# Aktywuj venv
source .venv/bin/activate

# Zainstaluj bibliotekę w trybie edycji
pip install -e .

# Wygeneruj dokumentację
python generate_docs.py

# Biblioteka jest teraz dostępna w środowisku
python -c "from jsktoolbox.configtool.main import Config; print(Config)"
```

## Przykład użycia dla agenta AI

```python
# 1. Agent AI sprawdza API_INDEX.md i znajduje moduł configtool
# 2. Agent konsultuje EXAMPLES_FOR_AI.md dla przykładów
# 3. Agent implementuje kod zgodnie z ustaleniami:

# ✓ PREFEROWANE: Leniwe importy
from jsktoolbox.configtool import Config
from jsktoolbox.logstool import LoggerQueue, LoggerClient
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.basetool import BData
from inspect import currentframe

# Definiuj immutable keys
class _Keys(object, metaclass=ReadOnlyClass):
    """Immutable keys for application."""
    DB_HOST: str = "db_host"

class MyApp(BData):
    def __init__(self):
        # Setup
        config = Config(app_name="MyApp", config_name="settings")
        log_queue = LoggerQueue()
        logger = LoggerClient(log_queue)
        
        # BData z immutable keys
        self._set_data(
            key=_Keys.DB_HOST,
            value="localhost",
            set_default_type=str
        )
        
        # Logging
        logger.info("Application started")
        
        # Config
        config.set("Database", "host", "localhost")
        config.save()
    
    def process(self):
        try:
            # Your logic
            pass
        except Exception as ex:
            # ✓ POPRAWNIE: z 'raise'
            raise Raise.error(
                f"Processing failed: {ex}",
                RuntimeError,
                self._c_name,  # Automatyczna property!
                currentframe()
            )
```

## Wskazówki dla agentów AI

### ✓ Dobre praktyki

- Zawsze używaj **leniwych importów** (np. `from jsktoolbox.configtool import Config`)
- Używaj **ReadOnlyClass** dla kluczy słowników
- **NIE DEKLARUJ** `_c_name` ani `_f_name` - są automatyczne
- Używaj **`raise Raise.error(...)`** - nie samego `Raise.error(...)`
- Stosuj **BData metody** (`_set_data`, `_get_data`) zamiast `_data[]`
- Używaj **type hints**
- Konsultuj dokumentację przed użyciem
- **Aktualizuj CAŁĄ dokumentację** przy zmianach (EN i PL)

### ✗ Unikaj

- Importów `from jsktoolbox import *`
- Modyfikacji chronionych atrybutów `_data` bezpośrednio
- Pomijania generowania dokumentacji przed pracą
- Deklarowania `_c_name` jako zmiennej klasowej
- Używania `Raise.error()` bez `raise`
- Mylenia `Address` z `Network` (IPv4)
- Mylenia `Address6` z `Network6` (IPv6)
- Kluczy bez `ReadOnlyClass`

### Checklist przed commitowaniem zmian

- [ ] Kod sformatowany (`make format`)
- [ ] Testy przechodzą (`make test`)
- [ ] Dokumentacja wygenerowana (`make docs`)
- [ ] **EXAMPLES_FOR_AI.md** zaktualizowane
- [ ] **AI_AGENT_GUIDE.md** zaktualizowane
- [ ] **AI_README.md** zaktualizowane
- [ ] **DOKUMENTACJA_PL.md** zaktualizowane
- [ ] **AGENTS.md** zaktualizowane
- [ ] Type hints dodane
- [ ] Docstringi w języku angielskim
- [ ] Użyto wzorców z ustaleń (ReadOnlyClass, Raise, etc.)

## Publikacja dokumentacji

### Read the Docs

Projekt zawiera plik `.readthedocs.yaml` gotowy do użycia z Read the Docs.

**Konfiguracja** (używa Poetry):
```yaml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.10"
  jobs:
    pre_install:
      - pip install poetry
    post_install:
      - poetry install --with dev
```

**Instalacja na Read the Docs**:
1. Załóż konto na https://readthedocs.org/
2. Importuj projekt JskToolBox
3. Dokumentacja zbuduje się automatycznie
4. Dostępna pod: `jsktoolbox.readthedocs.io`

**Zalety**:
- Automatyczne budowanie z każdym push do main
- Generuje HTML, PDF i EPUB
- Wsparcie dla wielu wersji
- Darmowe dla projektów open source

### GitHub Pages

```bash
# Wygeneruj dokumentację
make docs

# Skopiuj do katalogu gh-pages
cp -r docs_api/build/html/* /path/to/gh-pages/

# Commit i push do gh-pages branch
```

## Rozwiązywanie problemów

### Problem: Import Error przy generowaniu dokumentacji lokalnie

**Rozwiązanie**: Sprawdź `docs_api/source/conf.py` - ścieżka do projektu powinna być poprawna.

### Problem: Read the Docs - "No module named 'sphinx_autodoc_typehints'"

**Rozwiązanie**: Plik `.readthedocs.yaml` musi używać Poetry do instalacji zależności:
```yaml
build:
  jobs:
    pre_install:
      - pip install poetry
    post_install:
      - poetry install --with dev
```

**Weryfikacja**:
- Sprawdź czy `sphinx-autodoc-typehints` jest w `[tool.poetry.group.dev.dependencies]`
- Read the Docs automatycznie zainstaluje wszystkie zależności z Poetry

### Problem: Brakujące moduły w dokumentacji

**Rozwiązanie**: Sprawdź czy moduł ma docstring i czy jest dodany do `docs_api/source/index.rst`.

### Problem: Warnings podczas budowania

**Rozwiązanie**: Większość ostrzeżeń związana z docstringami nie przeszkadza w generowaniu. Sprawdź składnię docstringów jeśli chcesz je naprawić.

## Wsparcie

- **Repository**: https://github.com/Szumak75/JskToolBox
- **Issues**: Zgłaszaj problemy na GitHub
- **Documentation**: Zobacz wygenerowaną dokumentację HTML

## Licencja

MIT License - Zobacz plik LICENSE

---

**Uwaga**: Ta dokumentacja jest generowana automatycznie z kodu źródłowego. Zawsze regeneruj dokumentację po aktualizacji biblioteki.
