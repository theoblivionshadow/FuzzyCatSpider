import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("task-database.db")
        self.cursor = self.con.cursor()
        self.create_task_table()
    
    # create task table
    def create_task_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, difficulty varchar(1) NOT NULL, completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))"
        )
        self.con.commit()

    # create task
    def insert_new_task(self, task, difficulty):
        self.cursor.execute("INSERT INTO tasks (task, difficulty, completed) VALUES (?,?,?)", (task, difficulty, 0))
        self.con.commit()
    
        # get last entry
        created_task = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        return created_task[-1]
    
    # get tasks
    def select_all_tasks(self):
        '''Getting all tasks : completed and incompleted'''
        incompleted_tasks = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE completed = 0").fetchall()
        completed_tasks = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE completed = 1").fetchall()
        return completed_tasks, incompleted_tasks
    
    # update tasks
    def check_done(self, taskid):
        '''Mark tasks as completed'''
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (taskid,))
        self.con.commit()
    
    def check_toDo(self, taskid):
        '''Mark tasks as incompleted'''
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (taskid,))
        self.con.commit()
    
        # return task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]
    
    # delete tasks
    def remove_task(self, taskid):
        '''Deleting task'''
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.con.commit()

    # select a specific task
    def select_task(self, taskid):
        '''Selecting task'''
        task_text = self.cursor.execute("SELECT id, task, difficulty FROM tasks WHERE id = ?", (taskid,)).fetchall()
        return task_text

    # close connection
    def close_db_conn(self):
        self.con.close()