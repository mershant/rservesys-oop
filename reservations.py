class Reservation:
    def __init__(self, customer_name, resource_id, reservation_date):
        self.customer_name = customer_name
        self.resource_id = resource_id
        self.reservation_date = reservation_date

class ReservationSystem:
    def __init__(self):
        self.reservations_by_date = {}
        self.capacity_by_date = {}

    def set_capacity_for_date(self, date_str, capacity):
        self.capacity_by_date[date_str] = capacity

    def make_reservation(self, name, resource_id, date_str):
        if date_str not in self.reservations_by_date:
            self.reservations_by_date[date_str] = []

        capacity = self.capacity_by_date.get(date_str, 10)
        existing_reservations = self.reservations_by_date[date_str]

        if len(existing_reservations) < capacity:
            new_res = Reservation(name, resource_id, date_str)
            existing_reservations.append(new_res)
            return True, f"Reservation created for {name} on {date_str}."
        else:
            return False, f"Cannot reserve on {date_str}, capacity reached!"

    def list_reservations_for_date(self, date_str):
        if date_str in self.reservations_by_date:
            return self.reservations_by_date[date_str]
        return []

    def cancel_reservation(self, name, resource_id, date_str):
        if date_str in self.reservations_by_date:
            for r in self.reservations_by_date[date_str]:
                if r.customer_name == name and r.resource_id == resource_id:
                    self.reservations_by_date[date_str].remove(r)
                    return True, f"Reservation canceled for {name} on {date_str}."
        return False, f"No reservation found for {name} on {date_str}."
