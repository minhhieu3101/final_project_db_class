from flask import Flask, render_template, request, redirect, url_for
import database
from datetime import datetime

app = Flask(__name__)

# List of guests,
@app.route("/")
@app.route("/list")
def get_list():
    guests = database.get_guest_list()
    return render_template("guest_list.html", guests=guests)

@app.route("/create_guest", methods=['GET', 'POST'])
def create_guest():
    if request.method == "GET":
        return render_template("create_guest.html")
    
    if request.method == "POST":
        data = dict(request.form)
        if database.check_user_exist(data["phone_number"], data["email"]) is True:
            raise ValueError('User is existed')
        database.create_data('guest', data)
        return redirect(url_for('get_list'))
    
@app.route("/update_guest/<id>", methods=['GET', 'POST'])
def update_guest(id):
    if request.method == "GET":
        guest = database.get_guest(id)
        return render_template("update_guest.html", guest = guest)
    
    if request.method == "POST":
        data = dict(request.form)
        database.update_guest(id, data)
        return redirect(url_for('get_list'))
    
@app.route("/delete_guest/<id>")
def delete_guest(id):
    database.delete_guest(id)
    return redirect(url_for('get_list'))

@app.route("/room_list")
def get_room_list():
    rooms = database.get_room_list()
    return render_template("room_list.html", rooms=rooms)

@app.route("/create_room", methods=['GET', 'POST'])
def create_room():
    if request.method == "GET":
        return render_template("create_room.html")
    
    if request.method == "POST":
        data = dict(request.form)
        database.create_data('room', data)
        return redirect(url_for('get_room_list'))

@app.route("/update_room/<id>", methods=['GET', 'POST'])
def update_room(id):
    room = database.get_room(id)
    if request.method == "GET":
        return render_template("update_room.html", room = room)
    
    if request.method == "POST":
        data = dict(request.form)
        if room["room_type"] != data["room_type"]:
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
        database.update_room(id, data)
        return redirect(url_for('get_room_list'))
    
@app.route("/delete_room/<id>")
def delete_room(id):
    database.delete_room(id)
    return redirect(url_for('get_room_list'))

@app.route("/book_room", methods=['POST'])
def book_room():
    data = dict(request.form)
    print(data)
    room = database.get_room_by_number(data["room_number"])
    guest = database.get_guest_by_phone_number(data["phone_number"])
    if len(room) == 0 or room.status == 'Unavailable':
        raise ValueError('Room is unavailable, please select another room')
    if len(guest) == 0:
        raise ValueError('Guest is not found')
    data["guest_id"] = guest["id"]
    data["room_id"] = room["id"]
    format_str = "%Y-%m-%dT%H:%M"
    datetime1 = datetime.strptime(data['check_in_date'], format_str)
    datetime2 = datetime.strptime(data["check_out_date"], format_str)
    time_difference = datetime2 - datetime1
    hours_difference = time_difference.total_seconds() / 3600
    print(hours_difference)
    data["total_price"] = room["price"] * hours_difference
    database.create_data('guest_room', data)
    room["status"] = 'Unavailable'
    return redirect(url_for('get_room_list'))