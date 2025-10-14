# Konfiguracja Gemini dla projektu JskToolBox

## Konfiguracja plików
# Uwzględnij tylko pliki źródłowe Python i testy.
files.include:
  - "jsktoolbox/**/*.py"
  - "tests/**/*.py"

# Wyklucz katalogi wirtualnego środowiska, pamięć podręczną i inne.
files.exclude:
  - ".venv/**"
  - ".pytest_cache/**"
  - "__pycache__/**"
  - "dist/**"
  - "*.egg-info/**"

## Instrukcje dotyczące zachowania
behavior:
  # Język i zarządzanie projektem
  language: "Python 3.10+"
  project_management: "Projekt używa Poetry. Używaj `poetry run <polecenie>` do uruchamiania narzędzi takich jak `pytest` czy `black`."

  # Styl kodowania
  code_style:
    - "Kod jest formatowany za pomocą `black`. Zawsze uruchamiaj `poetry run black .` po wprowadzeniu zmian."
    - "Przestrzegaj standardów PEP 8, sprawdzanych za pomocą `pycodestyle`."
    - "Wszystkie nowe funkcje i metody muszą mieć podpowiedzi typów (type hints)."
    - "Docstringi mają specyficzny format. Pierwsza linia to krótkie podsumowanie. Sekcje takie jak argumenty są oznaczane nagłówkiem `### Arguments`. Analizuj istniejący kod, aby zachować spójność."
    - "Używaj pojedynczych cudzysłowów dla ciągów znaków, chyba że podwójne są konieczne."

  # Testowanie
  testing:
    - "Testy znajdują się w katalogu `tests/`."
    - "Testy są pisane przy użyciu klas `unittest.TestCase`, ale uruchamiane za pomocą `pytest`."
    - "Każdy nowy kod powinien być pokryty testami jednostkowymi."
    - "Uruchamiaj testy za pomocą polecenia `poetry run pytest`."

  # Obsługa błędów
  error_handling: "Do zgłaszania wyjątków używaj niestandardowego mechanizmu `raisetool.Raise.error(message, exception_type, class_name, frame)`."

  # Ogólne
  general:
    - "Odpowiadaj w języku polskim."
    - "Komentarze i dokumentację w plikach projektowych generuj w języku angielskim."
    - "Twoje odpowiedzi powinny być zwięzłe, techniczne i zgodne z konwencjami projektu."
    - "Przed wprowadzeniem zmian w wielu plikach, przedstaw plan i poproś o zatwierdzenie."