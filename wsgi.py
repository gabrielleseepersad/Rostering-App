import click, pytest, sys
#from flask import Flask
from flask.cli import with_appcontext, AppGroup
from datetime import datetime

from App.database import db, get_migrate
from App.models import User, Staff, Admin, Roster, TimeLog, Shift
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize,  )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    db.drop_all()
    db.create_all()

    hana = Admin(username = 'Hana', password = 'hanapass', role = 'admin', email = 'hana@mail.com')
    jordana = Staff(username = 'Jordana', password = 'jordanapass', role = 'staff' , email = 'jordana@mail.com')
    brittney = Staff(username = 'Brittney', password = 'brittneypass', role = 'staff', email = 'brittney@mail.com')
    sophia = Staff(username = 'Sophia', password = 'sophiapass', role = 'staff', email = 'sophia@mail.com')

    db.session.add_all([hana, jordana, brittney, sophia])
    db.session.commit()

    shift1 = Shift(staffAssigned=jordana.id, rosterid=1, shiftType='AM', week=1, hours=8, date=datetime.strptime('2023-10-02', '%Y-%m-%d').date())
    shift2 = Shift(staffAssigned=brittney.id, rosterid=1, shiftType='PM', week=1, hours=8, date=datetime.strptime('2023-10-02', '%Y-%m-%d').date())
    shift3 = Shift(staffAssigned=sophia.id, rosterid=1, shiftType='AM', week=1, hours=8, date=datetime.strptime('2023-10-03', '%Y-%m-%d').date())
    shift4 = Shift(staffAssigned=jordana.id, rosterid=1, shiftType='PM', week=1, hours=8, date=datetime.strptime('2023-10-03', '%Y-%m-%d').date())

    db.session.add_all([shift1, shift2, shift3, shift4])
    db.session.commit()

    roster1 = Roster(week = 1, shifts= [shift1, shift2, shift3, shift4])

    db.session.add(roster1)
    db.session.commit()

    print('database intialized')
'''
User Commands
'''

# User Commands

#command to create a user
@app.cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

#command to list users
@app.cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

'''Added Commands'''
#command to schedule staff
@app.cli.command("schedule-staff", help="Schedule staff to a shift")
def scheduleStaffCommand():
    name = input('Enter your name: ')
    name = name.capitalize()
    admin = Admin.query.filter_by(username = name).first()
    if not admin:
        print('Only admins can schedule staff')
        return
    passw = input('Enter your password: ')
    login = Admin.check_password(admin, passw)
    if not login:
        print('Incorrect password')
        return
    staff = Staff.query.filter_by(role='staff').all()
    print(staff)
    staffid = input('Enter the id of the staff you want to schedule: ')
    shifts = Shift.query.all()
    print(shifts)
    shiftid = input('Enter the id of the shift you want to schedule the staff to: ')

    staff = Staff.query.get(staffid)
    shift = Shift.query.get(shiftid)
    if staff and shift:
        admin.scheduleStaff(staffid, shiftid)
        print(f'Staff member {staff.username} scheduled to shift {shift.shiftid} on {shift.date} ({shift.shiftType})')
    else:
        print('Invalid staff or shift details')

#command to view combined roster
@app.cli.command("view-combined-roster", help="View combined roster for all staff")
@click.argument("week", default=1)
def viewCombinedRosterCommand(week):
    name = input('Enter your name: ')
    name = name.capitalize()
    staff = Staff.query.filter_by(username = name).first()
    if not staff:
        print('Only staff can view the combined roster')
        return
    passw = input('Enter your password: ')
    login = Staff.check_password(staff, passw)
    if not login:
        print('Incorrect password')
        return
    valid_weeks = [shift.week for shift in Shift.query.all()]
    if int(week) not in valid_weeks:
        print(f"Week {week} is not valid. Valid weeks are: {sorted(set(valid_weeks))}")
        return
    if staff:
        staff.viewCombinedRoster(week)

#command to allow staff to clock in
@app.cli.command("clock-in", help="Clock in at start of shift")
@click.argument("name", default='hana')
@click.argument("id", default=1)
def clockInCommand(name, id):
    name = name.capitalize()
    staff = Staff.query.filter_by(username = name).first()   
    if not staff:
        print('Only staff can clock in')
        return
    passw = input('Enter your password: ')
    login = Staff.check_password(staff, passw)
    if not login:
        print('Incorrect password')
        return
    shift = Shift.query.get(id)
    if not shift:
        print(f'No shift {id} found ')
        return
    assigned = Shift.query.filter_by(shiftid = id, staffAssigned = staff.id).first()
    if assigned:
        staff.clockIn(id)
    else:
        print('Invalid staff or shift details')

#command to allow staff to clock out
@app.cli.command("clock-out", help="Clock out at end of shift")
@click.argument("name", default='hana')
@click.argument("id", default=1)
def clockOutCommand(name, id):
    name = name.capitalize()
    staff = Staff.query.filter_by(username = name).first()
    if not staff:
        print('Only staff can clock out')
        return
    passw = input('Enter your password: ')
    login = Staff.check_password(staff, passw)
    if not login:
        print('Incorrect password')
        return
    shift = Shift.query.get(id)
    if not shift:
        print(f'No shift {id}found')
        return
    assigned = Shift.query.filter_by(shiftid = id, staffAssigned = staff.id).first()
    if assigned:
        staff.clockOut(id)
    else:
        print('Invalid staff or shift details')

#command to view shift reports
@app.cli.command("view-report", help="View shift report for week")
@click.argument("week", default=1)
def viewReportCommand(week):
    name = input('Enter your name: ')
    name = name.capitalize()
    admin = Admin.query.filter_by(username = name).first()
    if not admin:
        print('Only admins can view shift reoports')
        return
    passw = input('Enter your password: ')
    login = Admin.check_password(admin, passw)
    if not login:
        print('Incorrect password')
        return
    valid_weeks = [shift.week for shift in Shift.query.all()]
    if int(week) not in valid_weeks:
        print(f"Week {week} is not valid. Valid weeks are: {sorted(set(valid_weeks))}")
        return
    Admin.viewReport(week)
    
#Test Commands

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
