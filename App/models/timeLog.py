from App.database import db

class TimeLog(db.Model):
    timeid = db.Column(db.Integer, primary_key=True)
    staffid = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable = False)
    shiftid = db.Column(db.Integer, db.ForeignKey('shift.shiftid'), nullable = False)
    clockedin = db.Column(db.Boolean, nullable = False, default = False)
    startTime = db.Column(db.DateTime)
    endTime = db.Column(db.DateTime)
    clockedout = db.Column(db.Boolean, nullable = False, default = False)

    def __init__(self, staffid, shiftid, clockedin, clockedout):
        self.staffid = staffid
        self.shiftid = shiftid
        self.clockedin = clocked
        self.clockedout = clockedout

    def calculateHours(self):
        if self.startTime and self.endTime:
            diff = self.endTime - self.startTime
            hrs =  diff.total_seconds() / 3600 
            self.hours = hrs
            db.session.commit()
            return hrs
        return 0

    def __repr__(self):
        return f'<Staff {self.staffid} - Shift {self.shiftid} - Clocked In {self.clockedin} - Clocked Out {self.clockedout}>'
        
