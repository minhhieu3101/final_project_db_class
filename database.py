import sqlite3

connection = sqlite3.connect("hotels.db", check_same_thread=False)
connection.execute("PRAGMA foreign_keys = 1")

def create_data(table, data):
    cursor = connection.cursor()
    if table == 'guest':
        guests = cursor.execute("SELECT * FROM guests where phone_number = ? or email = ?", (data["phone_number"], data["email"])).fetchall()
        if len(guests) != 0:
            raise ValueError('This data is exist')
        cursor.execute("""
            INSERT INTO guests (name, phone_number, email) 
            VALUES (?, ?, ?)
        """, (data["name"], data["phone_number"], data["email"]))
    elif table == 'room':
        rooms = cursor.execute("SELECT * FROM rooms where name = ?", (data["name"])).fetchall()
        if len(rooms) != 0:
            raise ValueError('Room name is exist')
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
        room = cursor.execute("SELECT * FROM rooms WHERE id = ?", (int(data["room_id"]),)).fetchone()
        guest = cursor.execute("SELECT * FROM guests WHERE id = ?", (int(data["guest_id"]),)).fetchall()
        if room.status == 'Unavailable':
            raise ValueError('Room is unavailable, please select another room')
        if len(guest) == 0:
            raise ValueError('Guest is not found')
        cursor.execute("""
            INSERT INTO guest_rooms (guest_id, room_id, check_in_time, check_out_time, total_price) 
            VALUES (?, ?, ?, ?, ?)
        """, (data["guest_id"], data["room_id"], data["check_in_time"], data["check_out_time"], int(data["total_price"])))
    else:
        raise ValueError('Can not add')
    connection.commit()

#guest_table
def get_guest(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM guests where id = ?", (id,))
    return cursor.fetchone()

def get_guest_list():
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM guests """)
    guests = cursor.fetchall()
    guest_list = []
    
    # Create a list of pets with kind information by manually joining
    for guest in guests:
        guest_list.append({
            'id': guest[0],
            'name': guest[1],
            'phone_number': guest[2],
            'email': guest[3],
        })
    return guest_list

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

#room_table
def get_room(id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM rooms where id = ?", (id,))
    return cursor.fetchone()

def get_room_list():
    cursor = connection.cursor()
    cursor.execute(""" SELECT * FROM rooms """)
    rooms = cursor.fetchall()
    room_list = []
    
    # Create a list of pets with kind information by manually joining
    for room in rooms:
        room_list.append({
            'id': room[0],
            'room_number': room[1],
            'room_type': room[2],
            'price': room[3],
            'status': room[4]
        })
    return room_list