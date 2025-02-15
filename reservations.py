class Reservation:
    def __init__(self, customer_name, resource_id, reservation_date):
        self.customer_name = customer_name
        self.resource_id = resource_id
        self.reservation_date = reservation_date  # e.g., "2023-12-01"

class ReservationSystem:
    def __init__(self):
        # Dictionary keyed by date, each value is a list of Reservation objects
        self.reservations_by_date = {}
        # Dictionary keyed by date, each value is an integer indicating capacity
        self.capacity_by_date = {}

    def set_capacity_for_date(self, date_str, capacity):
        """Define or update the maximum reservations allowed for a given date."""
        self.capacity_by_date[date_str] = capacity

    def make_reservation(self, name, resource_id, date_str):
        if date_str not in self.reservations_by_date:
            self.reservations_by_date[date_str] = []

        # Default capacity is 10 if no custom value set
        capacity = self.capacity_by_date.get(date_str, 10)
        existing = self.reservations_by_date[date_str]

        # If there's room, create and store the new reservation
        if len(existing) < capacity:
            new_reservation = Reservation(name, resource_id, date_str)
            existing.append(new_reservation)
            return True, f"Reservation created for {name} on {date_str}."
        else:
            return False, f"Cannot reserve on {date_str}, capacity reached!"

    def list_reservations_for_date(self, date_str):
        """Return a list of reservations for the specified date."""
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
