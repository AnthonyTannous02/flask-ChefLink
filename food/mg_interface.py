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
                self.__get_conn().Food.find(
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
            for food in foods:
                food_id = food["id_food"]
                food["chef_name"] = self.__get_conn().Chef.find_one(
                    {"id_food_list": food_id},
                    {
                        "username": 1,
                        "id_food": {"$arrayElemAt": ["$id_food_list", 0]},
                        "_id": 0,
                    },
                )["username"]
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return foods

    def search_chefs(self, search: str) -> list:  ## TODO: Improve this function
        try:
            if not search.isalnum():
                return []
            chefs = list(
                self.__get_conn().Chef.find(
                    {"username": {"$regex": search, "$options": "i"}},
                    {"username": 1, "_id": 0},
                    ## TODO: Add chef ppf url here
                )
            )
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return chefs

    def filter_food_by(self, filter: str, select: str) -> list:
        try:
            filter = "category." + filter
            foods = list(
                self.__get_conn().Food.find(
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
                food["chef_name"] = self.__get_conn().Chef.find_one(
                    {"id_food_list": food_id},
                    {
                        "username": 1,
                        "id_food": {"$arrayElemAt": ["$id_food_list", 0]},
                        "_id": 0,
                    },
                )["username"]
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return foods

    def get_food_min_info(self, food_ids: str) -> dict:
        food = {}
        try:
            food = list(self.__get_conn().Food.find(
                {"id_food": {"$in": food_ids}},
                {
                    "name": 1,
                    "id_food": 1,
                    "price": 1,
                    "total_rating": 1,
                    "picture": 1,
                    "_id": 0,
                },
            ))
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return food
    
    def get_food_full_info(self, food_ids: str) -> dict:
        food = {}
        try:
            food = list(self.__get_conn().Food.find(
                {"id_food": {"$in": food_ids}},
                {
                    "_class": 0,
                    "_id": 0,
                },
            ))
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return food

    # def search_food_by_chef(self, chef: str) -> list:
    #     foods = []
    #     food_ids = []
    #     chefs = []
    #     query_chefs = self.search_chefs(chef)
    #     chefs = [c["username"] for c in query_chefs]
    #     chef_food_map: dict = {}
    #     try:
    #         for x in list(self.__get_conn().Chef.find({"username": {"$in": chefs}}, {"id_food_list": 1, "username": 1, "_id": 0})):
    #             for food_id in x["id_food_list"]:
    #                 chef_food_map[food_id] = x["username"]
    #                 food_ids.append(food_id)
    #         foods = list(
    #             self.__get_conn().Food.find(
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

    def __get_conn(self) -> Database:
        return self._conn
