from flask import Blueprint, render_template, send_file, redirect, url_for, request, jsonify, session
from facades.holiday_facade import HolidayFacade
from facades.auth_facade import AuthFacade
from models.role_model import RoleModel
from utils.image_handler import ImageHandler
from models.client_errors import ResourceNotFoundError, ValidationError, AuthError
from datetime import date

# Managing the entire view
holidays_blueprint = Blueprint("holidays_view", __name__) # "holidays_view" is the name of the view

# Create facade: 
holidays_facade = HolidayFacade()
auth_facade = AuthFacade()

@holidays_blueprint.route("/holidays") # Route
def user_list(): # View Function
    try:
        auth_facade.block_anonymous()
        user = session.get("current_user")
        holidays_facade.get_liked_holidays_for_holiday(user)
        holidays = holidays_facade.get_all_holidays_with_likes_count()
        error = request.args.get("error")
        if user["role_id"] == RoleModel.User.value:
            return render_template("user_holidays.html", holidays=holidays, error=error, active="user_list")
        return render_template("admin_holidays.html", holidays=holidays, error=error, active="user_list")
    except AuthError as err: 
        return redirect(url_for("auth_view.login", error=err.message)) # Send error to url query string

@holidays_blueprint.route("/holidays/admin")
def admin_list():
    try:
        auth_facade.block_non_admin()
        all_holidays = holidays_facade.get_all_holidays()
        return render_template("admin_holidays.html", holidays=all_holidays, active="admin_list")
    except AuthError as err:
        return redirect(url_for("auth_view.login", error = err.message)) 


# Display single holiday:
@holidays_blueprint.route("/holidays/details/<int:id>") # <int:id> is called a route parameter
def details(id):
    try:
        auth_facade.block_anonymous()
        one_holiday = holidays_facade.get_one_holiday(id)
        return render_template("details.html", holiday = one_holiday)
    except AuthError as err: 
        return redirect(url_for("auth_view.login", error = err.message)) 
    except ResourceNotFoundError as err:
        return render_template("404.html", error = err.message)

# Return image file:
@holidays_blueprint.route("/holidays/images/<string:image_name>")
def get_image(image_name):
    image_path = ImageHandler.get_image_path(image_name)
    return send_file(image_path) # Returns a complete file (an image file with pixels of the image...)

# Adding new holiday:
@holidays_blueprint.route("/holidays/new", methods=["GET", "POST"])
def insert():
    try:
        auth_facade.block_non_admin()
        if request.method == "GET": 
            # Fetch countries
            all_cities = holidays_facade.get_all_cities()
            current_date = date.today().isoformat()
            return render_template("insert.html", cities=all_cities, active="insert", current_date=current_date)
        holidays_facade.add_holiday()
        return redirect(url_for("holidays_view.admin_list"))
    except AuthError as err: 
        return redirect(url_for("auth_view.login", error=err.message)) # Send error to url query string
    except ValidationError as err:
        all_cities = holidays_facade.get_all_cities()  # Fetch cities again
        return render_template("insert.html", cities=all_cities, error=err.message)


# Updating existing holiday:
@holidays_blueprint.route("/holidays/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    try:
        auth_facade.block_non_admin()
        if request.method == "GET": 
            all_cities = holidays_facade.get_all_cities()
            one_holiday = holidays_facade.get_one_holiday(id)
            image_name = one_holiday['image_name']  # Assuming 'image_name' is the column name in your database
            return render_template("edit.html", cities=all_cities, holiday = one_holiday, image_name=image_name,)
        holidays_facade.update_holiday()
        return redirect(url_for("holidays_view.admin_list"))
    except AuthError as err: 
        return redirect(url_for("auth_view.login", error = err.message)) # Send error to url query string
    except ResourceNotFoundError as err:
        return render_template("404.html", error = err.message) 
    except ValidationError as err:
        all_cities = holidays_facade.get_all_cities()  # Fetch cities again
        return render_template("edit.html", cities=all_cities, error = err.message, holiday = err.model)

# Delete existing holiday:
@holidays_blueprint.route("/holidays/delete/<int:id>")
def delete(id):
    try:
        auth_facade.block_non_admin()
        holidays_facade.delete_holiday(id)
        return redirect(url_for("holidays_view.admin_list"))
    except AuthError as err: 
        return redirect(url_for("auth_view.login", error = err.message)) # Send error to url query string


# Get data and updates likes table
@holidays_blueprint.route("/holidays/update-likes", methods=["POST"])
def update_likes():
    try:
        data = request.json
        holidays_facade.update_likes(data)
        return jsonify({"message": "Like added"}), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400  # Return 400 Bad Request on error
    