from flask import Flask, request, render_template
from reservations import ReservationSystem

app = Flask(__name__)
system = ReservationSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    name = request.form.get('customerName')
    resource = request.form.get('resourceId')
    date_str = request.form.get('reservationDate')
    success, message = system.make_reservation(name, resource, date_str)
    return render_template('success.html', message=message)

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    name = request.form.get('cancelName')
    resource = request.form.get('cancelResource')
    date_str = request.form.get('cancelDate')
    success, message = system.cancel_reservation(name, resource, date_str)
    return render_template('success.html', message=message)

@app.route('/set_capacity', methods=['GET', 'POST'])
def set_capacity():
    if request.method == 'POST':
        date_str = request.form.get('capacityDate')
        capacity_value = int(request.form.get('capacityValue'))
        system.set_capacity_for_date(date_str, capacity_value)
        return render_template('success.html', message=f"Capacity for {date_str} set to {capacity_value}")
    else:
        return render_template('capacity.html')

@app.route('/list_reservations', methods=['GET', 'POST'])
def list_reservations():
    if request.method == 'POST':
        chosen_date = request.form.get('selectedDate')
        all_for_date = system.list_reservations_for_date(chosen_date)
        # Get capacity for chosen_date; defaulting to 10 if not set
        capacity = system.capacity_by_date.get(chosen_date, 10)
        return render_template('reservations.html',
                               date_str=chosen_date,
                               reservations=all_for_date,
                               capacity=capacity)
    else:
        date_keys = list(system.reservations_by_date.keys())
        return render_template('list_dropdown.html', date_keys=date_keys)


if __name__ == '__main__':
    app.run(debug=True)