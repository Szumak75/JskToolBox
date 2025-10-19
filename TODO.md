# Project Modules

- Projekt wymaga Python 3.10-3.12 - Python 3.13 zmienił threading.Thread i ma problemy z NoDynamicAttributes, sprawdzić i rozwiązać
- BData._get_data i _set_data - przemyśleć strategię set_default_type
- BData._get_data i _set_data - rozwiązać problem użycia set_default_type = Optional[type]

## Documentation Standards

**STATUS:** ✅ WSZYSTKIE ZADANIA UKOŃCZONE! (Aktualizacja 2025-10-19 01:09)

**Ukończone (✓):**
- [x] Przeprowadzić pełny audyt docstringów w projekcie
- [x] Standaryzować format Author (dwie spacje po dwukropku)
- [x] Naprawić format Author w edmctool/logs2.py
- [x] Usunąć nieprawidłowe `### Returns: None` z konstruktorów (logstool/engines.py)
- [x] Dodać brakujące pole Purpose w devices/mikrotik/elements/__init__.py
- [x] **Dodać sekcję `### Arguments:` do wszystkich metod __init__ z parametrami (47 przypadków)** ✅
- [x] **Dodać pełne docstringi do 3 metod bez dokumentacji** ✅
- [x] Zaktualizować DOCSTRING_AUDIT_REPORT.md
- [x] Regenerować dokumentację API (Sphinx/ReadTheDocs) po zmianach w docstringach ✅
- [x] Zaktualizować dokumentację Markdown (README.md, docs/*.md) ✅
  - Naprawiono preferowane importy (lazy loading) we wszystkich plikach docs/*.md
  - Usunięto importy z pełnych ścieżek (ipv4/ipv6/libs) → preferowane lazy imports
  - Zaktualizowano AGENTS.md z pełną procedurą aktualizacji dokumentacji
- [x] **Ustalić i zadokumentować konwencję getterów/setterów** ✅
  - Settery (3/3) wymagają sekcji `### Arguments:`
  - Gettery (11/11) bez parametrów (oprócz self) nie wymagają tej sekcji
  - Standard dodany do AGENTS.md i DOCSTRING_AUDIT_REPORT.md

**Do zrobienia (○):**
- [ ] Zweryfikować sekcje `### Raises:` - czy wszystkie metody rzucają deklarowane wyjątki
- [ ] Dodać sekcję `### Arguments:` do kluczowych metod API (50 najważniejszych - opcjonalnie)

**Szczegółowy breakdown (135 opcjonalnych metod bez Arguments):**
- netaddresstool/ipv6.py: 22 metody (głównie gettery/settery)
- edmctool/math.py: 20 metod (głównie metody wewnętrzne)
- devices/network/connectors.py: 18 metod (głównie właściwości)
- netaddresstool/ipv4.py: 14 metod (głównie gettery/settery)
- edmctool/logs.py: 12 metod (głównie metody pomocnicze)
- (pozostałe 49 metod w innych plikach)

**Uwaga:** Raport w DOCSTRING_AUDIT_REPORT.md zawiera pełną analizę i zalecenia. **WSZYSTKIE PRIORYTETOWE ZADANIA UKOŃCZONE!** ✅

- ✅ 47 metod `__init__` zaktualizowanych z pełną sekcją `### Arguments:`
- ✅ 3 metody bez docstringów otrzymały pełną dokumentację
- ✅ 3 settery i 11 getterów zweryfikowane i zgodne ze standardem
- ✅ Dokumentacja API zregenerowana (Sphinx/ReadTheDocs)
- ✅ Dokumentacja Markdown zaktualizowana z poprawnymi wzorcami importów
- ✅ AGENTS.md zawiera pełne procedury aktualizacji dokumentacji
- ✅ Ustalony i zadokumentowany standard getterów/setterów

Pozostałe przypadki to opcjonalne dokumentacje innych metod (~135 metod).
