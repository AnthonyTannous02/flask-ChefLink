from util.mg_interfacer import MG_Interfacer
from flask_pymongo.wrappers import Database
from flask import current_app


class Mongo(MG_Interfacer):
    def __init__(self):
        super().__init__()

    def search_food(self, search: str) -> list:
        try:
            if not search.isalnum():
                return []
            foods = list(
                self._conn.Food.find(
                    {"name": {"$regex": search, "$options": "i"}},
                    {
                        "name": 1,
                        "id_food": 1,
                        "price": 1,
                        "total_rating": 1,
                        "picture": 1,
                        "_id": 0,
                    },
                )
            )
        except:
            raise Exception("DB_CONNECTION_FAILED")
        
        for food in foods:
            try:
                food_id = food["id_food"]
            except Exception as e:
                print(str(e))
                raise Exception("FOOD_NOT_FOUND")
            try:
                food["chef_name"] = self._conn.Chef.find_one(
                    {"foodList": food_id},
                    {
                        "username": 1,
                        "id_food": {"$arrayElemAt": ["$foodList", 0]},
                        "_id": 0,
                    },
                )["username"]
            except Exception as e:
                print(str(e))
                print(food)
                raise Exception("CHEF_NOT_FOUND")
        return foods

    def search_chefs(self, search: str) -> list:  ## TODO: Improve this function
        try:
            if not search.isalnum():
                return []
            chefs = list(
                self._conn.Chef.find(
                    {"username": {"$regex": search, "$options": "i"}},
                    {"username": 1, "uUID": 1, "p_URL": 1, "_id": 0},
                    ## TODO: Add total rating for the chef
                )
            )
            print(chefs)
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return chefs

    def filter_food_by(self, filter: str, select: str) -> list:
        try:
            filter = "category." + filter
            foods = list(
                self._conn.Food.find(
                    {filter: select},
                    {
                        "name": 1,
                        "id_food": 1,
                        "price": 1,
                        "total_rating": 1,
                        "picture": 1,
                        "_id": 0,
                    },
                )
            )
            for food in foods:
                food_id = food["id_food"]
                food["chef_name"] = self._conn.Chef.find_one(
                    {"foodList": food_id},
                    {
                        "username": 1,
                        "id_food": {"$arrayElemAt": ["$foodList", 0]},
                        "_id": 0,
                    },
                )["username"]
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return foods

    def get_food_min_info(self, food_ids: list) -> dict:
        food = {}
        try:
            food = list(self._conn.Food.find(
                {"id_food": {"$in": food_ids}},
                {
                    "name": 1,
                    "id_food": 1,
                    "price": 1,
                    "total_rating": 1,
                    "picture": 1,
                    "timing": 1,
                    "_id": 0,
                },
            ))
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return food

    def get_food_full_info(self, food_ids: str) -> dict:
        food = {}
        try:
            food = list(self._conn.Food.find(
                {"id_food": {"$in": food_ids}},
                {
                    "_class": 0,
                    "_id": 0,
                },
            ))
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return food

    def find_chef_by_food(self, food_id):
        chef = self._conn.Chef.find_one(
            {"foodList": food_id},
            {
                "username": 1,
                "firstName": 1,
                "lastName": 1,
                "_id": 0,
            },
        )
        if len(chef) == 0:
            raise Exception("CHEF_NOT_FOUND")
        return chef

    def append_food_to_chef(self, chef_id, id_food):
        try:
            self._conn.Chef.update_one(
                {"uUID": chef_id},
                {"$push": {"foodList": id_food}},
            )
        except:
            raise Exception("DB_CONNECTION_FAILED")

    def remove_food_from_chef(self, chef_id, id_food):
        try:
            self._conn.Chef.update_one(
                {"uUID": chef_id},
                {"$pull": {"foodList": id_food}},
            )
        except:
            raise Exception("DB_CONNECTION_FAILED")

    def get_chef_foods(self, chef_id: str) -> list:
        foods: list = []
        try:
            food_ids = list(
                self._conn.Chef.find(
                    {"uUID": chef_id},
                    {
                        "foodList": 1,
                        "_id": 0,
                    },
                )
            )
            food_ids = food_ids[0]["foodList"]
            foods = list(
                self._conn.Food.find(
                    {"id_food": {"$in": food_ids}},
                    {
                        "name": 1,
                        "id_food": 1,
                        "total_rating": 1,
                        "_id": 0,
                    },
                )
            )
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return foods

    # def search_food_by_chef(self, chef: str) -> list:
    #     foods = []
    #     food_ids = []
    #     chefs = []
    #     query_chefs = self.search_chefs(chef)
    #     chefs = [c["username"] for c in query_chefs]
    #     chef_food_map: dict = {}
    #     try:
    #         for x in list(self._conn.Chef.find({"username": {"$in": chefs}}, {"foodList": 1, "username": 1, "_id": 0})):
    #             for food_id in x["foodList"]:
    #                 chef_food_map[food_id] = x["username"]
    #                 food_ids.append(food_id)
    #         foods = list(
    #             self._conn.Food.find(
    #                 {"id_food": {"$in": food_ids}},
    #                 {
    #                     "name": 1,
    #                     "id_food": 1,
    #                     "price": 1,
    #                     "total_rating": 1,
    #                     "picture": 1,
    #                     "_id": 0,
    #                 },
    #             )
    #         )
    #         for food in foods:
    #             food_id = food["id_food"]
    #             food["chef_name"] = chef_food_map[food_id]
    #     except Exception as e:
    #         raise Exception("DB_CONNECTION_FAILED")
    #     return foods
