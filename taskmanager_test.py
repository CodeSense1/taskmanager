
from tkinter import *
from task import Task
import datetime as dt
import sys
import sqlite3


# TODO: Sort tasks by deadline or importance
# TODO: Ability to edit existing task
# TODO: Add a details section
# TODO: More pleasing GUI

class Gui:

    def __init__(self):

        # self.task_file = "D:\\koodausta\\Python\\tkinter\\tasks.txt"
        self.db = "D:\\koodausta\\Python\\tkinter\\data.db"

        # Create database if it doesn't exist
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS tasks (name text, deadline text)")
        conn.commit()
        conn.close()

        # Gui is drawn here
        self.root = Tk()
        self.root.title("Task management")
        self.tasklabel = Label(text="Task name: ")
        self.tasklabel.grid(row=1, column=1, columnspan=2)

        self.taskText = StringVar()
        self.taskEntry = Entry(self.root, textvariable=self.taskText)
        self.taskEntry.grid(row=1, column=3)

        self.dateLabel = Label(text="Enter deadline (day, month, hour, min): ")
        self.dateLabel.grid(row=2, column=1, columnspan=2)

        self.datevar = StringVar()
        self.dateEntry = Entry(self.root, textvariable=self.datevar)
        self.dateEntry.grid(row=2, column=3)

        self.task = Listbox(self.root)
        self.task.grid(row=4, column=1, rowspan=10)
        self.task.config(width=60, height=15)

        self.add_button = Button(text="Add task", command=self.insert_task)
        self.add_button.grid(row=4, column=3)
        self.add_button.config(width=15)

        self.select_button = Button(
            text="Mark as done", command=self.mark_as_done)
        self.select_button.grid(row=5, column=3)
        self.select_button.config(width=15)

        self.end_button = Button(text="End", command=exit)
        self.end_button.grid(row=6, column=3)
        self.end_button.config(width=15)

        self.task_data = self.get_data()

        # Get tasks from database and insert them to listbox
        for row in self.task_data:
            task_to_add = Task(name=row[0], deadline=row[1])
            self.task.insert(END, task_to_add)

        self.root.mainloop()

    # End program
    def exit(self):
        sys.exit(0)

    # Inserts new task to listbox and database

    def insert_task(self):

        self.task.insert(
            END, Task(name=self.taskText.get(), deadline=self.datevar.get()))

        # with open(self.task_file, "a") as file:
        #     file.write(self.taskText.get() + ";" + self.datevar.get())

        # TODO: Optimize this!
        # program lags a bit when executing this part of the code
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks VALUES (?,?)",
                    (self.taskText.get(), self.datevar.get()))
        conn.commit()
        conn.close()

        self.datevar.set("")
        self.taskText.set("")

    # Removes element from listbox and from database
    # TODO: make a store for completed tasks

    def mark_as_done(self):
        if self.task.curselection():
            try:
                self.selected = self.task.curselection()[0]
                name = str(self.task.get(self.selected))
                name = name.split(",")[0]

                # with open(self.task_file, "r+") as file:
                #     content = file.readlines()

                conn = sqlite3.connect(self.db)
                cur = conn.cursor()
                cur.execute("DELETE FROM tasks WHERE name LIKE ?", (name,))

                conn.commit()
                conn.close()

                self.task.delete(self.selected)

            except IndexError:
                print("IndexError: No elements selected from ")
                return
        else:
            print("No selected element")
            return

    # Reads data from database and returns it as a list
    def get_data(self):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM tasks")
        data = cur.fetchall()
        conn.commit()
        conn.close()

        return data


my_gui = Gui()
