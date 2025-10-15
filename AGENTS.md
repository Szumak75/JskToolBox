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
- Docstringi zachowują format: krótka linia streszczenia, sekcje (`### Arguments`, `### Returns`, `### Raises`).
- Preferuj pojedyncze cudzysłowy, chyba że podwójne są wymagane.

### Testowanie

- Testy znajdują się w katalogu `tests/`.
- Klasy testowe dziedziczą po `unittest.TestCase`, a zestaw uruchamiaj przez `poetry run pytest`.
- Zapewnij pokrycie testami każdej nowej funkcjonalności.

### Obsługa błędów

- Do zgłaszania wyjątków używaj mechanizmu `raisetool.Raise.error(message, exception_type, class_name, frame)`.

### Ogólne zalecenia

- Odpowiadaj w języku polskim.
- Plik konfiguracyjny AGENTS.md uzupełniaj w języku polskim.
- Komentarze i dokumentację w repozytorium zapisuj po angielsku.
- Zachowuj zwięzłą, techniczną formę odpowiedzi zgodną z konwencjami projektu.
- Przy zmianach obejmujących wiele plików przedstaw plan i poproś o akceptację.

## Docstring Template

Docstringi tworzymy w języku angielskim według poniższych wzorców.

### Module-level Docstring

```python
"""
Author:  [Author Name] --<[author_email@example.com]>
Created: [YYYY-MM-DD]

Purpose: [Short, one-line summary of the module's purpose.]

[Optional: More detailed description of the module's functionality,
its components, and how they fit into the larger project.]
"""
```

### Class-level Docstring

```python
"""[Short, one-line summary of the class's purpose.]

[Optional: More detailed description of the class's responsibilities,
design choices, and its role (e.g., utility, data structure).]
"""
```

### Function/Method-level Docstring

```python
"""[Short, one-line summary of what the function does.]

[Optional: More detailed explanation of the function's logic,
its use cases, or any important algorithms used.]

### Arguments:
* arg1: [type] - [Description of the first argument.]
* arg2: Optional[[type]] - [Description of the second, optional argument. Defaults to [DefaultValue].]

### Returns:
[type] - [Description of the returned value.]

### Raises:
* [ExceptionType]: [Description of the condition that causes this exception to be raised.]
"""
```

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
