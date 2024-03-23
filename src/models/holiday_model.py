from datetime import datetime

class HolidayModel:

    def __init__(self, id, city_id, description, start_date, end_date, price, image):
        self.id = id
        self.city_id = city_id
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.image = image
        # self.likes_count = likes_count


# Validating a new product insert:
    def validate_insert(self):
        current_date = datetime.now() 
        if not self.city_id: return "Missing city."
        if not self.description: return "Missing description."
        if not self.start_date: return "Missing start date."
        if not self.end_date: return "Missing end date."
        if not self.price: return "Missing price."
        if not self.image: return "Missing image."
        if len(self.description) < 10 or len(self.description) > 1000: return "description must be 10 to 1000 chars"
        if int(self.price) < 0 or int(self.price) > 10000: return "price must be 0 - 10000."
        if datetime.strptime(self.start_date, "%Y-%m-%d") < current_date: return "Start date cannot be a past date"
        if datetime.strptime(self.end_date, "%Y-%m-%d") < current_date: return "End date cannot be a past date"
        if datetime.strptime(self.end_date, "%Y-%m-%d") < datetime.strptime(self.start_date, "%Y-%m-%d"): return "End date can't be earlier than the start date"
        return None # No error.

    # Validating an existing product update:
    def validate_update(self):
        if not self.start_date: return "Missing start date."
        if not self.end_date: return "Missing end date."
        if not self.price: return "Missing price."
        if int(self.price) < 0 or int(self.price) > 10000: return "price must be 0 - 10000."
        if datetime.strptime(self.end_date, "%Y-%m-%d") < datetime.strptime(self.start_date, "%Y-%m-%d"): return "End date can't be earlier than the start date"
        return None # No error.


class Like:
    def __init__(self, user_id, holiday_id):
        self.user_id = user_id
        self.holiday_id = holiday_id
