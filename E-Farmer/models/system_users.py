import connector


# Function for system_users login
def system_users_login(email, psw):
    conn = connector.connector()

    query = ''' SELECT id, name, email FROM system_users WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def check_email_exist(email):
    conn = connector.connector()

    query = ''' SELECT COUNT(id) FROM system_users WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def check_system_user_exist_by_id(id):
    conn = connector.connector()

    query = ''' SELECT COUNT(id) FROM system_users WHERE id = %s '''
    values = (int(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for add system user
def add_system_user(name, email, psw):
    conn = connector.connector()

    query = ''' INSERT INTO system_users (name, email, psw) 
                            VALUES (%s, %s, %s) '''
    values = (str(name), str(email), str(psw))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for get system users
def get_all_system_users():
    conn = connector.connector()

    query = ''' SELECT id, name, email FROM system_users '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get system users without logged user
def get_all_system_users_without_login(id):
    conn = connector.connector()

    query = ''' SELECT id, name, email FROM system_users WHERE id != %s '''

    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get system user details
def get_system_user_details(id):
    conn = connector.connector()

    query = ''' SELECT id, name, email FROM system_users WHERE id = %s '''

    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update system user details
def update_system_user_details(id, name):
    conn = connector.connector()

    query = ''' UPDATE system_users SET name = %s WHERE id = %s '''
    values = (str(name), int(id))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for update system user psw
def update_system_user_psw(id, psw):
    conn = connector.connector()

    query = ''' UPDATE system_users SET psw = %s WHERE id = %s '''
    values = (str(psw), int(id))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for delete system user
def delete_system_user(id):
    conn = connector.connector()

    query = ''' DELETE FROM system_users WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(query, value)

    conn.commit()
    return cur.rowcount
