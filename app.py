from flask import Flask, request, render_template
from reservations import ReservationSystem
from datetime import datetime
from openpyxl import Workbook
from flask import send_file

app = Flask(__name__)
system = ReservationSystem()

@app.route('/')
def index():
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', system=system, today=today)



@app.route('/make_reservation', methods=['POST'])
def make_reservation():
    name = request.form.get('customerName')
    resource = request.form.get('resourceId')
    date_str = request.form.get('reservationDate')
    time_slot = request.form.get('timeSlot')
    today = datetime.now().strftime('%Y-%m-%d')
    if date_str < today:
        return "Error: You can't book dates in the past."

    success, message = system.make_reservation(name, resource, date_str, time_slot)
    return render_template('success.html', message=message)

@app.route('/cancel_reservation', methods=['POST'])
def cancel_reservation():
    name = request.form.get('cancelName')
    resource = request.form.get('cancelResource')
    date_str = request.form.get('cancelDate')
    time_slot = request.form.get('cancelTimeSlot')
    success, message = system.cancel_reservation(name, resource, date_str, time_slot)
    return render_template('success.html', message=message)


@app.route('/set_capacity', methods=['GET', 'POST'])
def set_capacity():
    if request.method == 'POST':
        date_str = request.form.get('capacityDate')
        capacity_value = int(request.form.get('capacityValue'))
        system.set_capacity_for_date(date_str, capacity_value)
        return render_template('success.html',
                               message=f"Capacity for {date_str} updated to {capacity_value} and tables set.")
    else:
        return render_template('capacity.html')

@app.route('/export_excel/<date_str>')
def export_excel(date_str):
    from openpyxl import Workbook
    from flask import send_file
    data = system.list_reservations_for_date(date_str)

    wb = Workbook()
    safe_date = date_str.replace(":", "-")

    ws = wb.active
    ws.title = f"Reservations {safe_date}" 
    ws.append(["Name", "Table", "Time Slot"])

    for r in data:
        ws.append([r.customer_name, r.resource_id, r.time_slot])

    filename = f"reservations_{safe_date}.xlsx"
    wb.save(filename)
    return send_file(filename, as_attachment=True)

@app.route('/list_reservations', methods=['GET', 'POST'])
def list_reservations():
    if request.method == 'POST':
        chosen_date = request.form.get('selectedDate')
        all_for_date = system.list_reservations_for_date(chosen_date)
        capacity = system.capacity_by_date.get(chosen_date, 10)
        return render_template('reservations.html',
                               date_str=chosen_date,
                               reservations=all_for_date,
                               capacity=capacity)
    else:
        date_keys = list(system.reservations_by_date.keys())
        return render_template('list_dropdown.html', date_keys=date_keys)
    

@app.route('/admin/set_tables', methods=['GET', 'POST'])
def admin_set_tables():
    if request.method == 'POST':
        num = int(request.form.get('num_tables'))
        system.set_total_tables(num)
        return render_template('success.html', message=f"Set {num} tables")
    return render_template('set_tables.html')

import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)