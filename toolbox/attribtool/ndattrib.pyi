from typing import Any

class NoDynamicAttributes:
    def __setattr__(self, name: str, value: Any) -> None: ...
