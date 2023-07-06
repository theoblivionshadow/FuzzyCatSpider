from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout

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
    def mark(self, check, the_list_item):
        if check.active == True:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_as_complete(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_as_incomplete(the_list_item.pk))
    
    # delete task
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

class TaskQuest(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def rollForTask(self):
        task_qty = 0
        taskIDs = []
        taskNames = []
        taskDifficulties = []
        complted_tasks, incompleted_tasks = int(db.get_tasks())
        for task in incompleted_tasks:
            task_qty += 1
            taskIDs.append(task[0])
            taskNames.append(task[1])
            taskDifficulties.append(task[2])
        
        roll = randint(1, task_qty)
        taskID = taskIDs[roll]
        task = db.select_task(taskid=taskID)
        return task


class MainApp(MDApp):
    task_list_dialog = None
    # build function for setting the theme
    def build(self):
        self.theme_cls.primary_palette = ("Indigo")
        self.theme_cls.theme_style = "Dark"

    # show task function
    def show_task_function(self):
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
        created_task = db.create_task(task.text, difficulty.text)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = created_task[1], secondary_text= "Difficulty: " + created_task[2]))
        task.text = ""

    # close dialog function
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def on_start(self):
        '''Loads saved task and add them to MDList obj'''
        completed_tasks, incompleted_tasks = db.get_tasks()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text= '[s]' + task[1] + '[/s]', secondary_text = task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)

if __name__ == "__main__":
    app = MainApp()
    app.run()