from applications.models import *
from datetime import datetime
import csv
from celery.schedules import crontab
from applications.worker import celery
from applications.mailer import sendMail, SendMemer
from applications.store import reportGenrator


@celery.task()
def exporter(venue_details, show_details, rmail, user):
    fname = f'src/{user}_details.csv'

    venue_fields = ['Venue Name', 'Loaction', 'Capacity'] 
    show_fields = ['Show Movie', 'Start Time', 'End Time', 'Ticket Price', 'Movie Rating', 'Ticket Sold']

    with open(fname, 'w', newline='', encoding='utf8') as csvf: 
    # creating a csv writer object 
        cwriter = csv.writer(csvf) 
        cwriter.writerow(venue_fields) 
        cwriter.writerows(venue_details)
        cwriter.writerow(show_fields) 
        cwriter.writerows(show_details)

    SendMemer(receiver=rmail, subject="Venue Details Mail", message= "Please find attached venue details csv. Thankyou!", attachment=f'src/{user}_details.csv')
    return "CSV file exported!"


@celery.task()
def just_say_hello():
    users = User.query.filter_by(is_admin = False).all()
    for u in users:
        rm = u.email_id
        sendMail(rm, subject="Testing Mail", message="Hello! How are you?")
    return "Testing done!"



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('deadlineReminder') every 10 seconds.
    sender.add_periodic_task(10.0, just_say_hello.s(), name='just_say_hello')

    # Calls deadlineReminder.s() daily.
    sender.add_periodic_task(10, dailyReminder.s(), name='DailyReminder') 

    # Calls monthReport.s() on 1st day of the month.
    sender.add_periodic_task(10, monthlyReport.s(), name='MonthlyReport')

    sender.add_periodic_task(
        crontab(minute=0, hour=18, day_of_month='*'),
        dailyReminder.s(),
        name = 'Daily reminder everyday @6PM via mail.'
    )

    sender.add_periodic_task(
        crontab(day_of_month=1, month_of_year='*'),
        monthlyReport.s(),
        name = 'Monthly Entertainment Report @1st of every month via mail.'
    )


@celery.task
def dailyReminder():
    users = User.query.filter_by(is_admin = False).all()
    for u in users:
        if u.latest_log < str(datetime.now()):
            rmail = u.email_id
            sendMail(rmail, subject="Daily Reminder", message="Hey! Visit the TicketShow and book a ticket for your favourite movie!")
    return "Daily reminder done!"


@celery.task
def monthlyReport(): 
    users = User.query.filter_by(is_admin = False).all()
    for u in users:
        username = u.name
        usermail = u.email_id
        all_shows = Register.query.filter_by(user_id=u.id).all()
        if all_shows is not None:
            full_details = []
            for b in all_shows:
                show = Show.query.filter_by(show_id = b.show_id).first()
                booking_details = []
                booking_details.append(show.venue_name)
                booking_details.append(show.movie_name)
                booking_details.append(show.start)
                booking_details.append(show.end)
                booking_details.append(show.ticket_price)
                booking_details.append(show.movie_rating)
                booking_details.append(b.ticket_count)

                full_details.append(booking_details)

        file = reportGenrator("src/reporter.html", full_details, username)

        SendMemer(usermail, subject="Monthly Entertainment Report", message = "Hello! Please find attached you monthly entertainment report.", attachment=f'{file}')
    return "Monthly Reports Sent!"  
