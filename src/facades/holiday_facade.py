from logic.holiday_logic import HolidayLogic
from flask import jsonify, request, session
from models.holiday_model import HolidayModel
from models.client_errors import ResourceNotFoundError, ValidationError


class HolidayFacade:

    def __init__(self):
        self.logic = HolidayLogic()

    def get_all_holidays(self):
        return self.logic.get_all_holidays()

    def get_all_holidays_with_likes_count(self):
        holidays = self.logic.get_all_holidays()

        # Iterate through each holiday and update the likes count
        for holiday in holidays:
            likes = self.logic.get_likes_count(holiday['id'])
            holiday['likes'] = likes

        return holidays

    def get_liked_holidays_for_holiday(self, user):
        #get dictionary of liked holidays
        liked_holidays_dict = self.logic.get_liked_holidays_by_user(user["id"])
        #get list of liked holidays
        like_holidays_list = [holiday["holiday_id"]for holiday in liked_holidays_dict]
        user["liked_holidays"] = like_holidays_list
        session["current_user"] = user

    # Get one holiday:

    def get_one_holiday(self, id):
        holiday = self.logic.get_one_holiday(id)
        if not holiday:
            raise ResourceNotFoundError(id)
        return holiday

    # Add new Holiday
    def add_holiday(self):
        city = request.form.get("city_id")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        price = request.form.get("price")
        image = request.files["image"]
        holiday = HolidayModel(None, city, description,
                               start_date, end_date, price, image)
        error = holiday.validate_insert()
        if error:
            raise ValidationError(error, holiday)
        self.logic.add_holiday(holiday)

    # Update existing holiday
    def update_holiday(self):
        id = request.form.get("id")
        city = request.form.get("city_id")
        description = request.form.get("description")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        price = request.form.get("price")
        image = request.files["image"]
        holiday = HolidayModel(id, city, description,
                               start_date, end_date, price, image)
        error = holiday.validate_update()
        if error:
            raise ValidationError(error, holiday)
        self.logic.update_holiday(holiday)

    # Delete existing product:

    def delete_holiday(self, id):
        self.logic.delete_holiday(id)
    
    def update_likes(self, data):
        user = session.get("current_user")

        holiday_id = data.get("holiday_id")

        if holiday_id in user["liked_holidays"]:
            # Holiday already liked, so remove the like
            self.logic.remove_like(user["id"], holiday_id)
            user["liked_holidays"].remove(holiday_id)  # Remove from user's liked holidays list
        else:
            # Holiday not liked yet, so add the like
            self.logic.add_like(user["id"], holiday_id)
            user["liked_holidays"].append(holiday_id)  # Add to user's liked holidays list
        
        return jsonify({}), 200

    def get_all_cities(self):
        return self.logic.get_all_cities()

    # Close resources:

    def close(self):
        self.logic.close()
