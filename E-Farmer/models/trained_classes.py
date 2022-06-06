import connector


# Function for add disease name
def add_trained_class(disease_name, plant_name, date):
    conn = connector.connector()

    query = ''' INSERT INTO trained_classes (disease_name, plant_name, date) 
                            VALUES (%s, %s, %s) '''
    values = (str(disease_name), str(plant_name), str(date))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for get trained classes
def get_all_trained_classes():
    conn = connector.connector()

    query = ''' SELECT id, disease_name, plant_name, date FROM trained_classes '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get trained class details
def get_trained_class_details(id):
    conn = connector.connector()

    query = ''' SELECT id, disease_name, plant_name, date FROM trained_classes WHERE id = %s '''

    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update trained class update
def update_trained_class_update(id, disease_name, plant_name):
    conn = connector.connector()

    query = ''' UPDATE trained_classes SET disease_name = %s, plant_name = %s WHERE id = %s '''
    values = (str(disease_name), str(plant_name), int(id))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for delete trained class
def delete_trained_class(id):
    conn = connector.connector()

    query = ''' DELETE FROM trained_classes WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(query, value)

    conn.commit()
    return cur.rowcount
