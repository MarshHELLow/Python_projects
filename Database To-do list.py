from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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


def menu():
    print("1) Today's tasks\n2) Add a task\n0) Exit")
    input_user = int(input())
    if input_user == 1:
        today_task()
    elif input_user == 2:
        print("Enter a task")
        add_task()
    elif input_user == 0:
        print("\nBye!")
        exit()


def today_task():
    rows = session.query(Task).all()
    if len(rows) == 0:
        print("\nToday:\nNothing to do!")
    else:
        for row in rows:
            print(f"{row.id}. {row.task}")
    menu()


def add_task():
    new_row = Task(task=input())
    session.add(new_row)
    session.commit()
    menu()


menu()
