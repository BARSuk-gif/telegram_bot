
import random
import sys

from classes import (
Users, Target_words, Translate_words, Others_words,
 User_Target_Relations, Base)
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import configparser


config = configparser.ConfigParser()
config.read("settings.ini")
PASSWORD = config["postgres"]["password"]
login = config["postgres"]["login"]


DSN = sqlalchemy.URL.create(
    drivername="postgresql+psycopg2",
    username=login,
    password=PASSWORD,  
    host="localhost",
    port=5432,
    database="telegr_db"
)
engine = sqlalchemy.create_engine(DSN)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine) 

create_tables(engine)
print("Таблицы успешно созданы!")


Session = sessionmaker(bind=engine)
session = Session()


def initialize_default_data():
    """Функция для инициализации системных слов"""

    rw1 = Target_words(target_word="запрос", created_by=None)
    session.add(rw1)
    session.flush()
    tw1 = Translate_words(translate_word="request", target_id=rw1.id)
    ow1_1 = Others_words(other_word="question", target_id=rw1.id)
    ow1_2 = Others_words(other_word="problem", target_id=rw1.id)
    ow1_3 = Others_words(other_word="release", target_id=rw1.id)

    rw2 = Target_words(target_word="корень", created_by=None)
    session.add(rw2)
    session.flush()
    tw2 = Translate_words(translate_word="root", target_id=rw2.id)
    ow2_1 = Others_words(other_word="radical", target_id=rw2.id)
    ow2_2 = Others_words(other_word="origin", target_id=rw2.id)
    ow2_3 = Others_words(other_word="base", target_id=rw2.id)

    rw3 = Target_words(target_word="исключение", created_by=None)
    session.add(rw3)
    session.flush()
    tw3 = Translate_words(translate_word="exception", target_id=rw3.id)
    ow3_1 = Others_words(other_word="exclusion", target_id=rw3.id)
    ow3_2 = Others_words(other_word="exile", target_id=rw3.id)
    ow3_3 = Others_words(other_word="pushing", target_id=rw3.id)

    rw4 = Target_words(target_word="отклик", created_by=None)
    session.add(rw4)
    session.flush()
    tw4 = Translate_words(translate_word="response", target_id=rw4.id)
    ow4_1 = Others_words(other_word="comment", target_id=rw4.id)
    ow4_2 = Others_words(other_word="remark", target_id=rw4.id)
    ow4_3 = Others_words(other_word="echo", target_id=rw4.id)

    rw5 = Target_words(target_word="шаблон", created_by=None)
    session.add(rw5)
    session.flush()
    tw5 = Translate_words(translate_word="template", target_id=rw5.id)
    ow5_1 = Others_words(other_word="matrix", target_id=rw5.id)
    ow5_2 = Others_words(other_word="wildcard", target_id=rw5.id)
    ow5_3 = Others_words(other_word="stencil", target_id=rw5.id)

    rw6 = Target_words(target_word="извлекать", created_by=None)
    session.add(rw6)
    session.flush()
    tw6 = Translate_words(translate_word="eject", target_id=rw6.id)
    ow6_1 = Others_words(other_word="take", target_id=rw6.id)
    ow6_2 = Others_words(other_word="accept", target_id=rw6.id)
    ow6_3 = Others_words(other_word="derive", target_id=rw6.id)

    rw7 = Target_words(target_word="отображать", created_by=None)
    session.add(rw7)
    session.flush()
    tw7 = Translate_words(translate_word="display", target_id=rw7.id)
    ow7_1 = Others_words(other_word="mirror", target_id=rw7.id)
    ow7_2 = Others_words(other_word="chart", target_id=rw7.id)
    ow7_3 = Others_words(other_word="compare", target_id=rw7.id)

    rw8 = Target_words(target_word="попробуй", created_by=None)
    session.add(rw8)
    session.flush()
    tw8 = Translate_words(translate_word="try", target_id=rw8.id)
    ow8_1 = Others_words(other_word="test", target_id=rw8.id)
    ow8_2 = Others_words(other_word="analysis", target_id=rw8.id)
    ow8_3 = Others_words(other_word="experience", target_id=rw8.id)

    rw9 = Target_words(target_word="соединение", created_by=None)
    session.add(rw9)
    session.flush()
    tw9 = Translate_words(translate_word="connection", target_id=rw9.id)
    ow9_1 = Others_words(other_word="union", target_id=rw9.id)
    ow9_2 = Others_words(other_word="composition", target_id=rw9.id)
    ow9_3 = Others_words(other_word="communication", target_id=rw9.id)

    rw10 = Target_words(target_word="заявление", created_by=None)
    session.add(rw10)
    session.flush()
    tw10 = Translate_words(translate_word="statement", target_id=rw10.id)
    ow10_1 = Others_words(other_word="expression", target_id=rw10.id)
    ow10_2 = Others_words(other_word="conclusion", target_id=rw10.id)
    ow10_3 = Others_words(other_word="report", target_id=rw10.id)

    rw11 = Target_words(target_word="получать", created_by=None)
    session.add(rw11)
    session.flush()
    tw11 = Translate_words(translate_word="fetch", target_id=rw11.id)
    ow11_1 = Others_words(other_word="bear", target_id=rw11.id)
    ow11_2 = Others_words(other_word="give", target_id=rw11.id)
    ow11_3 = Others_words(other_word="grant", target_id=rw11.id)
 
    session.add_all([rw1, rw2, rw3, rw4, rw5, rw6, rw7, rw8, rw9, rw10, rw11,
                    tw1, tw2, tw3, tw4, tw5, tw6, tw7, tw8, tw9, tw10, tw11,
                    ow1_1, ow1_2, ow1_3, ow2_1, ow2_2, ow2_3, ow3_1, ow3_2, ow3_3,
                    ow4_1, ow4_2, ow4_3, ow5_1, ow5_2, ow5_3, ow6_1, ow6_2, ow6_3,
                    ow7_1, ow7_2, ow7_3, ow8_1, ow8_2, ow8_3, ow9_1, ow9_2, ow9_3,
                    ow10_1, ow10_2, ow10_3, ow11_1, ow11_2, ow11_3])
    session.commit()

def register_user(user_id, user_name):
    """Проверяет и добавляет пользователя в БД если его нет"""
    try:
        # Пытаемся найти пользователя в БД
        user = session.query(Users).filter(Users.id == user_id).first()            
        if not user:
            # Создаем пользователя
            user = Users(id=user_id, name=user_name, count_words=0)
            session.add(user)
            session.flush()

            # получаем системные слова
            system_words = session.query(Target_words).filter(
                Target_words.created_by == None).all()
            count_words = len(system_words)

            # Обновляем счетчик слов у пользователя
            user.count_words = count_words
            
            # Создаем связи для каждого системного слова
            relations = []
            for word in system_words:
                relation = User_Target_Relations(
                    user_id=user_id, 
                    target_id=word.id, 
                    is_active=True
                ) 
                relations.append(relation)            
       
            session.add_all(relations)
            session.commit()
            print(f"Зарегистрирован новый пользователь: {user_name} (id: {user_id})")
            return True
        else:
            print(f"Пользователь {user_name} уже существует")
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        session.rollback()
        return False

def get_target_word(user_id):
    try:
        q = session.query(Target_words).join(
            User_Target_Relations,
            Target_words.id == User_Target_Relations.target_id
        ).filter(
            User_Target_Relations.user_id == user_id, 
            User_Target_Relations.is_active == True).all()
        
        if q:
            random.shuffle(q)
            return q[0]
        return None
    except Exception as e:
        print(f"Ошибка при получении слова {e}")
        return None

def get_translate_word(target_word):
    q = session.query(Translate_words).filter(
        Translate_words.target_id == target_word.id).first()    
    return q.translate_word if q else None

def get_others_words(target_word):
    q = session.query(Others_words).filter(
        Others_words.target_id == target_word.id).all()    
    return [word.other_word for word in q]


def delete_user_word(user_id, target_word):
    try:
        # находим слово
        target = session.query(Target_words).filter(
            Target_words.target_word == target_word).first()
        if not target:
            return False
    
        # Получаем пользователя для проверки количества слов
        user = session.query(Users).filter(Users.id == user_id).first()
        if not user:
            return False

        # Проверяем, можно ли удалить слово (должно остаться минимум 5 слов)
        active_words_count = session.query(User_Target_Relations).filter(
            User_Target_Relations.user_id == user_id,
            User_Target_Relations.is_active == True
        ).count()

        if active_words_count <= 5:
            return False  # Нельзя удалить, останется меньше 5 слов
    
        if target.created_by == str(user_id):           # удаляем слово             
            session.query(Translate_words).filter(
                Translate_words.target_id == target.id).delete()
            session.query(Others_words).filter(
                Others_words.target_id == target.id).delete()
            session.query(User_Target_Relations).filter(
                User_Target_Relations.target_id == target.id).delete()
            session.query(Target_words).filter(Target_words.id == target.id).delete()

            # Уменьшаем счетчик у пользователя
            user.count_words -= 1

        else:               # удаляем связь
            session.query(User_Target_Relations).filter(
                User_Target_Relations.user_id == user_id,
                User_Target_Relations.target_id == target.id).update({'is_active': False})

           # Уменьшаем счетчик у пользователя
            user.count_words -= 1

        session.commit()
        return True
    except Exception as e:
        print(f"Ошибка при удалении слова: {e}")
        session.rollback()
        return False


def add_user_word(user_id, utarget_word, utranslate_word, 
                  uother_word_1, uother_word_2, uother_word_3):
    try:
        rw_us = Target_words(target_word=utarget_word, created_by=str(user_id))
        session. add(rw_us)
        session.flush()          # чтобы получить id

        tw_us = Translate_words(translate_word=utranslate_word, target_id=rw_us.id)
        ow_u1 = Others_words(other_word=uother_word_1, target_id=rw_us.id)
        ow_u2 = Others_words(other_word=uother_word_2, target_id=rw_us.id)
        ow_u3 = Others_words(other_word=uother_word_3, target_id=rw_us.id)
        ut = User_Target_Relations(user_id=user_id, target_id=rw_us.id, is_active=True)

        # Увеличиваем счетчик слов пользователя
        user = session.query(Users).filter(Users.id == user_id).first()
        if user:
            user.count_words += 1
        
        session.add_all([tw_us, ow_u1, ow_u2, ow_u3, ut])
        session.commit()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении слова: {e}")
        session.rollback()
        return False



if session.query(Target_words).count() == 0:
    initialize_default_data()


if __name__ == "__main__":  
    session.close()
