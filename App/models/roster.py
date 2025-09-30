from App.database import db
from .shift import Shift

class Roster(db.Model):
    rosterid = db.Column(db.Integer, primary_key=True)
    shiftid = db.Column(db.Integer, db.ForeignKey('shift.shiftid'), nullable = False)
    week = db.Column(db.Integer, nullable = False)

    shifts = db.relationship('Shift', backref = 'roster', lazy = True)

    def __init__(self, shiftid, week, shifts):
        self.shiftid = shiftid
        self.week = week
        self.shifts = shifts

    def addShift(self, shift):
        self.shifts.append(shift)
        db.session.commit()
        return self.shifts
        

    def __repr__(self):
        return f'<Roster {self.rosterid} - Week {self.week}>'
