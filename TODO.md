# Project Modules

- Projekt wymaga Python 3.10-3.12 - Python 3.13 zmienił threading.Thread i ma problemy z NoDynamicAttributes, sprawdzić i rozwiązać
- BData._get_data i _set_data - przemyśleć strategię set_default_type

## Documentation Standards

**STATUS:** Priorytetowe zadania zrealizowane ✅ (Aktualizacja 2025-10-18 23:33)

**Ukończone (✓):**
- [x] Przeprowadzić pełny audyt docstringów w projekcie
- [x] Standaryzować format Author (dwie spacje po dwukropku)
- [x] Naprawić format Author w edmctool/logs2.py
- [x] Usunąć nieprawidłowe `### Returns: None` z konstruktorów (logstool/engines.py)
- [x] Dodać brakujące pole Purpose w devices/mikrotik/elements/__init__.py
- [x] **Dodać sekcję `### Arguments:` do wszystkich metod __init__ z parametrami (44 przypadki)** ✅
- [x] Zaktualizować DOCSTRING_AUDIT_REPORT.md

**W trakcie (→):**
- [ ] Regenerować dokumentację API (Sphinx/ReadTheDocs) po zmianach w docstringach
- [ ] Zaktualizować dokumentację Markdown (README.md, docs/*.md)

**Do zrobienia (○):**
- [ ] Dodać pełne docstringi do 3 metod bez dokumentacji (AlgAStar, VerticalScrolledTkFrame, VerticalScrolledTtkFrame)
- [ ] Dodać sekcję `### Arguments:` do kluczowych metod API (50 najważniejszych)
- [ ] Rozważyć i ustalić konwencję: proste gettery/settery wymagają/nie wymagają `### Arguments:`
- [ ] Stopniowa aktualizacja pozostałych metod bez Arguments (opcjonalne - głównie gettery/settery)
- [ ] Zweryfikować sekcje `### Raises:` - czy wszystkie metody rzucają deklarowane wyjątki

**Szczegółowy breakdown (135 opcjonalnych metod bez Arguments):**
- netaddresstool/ipv6.py: 22 metody (głównie gettery/settery)
- edmctool/math.py: 20 metod (głównie metody wewnętrzne)
- devices/network/connectors.py: 18 metod (głównie właściwości)
- netaddresstool/ipv4.py: 14 metod (głównie gettery/settery)
- edmctool/logs.py: 12 metod (głównie metody pomocnicze)
- (pozostałe 49 metod w innych plikach)

**Uwaga:** Raport w DOCSTRING_AUDIT_REPORT.md zawiera pełną analizę i zalecenia. Wszystkie priorytetowe metody `__init__` zostały zaktualizowane! Pozostałe przypadki to głównie opcjonalne dokumentacje getterów/setterów.
