from django.shortcuts import render, redirect
from .models import PillReminder
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.dateparse import parse_datetime
from twilio.rest import Client

scheduler = BackgroundScheduler()
scheduler.start()

def send_sms(to, message):
    account_sid = 'YOUR_TWILIO_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_='+YOUR_TWILIO_NUMBER',
        to=to
    )

def set_reminder(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        medicine = request.POST.get("medicine")
        time = parse_datetime(request.POST.get("time"))

        reminder = PillReminder.objects.create(
            name=name,
            phone_number=phone,
            medicine=medicine,
            time=time
        )

        def job():
            send_sms(phone, f"Hi {name}, it's time to take your medicine: {medicine}")

        scheduler.add_job(job, 'date', run_date=time)

        return render(request, "remainder_setter/reminder_success.html", {"reminder": reminder})

    return render(request, "remainder_setter/set_reminder.html")
