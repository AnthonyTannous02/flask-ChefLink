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
            },
            {
                "name": "Pasta",
                "price": 15,
                "picture": "/chefname/pasta.jpg",
                "total_rating": 4.1,
            },
            {
                "name": "Mozarella Sticks",
                "price": 4,
                "picture": "/chefname/mozarellasticks.jpg",
                "total_rating": 3.5,
            },
            {
                "name": "Risotto",
                "price": 8,
                "picture": "/chefname/risotto.jpg",
                "total_rating": 4.8,
            },
        ],
        "Lebanese": [
            {
                "name": "Hummus",
                "price": 6,
                "picture": "/chefname/hummus.jpg",
                "total_rating": 4.2,
            },
            {
                "name": "Tabbouleh",
                "price": 7,
                "picture": "/chefname/tabbouleh.jpg",
                "total_rating": 4.6,
            },
            {
                "name": "Falafel",
                "price": 5,
                "picture": "/chefname/falafel.jpg",
                "total_rating": 4.3,
            },
            {
                "name": "Shawarma",
                "price": 9,
                "picture": "/chefname/shawarma.jpg",
                "total_rating": 4.7,
            },
        ],
        "Chinese": [
            {
                "name": "Kung Pao Chicken",
                "price": 15,
                "picture": "/chefname/kungpaochicken.jpg",
                "total_rating": 4.7,
            },
            {
                "name": "Sweet and Sour Pork",
                "price": 13,
                "picture": "/chefname/sweetandsourpork.jpg",
                "total_rating": 4.6,
            },
            {
                "name": "Mapo Tofu",
                "price": 12,
                "picture": "/chefname/mapotofu.jpg",
                "total_rating": 4.5,
            },
            {
                "name": "Wonton Soup",
                "price": 10,
                "picture": "/chefname/wontonsoup.jpg",
                "total_rating": 4.8,
            },
        ],
    }
    return {"data": data}


if __name__ == "__main__":
    app.run(debug=True, port=3030)
