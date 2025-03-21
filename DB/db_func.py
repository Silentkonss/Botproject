from main_db import conn


def db_new_chat(chat_id:int, username:str, topic_id):
    """Для создания и записи нового топика"""
    with conn.cursor() as cur:
        insert_query = ("insert into chatuser (chat_id, user_name, topic_id) VALUES"
                        " (%s, %s, %s) ON CONFLICT DO NOTHING")
        cur.execute(insert_query, (chat_id, username, topic_id))
        conn.commit()

def db_list_id():
    """Вытаскивает все чат id юзеров"""
    with conn.cursor() as cur:
        select_query = "select chat_id from chatuser"
        cur.execute(select_query)
        ret = cur.fetchall()
        ret_list = []
        for tup in ret:
            for row in tup:
                ret_list.append(row)
        return ret_list

# print(db_list_id())

def db_user_topic(chat_id):
    """Ищет нужный топик для каждого юзернейма"""
    with conn.cursor() as cur:
        select_query = "select topic_id from chatuser where chat_id = {}".format(chat_id)
        cur.execute(select_query)
        ret = cur.fetchone()
        return ret[0]

def db_user_id(topic):
    """Ищет чат ид для по номеру топика"""
    with conn.cursor() as cur:
        select_query = "select chat_id from chatuser where topic_id = {}".format(int(topic))
        cur.execute(select_query)
        ret = cur.fetchone()
        return ret[0]


def db_delete_chat(chat_id):
    """"Удаляет из базы чат"""
    with conn.cursor() as cur:
        delete_query = "DELETE FROM chatuser where chat_id = {}".format(chat_id)
        cur.execute(delete_query)
        conn.commit()