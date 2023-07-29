# kivy and kivymd imports
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBody, IRightBody
from kivymd.uix.selectioncontrol import MDCheckbox

# import database class from database file
from database import Database

# initialize db class
db = Database()

#import random number module for random number generation
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
            list_task.text = '[s][b]' + list_task.text + '[/b][/s]'
            db.check_done(list_task.pk)
            list_task.theme_text_color = "Primary"
            list_task.bg_color = 38/255, 50/255, 56/255, 1
        else:
            list_task.text = str(db.check_toDo(list_task.pk))
    
    # delete task
    def delete_item(self, list_task):
        self.parent.remove_widget(list_task)
        db.remove_task(list_task.pk)

    # highlight task
    def highlight(self, list_task, id):
        if id == list_task.pk:
            list_task.text = '[b]' + list_task.text + '[/b]'
            list_task.theme_text_color = "Custom"
            list_task.text_color = app.theme_cls.primary_color

            list_task.secondary_text = '[b]' + list_task.secondary_text + '[/b]'
            list_task.Secondary_theme_text_color = "Custom"
            list_task.secondary_text_color = app.theme_cls.primary_color
            
            list_task.bg_color = app.theme_cls.accent_dark
        else:
            pass

class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

class MainApp(MDApp):
    # initialize variables
    task_list_dialog = None

    # build function for setting the theme
    def build(self):
        # establish primary palette
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "A200"
        self.theme_cls.primary_light_hue = "A100"
        self.theme_cls.primary_dark_hue = "A700"

        # establish accent palette
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.accent_hue = "A400"
        self.theme_cls.accent_light_hue = "A200"
        self.theme_cls.accent_dark_hue = "A700"
        
        # establish theme
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
        created_task = db.insert_new_task(task.text, difficulty.text)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = created_task[1], secondary_text= "Difficulty: " + created_task[2]))
        task.text = ""
        difficulty.text = ""

        for child in self.root.ids['container'].children:
            list_task = child
            list_task.theme_text_color = "Primary"
            list_task.bg_color = 38/255, 50/255, 56/255, 1

    # close dialog function
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
        
    # define function to randomly pick task (roll D20)
    def rollForTask(self):
            # initialize variables
            task_qty = 0
            taskIDs = []
            taskNames = []
            taskDifficulties = []
            
            # get tasks
            complted_tasks, tasks_incomplete = db.select_all_tasks()
            
            # loop to add incomplete task details to list
            # and count quantity of incomplete tasks
            for task in tasks_incomplete:
                task_qty += 1
                taskIDs.append(task[0])
                taskNames.append(task[1])
                taskDifficulties.append(task[2])

            # randomly generate task (roll D20)
            roll = randint(1, task_qty)

            # use randomly generated number to get task ID
            taskID = taskIDs[roll - 1]

            # use taskID to select task from database
            task = db.select_task(taskID)

            # parse data from task query
            for data in task:
                id = data[0]
                name = data[1]
                difficulty = data[2]
            
            # formatting for text display on app
            text = f'Quest to complete is "[b]{name}[/b]".\nDifficulty Rating is [b]{difficulty}[/b].\nQuest task is highlighted below in the list.'
            quest_hint = "Quest task is highlighted below in list. You may need to scroll down to see it.\nQuest task will be reset when app is closed."
            
            # display result of task using formatted string
            self.root.ids['quest_task'].text = text
            self.root.ids['hint'].text = quest_hint

            '''what do'''
            for child in self.root.ids['container'].children:
                list_task = child
                
                list_task.theme_text_color = "Primary"
                list_task.bg_color = 38/255, 50/255, 56/255, 1
                
                ListItemWithCheckbox.highlight(self, list_task, id)

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
                
        for child in self.root.ids['container'].children:
            list_task = child
            list_task.bg_color = 38/255, 50/255, 56/255, 1

if __name__ == "__main__":
    app = MainApp()
    app.run()