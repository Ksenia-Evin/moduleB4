# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class Athelete(Base):
    """
    Описывает структуру таблицы athelete для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    #возраст атлета
    age = sa.Column(sa.Integer)
    #др атлета
    birthdate = sa.Column(sa.Text)
    #пол атлета
    gender = sa.Column(sa.Text)
    #рост атлета
    height = sa.Column(sa.Float)
    # имя атлета
    name = sa.Column(sa.Text)
    #вес атлета
    weight = sa.Column(sa.Integer)
    #золотые медали
    gold_medals = sa.Column(sa.Integer)
    #серебряные медали
    silver_medals = sa.Column(sa.Integer)
    #бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    #всего медлаей
    total_medals = sa.Column(sa.Integer)
    #вид спорта
    sport = sa.Column(sa.Text)
    #страна 
    country = sa.Column(sa.Text)

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True, autoincrement = True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    #пол пользователя
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    #др пользователя
    birthdate = sa.Column(sa.Text)
    #рост пользователя
    height = sa.Column(sa.Float)

def request_data():
    """
    Запрашивает у пользователя данные
    """
    # выводим приветствие
    print("Привет! Я найду атлета, похожего на одного из пользователей!")
    # запрашиваем у пользователя данные
    user_id = input("Введи id пользователя: ")
    
    return int(user_id)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def convert_str_to_date(date_str):
    """
    Конвертирует строку с датой в формате ГГГГ-ММ-ЧЧ в объект datetime.date
    """
    parts = date_str.split("-")
    date_parts = map(int, parts)
    date = datetime.date(*date_parts)
    return date




def find_by_birthday(user, session):
    """
    Производит поиск пользователя в таблице athelete по заданному имени name
    """
    # находим все записи в таблице athelete
    atheletes = session.query(Athelete).all()
    
    atheletes_id_birthdate = {}
    for athelete in atheletes:
        atheletes_id_birthdate[athelete.id] = convert_str_to_date(athelete.birthdate)

    user_bd = convert_str_to_date(user.birthdate)
    min_dist = None
    athlete_id = None
    athlete_bd = None

    for id_, birthdate in atheletes_id_birthdate.items():
        dist = abs(user_bd - birthdate)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_bd = birthdate
    
    return athlete_id, athlete_bd


def find_by_height(user, session):
    """
    Производит поиск пользователя в таблице athelete по заданному имени name
    """
    # находим все записи в таблице athelete
    atheletes = session.query(Athelete).all()
    
    atheletes_id_height = {}
    for athelete in atheletes:
        atheletes_id_height[athelete.id] = athelete.height

    user_height = user.height
    min_dist = None
    athlete_id = None
    athlete_height = None

    for id_, height in atheletes_id_height.items():
        if height is None:
            continue
        dist = abs(user_height - height)
        if not min_dist or dist < min_dist:
            min_dist = dist
            athlete_id = id_
            athlete_height = height
    
    return athlete_id, athlete_height

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print('Такого пользователя нет!:(')
    else:
        birthday_athlete, birthday = find_by_birthday(user, session)
        height_athlete, height = find_by_height(user, session)
        print(
            "Ближайший по дате рождения атлет: {}, его дата рождения: {}".format(birthday_athlete, birthday)
        )
        print(
            "Ближайший по росту атлет: {}, его рост: {}".format(height_athlete, height)
        )


if __name__ == "__main__":
    main()