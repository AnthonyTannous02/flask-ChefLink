from flask import Flask, jsonify, request

app = Flask(__name__, instance_relative_config=True)

data = {
    "Italian": [
        {
            "food_id": 1,
            "name": "BBQ Pizza",
            "price": 10,
            "picture": "/chefname/bbqpizza.jpg",
            "total_rating": 4.5,
            "time_till_completion": 30,
        },
        {
            "food_id": 2,
            "name": "Pasta",
            "price": 15,
            "picture": "/chefname/pasta.jpg",
            "total_rating": 4.1,
            "time_till_completion": 25,
        },
        {
            "food_id": 3,
            "name": "Mozarella Sticks",
            "price": 4,
            "picture": "/chefname/mozarellasticks.jpg",
            "total_rating": 3.5,
            "time_till_completion": 20,
        },
        {
            "food_id": 4,
            "name": "Risotto",
            "price": 8,
            "picture": "/chefname/risotto.jpg",
            "total_rating": 4.8,
            "time_till_completion": 35,
        },
    ],
    "Lebanese": [
        {
            "food_id": 5,
            "name": "Hummus",
            "price": 6,
            "picture": "/chefname/hummus.jpg",
            "total_rating": 4.2,
            "time_till_completion": 15,
        },
        {
            "food_id": 6,
            "name": "Tabbouleh",
            "price": 7,
            "picture": "/chefname/tabbouleh.jpg",
            "total_rating": 4.6,
            "time_till_completion": 18,
        },
        {
            "food_id": 7,
            "name": "Falafel",
            "price": 5,
            "picture": "/chefname/falafel.jpg",
            "total_rating": 4.3,
            "time_till_completion": 22,
        },
        {
            "food_id": 8,
            "name": "Shawarma",
            "price": 9,
            "picture": "/chefname/shawarma.jpg",
            "total_rating": 4.7,
            "time_till_completion": 28,
        },
    ],
    "Chinese": [
        {
            "food_id": 9,
            "name": "Kung Pao Chicken",
            "price": 15,
            "picture": "/chefname/kungpaochicken.jpg",
            "total_rating": 4.7,
            "time_till_completion": 40,
        },
        {
            "food_id": 10,
            "name": "Sweet and Sour Pork",
            "price": 13,
            "picture": "/chefname/sweetandsourpork.jpg",
            "total_rating": 4.6,
            "time_till_completion": 38,
        },
        {
            "food_id": 11,
            "name": "Mapo Tofu",
            "price": 12,
            "picture": "/chefname/mapotofu.jpg",
            "total_rating": 4.5,
            "time_till_completion": 42,
        },
        {
            "food_id": 12,
            "name": "Wonton Soup",
            "price": 10,
            "picture": "/chefname/wontonsoup.jpg",
            "total_rating": 4.8,
            "time_till_completion": 36,
        },
    ],
}

@app.route("/get", methods=["GET"])
def get_data():
    return data


@app.route("/get2")
def get2():
    return {
        "top_rated": [
            {
                "food_id": 4,
                "name": "Risotto",
                "price": 8,
                "picture": "/chefname/risotto.jpg",
                "total_rating": 4.8,
                "time_till_completion": 35,
            },
            {
                "food_id": 8,
                "name": "Shawarma",
                "price": 9,
                "picture": "/chefname/shawarma.jpg",
                "total_rating": 4.7,
                "time_till_completion": 28,
            },
            {
                "food_id": 12,
                "name": "Wonton Soup",
                "price": 10,
                "picture": "/chefname/wontonsoup.jpg",
                "total_rating": 4.8,
                "time_till_completion": 36,
            },
        ],
        "near_you": [
            {
                "food_id": 1,
                "name": "BBQ Pizza",
                "price": 10,
                "picture": "/chefname/bbqpizza.jpg",
                "total_rating": 4.5,
                "time_till_completion": 30,
            },
            {
                "food_id": 3,
                "name": "Mozzarella Sticks",
                "price": 4,
                "picture": "/chefname/mozarellasticks.jpg",
                "total_rating": 3.5,
                "time_till_completion": 20,
            },
            {
                "food_id": 5,
                "name": "Hummus",
                "price": 6,
                "picture": "/chefname/hummus.jpg",
                "total_rating": 4.2,
                "time_till_completion": 15,
            },
        ],
        "new": [
            {
                "food_id": 2,
                "name": "Pasta",
                "price": 15,
                "picture": "/chefname/pasta.jpg",
                "total_rating": 4.1,
                "time_till_completion": 25,
            },
            {
                "food_id": 6,
                "name": "Tabbouleh",
                "price": 7,
                "picture": "/chefname/tabbouleh.jpg",
                "total_rating": 4.6,
                "time_till_completion": 18,
            },
            {
                "food_id": 7,
                "name": "Falafel",
                "price": 5,
                "picture": "/chefname/falafel.jpg",
                "total_rating": 4.3,
                "time_till_completion": 22,
            },
            {
                "food_id": 9,
                "name": "Kung Pao Chicken",
                "price": 15,
                "picture": "/chefname/kungpaochicken.jpg",
                "total_rating": 4.7,
                "time_till_completion": 40,
            },
            {
                "food_id": 10,
                "name": "Sweet and Sour Pork",
                "price": 13,
                "picture": "/chefname/sweetandsourpork.jpg",
                "total_rating": 4.6,
                "time_till_completion": 38,
            },
            {
                "food_id": 11,
                "name": "Mapo Tofu",
                "price": 12,
                "picture": "/chefname/mapotofu.jpg",
                "total_rating": 4.5,
                "time_till_completion": 42,
            },
        ],
    }


if __name__ == "__main__":
    app.run(debug=True, port=3030)
