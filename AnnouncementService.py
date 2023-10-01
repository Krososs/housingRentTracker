from flask import jsonify
from Utils.Database import Database


class AnnouncementService:

    @staticmethod
    def price_meet_preferences(announcement, preferences):
        return announcement['Price'] is not None and announcement['Price'] >= preferences['Rent_min'] and announcement[
            'Price'] <= preferences['Rent_max']

    @staticmethod
    def surface_meet_preferences(announcement, preferences):
        return announcement['Surface'] is not None and announcement['Surface'] >= preferences['Surface_min'] and \
            announcement[
                'Surface'] <= preferences['Surface_max']

    @staticmethod
    def rooms_meet_preferences(announcement, preferences):
        return announcement['Rooms'] is not None and announcement['Rooms'] >= preferences['Rooms_min'] and \
            announcement[
                'Rooms'] <= preferences['Rooms_max']

    @staticmethod
    def announcement_meet_preferences(announcement, preferences):
        return AnnouncementService.price_meet_preferences(announcement,
                                                          preferences) and AnnouncementService.surface_meet_preferences(
            announcement, preferences) and AnnouncementService.rooms_meet_preferences(announcement, preferences)

    @staticmethod
    def get_average_rent_price(result_announcements):
        total = 0
        for announcement in result_announcements:
            total += announcement['Price']
        if len(result_announcements) == 0:
            return 0
        return total / len(result_announcements)

    @staticmethod
    def get_announcements(preferences):
        data = Database.get_announcements()
        result_announcements = []
        result = []
        for record in data.find():
            result_announcements = []
            for city in preferences['Cities']:
                total_announcements = record[city]['Number_of_announcements']
                city_announcements = []
                for announcement in record[city]['Announcements']:
                    if AnnouncementService.announcement_meet_preferences(announcement, preferences):
                        city_announcements.append(announcement)
                city_data = {
                    'City': city,
                    'Total_announcements': total_announcements,
                    'Result_announcements': len(city_announcements),
                    'Average_rent_price': round(AnnouncementService.get_average_rent_price(city_announcements), 2),
                    'Average_rent_price_per_m_2': None
                }
                result_announcements.append(city_data)

            result.append({
                'Date': record['Date'],
                'Result': result_announcements
            })
        return jsonify(result)
