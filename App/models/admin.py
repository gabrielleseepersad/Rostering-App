from App.database import db
from .shift import Shift
from .timeLog import TimeLog
from .staff import Staff
from .user import User

class Admin(User):
    def __init__(self, name, password, role, email):
        super().__init__(name, password, role, email)

    def scheduleStaff(self, staffid, shiftid):
        shift = Shift.query.filter_by(shiftid=shiftid)
        staff = Staff.query.filter_by(id=staffid)
        shift.staffAssigned.append(staff.name)
        db.session.commit()
        return shift

    def viewReport(week):
        allshifts = Shift.query.filter_by(week=week).all()
        print(f'Shifts for week {week}: {allshifts}')
        return allshifts
