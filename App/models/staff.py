from App.database import db
from .shift import Shift
from .roster import Roster
from .timeLog import TimeLog
from .user import User
from datetime import datetime


class Staff(User):
    timelog = db.relationship('TimeLog', backref = 'staff', lazy = True)

    def __init__(self, name, password, role, email):
        super().__init__(name, password, role, email)

    def viewCombinedRoster(self, week):
        allshifts = Shift.query.filter_by(week=week).all()
        print(f'Shifts for week {week}: {allshifts}')
        return 
        
        
    def clockIn(self, shiftid):
        # Check if already clocked in for this shift
        clocked = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedin=True).first()
        if clocked:
            print(f'Already clocked in for shift {shiftid}')
            return 
        #Clock in
        new_log = TimeLog(self.id, shiftid, True, False)
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'Clocked in at {current_time}')
        new_log.startTime = current_time
        db.session.add(new_log)
        db.session.commit()
        return 
    
    def clockOut(self, shiftid):
        # Check if already clocked out for this shift
        clocked = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedout=True).first()
        if clocked:
            print(f'Already clocked out for shift {shiftid}')
            return 
        #Clock out
        clock = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedin=True, clockedout=False).first()
        if not log:
            print(f'Staff is not clocked in for shift {shiftid}')
            return 
        clock.clockedout = True
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'Clocked out at {current_time}')
        clock.endTime = current_time
        db.session.commit()
        return 

    