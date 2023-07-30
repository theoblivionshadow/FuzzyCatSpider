'''
Shadow - (theoblivionshadow)
Database Python file for FuzzyCatSpider task management program
Last Rev. 
    07.29.2023
    - added header comment
    - added comments throughout program to further solidify documentation
'''

# import sqlite3 for database
import sqlite3

# initialize Database class
class Database():
    # define initilization function
    def __init__(self):
        self.con = sqlite3.connect("task-database.db") # connect to database
        self.cursor = self.con.cursor() # initialize cursor
        self.create_task_table() # create table for tasks
    
    # create task table
    def create_task_table(self):
        # use cursor to execute SQL "CREATE TABLE" command if it does not exist yet
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, difficulty varchar(1) NOT NULL, completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))"
        )
        self.con.commit() # commit changes to database

    # create task
    def insert_new_task(self, task, difficulty):
        # use cursor to execute SQL "INSERT" command w/ undefined variables '?' for later assignment via user input
        # assign completed default value of '0' for all added tasks
        self.cursor.execute("INSERT INTO tasks (task, difficulty, completed) VALUES (?,?,?)", (task, difficulty, 0))
        self.con.commit() # commit changes to database
    
        # get last entry
        # use cursor to execute SQL "SELECT" command w/ undefined var for task and where task in not complete
        created_task = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        return created_task[-1] # return the result from query
    
    # get tasks
    def select_all_tasks(self):
        '''Getting all tasks : completed and incompleted'''
        # use cursor to execute SQL "SELECT" command to get all incomplete tasks
        incompleted_tasks = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE completed = 0").fetchall()
        # use cursor to execute SQL "SELECT" command to get all completed tasks
        completed_tasks = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE completed = 1").fetchall()
        return completed_tasks, incompleted_tasks # return results for both
    
    # update tasks
    def check_done(self, taskid):
        '''Mark tasks as completed'''
        # use cursor to execute SQL "UPDATE" command w/ undefined var for id and set task to complete
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (taskid,))
        self.con.commit() # commit changes to database
    
    def check_toDo(self, taskid):
        '''Mark tasks as incompleted'''
        # use cursor to execute SQL "UPDATE" command w/ undefined var for id and set task to incomplete
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (taskid,))
        self.con.commit() # commite changes to database
    
        # return task text using cursor to execture SQL "SELECT" command w/ undef. var for id
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0] # return query results
    
    # delete tasks
    def remove_task(self, taskid):
        '''Deleting task'''
        # use cursor to execute SQL "DELETE" command w/ undef. id var
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit() # commit changes to database

    # select a specific task
    def select_task(self, taskid):
        '''Selecting task'''
        # use cursor to execute SQL "SELECT" command w/ undef. id var
        task_text = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text # return query results

    # close connection
    def close_db_conn(self):
        self.con.close() # close connection to database