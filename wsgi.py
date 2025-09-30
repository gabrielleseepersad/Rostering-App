import click, pytest, sys
#from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Staff, Admin, Shift, Roster, TimeLog)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize,  )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    hana = User(id = 1, name = 'Hana', password = 'hanapass', role = 'admin', email = 'hana@mail.com')
    jordana = User(id = 2, name = 'Jordana', password = 'jordanapass', role = 'staff' , email = 'jordana@mail.com')
    brittney = User(id = 3, name = 'Brittney', password = 'brittneypass', role = 'staff', email = 'brittney@mail.com')
    shift1 = Shift(shiftid = 1, staffAssigned = 'Jordana', rosterid = 1, shiftType = 'AM', week = 1, hours = 8, date = '2025-06-02')
    shift2 = Shift(shiftid = 2, staffAssigned = 'Brittney', rosterid = 1, shiftType = 'PM', week = 1, hours = 8, date = '2025-06-02')
    shift3 = Shift(shiftid = 3, staffAssigned = 'Jordana', rosterid = 1, shiftType = 'AM', week = 1, hours = 8, date = '2025-06-03')
    shift4 = Shift(shiftid = 4, staffAssigned = 'Brittney', rosterid = 1, shiftType = 'PM', week = 1, hours = 8, date = '2025-06-03')
    shift5 = Shift(shiftid = 5, staffAssigned = 'Jordana', rosterid = 1, shiftType = 'AM', week = 1, hours = 8, date = '2025-06-04')
    shift6 = Shift(shiftid = 6, staffAssigned = 'Brittney', rosterid = 1, shiftType = 'PM', week = 1, hours = 8, date = '2025-06-04')
    shift7 = Shift(shiftid = 7, staffAssigned = 'Jordana', rosterid = 1, shiftType = 'AM', week = 1, hours = 8, date = '2025-06-05')
    shift8 = Shift(shiftid = 8, staffAssigned = 'Brittney', rosterid = 1, shiftType = 'PM', week = 1, hours = 8, date = '2025-06-05')
    shift9 = Shift(shiftid = 9, staffAssigned = 'Jordana', rosterid = 1, shiftType = 'AM', week = 1, hours = 8, date = '2025-06-06')
    shift10 = Shift(shiftid = 10, staffAssigned = 'Brittney ', rosterid = 1, shiftType = 'PM', week = 1, hours = 8, date = '2025-06-06')
    shift11 = Shift(shiftid = 11, staffAssigned = 'Brittney', rosterid = 2, shiftType = 'AM', week = 2, hours = 8, date = '2025-06-09')
    shift12 = Shift(shiftid = 12, staffAssigned = 'Jordana', rosterid = 2, shiftType = 'PM', week = 2, hours = 8, date = '2025-06-09')
    shift13 = Shift(shiftid = 13, staffAssigned = 'Brittney', rosterid = 2, shiftType = 'AM', week = 2, hours = 8, date = '2025-06-10')
    shift14 = Shift(shiftid = 14, staffAssigned = 'Jordana', rosterid = 2, shiftType = 'PM', week = 2, hours = 8, date = '2025-06-10')
    roster1 = Roster(rosterid = 1, week = 1)
    roster2 = Roster(rosterid = 2, week = 2)
    db.session.add_all([hana, jordana, brittney, shift1, shift2, shift3, shift4, shift5, shift6, shift7, shift8, shift9, shift10, shift11,
    shift12, shift13, shift14, roster1, roster2])
    db.session.commit()
    print('Database intialized')


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

#command to schedule staff
@app.cli.command("schedule-staff", help="Schedule staff to a shift")
def scheduleStaffCommand():
    userid = input('Enter your user id: ')
    user = User.query.get(userid)
    role = user.role
    if role != 'admin':
        print('Only admins can schedule staff')
        return
    staff = User.query.filter_by(role='staff').all()
    print(staff)
    staffid = input('Enter the id of the staff you want to schedule: ')
    shifts = Shift.query.all()
    print(shifts)
    date = input('Enter the date of the shift you want to schedule the staff to: ')
    type = input('Enter the type of shift (AM/PM): ')

    staff = User.query.get(staffid)
    shift = Shift.query.filter_by(date=date, shiftType=type).first()

    if staff and shift:
        admin.scheduleStaff(staff.id, shift.shiftid)
        print(f'Staff member {staff.name} scheduled to shift {shift.shiftid} on {shift.date} ({shift.shiftType})')
    else:
        print('Invalid staff or shift details')

#command to view combined roster
@app.cli.command("view-combined-roster", help="View combined roster for all staff")
@click.argument("week", default=1)
def viewCombinedRosterCommand(week):
    userid = input('Enter your user id: ')
    user = User.query.get(userid)
    role = user.role
    if role != 'staff':
        print('Only staff can view combined roster')
        return
    if role == 'staff':
        staff.viewCombinedRoster(week)
    else:
        print('Invalid week entered')

#command to allow staff to clock in
@app.cli.command("clock-in", help="Clock in at start of shift")
@click.argument("staffid", default=1)
@click.argument("date", default="2025-06-02")
def clockInCommand(staffid, date):
    staff = User.query.get(staffid)
    role = staff.role
    if role != 'staff':
        print('Only staff can clock in')
        return
    shift = Shift.query.filter_by(staffAssigned=staff.name, date=date).first()
    if not shift:
        print(f'No shift found for staff {staff.name} on {date}')
        return
    if staff:
        staff.clockIn(shift.shiftid)
    else:
        print('Invalid staff or shift details')

#command to allow staff to clock out
@app.cli.command("clock-out", help="Clock out at end of shift")
@click.argument("staffid", default=1)
@click.argument("date", default="2025-06-02")
def clockOutCommand(staffid, date):
    staff = User.query.get(staffid)
    role = staff.role
    if role != 'staff':
        print('Only staff can clock out')
        return
    shift = Shift.query.filter_by(staffAssigned=staff.name, date=date).first()
    if not shift:
        print(f'No shift found for staff {staff.name} on {date}')
        return
    if staff:
        staff.clockOut(shift.shiftid)
    else:
        print('Invalid staff or shift details')

#command to view shift reports
@app.cli.command("view-report", help="View shift report for week")
@click.argument("week", default=1)
def viewReportCommand(week):
    userid = input('Enter your user id: ')
    user = User.query.get(userid)
    role = user.role
    if role != 'admin':
        print('Only admins can view shift reports')
        return
    if role == 'admin':
        admin.viewReport(week)
    else:
        print('Invalid week entered')


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