# Changelog

This file tracks project history using Semantic Versioning.

Older entries were reconstructed from `git log`, release commits, and the
available `git tag` metadata where explicit changelog records were missing.

Entry format:

```text
<type>: <subject>
```

Add commit hashes or pull request references when they are available.

Allowed types:

- `feat`
- `fix`
- `docs`
- `style`
- `refactor`
- `test`
- `chore`

## [Unreleased]

## [1.2.9]

### Refactor

- `refactor: move configtool FileProcessor keys registry into private FileProcessor.__Keys class`

## [1.2.8]

### Fixes

- `fix: move configtool main keys registry into private Config.__Keys class`
- `fix: refactor configtool Config storage to use BData accessors instead of direct storage writes`
- `fix: enforce strict runtime type validation for Config helper object and regex storage`

### Test

- `test: extend configtool Config coverage for typed storage behavior`

## [1.2.7]

### Fixes

- `fix: refactor configtool DataProcessor to use BData accessors instead of direct storage writes`
- `fix: enforce strict runtime type validation for DataProcessor section storage`

### Test

- `test: extend configtool data processor coverage for typed section storage behavior`

## [1.2.6]

### Fixes

- `fix: refactor configtool SectionModel to use BData accessors instead of direct storage writes`
- `fix: enforce strict runtime type validation for SectionModel name and variables storage`

### Test

- `test: extend configtool data model coverage for SectionModel typed storage behavior`

## [1.2.5]

### Fixes

- `fix: refactor configtool VariableModel to use BData accessors instead of direct storage writes`
- `fix: enforce strict runtime type validation for VariableModel constructor, setters, and parser`

### Test

- `test: extend configtool data model coverage for VariableModel typed storage behavior`

## [1.2.4]

### Chore

- `chore: bump version to 1.2.4`
- `chore: update project dependencies`
- `chore: update urllib3 to 2.6.3 and refresh poetry lock metadata`

### Features

- `feat: update Python version support to include 3.13`

### Fixes

- `fix: correct import statements for attribtool and basetool modules`

### Documentation

- `docs: fix README content for public PyPI and GitHub presentation`
- `docs: remove outdated development rules and versioning guidelines from README`

### Refactor

- `refactor: clean up widget class definitions and improve widget docstrings`
- `refactor: simplify TkBase mixin and remove redundant properties`
- `refactor: rename internal storage attributes for clarity and consistency`

## [1.2.3]

### Chore

- `chore: bump version to 1.2.3`
- `chore: update project dependencies`
- `chore: update iniconfig and adjust minimum supported Python requirement metadata`

### Features

- `feat: add support for complex generic types in BData, including Optional, Dict, List, Union, and nested validation`
- `feat: improve Python 3.13 compatibility in threading-related code and tests`
- `feat: standardize docstring formats and expand project documentation`
- `feat: add logs2 module with LoggerEngineConfig and LoggingServer`
- `feat: add log rotation support for LoggerEngineFile`
- `feat: add lazy loading for string utilities and export SimpleCrypto`
- `feat: improve TkBase property handling with stronger type hints and default values`

### Documentation

- `docs: define mandatory class section layout and 80-character separators`
- `docs: define semantic versioning workflow for project code changes`
- `docs: introduce changelog rules and entry format`
- `docs: refine ReadOnlyClass pattern selection and public keys module guidance`
- `docs: document Optional handling requirements for BData getters`
- `docs: add comprehensive AI and API guidance, lazy import usage notes, and Read the Docs setup updates`
- `docs: enhance module and logging subsystem documentation across the project`

### Refactor

- `refactor: deprecate set_default_type usage in BData getters and tighten type handling`
- `refactor: improve lazy loading in netaddresstool and related package __init__ modules`
- `refactor: streamline logging engine initialization, key classes, and message handling`
- `refactor: remove deprecated thlogs implementation and legacy imports`
- `refactor: improve Address, Address6, Octet, and Word16 comparison type checks`

### Test

- `test: add lazy loading and type hint coverage for configtool and logstool`
- `test: update tests to remove SSH-specific assumptions and improve API-focused coverage`

## [1.1.3]

### Features

- `feat: add StatusBar widgets for tktool, including ttk integration`
- `feat: add multi-backend clipboard support for Tk, Qt, GTK, and Windows environments`
- `feat: extend CommandLineParser with help handling, has_option, and related API improvements`
- `feat: improve BData collection handling with List and Dict support, _delete_data, and _clear_data helpers`
- `feat: add threaded log processing support and configurable LogProcessor options`

### Fixes

- `fix: streamline ClipBoard tool detection and remove deprecated clipboard initialization paths`
- `fix: improve Windows clipboard handling and Qt clipboard initialization`
- `fix: correct help and purpose metadata in systemtool and tktool modules`

### Documentation

- `docs: normalize docstring header formatting in modules and tests`
- `docs: expand tktool, datetool, raisetool, and systemtool documentation`

### Refactor

- `refactor: rename StatusBar implementation for clearer Tk and ttk separation`
- `refactor: clean up clipboard class hierarchy and related tests`
- `refactor: simplify BData internals and related deletion semantics`

## [1.0.0]

### Features

- `feat: initial public release of JskToolBox`
- `feat: add NetAddressTool foundations, including Address, Netmask, and related utilities`
- `feat: add RaiseTool formatter support and early error handling helpers`

### Fixes

- `fix: optimize and correct Netmask behavior before first stable release`

### Documentation

- `docs: add initial NetAddressTool and Octet documentation set`

### Chore

- `chore: rename project and prepare the 1.0.0 release`
