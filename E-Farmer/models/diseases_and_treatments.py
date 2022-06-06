import connector


# Function for add disease name
def add_diseases_and_treatments(plant_name, disease_name, details, treatments, image):
    conn = connector.connector()

    query = ''' INSERT INTO diseases_and_treatments (plant_name, disease_name, details, treatments, image) 
                            VALUES (%s, %s, %s, %s, %s) '''
    values = (str(plant_name), str(disease_name),
              str(details), str(treatments), str(image))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for get diseases and treatments
def get_all_diseases_and_treatments():
    conn = connector.connector()

    query = ''' SELECT id, plant_name, disease_name, details, treatments, image FROM diseases_and_treatments '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get diseases and treatments details
def get_diseases_and_treatments_details(id):
    conn = connector.connector()

    query = ''' SELECT id, plant_name, disease_name, details, treatments, image FROM diseases_and_treatments WHERE id = %s '''

    values = (int(id),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for update diseases and treatments update
def update_diseases_and_treatments_update(id, plant_name, disease_name, details, treatments):
    conn = connector.connector()

    query = ''' UPDATE diseases_and_treatments SET 
                        plant_name = %s, disease_name = %s, details = %s, treatments = %s WHERE id = %s '''
    values = (str(plant_name), str(disease_name),
              str(details), str(treatments), int(id))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for update diseases and treatments image update
def update_diseases_and_treatments_image_update(id, image):
    conn = connector.connector()

    query = ''' UPDATE diseases_and_treatments SET image = %s WHERE id = %s '''
    values = (str(image), int(id))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    return cur.rowcount


# Function for delete diseases and treatments
def delete_diseases_and_treatments(id):
    conn = connector.connector()

    query = ''' DELETE FROM diseases_and_treatments WHERE id = %s '''
    value = (str(id),)
    cur = conn.cursor()
    cur.execute(query, value)

    conn.commit()
    return cur.rowcount
