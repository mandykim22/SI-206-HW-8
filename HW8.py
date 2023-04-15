# Your name: Amanda KIm
# Your student id: 419200321
# Your email: mandykim@umich.edu
# List who you have worked with on this homework: n/a

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    return_dict = {}
    cur2 = con.execute("SELECT r.name, r.rating, c.category, b.building FROM restaurants r, categories c, buildings b WHERE r.category_id=c.id AND r.building_id=b.id")
    places = cur2.fetchall()
    for place in places:
        mini_dict = {"category": place[2], "building": place[3], "rating": place[1]}
        return_dict[place[0]] = mini_dict
    return return_dict
    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    return_dict = {}
    cur2 = con.execute("SELECT c.category, COUNT(r.id) FROM restaurants r, categories c WHERE r.category_id=c.id GROUP BY c.category ORDER BY COUNT(r.id) ASC")
    places = cur2.fetchall()
    for place in places:
        return_dict[place[0]] = place[1]
    plt.barh(list(return_dict.keys()), list(return_dict.values()))
    plt.title('Types of Restaurant on South Univeristy Ave')
    plt.ylabel('Restaurant Categories')
    plt.xlabel('Number of Restaurants')
    plt.xticks([0, 1, 2, 3, 4])
    plt.show()
    return return_dict

    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''

    con = sqlite3.connect(db)
    cur = con.cursor()
    return_dict = {}
    cur2 = con.execute("SELECT r.name FROM restaurants r, buildings b WHERE r.building_id=b.id AND b.building=? ORDER BY rating DESC", (building_num,))
    places = cur2.fetchall()
    return_list = []
    for place in places:
        return_list.append(place[0])
    return return_list
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    con = sqlite3.connect(db)
    cur = con.cursor()
    return_dict = {}
    return_dict2 = {}
    return_list = []
    cur2 = con.execute("select c.category, AVG(r.rating) FROM restaurants r, buildings b, categories c WHERE r.building_id=b.id AND r.category_id=c.id GROUP BY c.category ORDER BY AVG(r.rating) ASC")
    places = cur2.fetchall()
    i = 0
    for place in places:
        if(i == len(places) - 1):
            return_list.append((place[0], place[1]))
        return_dict[place[0]] = place[1]
        i += 1
    cur2 = con.execute("SELECT b.building, AVG(r.rating) FROM restaurants r, buildings b, categories c WHERE r.building_id=b.id AND r.category_id=c.id GROUP BY b.building ORDER BY AVG(r.rating) ASC")
    places = cur2.fetchall()
    i = 0
    for place in places:
        if(i == len(places) - 1):
            return_list.append((place[0], place[1]))
        return_dict2[str(place[0])] = place[1]
        i += 1

    plt.barh(list(return_dict.keys()), list(return_dict.values()))
    plt.title('Average Restaurant Ratings by Category')
    plt.ylabel('Categories')
    plt.xlabel('Ratings')
    plt.xticks([0, 1, 2, 3, 4, 5])
    plt.show()
    plt.barh(list(return_dict2.keys()), list(return_dict2.values()))
    plt.title('Average Restaurant Ratings by Building')
    plt.ylabel('Buildings')
    plt.xlabel('Ratings')
    plt.xticks([0, 1, 2, 3, 4, 5])
    plt.show()

    return return_list

    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
