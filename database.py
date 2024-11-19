import sqlite3

connection = sqlite3.connect("hotels.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

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
            raise ValueError('Room type is undefined')
        cursor.execute("""
            INSERT INTO rooms (name, room_type, price) 
            VALUES (?, ?, ?)
        """, (data["name"], data["room_type"], data["price"]))
    elif table == 'guest_room':
        room = cursor.execute("SELECT * FROM rooms WHERE id = ?", (int(data["room_id"]),))
        guest = cursor.execute("SELECT * FROM guests WHERE id = ?", (int(data["guest_id"]),))
        if room.status == 'Unavailable':
            raise ValueError('Room is unavailable, please select another room')
        elif guest is None:
            raise ValueError('Guest is not found')
        cursor.execute("""
            INSERT INTO guest_rooms (guest_id, room_id, check_in_time, check_out_time, total_price) 
            VALUES (?, ?, ?, ?, ?)
        """, (data["guest_id"], data["room_id"], data["check_in_time"], data["check_out_time"], int(data["total_price"])))
    else:
        raise ValueError('Can not add')
    connection.commit()

#guest_table

def get_guest_list():
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM guests """)
    guests = cursor.fetchall()
    return guests

def delete_guest(id):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("DELETE FROM guests WHERE id = ?", (id,))
    connection.commit()

def update_guest(id, data):
    cursor = connection.cursor()
    id = int(id)
    cursor.execute("""
            UPDATE guests 
            SET name=?, phone_number=?, email=?
            WHERE id=?
        """, (data["name"], data["phone_number"], data["email"],id))
    connection.commit()
