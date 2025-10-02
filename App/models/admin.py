from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable = False, default='admin')
    email = db.Column(db.String(50), unique = True)

    def __init__(self, username, password, role, email):
        self.username = username
        self.set_password(password)
        self.role = role
        self.email = email

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Staff ID: {self.id}, Name: {self.username}, Role: {self.role}, Email: {self.email}>'

    
    def scheduleStaff(self, staffid, shiftid):
        from .shift import Shift
        from .staff import Staff
        shift = Shift.query.get(shiftid)
        staff = Staff.query.get(staffid)
        shift.staffAssigned = staff.id
        db.session.commit()
        return shift

    def viewReport(week):
        from .shift import Shift
        from .timeLog import TimeLog
        allshifts = Shift.query.filter_by(week=week).all()
        if not allshifts:
            print(f'No shifts found for week {week}')
            return 
        print(f'Shifts for week {week}:')
        for shift in allshifts:
            print(f'ShiftId: {shift.shiftid}, Date: {shift.date}, Staff Assigned: {shift.staffAssigned}')
        timelogs = TimeLog.query.filter_by(shiftid=shift.shiftid).all()
        if not timelogs:
            print("No time logs found for this shift")
        else:
            print("Time Logs:")
            for log in timelogs:
                print(f"Staff ID: {log.staffid}, Shift: {log.shiftid}, Start: {log.startTime.strftime('%H:%M:%S')}, End: {log.endTime.strftime('%H:%M:%S')}")
        return allshifts
        
