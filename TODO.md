# Project Modules

- Projekt wymaga Python 3.10-3.12 - Python 3.13 zmienił threading.Thread i ma problemy z NoDynamicAttributes, sprawdzić i rozwiązać
- BData._get_data i _set_data - przemyśleć strategię set_default_type

## Documentation Standards

- Przeprowadzić pełny audyt docstringów w projekcie
- Standaryzować format Author (dwie spacje po dwukropku)
- Dodać brakujące pola Author/Created/Purpose w modułach edmctool
- Dodać sekcję `### Arguments:` do metod z parametrami
- Sprawdzić sekcję `### Returns:` w metodach zwracających None
- Zweryfikować użycie `### Raises:` - tylko gdy metoda faktycznie rzuca wyjątki
