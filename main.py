from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.scrollview import MDScrollView

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody, IRightBody
from kivymd.uix.selectioncontrol import MDCheckbox

# import database class from database file
from database import Database
# initialize db class
db = Database()

from random import randint

class DialogContent(MDBoxLayout):
    # init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# task status class
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # strikethrough task = complete
    def mark(self, check, list_task):
        if check.active == True:
            list_task.text = '[s]' + list_task.text + '[/s]'
            db.check_done(list_task.pk)
        else:
            list_task.text = str(db.check_toDo(list_task.pk))
    
    # delete task
    def delete_item(self, list_task):
        self.parent.remove_widget(list_task)
        db.remove_task(list_task.pk)

class TaskQuestWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # strikethrough task = complete
    def mark(self, check, list_task):
        if check.active == True:
            list_task.text = '[s]' + list_task.text + '[/s]'
            db.check_done(list_task.pk)
        else:
            list_task.text = str(db.check_toDo(list_task.pk))

class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

class TaskQuest(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class ContentNavDrawer(MDScrollView):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class MainApp(MDApp):
    task_list_dialog = None
    # build function for setting the theme
    def build(self):
        self.theme_cls.primary_palette = ("Indigo")
        self.theme_cls.theme_style = "Dark"

    # show task function
    def show_tasks(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                                    title = "Create Task",
                                    type = "custom",
                                    content_cls = DialogContent()
                                    )
        self.task_list_dialog.open()
    
    # add tasks
    def add_task(self, task, difficulty):
        print(task.text, difficulty.text)
        created_task = db.insert_new_task(task.text, difficulty.text)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = created_task[1], secondary_text= "Difficulty: " + created_task[2]))
        task.text = ""
        difficulty.text = ""

    # close dialog function
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def rollForTask(self):
            task_qty = 0
            taskIDs = []
            taskNames = []
            taskDifficulties = []
            complted_tasks, tasks_incomplete = db.select_all_tasks()
            for task in tasks_incomplete:
                task_qty += 1
                taskIDs.append(task[0])
                taskNames.append(task[1])
                taskDifficulties.append(task[2])

            roll = randint(1, task_qty)
            taskID = taskIDs[roll - 1]

            task = db.select_task(taskID)
            for data in task:
                id = data[0]
                name = data[1]
                difficulty = data[2]

            self.root.ids['task_display'].add_widget(TaskQuestWithCheckbox(pk = id, text = name, secondary_text= "Difficulty: " + difficulty))

    def refresh(self):
        # refresh manage tasks list when switching screens

    def on_start(self):
        '''Loads saved task and add them to MDList obj'''
        tasks_complete, tasks_incomplete = db.select_all_tasks()

        if tasks_incomplete != []:
            for task in tasks_incomplete:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text= "Difficulty: " + task[2])
                self.root.ids.container.add_widget(add_task)

        if tasks_complete != []:
            for task in tasks_complete:
                add_task = ListItemWithCheckbox(pk=task[0], text= '[s]' + task[1] + '[/s]', secondary_text = "Difficulty: " + task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

if __name__ == "__main__":
    app = MainApp()
    app.run()