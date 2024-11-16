import sqlite3

connection = sqlite3.connect("hotels.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

#guest_table

def get_guest_list():
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM guests """)
    guests = cursor.fetchall()
    return guests

def create_data(table, data):
    cursor = connection.cursor()
    if table == 'guest':
        cursor.execute("""
            INSERT INTO guests (name, phone_number, email) 
            VALUES (?, ?, ?)
        """, (data["name"], data["phone_number"], data["email"]))
    elif table == 'room':
        if data['room_type'] == 'Single':
            data['price'] = 50
        elif data['room_type'] == 'Twin':
            data['price'] = 100
        elif data['room_type'] == 'Double':
            data['price'] = 120
        elif data['room_type'] == 'Triple':
            data['price'] = 150
        else:
            return ValueError()
        cursor.execute("""
            INSERT INTO rooms (name, room_type, price) 
            VALUES (?, ?, ?)
        """, (data["name"], data["room_type"], data["price"]))
    elif table == 'guest_room':
        
        
    connection.commit()
