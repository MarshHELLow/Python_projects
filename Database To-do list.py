from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()


def start_menu():
    print("\n1) Today's tasks\n2) Week's tasks\n"
          "3) All tasks\n4) Missed tasks\n5) Add a task\n6) Delete a task\n0) Exit")
    menu = {
        1: today_task,
        2: week_task,
        3: all_task,
        4: missed_task,
        5: add_task,
        6: delete_task,
        0: exit_program,
    }

    input_user = int(input())
    if input_user in menu:
        menu[input_user]()
    else:
        print("Invalid input")
        start_menu()


def today_task():
    rows = session.query(Task).all()
    if len(rows) == 0:
        print(f"Today {today.day} {today.strftime('%b')}:\nNothing to do!")
    else:
        for row in rows:
            if row.deadline == today.date():
                print(f"{row.id}. {row.task}")
    start_menu()


def week_task():
    end_of_week = today + timedelta(days=7)
    tasks = session.query(Task).filter(Task.deadline >= today.date(), Task.deadline <= end_of_week.date()).order_by(Task.deadline).all()
    for i in range(7):
        current_day = today + timedelta(days=i)
        tasks_for_current_day = [task for task in tasks if task.deadline == current_day.date()]
        print(f"{current_day.strftime('%A %d %b')}:")
        if len(tasks_for_current_day) == 0:
            print("Nothing to do!\n")
        else:
            for j, task in enumerate(tasks_for_current_day):
                print(f"{j+1}. {task.task}")
            print()
    start_menu()


def all_task():
    tasks = session.query(Task).order_by(Task.deadline).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        print("\nAll tasks:")
        for i, task in enumerate(tasks):
            deadline_all_task = task.deadline.strftime("%#d %b")
            print(f"{i+1}. {task.task}. {deadline_all_task}")
    start_menu()


def missed_task():
    missed_tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
    print("Missed tasks:")
    if len(missed_tasks) == 0:
        print("All tasks have been completed!")
    else:
        for i, task in enumerate(missed_tasks):
            deadline_missed_task = task.deadline.strftime("%#d %b")
            print(f"{i+1}. {task.task}. {deadline_missed_task}")
    start_menu()


def add_task():
    print("\nEnter a task:")
    task_input = input()
    print("\nEnter a deadline:")
    deadline_input = input()
    new_row = Task(task=task_input, deadline=datetime.strptime(deadline_input, "%Y-%m-%d").date())
    session.add(new_row)
    session.commit()
    print("\nThe task has been added!")
    start_menu()


def delete_task():
    tasks = session.query(Task).order_by(Task.deadline).all()
    if len(tasks) == 0:
        print("Nothing to delete")
    else:
        print("Choose the number of the task you want to delete:")
        for i, task in enumerate(tasks):
            deadline_all_task = task.deadline.strftime("%#d %b")
            print(f"{i+1}. {task.task}. {deadline_all_task}")
        task_number = int(input()) - 1
        session.delete(tasks[task_number])
        session.commit()
        print("The task has been deleted!")
    start_menu()


def exit_program():
    print("\nBye!")
    exit()


start_menu()
