class HotelReservation:
    def __init__(self):
        self.checkindate = None
        self.checkoutdate = None
        self.roomtype = None
        self.numberofguests = None

    def set_reservation(self, checkindate, checkoutdate, roomtype, numberofguests):
        self.checkindate = checkindate
        self.checkoutdate = checkoutdate
        self.roomtype = roomtype
        self.numberofguests = numberofguests

    def get_reservation(self):
        return {
            "checkindate": self.checkindate,
            "checkoutdate": self.checkoutdate,
            "roomtype": self.roomtype,
            "numberofguests": self.numberofguests,
        }

    def clear_reservation(self):
        self.checkindate = None
        self.checkoutdate = None
        self.roomtype = None
        self.numberofguests = None