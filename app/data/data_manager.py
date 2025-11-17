import json
from pathlib import Path
from typing import List, Optional
from app.core.config import CLASSES_FILE
from app.models.response_models import ClassModel


class DataManager:
    def __init__(self):
        self._initialize_classes()

    def _initialize_classes(self):
        if not CLASSES_FILE.exists():
            default_classes = [
                {"id": 1, "name": "Historia"},
                {"id": 2, "name": "Quimica"},
                {"id": 3, "name": "Fisica"},
                {"id": 4, "name": "Ingles"},
                {"id": 5, "name": "Matematicas"},
                {"id": 6, "name": "Artes"},
                {"id": 7, "name": "Atletismo"},
                {"id": 8, "name": "Etica"}
            ]
            self._save_classes(default_classes)

    def _load_classes(self) -> List[dict]:
        try:
            with open(CLASSES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_classes(self, classes: List[dict]):
        with open(CLASSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(classes, f, ensure_ascii=False, indent=2)

    def get_all_classes(self) -> List[ClassModel]:
        classes_data = self._load_classes()
        return [ClassModel(**cls) for cls in classes_data]

    def add_class(self, name: str) -> ClassModel:
        classes_data = self._load_classes()
        new_id = max([cls['id'] for cls in classes_data], default=0) + 1
        new_class = {"id": new_id, "name": name}
        classes_data.append(new_class)
        self._save_classes(classes_data)
        return ClassModel(**new_class)

    def update_class(self, class_id: int, new_name: str) -> Optional[ClassModel]:
        classes_data = self._load_classes()
        for cls in classes_data:
            if cls['id'] == class_id:
                cls['name'] = new_name
                self._save_classes(classes_data)
                return ClassModel(**cls)
        return None

    def delete_class(self, class_id: int) -> bool:
        classes_data = self._load_classes()
        initial_length = len(classes_data)
        classes_data = [cls for cls in classes_data if cls['id'] != class_id]

        if len(classes_data) < initial_length:
            self._save_classes(classes_data)
            return True
        return False