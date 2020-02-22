import requests
import json
import re


# class to treate data from API openfoodfacts
class DbRequests():

    def __init__(self):
        # Call the parent class constructor
        super().__init__()

    # --Request api openfoodfacts categories
    def Request_categories(self):
        url_category = 'https://world.openfoodfacts.org/categories.json'
        json_data = requests.get(url_category).json()
        categories = []

        for each in json_data['tags']:
            category = {}

            id_categorie = each['id']
            category_name = each['name']  # collect item name
            # Removing a Single Character
            result = re.sub(r"\s+[a-zA-Z]\s+", " ", category_name)
            # Removing Non-Word Characters
            final_string = re.sub(r"[,@\'?\.$%_]", "", result, flags=re.I)

            if final_string != "":
                category["id"] = id_categorie
                category["nameCategory"] = final_string  # Add to dictionary
                categories.append(category)  # Add items dictionary to list

        return(categories)

    # --Request api openfoodfacts stores
    def Request_stores(self):
        url_stores = 'https://world.openfoodfacts.org/stores.json'
        json_data = requests.get(url_stores).json()
        stores = []

        for each in json_data['tags']:
            store = {}

            idstore = each['id']  # collect item name
            store_name = each['name']  # collect item name
            # Removing a Single Character
            result = re.sub(r"\s+[a-zA-Z]\s+", " ", store_name)
            # Removing Non-Word Characters
            final_string = re.sub(r"[,@\'?\.$%_]", "", result, flags=re.I)

            if final_string != "":
                store["id"] = idstore
                store["nameStore"] = final_string  # Add to dictionary
                stores.append(store)  # Add items dictionary to list

        return(stores)

    # --Request api openfoodfacts products
    def Request_products(self):
        for i in range(10):
            i += 1
            url_ingredients = ("https://world.openfoodfacts.org/cgi/search." +
                               "pl?search_terms=products&search_simple=1&" +
                               "action=process&page_size=1000" +
                               "&page={}&json=1".format(i))

            json_data = requests.get(url_ingredients).json()

            list_products = self.data_treatement(json_data)

            return(list_products)

    # teatement of strings
    def data_treatement(self, data):
        ingredients = []
        for each in data['products']:
            ingredient = {}

            pre = self.check_presence(each)
            if (pre is True):
                void = self.check_void(each)

                if (pre is True) and (void is True):
                    # collect item name
                    Namee_category = each['categories'].split(",")
                    categorie = Namee_category[0]
                    Name_category = categorie
                    Name_prod = each['product_name'].split(",")
                    Name_ingredients = Name_prod[0]

                    if 'stores' in each:
                        if each['stores'] != "":
                            Namee_Store = each['stores'].split(",")
                            Name_Store = Namee_Store[0]

                    if 'ingredients_text_debug' in each:
                        description_ingred = each['ingredients_text_debug']
                    else:
                        description_ingred = ""

                    if 'image_small_url' in each:
                        Image = each['image_small_url']

                    Url = each['url']

                    if 'nutrition_grade_fr' in each:
                        nutrition_grades = each['nutrition_grade_fr']
                    else:
                        nutrition_grades = "default"

                    # Add to dictionary
                    ingredient["nameAlim"] = Name_ingredients
                    ingredient["image"] = Image
                    ingredient["url"] = Url
                    ingredient["descriptionAlim"] = description_ingred
                    ingredient["nutritionGrade"] = nutrition_grades
                    ingredient["idCategory"] = Name_category
                    ingredient["idStore"] = Name_Store
                    # Add dictionary's items to list
                    ingredients.append(ingredient)

        return(ingredients)

    # check if data is present
    def check_presence(self, each):
        presence = False

        if ('stores' in each) and\
           ('categories'in each) and\
           ('product_name' in each) and\
           ('ingredients_text_debug' in each) and\
           ('image_small_url' in each) and\
           ('nutrition_grade_fr' in each) and\
           ('url' in each):
            presence = True

        return(presence)

    # check if variables not void
    def check_void(self, each):
        full = False

        if (each['stores'] != "") and\
           (each['categories'] != "") and\
           (each['product_name'] != "") and\
           (each['ingredients_text_debug'] != "") and\
           (each['image_small_url'] != "") and\
           (each['nutrition_grade_fr'] != "") and\
           (each['url'] != ""):
            full = True

        return(full)
