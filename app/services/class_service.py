from typing import List, Optional
from app.data.data_manager import DataManager
from app.models.response_models import ClassModel


class ClassService:
    def __init__(self):
        self.data_manager = DataManager()

    def get_all_classes(self) -> List[ClassModel]:
        return self.data_manager.get_all_classes()

    def create_class(self, name: str) -> ClassModel:
        return self.data_manager.add_class(name)

    def update_class(self, class_id: int, new_name: str) -> Optional[ClassModel]:
        return self.data_manager.update_class(class_id, new_name)

    def delete_class(self, class_id: int) -> bool:
        return self.data_manager.delete_class(class_id)