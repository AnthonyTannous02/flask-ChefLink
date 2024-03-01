from flask import Flask, jsonify, request

app = Flask(__name__, instance_relative_config=True)


@app.route("/get", methods=["GET"])
def get_data():
    data = {
        "Italian": [
            {
                "name": "BBQ Pizza",
                "price": 10,
                "picture": "/chefname/bbqpizza.jpg",
                "total_rating": 4.5,
                "time_till_completion": 30,
            },
            {
                "name": "Pasta",
                "price": 15,
                "picture": "/chefname/pasta.jpg",
                "total_rating": 4.1,
                "time_till_completion": 25,
            },
            {
                "name": "Mozarella Sticks",
                "price": 4,
                "picture": "/chefname/mozarellasticks.jpg",
                "total_rating": 3.5,
                "time_till_completion": 20,
            },
            {
                "name": "Risotto",
                "price": 8,
                "picture": "/chefname/risotto.jpg",
                "total_rating": 4.8,
                "time_till_completion": 35,
            },
        ],
        "Lebanese": [
            {
                "name": "Hummus",
                "price": 6,
                "picture": "/chefname/hummus.jpg",
                "total_rating": 4.2,
                "time_till_completion": 15,
            },
            {
                "name": "Tabbouleh",
                "price": 7,
                "picture": "/chefname/tabbouleh.jpg",
                "total_rating": 4.6,
                "time_till_completion": 18,
            },
            {
                "name": "Falafel",
                "price": 5,
                "picture": "/chefname/falafel.jpg",
                "total_rating": 4.3,
                "time_till_completion": 22,
            },
            {
                "name": "Shawarma",
                "price": 9,
                "picture": "/chefname/shawarma.jpg",
                "total_rating": 4.7,
                "time_till_completion": 28,
            },
        ],
        "Chinese": [
            {
                "name": "Kung Pao Chicken",
                "price": 15,
                "picture": "/chefname/kungpaochicken.jpg",
                "total_rating": 4.7,
                "time_till_completion": 40,
            },
            {
                "name": "Sweet and Sour Pork",
                "price": 13,
                "picture": "/chefname/sweetandsourpork.jpg",
                "total_rating": 4.6,
                "time_till_completion": 38,
            },
            {
                "name": "Mapo Tofu",
                "price": 12,
                "picture": "/chefname/mapotofu.jpg",
                "total_rating": 4.5,
                "time_till_completion": 42,
            },
            {
                "name": "Wonton Soup",
                "price": 10,
                "picture": "/chefname/wontonsoup.jpg",
                "total_rating": 4.8,
                "time_till_completion": 36,
            },
        ],
    }
    return data


@app.route("/get2")
def get2():
    return {
        "top_rated": [
            {
                "name": "Risotto",
                "price": 8,
                "picture": "/chefname/risotto.jpg",
                "total_rating": 4.8,
                "time_till_completion": 35,
            },
            {
                "name": "Shawarma",
                "price": 9,
                "picture": "/chefname/shawarma.jpg",
                "total_rating": 4.7,
                "time_till_completion": 28,
            },
            {
                "name": "Wonton Soup",
                "price": 10,
                "picture": "/chefname/wontonsoup.jpg",
                "total_rating": 4.8,
                "time_till_completion": 36,
            },
        ],
        "near_you": [
            {
                "name": "BBQ Pizza",
                "price": 10,
                "picture": "/chefname/bbqpizza.jpg",
                "total_rating": 4.5,
                "time_till_completion": 30,
            },
            {
                "name": "Mozzarella Sticks",
                "price": 4,
                "picture": "/chefname/mozarellasticks.jpg",
                "total_rating": 3.5,
                "time_till_completion": 20,
            },
            {
                "name": "Hummus",
                "price": 6,
                "picture": "/chefname/hummus.jpg",
                "total_rating": 4.2,
                "time_till_completion": 15,
            },
        ],
        "new": [
            {
                "name": "Pasta",
                "price": 15,
                "picture": "/chefname/pasta.jpg",
                "total_rating": 4.1,
                "time_till_completion": 25,
            },
            {
                "name": "Tabbouleh",
                "price": 7,
                "picture": "/chefname/tabbouleh.jpg",
                "total_rating": 4.6,
                "time_till_completion": 18,
            },
            {
                "name": "Falafel",
                "price": 5,
                "picture": "/chefname/falafel.jpg",
                "total_rating": 4.3,
                "time_till_completion": 22,
            },
            {
                "name": "Kung Pao Chicken",
                "price": 15,
                "picture": "/chefname/kungpaochicken.jpg",
                "total_rating": 4.7,
                "time_till_completion": 40,
            },
            {
                "name": "Sweet and Sour Pork",
                "price": 13,
                "picture": "/chefname/sweetandsourpork.jpg",
                "total_rating": 4.6,
                "time_till_completion": 38,
            },
            {
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
