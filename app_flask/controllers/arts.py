from flask import Flask, render_template, session, redirect, request
from app_flask import app
from app_flask.models.user import User
from app_flask.models.art import Art
from flask import flash


@app.route("/dashboard/loggedIn")
def user_dashboard():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    art = Art.get_all()
    return render_template("dashboard.html", user=user, art=art)

@app.route("/arts/new")
def new_arts_form():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template("create_arts.html", user=user)

@app.route("/arts/create", methods=["POST"])
def create_arts():
    if not Art.is_valid(request.form):
        return redirect("/arts/new")
    else:
        Art.create_valid_arts(request.form)
        return redirect("/dashboard/loggedIn")


@app.route("/arts/<art_id>/edit")
def show_edit_art(art_id):
    data = {"id" : art_id}
    art = Art.get_one(data)
    user_data = {"id" : session["user_id"]}
    user = User.get_by_id(user_data)
    return render_template("edit_arts.html", art = art, user=user)

@app.route("/arts/<art_id>", methods=["POST"])
def edit_art(art_id):
    art_id = {"id" : art_id}
    user_id = {"id" : session["user_id"]}
    valid_update = Art.update_arts(request.form, art_id, user_id)

    if not valid_update:
        return redirect("/dashboard/loggedIn")
    return  redirect("/dashboard/loggedIn")


@app.route("/arts/<art_id>/delete", methods=["POST"])
def delete_art(art_id):
    Art.delete_arts_by_id(art_id)
    return  redirect("/dashboard/loggedIn")

@app.route('/arts/<art_id>')
def show_art(art_id):
    data = {"id": art_id}
    art = Art.get_one(data)
    user_data = {'id': session['user_id']}
    user = User.get_by_id(user_data)
    return render_template("view_arts.html", art = art, user=user)

    

    








