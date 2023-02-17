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
count_row = 0


def main():
    global first_row
    print("1) Today's tasks\n2) Add a task\n0) Exit")
    input_user = int(input())
    if input_user == 0:
        print("Bye!")
        exit()
    elif input_user == 2:
        print("Enter a task")
        add_task = input()
        new_row = Task(task=add_task)
        session.add(new_row)
        session.commit()
        rows = session.query(Task).all()
        first_row = rows[0]
        main()
    elif input_user == 1:
        print("Today:")
        if count_row == 0:
            print("Nothing to do!")
        else:
            print(f"{first_row.id}. {first_row.task}")
        main()


main()
