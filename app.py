from flask import Flask, render_template, request
import json, uuid

app = Flask(__name__)

# Load buses from JSON file
def load_buses():
    with open("buses.json", "r") as f:
        return json.load(f)

# Save booking details
def save_booking(data):
    try:
        with open("bookings.json", "r") as f:
            bookings = json.load(f)
    except:
        bookings = []

    bookings.append(data)

    with open("bookings.json", "w") as f:
        json.dump(bookings, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/buses")
def buses():
    bus_list = load_buses()
    return render_template("buses.html", buses=bus_list)

@app.route("/book/<bus_id>")
def book(bus_id):
    bus_list = load_buses()
    bus = next((b for b in bus_list if b["id"] == bus_id), None)
    return render_template("book.html", bus=bus)

@app.route("/confirm", methods=["POST"])
def confirm():
    booking = {
        "id": str(uuid.uuid4())[:8],
        "bus_id": request.form["bus_id"],
        "name": request.form["name"],
        "age": request.form["age"],
        "seat": request.form["seat"]
    }

    save_booking(booking)
    return render_template("success.html", booking=booking)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
