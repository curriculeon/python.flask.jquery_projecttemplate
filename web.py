from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Person:
    def __init__(self, id, firstName, lastName):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName

people = []
personId = 1

@app.route('/api/person/create', methods=['POST'])
def create_person():
    global personId
    data = request.get_json()
    person = Person(personId, data['firstName'], data['lastName'])
    people.append(person)
    personId += 1
    print("New person created: {} {} {}".format(person.id, person.firstName, person.lastName))
    return '', 204

@app.route('/api/person/read/<int:id>', methods=['GET'])
def get_person_by_id(id):
    person = next((p for p in people if p.id == id), None)
    if person is None:
        raise ValueError("Person not found with id {}".format(id))
    return jsonify(person.__dict__)

@app.route('/api/person/readAll', methods=['GET'])
def get_all_people():
    return jsonify([p.__dict__ for p in people])

@app.route('/api/person/update/<int:id>', methods=['PUT'])
def update_person_by_id(id):
    data = request.get_json()
    person = next((p for p in people if p.id == id), None)
    if person is None:
        raise ValueError("Person not found with id {}".format(id))
    person.firstName = data['firstName']
    person.lastName = data['lastName']
    print("Person with id {} updated.".format(id))
    return '', 204

@app.route('/api/person/delete/<int:id>', methods=['DELETE'])
def delete_person_by_id(id):
    global people
    people = [p for p in people if p.id != id]
    print("Person with id {} deleted.".format(id))
    return '', 204

@app.route("/")
def main():
    return render_template('index.html')
 
if __name__ == "__main__":
    app.run(host="localhost", port=8082, debug=True)