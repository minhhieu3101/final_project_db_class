from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# List of pets, showing related kind information
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
        database.create_data('guest', data)
        return redirect(url_for('create_guest'))
    
@app.route("/update_guest/<id>", methods=['GET', 'POST'])
def update_guest(id):
    if request.method == "GET":
        guest = database.get_guest(id)
        return render_template("update_guest.html", guest = guest)
    
    if request.method == "POST":
        data = dict(request.form)
        database.update_guest(id, data)
        return redirect(url_for('update_guest'))
    
@app.route("/delete_guest/<id>")
def delete_guest(id):
    database.delete_guest(id)
    return redirect(url_for('get_list'))
