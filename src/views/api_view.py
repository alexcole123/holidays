from flask import Blueprint, jsonify, make_response
from facades.holiday_facade import HolidayFacade
from models.client_errors import ResourceNotFoundError
from models.status_code import StatusCode

# Managing the entire view
api_blueprint = Blueprint("api_view", __name__) # "api_view" is the name of the view

# Create facade: 
holidays_facade = HolidayFacade()

#API for all holidays
@api_blueprint.route("/api/holidays")
def holidays():
    try:
        holidays =  holidays_facade.get_all_holidays()
        return jsonify(holidays)
    except Exception as err:
        json = jsonify({"error": err.message})
        return make_response(json, StatusCode.InternalServerError.value)

#API for one holiday
@api_blueprint.route("/api/holidays/<int:id>")
def holiday(id):
    try:
        holiday =  holidays_facade.get_one_holiday(id)
        return jsonify(holiday)
    except ResourceNotFoundError as err:
        json = jsonify({"error": err.message})
        return make_response(json, StatusCode.NotFound.value)
