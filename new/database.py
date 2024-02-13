import sqlite3
import os
from user_data import db_path



class DbSpamer:
    def __init__(self) -> None:
        self.db_path = db_path

    def __enter__(self):
        print('Database was started')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Database was closed')
        self.conn.close()


    
    def db_add_message_in_messages_admin(self, chat_id, message_id):
        self.cursor.execute("INSERT INTO admin_messages (user_id, message) VALUES (?, ?)", (chat_id, message_id))
        self.conn.commit()
        return True
    

    def db_get_messages_in_chat_admin(self, chat):
        self.cursor.execute("SELECT * FROM admin_messages WHERE user_id = ?", (chat,))
        result = self.cursor.fetchall()
        return result


    def db_delete_message_in_chat_admin(self, chat):
        self.cursor.execute("DELETE FROM admin_messages WHERE user_id = ?", (chat,))
        self.conn.commit()
        return True
    



    def db_set_name_for_group_id(self, group_id, new_name):
        self.cursor.execute("UPDATE groups SET name = ? WHERE id = ?", (new_name, group_id))
        self.conn.commit()

    def db_set_sms_for_group_id(self, group_id, new_time):
        self.cursor.execute("UPDATE groups SET time_sms = ? WHERE id = ?", (new_time, group_id))
        self.conn.commit()

    def db_set_start_for_group_id(self, group_id, new_time):
        self.cursor.execute("UPDATE groups SET time_start = ? WHERE id = ?", (new_time, group_id))
        self.conn.commit()

    def db_set_onlineon_for_group_id(self, group_id):
        self.cursor.execute("UPDATE groups SET tag_online = TRUE WHERE id = ?", (group_id, ))
        self.conn.commit()

    def db_set_onlineoff_for_group_id(self, group_id):
        self.cursor.execute("UPDATE groups SET tag_online = FALSE WHERE id = ?", (group_id, ))
        self.conn.commit()

    def db_set_recentlyon_for_group_id(self, group_id):
        self.cursor.execute("UPDATE groups SET tag_recently = TRUE WHERE id = ?", (group_id, ))
        self.conn.commit()

    def db_set_recentlyoff_for_group_id(self, group_id):
        self.cursor.execute("UPDATE groups SET tag_recently = FALSE WHERE id = ?", (group_id, ))
        self.conn.commit()



    def db_get_user_info(self, user_id):
        self.cursor.execute("SELECT * FROM accounts WHERE id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result
    

    def db_get_user_info_where_phone(self, phone):
        self.cursor.execute("SELECT * FROM accounts WHERE phone = ?", (phone,))
        result = self.cursor.fetchone()
        return result
    

    def db_get_group_with_id(self, group_id):
        self.cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
        result = self.cursor.fetchone()
        return result
    

    def db_set_user_group(self, user_id, new_group):
        self.cursor.execute("UPDATE accounts SET group_id = ? WHERE id = ?", (new_group, user_id))
        self.conn.commit()
        return True



    def db_set_user_proxy(self, user_id, new_group):
        self.cursor.execute("UPDATE accounts SET proxy = ? WHERE id = ?", (new_group, user_id))
        self.conn.commit()
        return True



    
    def db_get_group_info(self, group_id):
        self.cursor.execute("SELECT * FROM groups WHERE id = ?", (group_id,))
        result = self.cursor.fetchone()
        return result





    def db_add_group(self, name):
        self.cursor.execute("INSERT INTO groups (name) VALUES (?)", (name, ))
        self.conn.commit()
        return True
    

    def db_del_group_with_id(self, text):
        self.cursor.execute("DELETE FROM groups WHERE id = ?", (text,))
        self.conn.commit()
        return True

    


    def db_check_user_with_group(self, text):
        self.cursor.execute("SELECT * FROM accounts WHERE group_id = ?", (text,))
        result = self.cursor.fetchall()
        return result




    def db_add_user(self, user_data):
        group_id = user_data['group_id']
        login = user_data['login']
        password = user_data['password']
        proxy = user_data['proxy']
        phone = user_data['phone']
        username = user_data['username']
        self.cursor.execute("INSERT INTO accounts (group_id, login, password, proxy, phone, username) VALUES (?, ?, ?, ?, ?, ?)", (group_id, login, password, proxy, phone, username))
        self.conn.commit()
        return True
    

    def db_del_user_with_id(self, text):
        self.cursor.execute("DELETE FROM accounts WHERE id = ?", (text,))
        self.conn.commit()
        return True
    


    def db_get_all_users(self):
        self.cursor.execute("SELECT * FROM accounts")
        result = self.cursor.fetchall()
        return result
    

    def db_set_user_dialogs(self, groups_string, user_id):
        self.cursor.execute("UPDATE accounts SET chats = ? WHERE id = ?", (groups_string, user_id))
        self.conn.commit()
        return True
    
    def db_set_user_dialogs_old(self, groups_string, user_id):
        self.cursor.execute("UPDATE accounts SET chats_old = ? WHERE id = ?", (groups_string, user_id))
        self.conn.commit()
        return True
    

    def db_set_user_stop(self, user_id):
        print('db_stop')
        self.cursor.execute("UPDATE accounts SET running = FALSE WHERE id = ?", (user_id,))
        self.conn.commit()
        return True
    

    def db_set_user_start(self, user_id):
        self.cursor.execute("UPDATE accounts SET running = TRUE WHERE id = ?", (user_id,))
        self.conn.commit()
        return True
    

    def db_update_count(self, user_id, count):
        self.cursor.execute("UPDATE accounts SET sms_count = ? WHERE id = ?", (count, user_id))
        self.conn.commit()
        return True
    
    def db_get_all_users_off(self):
        self.cursor.execute("SELECT * FROM accounts WHERE running = FALSE")
        result = self.cursor.fetchall()
        return result
    




    def db_get_pair_with_group_a(self, group_a):
        self.cursor.execute("SELECT * FROM pairs WHERE group_a = ?", (group_a,))
        result = self.cursor.fetchone()
        return result



    def db_delete_pair(self, pair_id):
        self.cursor.execute("DELETE FROM pairs WHERE id = ?", (pair_id,))
        self.conn.commit()
        return True
    




    def db_save_media(self, id, paths_as_string, text, group_b, capt):
        self.cursor.execute("INSERT INTO media (id, file_paths, message, group_b, capt) VALUES (?, ?, ?, ?, ?)", (id, paths_as_string, text, group_b, capt))
        self.conn.commit()
        return True
    


    def db_get_media_with_id(self, media_id):
        self.cursor.execute("SELECT * FROM media WHERE id = ?", (media_id,))
        result = self.cursor.fetchone()
        return result
    


    def db_save_photovideo(self, id, message, caption, group_b):
        self.cursor.execute("INSERT INTO photovideo (id, message, caption, group_b) VALUES (?, ?, ?, ?)", (str(id), message, caption, group_b))
        self.conn.commit()
        return True
    


    def db_get_photovideo_with_id(self, media_id):
        self.cursor.execute("SELECT * FROM photovideo WHERE id = ?", (media_id,))
        result = self.cursor.fetchone()
        return result




    def db_get_all_pairs(self):
        self.cursor.execute("SELECT * FROM pairs")
        result = self.cursor.fetchall()
        return result



    def db_add_pair_to_db(self, pair_data):
        group_a = pair_data['group_a']
        group_b = pair_data['group_b']
        type = pair_data['type']
        capt_a = pair_data['capt_a']
        capt_b = pair_data['capt_b']
        name = pair_data['name']
        self.cursor.execute("INSERT INTO pairs (group_a, group_b, type, capt_a, capt_b, name) VALUES (?, ?, ?, ?, ?, ?)", (group_a, group_b, type, capt_a, capt_b, name))
        self.conn.commit()
        return True



    def db_set_pause_to_pair(self, pair_id):
        self.cursor.execute("UPDATE pairs SET pause = TRUE WHERE id = ?", (pair_id,))
        self.conn.commit()


    def db_set_start_to_pair(self, pair_id):
        self.cursor.execute("UPDATE pairs SET pause = FALSE WHERE id = ?", (pair_id,))
        self.conn.commit()



    def db_check_and_create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pairs(
            id INTEGER PRIMARY KEY,
            group_a TEXT,
            group_b TEXT,
            type INTEGER,
            capt_a TEXT,
            capt_b TEXT,
            name TEXT,
            pause BOOLEAN DEFAULT FALSE
            )''')
        self.conn.commit()
        print("table pairs was created")


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS photovideo (
            id TEXT,
            message TEXT,
            caption TEXT,
            group_b TEXT
            )''')
        self.conn.commit()
        print('Table admin_messages was created')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS media (
            id TEXT,
            file_paths TEXT,
            message TEXT,
            group_b TEXT,
            capt TEXT
            )''')
        self.conn.commit()
        print('Table admin_messages was created')


        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_messages (
            user_id INTEGER,
            message TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
            )''')
        self.conn.commit()
        print('Table admin_messages was created')


#db = DbSpamer()



#db.db_path = db_path
#db.db_initialize()