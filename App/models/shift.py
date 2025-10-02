from App.database import db

class Shift(db.Model):
    shiftid = db.Column(db.Integer, primary_key=True)
    staffAssigned = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable = True) 
    rosterid = db.Column(db.Integer, db.ForeignKey('roster.rosterid'), nullable = False)
    shiftType = db.Column(db.String(5), nullable = False)
    week = db.Column(db.Integer, nullable = False)
    hours = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, nullable = False)

    logs = db.relationship('TimeLog', backref = 'shift', lazy = True)


    def __init__(self, staffAssigned, rosterid, shiftType, week, hours, date):
        self.staffAssigned = staffAssigned
        self.rosterid = rosterid
        self.shiftType = shiftType
        self.week = week
        self.hours = hours
        self.date = date

    def __repr__(self):
        return f'<Shift {self.shiftid} - Staff {self.staffAssigned} - Date {self.date} - Type {self.shiftType} - Week {self.week}>' 
        
