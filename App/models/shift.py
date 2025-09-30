from App.database import db
from datetime import date 
from .staff import Staff

class Shift(db.Model):
    shiftid = db.Column(db.Integer, primary_key=True)
    staffAssigned = db.Column(db.String(50), db.ForeignKey('staff.name')) 
    rosterid = db.Column(db.Integer, db.ForeignKey('roster.rosterid'), nullable = False)
    shiftType = db.Column(db.String(5), nullable = False)
    week = db.Column(db.Integer, nullable = False)
    hours = db.Column(db.Integer, nullable = False)
    date = db.Column(db.Date, default = date.today)

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
        
