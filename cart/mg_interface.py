from util.mg_interfacer import MG_Interfacer
from flask_pymongo.wrappers import Database
import uuid
from decimal import Decimal as D
from bson.decimal128 import Decimal128 as Dx
import random
import time

delivery_people_names = ["Samir Patel", "Maria Garcia", "Ahmed Khan", "Emily Nguyen", "Carlos Rodriguez", 
                        "Priya Sharma", "Daniel Chang", "Fatima Ali", "Liam O'Connor", "Sofia Hernandez", 
                        "Amir Khan", "Olivia Smith", "Juan Martinez", "Leila Rahman", "Miguel Santos", 
                        "Isabella Rossi", "Rashid Ahmed", "Hannah Johnson", "Rafael Silva", "Mei Chen"]


class Mongo(MG_Interfacer):
    def __init__(self):
        super().__init__()

    def check_location_exists(self, loc: str, role: str) -> None:
        if role == "customer":
            cursor = self._conn.Customer.find_one({"locations": loc})
        else:
            cursor = self._conn.Chef.find_one({"locations": loc})
        if not cursor or len(cursor) < 1:
            raise Exception("LOCATION_NOT_FOUND")
        return

    def get_stand_by_cart(self, uUID, only_id=False):
        try:
            self._conn.Cart.create_index([("user_id", 1), ("status", 1)])

            args = {"_class": 0, "user_id": 0, "_id": 0}
            if only_id:
                args = {"_id": 0, "iD": 1}

            cart = self._conn.Cart.find_one(
                {"user_id": uUID, "status": "StandBy"},
                args,
            )

            if cart and "price" in cart:
                cart["price"] = str(cart["price"])

        except:
            raise Exception("DB_CONNECTION_FAILED")
        return cart

    def create_cart(self, uUID):
        try:
            cart = {
                "iD": "cart_" + uuid.uuid4().hex,
                "location": "",
                "price": Dx("0.0"),
                "bundle_ids": [],
                "order_date": "",
                "completion_time": "",
                "status": "StandBy",
                "delivery_person": "",
                "payment_method": "",
                "user_id": uUID,
            }

            self._conn.Cart.insert_one(cart)
            del cart["_id"]
        except:
            raise Exception("DB_CONNECTION_FAILED")
        return cart

    def add_to_cart(
        self, uUID, food_id, options: dict, spec_inst: str, qty: int = 1
    ):  ## TODO Keep an eye on performance
        chosen_options = []
        total_bundle_price = D("0")
        bundle_id = "bundle_" + uUID[-6:] + "_" + uuid.uuid4().hex
        t1s = time.perf_counter()
        cart = self.get_stand_by_cart(uUID, only_id=True)
        if cart is None:
            cart = self.create_cart(uUID)
        t1e = time.perf_counter()
        print(t1e - t1s)

        t1s = time.perf_counter()
        food = (
            self._conn.Food.find({"id_food": food_id}, {"_class": 0, "_id": 0})
            .limit(1)
            .next()
        )
        if food is None:
            raise Exception("FOOD_NOT_FOUND")
        total_bundle_price += D(str(food["price"]))
        t1e = time.perf_counter()
        print(t1e - t1s)

        t1s = time.perf_counter()
        try:
            for option_check in food["options"]:
                if options[option_check["option_name"]]:
                    chosen_options.append(option_check["option_name"])
                    total_bundle_price += D(str(option_check["option_price"]))
        except:
            raise Exception("INVALID_OPTIONS")

        t1e = time.perf_counter()
        print(t1e - t1s)

        t1s = time.perf_counter()
        total_bundle_price *= D(str(qty))

        chef_id = self._conn.Chef.find_one(
                {
                    "foodList": food_id
                },
                {
                    "_id": 0,
                    "uUID": 1
                }
            )
        if chef_id is None:
            raise Exception("CHEF_NOT_FOUND")
        
        bundle = {
            "id_bundle": bundle_id,
            "id_food": food_id,
            "special_instruction": spec_inst,
            "quantity": qty,
            "id_options": chosen_options,
            "total_bundle_price": Dx(total_bundle_price),
            "id_chef": chef_id["uUID"],
        }
        t1e = time.perf_counter()
        print(t1e - t1s)
        print(bundle)
        self._conn.Bundle.insert_one(bundle)
        self._conn.Cart.update_one(
            {"iD": cart["iD"]},
            {
                "$push": {"bundle_ids": bundle_id},
                "$inc": {"price": Dx(total_bundle_price)},
            },
        )

    def remove_from_cart(self, cart_id, bundle_id):
        res = self._conn.Bundle.find_one_and_delete({"id_bundle": bundle_id})
        if not res or len(res) < 1:
            raise Exception("BUNDLE_NOT_FOUND")

        self._conn.Cart.update_one(
            {"iD": cart_id},
            {
                "$pull": {"bundle_ids": bundle_id},
                "$inc": {"price": Dx("-" + str(res["total_bundle_price"]))},
            },
        )

    def get_cart_details(self, cart: dict) -> dict:
        result = {}
        bundle_ids = cart["bundle_ids"]
        del cart["bundle_ids"]
        result["cart"] = cart
        result["cart"]["price"] = str(result["cart"]["price"])

        cursor = list(
            self._conn.Bundle.aggregate(
                [
                    {
                        "$match": {"id_bundle": {"$in": bundle_ids}},
                    },
                    {
                        "$project": {"_class": 0, "_id": 0},
                    },
                    {
                        "$lookup": {
                            "from": "Food",
                            "localField": "id_food",
                            "foreignField": "id_food",
                            "as": "foody",
                        }
                    },
                    {"$unwind": "$foody"},
                    {
                        "$project": {
                            "name": "$foody.name",
                            "picture": "$foody.picture",
                            "id_bundle": 1,
                            "id_food": 1,
                            "special_instruction": 1,
                            "quantity": 1,
                            "id_options": 1,
                            "total_bundle_price": {"$toString": "$total_bundle_price"},
                        }
                    },
                ]
            )
        )
        result["bundles"] = cursor
        return result

    def delete_cart(self, user_id: str) -> None:
        self._conn.Cart.delete_one({"user_id": user_id, "status": "StandBy"})

    def update_current_cart_attribute(self, cart_id: str, query: dict, role: str) -> None:
        keys = ["new_vals", "to_change"]
        if not all(key in query for key in keys):
            raise Exception("INVALID_REQUEST")
        
        update_query = {}
        if len(query["new_vals"]) != len(query["to_change"]):
            raise Exception("INVALID_REQUEST")
        
        for i in range(0, len(query["new_vals"])):
            if query["to_change"][i] not in ["location", "payment_method"]:
                raise Exception("INVALID_REQUEST")
            if query["to_change"][i] == "location":
                self.check_location_exists(query["new_vals"][i], role)
            if query["to_change"][i] == "payment_method":
                if query["new_vals"][i] not in ["cash", "card"]:
                    raise Exception("CASH_CARD_ONLY")
            update_query[query["to_change"][i]] = query["new_vals"][i]
        
        
        self._conn.Cart.update_one(
            {"iD": cart_id}, {"$set": update_query}
        )

    def place_order(self, cart: dict, user_id: str, role: str) -> None:
        if len(cart["bundle_ids"]) < 1:
            raise Exception("NO_ITEMS_IN_CART")
        bundles = self._conn.Bundle.find({"id_bundle": {"$in": cart["bundle_ids"]}}, {"_id": 0, "id_bundle": 1, "id_chef": 1, "total_bundle_price": 1})
        chef_to_bundles: dict = {}
        for bundle in bundles:
            if bundle["id_chef"] not in chef_to_bundles:
                chef_to_bundles[bundle["id_chef"]] = {"bundle_ids": [], "price": D("0")}
            chef_to_bundles[bundle["id_chef"]]["bundle_ids"].append(bundle["id_bundle"])
            chef_to_bundles[bundle["id_chef"]]["price"] += D(str(bundle["total_bundle_price"]))
            
        new_carts = []
        chefs_to_cart = {}
        for chef in chef_to_bundles:
            new_cart = {
                "iD": "cart_" + uuid.uuid4().hex,
                "location": cart["location"],
                "price": Dx(str(chef_to_bundles[chef]["price"])),
                "bundle_ids": chef_to_bundles[chef]["bundle_ids"],
                "order_date": "",
                "completion_time": "",
                "status": "Ordered",
                "delivery_person": "",
                "payment_method": cart["payment_method"],
                "user_id": user_id,
            }
            new_carts.append(new_cart)
            chefs_to_cart[chef] = new_cart["iD"]
        
        self._conn.Cart.insert_many(new_carts)
        for chef in chefs_to_cart.keys():
            self._conn.ChefOrderMatch.update_one(
                {"id_chef": chef},
                {"$push": {"active_orders": chefs_to_cart[chef], "finished_orders": {"$each": []}}},
                upsert=True
            )
        

    def checkout_cart(self, cart: dict, role: str) -> None:
        if len(cart["bundle_ids"]) < 1:
            raise Exception("NO_ITEMS_IN_CART")
        loc = cart["location"]
        self.check_location_exists(loc, role)
        cart["delivery_person"] = delivery_people_names[random.randint(0, len(delivery_people_names) - 1)]
        cart["status"] = "Ordered"
        cart["order_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
        cart["price"] = Dx(cart["price"])
        self._conn.Cart.update_one(
            {"iD": cart["iD"]}, {"$set": cart}
        )

    def deliver_order(self, cart_id: str) -> None:
        try:
            cart = self._conn.Cart.find_one({"iD": cart_id})
            if not cart or len(cart) < 1:
                raise Exception("CART_NOT_FOUND")
            if cart["status"] != "Ordered":
                raise Exception("CART_NOT_ORDERED")
            cart["status"] = "Delivered"
            cart["completion_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            self._conn.Cart.update_one(
                {"iD": cart_id}, {"$set": cart}
            )
            print("done")
        except: 
            raise Exception("DB_CONNECTION_FAILED")

    def get_order_history(self, uUID: str) -> dict:
        orders = []
        try:
            orders = list(
                self._conn.Cart.aggregate([
                    {"$match": {"user_id": uUID, "status": {"$in": ["Delivered", "Ordered"]}}},
                    {"$project": {"_id": 0, "_class": 0}}
                ])
            )
            for order in orders:
                order["price"] = str(order["price"])
        except Exception as e:
            raise Exception("DB_CONNECTION_FAILED")
        return orders    

    def get_bundle_info(self, bundle_ids: list) -> list:
        bundles = []
        try:
            Cursor = self._conn.Bundle.aggregate([
                    {"$match": {"id_bundle": {"$in": bundle_ids}}},
                    {"$project": {"_id": 0, "_class": 0}}
                ])
            while Cursor.alive:
                bundle = Cursor.next()
                bundle["total_bundle_price"] = str(bundle["total_bundle_price"])
                food = self._conn.Food.find_one(
                    {"id_food": bundle["id_food"]},
                    {
                        "_id": 0, 
                        "id_food": 1,
                        "name": 1,
                        "picture": 1,
                        "price": 1,
                        "timing": 1,
                        "total_rating": 1,
                        "id_chef": 1,
                        "options": 1,
                    }
                )
                options = []
                if food is not None:
                    for option in food["options"]:
                        if option["option_name"] in bundle["id_options"]:
                            options.append(option)
                    food["options"] = options
                    del bundle["id_options"]
                    bundle["food"] = food
                bundles.append(bundle)
            
        except Exception as e:
            raise Exception("DB_CONNECTION_FAILED")
        return bundles
