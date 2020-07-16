from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='task')
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return f'{self.task}. {self.deadline.day} {self.deadline.strftime("%b")}'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def day_tasks(day, day_w='\nToday'):
    rows = session.query(Table).filter(Table.deadline == day.date()).order_by(Table.deadline).all()
    print(f'{day_w} {day.day} {day.strftime("%b")}:')
    print_tasks(rows)
    print()


def week_tasks():
    day_w = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    for i in range(7):
        date = datetime.today() + timedelta(days=i)
        day_tasks(date, day_w[date.weekday()])
    main_menu()


def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('\nAll tasks:')
    print_tasks(rows, 1)
    print()
    main_menu()


def print_tasks(rows, date=0):
    if len(rows) > 0:
        for i in range(len(rows)):
            if date == 1:
                print(f'{i + 1}. {rows[i]}')
            else:
                print(f'{i + 1}. {str(rows[i])[:-7]}' if str(rows[i])[-7] == '.' else f'{i + 1}. {str(rows[i])[:-8]}')
    else:
        print('Nothing to do!')


def add_task():
    task = input('\nEnter task\n')
    deadline = input('Enter deadline\n').split(sep='-')
    new_row = Table(task=task, deadline=datetime(int(deadline[0]), int(deadline[1]), int(deadline[2]))) if \
        len(deadline) > 1 else Table(task=task)
    session.add(new_row)
    session.commit()
    print('The task has been added!\n')
    main_menu()


def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    print('\nMissed tasks:')
    print_tasks(rows, 1)
    print()
    main_menu()


def delete_task():
    rows = session.query(Table).order_by(Table.deadline).all()
    print('\nChose the number of the task you want to delete:')
    print_tasks(rows, 1)
    session.delete(rows[int(input()) - 1])
    session.commit()
    print('The task has been deleted!\n')
    main_menu()


def main_menu():
    user_choice = int(input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n"
                            "5) Add task\n6) Delete task\n0) Exit\n"))
    if user_choice == 1:
        day_tasks(datetime.today())
        main_menu()
    elif user_choice == 2:
        week_tasks()
    elif user_choice == 3:
        all_tasks()
    elif user_choice == 4:
        missed_tasks()
    elif user_choice == 5:
        add_task()
    elif user_choice == 6:
        delete_task()
    elif user_choice == 0:
        print('\nBye!')


main_menu()
