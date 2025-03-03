
from .models import Mailing, Attempt
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.utils import timezone
from datetime import timedelta





def send_emails():
    now = timezone.now()
    mailings = Mailing.objects.filter(status='CREATED', first_sanding_data__lte=now)

    for mailing in mailings:
        mailing.status = 'STARTED'
        if mailing.intervals == 'DAILY':
            mailing.first_sanding_data = now + timedelta(days=1)
        elif mailing.intervals == 'WEEKLY':
            mailing.first_sanding_data = now + timedelta(days=7)
        elif mailing.intervals == 'MONTHLY':
            mailing.first_sanding_data = now + timedelta(days=31)
        mailing.save()
        topic = mailing.message.topic
        content = mailing.message.content
        list_emails = mailing.clients.all()

        print(topic)
        print(content)
        print([client.email for client in list_emails])
        try:

            send_mail(
                subject=topic,
                message=content,
                from_email='Trueinstrument.ru@yandex.ru',
                recipient_list=[client.email for client in list_emails],
                fail_silently=False
            )

            Attempt.objects.create(mailing=mailing, status='SUCCESS', last_sanding_data=now, server_answer=f"Рассылка успешно отправлена :)")
            mailings.status = 'COMPLETED'
            mailing.save()
            print(f"Рассылка {mailing.id} успешно отправлена :)")
        except Exception as e:
            # В случае ошибки фиксируем неудачную попытку с указанием причины
            Attempt.objects.create(mailing=mailing, status='FAILED', last_sanding_data=now, server_answer=f"Рассылка не отправлена :(")
            print(f"Ошибка при отправке рассылки: Некоретно введен email")

        else:
            Attempt.objects.create(mailing=mailing, status='FAILED', last_sanding_data=now,
                                   server_answer=f"Нету клиентов у рассылки.")
            print(f"Ошибка при отправке рассылки: Нету клиентов у рассылки.")


scheduler = BackgroundScheduler()

def start_scheduler():
    # Запланируйте выполнение задачи каждую минуту:
    scheduler.add_job(send_emails, IntervalTrigger(minutes=1))
    scheduler.start()
