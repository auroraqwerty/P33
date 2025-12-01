from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import datetime
import json
import os


class DataManager:
    def __init__(self):
        self.data_file = "student_data.json"
        self.default_classes = [
            {"id": 1, "name": "Historia"},
            {"id": 2, "name": "Quimica"},
            {"id": 3, "name": "Fisica"},
            {"id": 4, "name": "Ingles"},
            {"id": 5, "name": "Matematicas"},
            {"id": 6, "name": "Artes"},
            {"id": 7, "name": "Atletismo"},
            {"id": 8, "name": "Etica"}
        ]
        self.ensure_data_exists()

    def ensure_data_exists(self):
        if not os.path.exists(self.data_file):
            self.save_data({"classes": self.default_classes})

    def load_data(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except:
            return {"classes": self.default_classes}

    def save_data(self, data):
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
            return True
        except:
            return False

    def get_classes(self):
        data = self.load_data()
        return data.get("classes", [])

    def add_class(self, class_name):
        data = self.load_data()
        classes = data.get("classes", [])
        new_id = max([c['id'] for c in classes], default=0) + 1
        new_class = {"id": new_id, "name": class_name}
        classes.append(new_class)
        data["classes"] = classes
        self.save_data(data)
        return new_class

    def update_class(self, class_id, new_name):
        data = self.load_data()
        classes = data.get("classes", [])
        for cls in classes:
            if cls['id'] == class_id:
                cls['name'] = new_name
                self.save_data(data)
                return True
        return False

    def delete_class(self, class_id):
        data = self.load_data()
        classes = data.get("classes", [])
        classes = [c for c in classes if c['id'] != class_id]
        data["classes"] = classes
        return self.save_data(data)


class MainScreen(Screen):
    pass


class ClassesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_manager = DataManager()
        self.selected_class_id = None

    def on_enter(self):
        self.load_classes()

    def load_classes(self):
        classes_data = self.data_manager.get_classes()
        self.ids.classes_list.clear_widgets()
        for cls in classes_data:
            item = OneLineListItem(
                text=f"{cls['name']}",
                on_release=lambda x, cls_id=cls['id'], cls_name=cls['name']: self.show_class_actions(cls_id, cls_name)
            )
            self.ids.classes_list.add_widget(item)

    def show_class_actions(self, class_id, class_name):
        self.selected_class_id = class_id
        self.dialog = MDDialog(
            title=f"Class: {class_name}",
            buttons=[
                MDFlatButton(text="Rename", on_release=lambda x: self.rename_class(class_id, class_name)),
                MDFlatButton(text="Delete", on_release=lambda x: self.delete_class(class_id)),
                MDFlatButton(text="Cancel", on_release=lambda x: self.dialog.dismiss())
            ]
        )
        self.dialog.open()

    def rename_class(self, class_id, old_name):
        self.dialog.dismiss()
        self.rename_dialog = MDDialog(
            title="Rename Class",
            type="custom",
            content_cls=MDBoxLayout(
                orientation="vertical",
                spacing="10dp",
                size_hint_y=None,
                height="100dp"
            ),
            buttons=[
                MDFlatButton(text="Save", on_release=lambda x: self.save_rename(class_id)),
                MDFlatButton(text="Cancel", on_release=lambda x: self.rename_dialog.dismiss())
            ]
        )
        self.rename_dialog.content_cls.add_widget(
            MDTextField(
                id="rename_field",
                hint_text="New class name",
                text=old_name
            )
        )
        self.rename_dialog.open()

    def save_rename(self, class_id):
        new_name = self.rename_dialog.content_cls.ids.rename_field.text
        if new_name and self.data_manager.update_class(class_id, new_name):
            self.load_classes()
            self.show_success("Class renamed")
        self.rename_dialog.dismiss()

    def delete_class(self, class_id):
        if self.data_manager.delete_class(class_id):
            self.load_classes()
            self.show_success("Class deleted")
        self.dialog.dismiss()

    def add_new_class(self):
        class_name = self.ids.new_class_name.text
        if class_name:
            self.data_manager.add_class(class_name)
            self.ids.new_class_name.text = ""
            self.load_classes()
            self.show_success("Class added")

    def reset_to_default(self):
        self.data_manager.save_data({"classes": self.data_manager.default_classes})
        self.load_classes()
        self.show_success("Reset to default classes")

    def show_error(self, message):
        MDDialog(title="Error", text=message, size_hint=(0.8, 0.3)).open()

    def show_success(self, message):
        MDDialog(title="Success", text=message, size_hint=(0.8, 0.3)).open()


class AttendanceScreen(Screen):
    def calculate_attendance(self):
        try:
            total = self.ids.total_classes.text
            missed = self.ids.missed_classes.text
            if total and missed:
                total_int = int(total)
                missed_int = int(missed)

                if missed_int > total_int:
                    self.ids.attendance_result.text = "Error: Missed > Total"
                    return
                if total_int <= 0:
                    self.ids.attendance_result.text = "Error: Total must be > 0"
                    return

                attended = total_int - missed_int
                percentage = (attended / total_int) * 100

                self.ids.attendance_result.text = (
                    f"Attended: {attended}/{total_int}\n"
                    f"Percentage: {percentage:.1f}%"
                )
        except:
            self.ids.attendance_result.text = "Error: Check inputs"


class GradesScreen(Screen):
    def calculate_grades(self):
        try:
            grades = []
            if self.ids.grade1.text: grades.append(float(self.ids.grade1.text))
            if self.ids.grade2.text: grades.append(float(self.ids.grade2.text))
            if self.ids.grade3.text: grades.append(float(self.ids.grade3.text))
            if self.ids.grade4.text: grades.append(float(self.ids.grade4.text))
            if self.ids.grade5.text: grades.append(float(self.ids.grade5.text))

            if grades:
                average = sum(grades) / len(grades)

                self.ids.grades_result.text = (
                    f"Average: {average:.2f}\n"
                    f"Subjects: {len(grades)}"
                )
            else:
                self.ids.grades_result.text = "Enter at least one grade"
        except:
            self.ids.grades_result.text = "Error: Check inputs"


class TimeScreen(Screen):
    def calculate_time(self):
        try:
            hour = int(self.ids.exit_hour.text)
            minute = int(self.ids.exit_minute.text)

            if 0 <= hour <= 23 and 0 <= minute <= 59:
                now = datetime.now()
                exit_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                if exit_time < now:
                    exit_time = exit_time.replace(day=exit_time.day + 1)

                time_diff = exit_time - now
                total_seconds = int(time_diff.total_seconds())

                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60

                self.ids.time_result.text = (
                    f"Time remaining:\n"
                    f"{hours}h {minutes}m {seconds}s"
                )
            else:
                self.ids.attendance_result.text = "Error: Invalid time"
        except:
            self.ids.time_result.text = "Error: Check inputs"


class StudentApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(ClassesScreen(name='classes'))
        sm.add_widget(AttendanceScreen(name='attendance'))
        sm.add_widget(GradesScreen(name='grades'))
        sm.add_widget(TimeScreen(name='time'))

        return sm


if __name__ == '__main__':
    StudentApp().run()