from flask import Flask, request, render_template, redirect, url_for
from reservations import ReservationSystem

app = Flask(__name__)
system = ReservationSystem()

@app.route('/')
def index():
    # Show a form to make reservations
    return render_template('index.html')

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    name = request.form.get('customerName')
    resource = request.form.get('resourceId')
    date_str = request.form.get('reservationDate')

    success, message = system.make_reservation(name, resource, date_str)
    if success:
        return render_template('success.html', message=message)
    else:
        return render_template('success.html', message=message)

@app.route('/list_reservations', methods=['GET', 'POST'])
def list_reservations():
    if request.method == 'POST':
        date_str = request.form.get('listDate')
        reservations = system.list_reservations_for_date(date_str)
        return render_template('reservations.html',
                               date_str=date_str,
                               reservations=reservations)
    else:
        return render_template('reservations.html', date_str=None, reservations=[])

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    name = request.form.get('cancelName')
    resource = request.form.get('cancelResource')
    date_str = request.form.get('cancelDate')
    success, message = system.cancel_reservation(name, resource, date_str)
    return render_template('success.html', message=message)

@app.route('/capacity', methods=['GET', 'POST'])
def set_capacity():
    if request.method == 'POST':
        date_str = request.form.get('capacityDate')
        capacity = int(request.form.get('capacityValue'))
        system.set_capacity_for_date(date_str, capacity)
        return render_template('success.html',
                               message=f"Capacity for {date_str} set to {capacity}")
    else:
        return render_template('capacity.html')

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)
