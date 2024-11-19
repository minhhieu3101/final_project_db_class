from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

# List of pets, showing related kind information
@app.route("/")
@app.route("/list")
def get_list():
    guests = database.get_guest_list()
    return render_template("list.html", guests=guests)

@app.route("/create", methods=['GET', 'POST'])
def create_guest():
    guests = database.create_data('guests', )
    # if request.method == 'GET':
    #     kinds = database.retrieve_kinds()
    #     return render_template("create.html", kinds=kinds)
    
    data = dict(request.form)
    guests = database.create_data('guests', data)
    return redirect(url_for('get_list'))