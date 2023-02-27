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


def menu():
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add a task\n0) Exit")
    input_user = int(input())
    if input_user == 1:
        today_task()
    elif input_user == 2:
        week_task()
    elif input_user == 3:
        all_task()
    elif input_user == 4:
        add_task()
    elif input_user == 0:
        print("\nBye!")
        exit()


def today_task():
    rows = session.query(Task).all()
    if len(rows) == 0:
        print(f"Today {today.day} {today.strftime('%b')}:\nNothing to do!")
    else:
        for row in rows:
            if row.deadline == today.date():
                print(f"{row.id}. {row.task}")
    menu()


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
    menu()


def all_task():
    tasks = session.query(Task).order_by(Task.deadline).all()
    if len(tasks) == 0:
        print("Nothing to do!")
    else:
        print("\nAll tasks:")
        for i, task in enumerate(tasks):
            deadline_all_task = task.deadline.strftime("%#d %b")
            print(f"{i+1}. {task.task}. {deadline_all_task}")
    menu()


def add_task():
    print("\nEnter a task:")
    task_input = input()
    print("\nEnter a deadline:")
    deadline_input = input()
    deadline = datetime.strptime(deadline_input, "%Y-%m-%d").date()
    new_row = Task(task=task_input, deadline=deadline)
    session.add(new_row)
    session.commit()
    print("\nThe task has been added!")
    menu()


menu()
