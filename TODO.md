# Project Modules

- ~~Projekt wymaga Python 3.10-3.12 - Python 3.13 zmienił threading.Thread i ma problemy z NoDynamicAttributes, sprawdzić i rozwiązać~~ ✅ ZAKOŃCZONO (2024-10-19)
  - Python 3.13 zmienił typ `threading.Thread._handle` z `LockType` na `_thread._ThreadHandle`
  - Dodano kompatybilność wsteczną z Python 3.10-3.12 w `jsktoolbox/basetool/threads.py`
  - Użyto `Union[_thread._ThreadHandle, LockType, None]` dla Python 3.13+
  - Testy przechodzą na Python 3.13.9
- ~~BData.\_get_data i \_set_data - przemyśleć strategię set_default_type~~ ✅ ZAKOŃCZONO (2024-10-19)
- ~~BData.\_get_data i \_set_data - rozwiązać problem użycia set_default_type = Optional[type]~~ ✅ ZAKOŃCZONO (2024-10-19)

## Python 3.13 Compatibility

**STATUS:** ✅ ZAKOŃCZONO (Aktualizacja 2024-10-19)

**Problem:**

Python 3.13 wprowadził breaking change w module `threading`:

- `threading.Thread._handle` zmienił typ z `_thread.LockType` na `_thread._ThreadHandle`
- Powodowało to problemy z type hints w `jsktoolbox/basetool/threads.py`
- NoDynamicAttributes działało poprawnie, problem był tylko w typowaniu

**Rozwiązanie:**

- [x] **Dodano kompatybilność wsteczną dla Python 3.10-3.13** ✅
  - Wykrywanie wersji Python przez `sys.version_info`
  - Dla Python 3.13+: `Union[_thread._ThreadHandle, LockType, None]`
  - Dla Python 3.10-3.12: `Optional[LockType]`
  - Użycie `ThreadHandleType` jako aliasu typu
- [x] **Zaktualizowano property `_handle` w ThBaseObject** ✅
  - Type hint używa `ThreadHandleType`
  - Setter akceptuje `Any` dla maksymalnej kompatybilności
  - Dodano notatki w docstringach o różnicach między wersjami
- [x] **Testy** ✅
  - Przetestowano na Python 3.13.9 - ✓ działa
  - Przetestowano na Python 3.12.12 (venv) - ✓ działa
  - ThLoggerProcessor działa poprawnie z nowym typowaniem
  - NoDynamicAttributes działa poprawnie

**Kompatybilność:**

Projekt teraz obsługuje **Python 3.10, 3.11, 3.12 i 3.13** ✅

**Pliki zmienione:**

- `jsktoolbox/basetool/threads.py` - dodano kompatybilność typów dla \_handle

## BData Enhancements

**STATUS:** ✅ ZAKOŃCZONO (Aktualizacja 2024-10-19)

**Ukończone (✓):**

- [x] **Refaktoryzacja set_default_type w BData** ✅
  - set_default_type tylko w \_set_data() (nie w \_get_data())
  - Typ raz ustawiony jest niezmienny (wymaga \_delete_data())
  - set_default_type=None zachowuje istniejący typ
  - Kompatybilność wsteczna z deprecation warning
- [x] **Obsługa typów złożonych w BData** ✅
  - Dodano metodę \_\_validate_type() z obsługą typing module
  - Optional[T], Dict[K, V], List[T], Union[T1, T2]
  - Zagnieżdżone typy: Optional[List[Dict[str, int]]]
  - Rekursywna walidacja wszystkich poziomów
- [x] **Testy dla nowej funkcjonalności** ✅
  - 7 nowych testów dla typów złożonych
  - Wszystkie testy przechodzą (42/42)
- [x] **Dokumentacja** ✅
  - Zaktualizowano EXAMPLES_FOR_AI.md
  - Zaktualizowano AI_AGENT_GUIDE.md
  - Zaktualizowano AGENTS.md
  - Zregenerowano dokumentację API

## AGENTS Configuration Template

**STATUS:** ✅ ZAKOŃCZONO (Aktualizacja 2024-10-19)

**Ukończone (✓):**

- [x] **AGENTS-PYTEMPLATE.md** ✅
  - Szablon konfiguracji dla nowych projektów Python
  - Zmienne do wypełnienia: PROJECT_NAME, PACKAGE_NAME, AUTHOR_NAME, etc.
  - Sekcje: konfiguracja plików, styl kodowania, testowanie, dokumentacja
  - Wzorce JskToolBox (opcjonalne dla projektów bez tej biblioteki)
  - Docstring templates, Git workflow, narzędzia development
- [x] **AGENTS-PYTEMPLATE-README.md** ✅
  - Pełna instrukcja użycia szablonu
  - Przykłady dla różnych scenariuszy
  - Wskazówki dla projektów z/bez JskToolBox
- [x] **AGENTS-PYTEMPLATE-QUICKSTART.md** ✅
  - Quick start guide z 3 metodami użycia
  - Automatyczny skrypt, ręczna zamiana, edycja w IDE
  - Przykłady dla Linux/macOS i Windows
- [x] **tools/setup-agents-config.sh** ✅
  - Interaktywny skrypt do konfiguracji
  - Automatyczna zamiana wszystkich zmiennych
  - Walidacja wymaganych pól
  - Kolorowy output z podsumowaniem

**Użycie:**

```bash
# Automatyczna konfiguracja
./tools/setup-agents-config.sh

# Lub ręcznie
cp AGENTS-PYTEMPLATE.md /path/to/project/AGENTS.md
# Zamień zmienne {PROJECT_NAME}, {PACKAGE_NAME}, etc.
```

## Documentation Standards

**STATUS:** ✅ ZAKOŃCZONO KOMPLEKSOWĄ STANDARYZACJĘ (Aktualizacja 2025-10-19 03:46)

**Ukończone (✓):**

- [x] Przeprowadzić pełny audyt docstringów w projekcie
- [x] Standaryzować format Author (dwie spacje po dwukropku)
- [x] Naprawić format Author w edmctool/logs2.py
- [x] Usunąć nieprawidłowe `### Returns: None` z konstruktorów (logstool/engines.py)
- [x] Dodać brakujące pole Purpose w devices/mikrotik/elements/**init**.py
- [x] **Dodać sekcję `### Arguments:` do wszystkich metod **init** z parametrami (47 przypadków)** ✅
- [x] **Dodać pełne docstringi do 3 metod bez dokumentacji** ✅
- [x] **Dodać sekcję `### Arguments:` do WSZYSTKICH setterów w projekcie (105 setterów)** ✅
- [x] **Dodać sekcję `### Returns:` do WSZYSTKICH getterów w projekcie (90 getterów)** ✅
- [x] Regenerować dokumentację API (Sphinx/ReadTheDocs) po zmianach w docstringach ✅
- [x] Zaktualizować dokumentację Markdown (README.md, docs/\*.md) ✅
  - Naprawiono preferowane importy (lazy loading) we wszystkich plikach docs/\*.md
  - Usunięto importy z pełnych ścieżek (ipv4/ipv6/libs) → preferowane lazy imports
  - Zaktualizowano AGENTS.md z pełną procedurą aktualizacji dokumentacji
- [x] **Ustalić i zadokumentować konwencję getterów/setterów** ✅
  - Settery (105/105) wymagają sekcji `### Arguments:`
  - Gettery (90/90) wymagają sekcji `### Returns:`
  - Standard dodany do AGENTS.md i DOCSTRING_AUDIT_REPORT.md
- [x] Zweryfikować sekcje `### Raises:` - czy wszystkie metody rzucają deklarowane wyjątki ✅

**Zadania ciągłe (maintenance):**

- [ ] Okresowa aktualizacja dokumentacji przy zmianach w kodzie
- [ ] Dodawanie docstringów do nowych metod zgodnie ze standardem
- [ ] Opcjonalnie: Dodać docstringi do ~88 prywatnych properties (priorytet niski)

**Standard obowiązujący:**

- Metody `__init__` z parametrami: wymagają sekcji `### Arguments:`
- Settery z parametrami: wymagają sekcji `### Arguments:`
- Gettery: **wymagają sekcji `### Returns:`** ✅ (90/90 ukończone)
- Gettery: nie wymagają sekcji `### Arguments:`
- Metody magiczne comparatory (`__lt__`, `__le__`, itp.): nie wymagają sekcji `### Arguments:`
- Pozostałe metody magiczne z parametrami: wymagają sekcji `### Arguments:`
- Metody z parametrami (poza self/cls): wymagają sekcji `### Arguments:`

**Weryfikacja modułów priorytetowych:**

✅ jsktoolbox/systemtool.py - wszystkie funkcje mają docstringi
✅ jsktoolbox/configtool/**init**.py - wszystkie funkcje mają docstringi
✅ jsktoolbox/edmctool/logs.py - wszystkie funkcje mają docstringi
✅ jsktoolbox/edmctool/edsm.py - wszystkie funkcje mają docstringi

**Podsumowanie:**

Kompleksowa standaryzacja docstringów w projekcie została zakończona. Wszystkie publiczne metody, gettery i settery mają wymagane sekcje dokumentacji. Standard jest udokumentowany w AGENTS.md i stosowany konsekwentnie w całym projekcie. Pozostaje tylko okresowa aktualizacja przy dodawaniu nowego kodu.
