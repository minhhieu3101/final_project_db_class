CREATE TABLE guests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_number INTEGER NOT NULL,
    room_type TEXT NOT NULL CHECK (room_type IN ('Single', 'Twin', 'Double', 'Triple')),
    price INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'Available' CHECK (status IN ('Available', 'Unavailable'))
);

CREATE TABLE guest_rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in_time DATE NOT NULL,
    check_out_time DATE NOT NULL,
    total_price INTEGER NOT NULL,
    FOREIGN KEY (guest_id) REFERENCES guests(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);