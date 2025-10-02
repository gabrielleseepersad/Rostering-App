from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import datetime

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable = False, default='staff')
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
    
    
    def viewCombinedRoster(self, week):
        from .shift import Shift
        allshifts = Shift.query.filter_by(week=week).all()
        print(f'Shifts for week {week}: {allshifts}')
        return 
        
        
    def clockIn(self, shiftid):
        from .timeLog import TimeLog
        clocked = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedin=True).first()
        if clocked:
            print(f'Already clocked in for shift {shiftid}')
            return 
        new_log = TimeLog(staffid = self.id, shiftid = shiftid, clockedin=True, clockedout=False)
        new_log.startTime = datetime.now()
        db.session.add(new_log)
        db.session.commit()
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'Clocked in at {current_time}')        
        return 
    
    def clockOut(self, shiftid):
        from .timeLog import TimeLog
        clocked = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedout=True).first()
        if clocked:
            print(f'Already clocked out for shift {shiftid}')
            return 
        clock = TimeLog.query.filter_by(staffid=self.id, shiftid=shiftid, clockedin=True, clockedout = False).first()
        if not clock:
            print(f'Staff is not clocked in for shift {shiftid}')
            return 
        new_log = TimeLog(staffid = self.id, shiftid = shiftid, clockedin=True, clockedout=True)
        new_log.endTime = datetime.now()
        db.session.add(new_log)
        db.session.commit()
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'Clocked out at {current_time}')        
        return 
