'''
Shadow - (theoblivionshadow)
Main Python file for FuzzyCatSpider task management program
Last Rev. 
    07.29.2023
    - added further comments to strengthen documentation
    - modified highlight and resets for list task items
    07.28.2023
    - finalized program for SDEV220 Final Project submission
'''

'''
To Do:
    [] Task Management
        [] Task Deletion Confirmation Dialog Boxes
        [] Add ability for user to edit tasks
        [] Task filter/sort
            [] by difficulty
            [] by display quantity of tasks
                [] fixed from user input
                [] randomly generated
            [] by priority
            [] by category
        [] user input for task category
        [] user input for task priority
        [] check done animation (like confetti)
    [] Gamification:
        [] Separate task list management into its own screen or use a toggle bin style to hide/unhide list
        [] Add game screen
            [] Creature section
                [] user input to battle vs tame
                    [] UI effect on health bar
                        [] battle
                            [] swords icon
                            [] full = green
                            [] < 1/2 = yellow
                            [] < 1/4 = red
                            [] empty space = grey
                        [] affection
                            [] heart icon
                            [] begin empty = grey
                            [] pinkish-red as it fills
                [] task difficulty to dmg/affection dealt to HP/AP conversion
                [] creature name generation
                    [] name
                    [] title
                [] creature image generation
                [] creature description / backstory generation
                [] user energy level to max HP/AP conversion
            [] User class
                [] user input for energy level
                [] Gallery of previously defeated and/or tamed creature
                    [] its own database
                        [] creature name & title
                        [] creature image
                        [] creature description / backstory
                        [] date tamed/defeated
            [] Task Completion mirroring to Task Management List and Database
            [] User input to select a task vs roll for a random task in facing the creature
    [] App Stuff
        [] Official App Name
        [] Official App Logo
        [] .py to .exe
        [] web app
        [] mobile app
            [] Android
            [] iOS
        [] user account stuff
        [] hosting stuff
        [] About / Help Screen
        [] Nav/Menu Bar
'''

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

# create dialog class
class DialogContent(MDBoxLayout):
    # init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

# task status class
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        # init function for class constructor
        super().__init__(**kwargs)
        self.pk = pk

    # strikethrough task = complete
    def mark(self, check, list_task):
        # check if checkbox is checked
        if check.active == True:
            list_task.text = '[s][b]' + list_task.text + '[/b][/s]' #if it is, strikethrough text
            db.check_done(list_task.pk) # note change in task database

            list_task.theme_text_color = "Primary" # reset text color
            list_task.font_style = "Body1" # reset font style to body 1

            list_task.secondary_theme_text_color = "Primary" # reset secondary line of text's color
            list_task.secondary_font_style = "Body1" # reset secondary line of text's font style to body 1

            list_task.bg_color = 38/255, 50/255, 56/255, 1 # reset background color
        else:
            list_task.text = str(db.check_toDo(list_task.pk))
    
    # delete task
    def delete_item(self, list_task):
        self.parent.remove_widget(list_task) # removes task from app screen
        db.remove_task(list_task.pk) # removes task from database

    # highlight task
    def highlight(self, list_task, id):
        # check if task's primary key is equal to the id of randomly selected task
        if id == list_task.pk:
            list_task.theme_text_color = "Custom" # change first line of text's color
            list_task.text_color = app.theme_cls.primary_dark # set custom text color
            list_task.font_style = "H6" # change font style to heading 6

            list_task.secondary_theme_text_color = "Secondary" # change secondary line of text's color
            list_task.secondary_font_style = "H6" # change secondary line of text's font style to heading 6
            
            list_task.bg_color = app.theme_cls.accent_dark # change task's background color to highlight it
            
        else:
            pass # if list task is NOT the same as the randomly selected task, do not change anything

# set up left check box class
class LeftCheckbox(ILeftBody, MDCheckbox):
    pass

# set up main app class
class MainApp(MDApp):
    # initialize variables
    task_list_dialog = None

    # build function for setting the theme
    def build(self):
        # establish primary palette
        self.theme_cls.primary_palette = "DeepPurple" # set primary theme color
        self.theme_cls.primary_hue = "A200" # set primary theme color's hue
        self.theme_cls.primary_light_hue = "A100" # set light version of primary color
        self.theme_cls.primary_dark_hue = "A700" # set dark version of primary color

        # establish accent palette
        self.theme_cls.accent_palette = "Teal" # set accent theme color
        self.theme_cls.accent_hue = "A400" # set accent theme color's hue
        self.theme_cls.accent_light_hue = "A200" # set light version of accent color
        self.theme_cls.accent_dark_hue = "A700" # set dark version of accent color
        
        # establish theme
        self.theme_cls.theme_style = "Dark" # set app overall theme

    # show task function
    def show_tasks(self):
        if not self.task_list_dialog:
            # dialog details
            self.task_list_dialog = MDDialog(
                                    title = "Create Task",
                                    type = "custom",
                                    content_cls = DialogContent() # reference previously created custom dialog class
                                    )
        self.task_list_dialog.open() # open dialog box
    
    # add tasks
    def add_task(self, task, difficulty):
        # access database to add new task
        # use task and difficulty from user input in dialog box to populate database item
        created_task = db.insert_new_task(task.text, difficulty.text)
        # access id of list to show task & add it to the list using custom list w/ checkbox class
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text = created_task[1], secondary_text= "Difficulty: " + created_task[2]))
        task.text = "" # initialize task text to empty string
        difficulty.text = "" # initialize difficulty text to empty string

        # match aesthetic of newly added tasks to rest of list
        for child in self.root.ids['container'].children: # .children grants access to specific list items locations
            list_task = child # assigns child data to variable

            list_task.theme_text_color = "Primary" # reset text color
            list_task.font_style = "Body1" # reset font style to body 1

            list_task.secondary_theme_text_color = "Primary" # reset secondary line of text's color
            list_task.secondary_font_style = "Body1" # reset secondary line of text's font style to body 1

            list_task.bg_color = 38/255, 50/255, 56/255, 1 # reset background color

    # close dialog function
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss() # closes dialog box
        
    # define function to randomly pick task (roll D20)
    def rollForTask(self):
            # initialize variables
            task_qty = 0
            taskIDs = []
            taskNames = []
            taskDifficulties = []
            
            # get tasks from database
            complted_tasks, tasks_incomplete = db.select_all_tasks()
            
            # loop to add incomplete task details to list
            # and count quantity of incomplete tasks
            for task in tasks_incomplete:
                task_qty += 1 # counter for number of tasks
                taskIDs.append(task[0]) # adds task ID to taskIDs list
                taskNames.append(task[1]) # adds task name to taskNames list
                taskDifficulties.append(task[2]) # adds task difficulty to taskDifficulties list
                # task is saved as list, so using index of items w/in task to assign to appropriate list

            # randomly generate task (roll D20)
            roll = randint(1, task_qty) # uses the counted number of tasks as the max range & randint from random to randomly pick a number w/in range

            # use randomly generated number to get task ID
            taskID = taskIDs[roll - 1] # sets taskID variable to the index value equal to the roll value (-1 because lists start at 0 index)

            # use taskID to select task info from database
            task = db.select_task(taskID)

            # parse data from task query
            for data in task:
                id = data[0] # save pk as ID
                name = data[1] # save task name
                difficulty = data[2] # save task difficulty
            
            # formatting for text display on app
            text = f'Quest to complete is "[b]{name}[/b]".\nDifficulty Rating is [b]{difficulty}[/b].'
            quest_hint = "Quest task is highlighted below in list. You may need to scroll down to see it.\nQuest task will be reset when app is closed."
            
            # display result of task using formatted string
            self.root.ids['quest_task'].text = text
            self.root.ids['hint'].text = quest_hint

            # iterates through list task items
            for child in self.root.ids['container'].children: # .children gives access to specific list task item so changes only affect it and not all list items
                list_task = child # save child data into variable
                
                list_task.theme_text_color = "Primary" # reset text color
                list_task.font_style = "Body1" # reset font style to body 1

                list_task.secondary_theme_text_color = "Primary" # reset secondary line of text's color
                list_task.secondary_font_style = "Body1" # reset secondary line of text's font style to body 1

                list_task.bg_color = 38/255, 50/255, 56/255, 1 # reset background color
                
                # call highlight function from ListItemWithCheckbox class to emphasize randomly selected task
                ListItemWithCheckbox.highlight(self, list_task, id)

    # function to define what occurs on program start up
    def on_start(self):
        '''Loads saved task and add them to MDList obj'''
        tasks_complete, tasks_incomplete = db.select_all_tasks() # gets tasks from database

        # checks if task is incompleted and loads those at the top of the list
        if tasks_incomplete != []:
            # iterates through tasks to populate list with appropriate data on the UI
            for task in tasks_incomplete:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text= "Difficulty: " + task[2]) # saves data as string to variable
                self.root.ids.container.add_widget(add_task) # adds task to list
                
        # checks if task is already complete and loads those after the incomplete tasks in the list
        if tasks_complete != []:
            # iterates through tasks to populate list with appropriate data on the UI
            for task in tasks_complete:
                add_task = ListItemWithCheckbox(pk=task[0], text= '[s]' + task[1] + '[/s]', secondary_text = "Difficulty: " + task[2]) # saves data as string to variable
                add_task.ids.check.active = True # sets check mark status to active/true to display it as checked off in list
                self.root.ids.container.add_widget(add_task) # adds task to list
        
        # iterates through children of list of tasks to reset background color
        for child in self.root.ids['container'].children: # .children gives access to specific list task items
            list_task = child # assigns child to variable

            list_task.theme_text_color = "Primary" # reset text color
            list_task.font_style = "Body1" # reset font style to body 1

            list_task.secondary_theme_text_color = "Primary" # reset secondary line of text's color
            list_task.secondary_font_style = "Body1" # reset secondary line of text's font style to body 1

            list_task.bg_color = 38/255, 50/255, 56/255, 1 # reset background color

# calls main program to run
if __name__ == "__main__":
    app = MainApp()
    app.run()