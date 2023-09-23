"""
이중 DB setting
"""
from django.db.models import Model
from typing import Any

class MultiDBRouter:
    def __init__(self) -> None:
        self.model_list: list[str] = ["default", "authentication"]
    
    def db_for_read(self, model: Model, **hints: dict[str, Any]) -> str | None:
        if model.__meta.app_label in self.model_list:
            return model._meta.app_label
        return None
    
    def db_for_write(self, model: Model, **hints: dict[str, Any]) -> None:
        return None
    
    def allow_relation(self, obj1, obj2, **hints: dict[str, Any]) -> None:
        return None
    
    def allow_migrate(self, db: Model, app_label: str, model_name=None, **hints: dict[str, Any]) -> None:
        return None