from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)


# create database with sqlite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jov.db"

# create a object database
db = SQLAlchemy(app)

# a model is created
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(50), nullable= False)
    country = db.Column(db.String(50), nullable= False)
    rating = db.Column(db.Float, nullable = False)

# converted to json format
    def to_dict(self):
        return {
            "id": self.id,
            "destination" : self.destination,
            "country": self.country,
            "rating": self.rating
        }

#then rapid context
with app.app_context():
    db.create_all()


# create routes
@app.route("/")
def home():
    return jsonify({"message": "welcome to the travel"})

#example to url https://www.jov.io/example
@app.route("/destinations", methods=["GET"])
def get_destinations():
    destinations = Destination.query.all()
    return jsonify([destination.to_dict() for destination in destinations])

@app.route("/destinations/<int:destination_id>", methods=["GET"])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination: 
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "destination not found"}), 404

#method POST - send information to the api
@app.route("/destinations", methods=["POST"])
def add_destination():
    data = request.get_json()

    #creamos nuevo objeto para insertar a la db
    new_destination = Destination(destination= data["destination"],
                                  country=data["country"],
                                  rating= data["rating"])
    db.session.add(new_destination)
    db.session.commit()

    return jsonify(new_destination.to_dict()),201

#put -> update
@app.route("/destinations/<int:destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()

    destination = Destination.query.get(destination_id)
    if destination:
        #objeto.destino
        destination.destination = data.get("destination", destination.destination)
        destination.country = data.get("country", destination.country)
        destination.rating = data.get("rating", destination.rating)
        #accedemos a la sesion actual y queremos confirmar los cambios actuales
        db.session.commit()
        #devolvemos la version json
        return jsonify(destination.to_dict())
    else:
        return jsonify({"error": "destination not found!"}), 404


#delete
@app.route("/destinations/<int:destination_id>", methods=["GET"])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination:
        db.session.delete()
        db.session.commit()

        return jsonify({"message": "destination was deleted"})
    else:
        return jsonify({"error": "destination not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
