# Project Modules

- Projekt wymaga Python 3.10-3.12 - Python 3.13 zmienił threading.Thread i ma problemy z NoDynamicAttributes, sprawdzić i rozwiązać
- BData.\_get_data i \_set_data - przemyśleć strategię set_default_type
- BData.\_get_data i \_set_data - rozwiązać problem użycia set_default_type = Optional[type]

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

**Pozostałe zadania:**

- [ ] Dodać brakujące docstringi do ~88 metod (głównie prywatne properties) - priorytet niski
- [ ] Okresowa aktualizacja dokumentacji przy zmianach w kodzie

**Standard obowiązujący:**

- Metody `__init__` z parametrami: wymagają sekcji `### Arguments:`
- Settery z parametrami: wymagają sekcji `### Arguments:`
- Gettery: **wymagają sekcji `### Returns:`** ✅ (90/90 ukończone)
- Gettery: nie wymagają sekcji `### Arguments:`
- Metody magiczne comparatory (`__lt__`, `__le__`, itp.): nie wymagają sekcji `### Arguments:`
- Pozostałe metody magiczne z parametrami: wymagają sekcji `### Arguments:`
- Metody z parametrami (poza self/cls): wymagają sekcji `### Arguments:`

**Moduły priorytetowe do ukończenia:**

1. jsktoolbox/systemtool.py (2 metody)
2. jsktoolbox/configtool/**init**.py (1 metoda)
3. jsktoolbox/edmctool/logs.py (3 pozostałe metody)
4. jsktoolbox/edmctool/edsm.py (3 metody)
5. Pozostałe moduły zgodnie z analizą check_docstrings.py
