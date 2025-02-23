import json
import os

class Reservation:
    def __init__(self, customer_name, resource_id, reservation_date, time_slot):
        self.customer_name = customer_name
        self.resource_id = resource_id
        self.reservation_date = reservation_date
        self.time_slot = time_slot

class ReservationSystem:
    def __init__(self, data_file='reservation_data.json'):
        self.data_file = data_file
        self.reservations_by_date = {}
        self.capacity_by_date = {}
        self.tables_by_date = {}
        self.default_capacity = 10
        # If you want all tables to default to 10, you can set that too.
        # Load from file if it exists:
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                stored = json.load(f)
                # Rebuild reservations_by_date into actual Reservation objects
                self.reservations_by_date = {}
                for key, list_of_entries in stored.get('reservations_by_date', {}).items():
                    self.reservations_by_date[key] = [
                        Reservation(
                            r['customer_name'],
                            r['resource_id'],
                            r['reservation_date'],
                            r['time_slot']
                        )
                        for r in list_of_entries
                    ]
                self.capacity_by_date = stored.get('capacity_by_date', {})
                self.tables_by_date = stored.get('tables_by_date', {})
        else:
            self.reservations_by_date = {}
            self.capacity_by_date = {}
            self.tables_by_date = {}

    def save_data(self):
        # Convert Reservation objects to dictionaries for JSON
        data_to_save = {
            'reservations_by_date': {},
            'capacity_by_date': self.capacity_by_date,
            'tables_by_date': self.tables_by_date
        }
        for key, reservation_list in self.reservations_by_date.items():
            data_to_save['reservations_by_date'][key] = []
            for res_obj in reservation_list:
                data_to_save['reservations_by_date'][key].append({
                    'customer_name': res_obj.customer_name,
                    'resource_id': res_obj.resource_id,
                    'reservation_date': res_obj.reservation_date,
                    'time_slot': res_obj.time_slot
                })
        with open(self.data_file, 'w') as f:
            json.dump(data_to_save, f, indent=2)

    def set_total_tables(self, num_tables):
        # This was requested by the user for some admin usage
        self.available_tables = [f"Table{i+1}" for i in range(num_tables)]
        self.save_data()

    def set_capacity_for_date(self, date_str, time_slot, capacity):
        key = f"{date_str}:{time_slot}"
        self.capacity_by_date[key] = capacity
        self.tables_by_date[key] = [f"Table{i+1}" for i in range(capacity)]
        self.save_data()

    def make_reservation(self, name, resource_id, date_str, time_slot):
        key = f"{date_str}:{time_slot}"
        capacity = self.capacity_by_date.get(key, self.default_capacity)
        # If no entry, create an empty list
        if key not in self.reservations_by_date:
            self.reservations_by_date[key] = []
        # Check if table is already taken
        for res in self.reservations_by_date[key]:
            if res.resource_id == resource_id:
                return False, f"{resource_id} is taken for {time_slot} on {date_str}."
        # Check if capacity is not exceeded
        if len(self.reservations_by_date[key]) < capacity:
            new_res = Reservation(name, resource_id, date_str, time_slot)
            self.reservations_by_date[key].append(new_res)
            self.save_data()
            return True, f"Reserved table {resource_id} on {date_str} at {time_slot}."
        else:
            return False, f"Full for {time_slot} on {date_str}, capacity {capacity}."

    def list_reservations_for_date(self, date_str):
        # This is the old version: does not look at time_slot
        # but you can adapt if you want to filter by times
        if date_str in self.reservations_by_date:
            return self.reservations_by_date[date_str]
        return []

    def cancel_reservation(self, name, resource_id, date_str, time_slot):
        key = f"{date_str}:{time_slot}"
        if key in self.reservations_by_date:
            for r in self.reservations_by_date[key]:
                if r.customer_name == name and r.resource_id == resource_id:
                    self.reservations_by_date[key].remove(r)
                    self.save_data()
                    return True, f"Canceled table {resource_id} for {name}, {time_slot} on {date_str}."
        return False, f"No reservation found for {name}, {time_slot} on {date_str}."

    def get_free_tables_for_date(self, date_str):
        # Not time-slot aware, only if you want date-wise
        all_tables = self.tables_by_date.get(date_str, [f"Table{i+1}" for i in range(self.default_capacity)])
        taken = []
        for res in self.reservations_by_date.get(date_str, []):
            taken.append(res.resource_id)
        free = [t for t in all_tables if t not in taken]
        return free

    def get_free_tables_for_datetime(self, date_str, time_slot):
        key = f"{date_str}:{time_slot}"
        all_tables = self.tables_by_date.get(key, [f"Table{i+1}" for i in range(self.default_capacity)])
        taken = []
        for r in self.reservations_by_date.get(key, []):
            taken.append(r.resource_id)
        free = [t for t in all_tables if t not in taken]
        return free

    def get_tables_for_date(self, date_str):
        if date_str in self.tables_by_date:
            return self.tables_by_date[date_str]
        return [f"Table{i+1}" for i in range(self.default_capacity)]
