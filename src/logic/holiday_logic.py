from utils.dal import DAL
from utils.image_handler import ImageHandler

class HolidayLogic:
    def __init__(self):
        self.dal = DAL()

    def get_all_holidays(self):
        sql = """
        SELECT holidays.*, cities.city AS city, COUNT(likes.holiday_id) AS likes_count
        FROM holidays
        JOIN cities ON holidays.city_id = cities.id
        LEFT JOIN likes ON holidays.id = likes.holiday_id
        GROUP BY holidays.id
        ORDER BY holidays.start_date
        """
        holidays = self.dal.get_table(sql)
        return holidays

    # New method to get likes count for a holiday
    def get_likes_count(self, id):
        sql = "SELECT COUNT(holiday_id) As likes_count FROM likes WHERE holiday_id = %s"
        result = self.dal.get_scalar(sql, (id, ))
        return result["likes_count"]

    #get all vacations users liked
    def get_liked_holidays_by_user(self, id):
        sql = "Select holiday_id From likes Where user_id=%s"
        liked_holidays = self.dal.get_table(sql, (id, ))
        return liked_holidays


    #show holiday details
    def get_one_holiday(self, id):
        sql = "Select holidays.*, cities.city As city From holidays Join cities On holidays.city_id = cities.id WHERE holidays.id = %s;"
        return self.dal.get_scalar(sql, (id, ))

    #add new holiday
    def add_holiday(self, holiday):
        image_name = ImageHandler.save_image(holiday.image)
        sql = "INSERT INTO holidays(city_id, description, start_date, end_date, price, image_name) VALUES (%s, %s, %s, %s, %s, %s)"
        self.dal.insert(sql, (holiday.city_id, holiday.description, holiday.start_date, holiday.end_date, holiday.price, image_name))

    #update existing holiday
    def update_holiday(self, holiday):
        old_image_name = self.__get_old_image_name(holiday.id)
        image_name = ImageHandler.update_image(old_image_name, holiday.image)
        sql = "Update holidays Set city_id = %s, description = %s, start_date = %s, end_date = %s, price = %s, image_name=%s Where id = %s"
        self.dal.update(sql, (holiday.city_id, holiday.description ,holiday.start_date, holiday.end_date, holiday.price, image_name, holiday.id))

    #remove holiday
    def delete_holiday(self, holiday_id):
        image_name = self.__get_old_image_name(holiday_id)
        ImageHandler.delete_image(image_name)
        sql = "DELETE FROM holidays WHERE id = %s"
        self.dal.delete(sql, (holiday_id,))


    # Add the like to the Likes table
    def add_like(self, user_id, holiday_id):    
        sql = "INSERT INTO Likes VALUES (%s, %s)"
        self.dal.insert(sql, (user_id, holiday_id))

    # Delete the like from the Likes table
    def remove_like(self, user_id, holiday_id):
        sql = "DELETE FROM Likes WHERE user_id = %s AND holiday_id = %s"
        self.dal.delete(sql, (user_id, holiday_id))

    # Delete the like from the Likes table
    # def remove_like(self, holiday_id):
    #     sql = "DELETE FROM Likes WHERE holiday_id = %s"
    #     self.dal.delete(sql, (holiday_id,))

    def get_all_cities(self):
        sql = "SELECT * FROM cities"
        return self.dal.get_table(sql)
    
    def __get_old_image_name(self, id):
        sql = "SELECT image_name FROM holidays WHERE id=%s"
        result = self.dal.get_scalar(sql, (id, ))
        return result["image_name"]

    def close(self):
        self.dal.close()
