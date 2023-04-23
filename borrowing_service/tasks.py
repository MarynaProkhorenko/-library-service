import datetime

from borrowing_service.models import Borrowing
from celery import shared_task

from borrowing_service.notifications_bot import send_message


@shared_task
def notification_overdue_borrowings() -> None:
    today_data = datetime.date.today()
    overdue_borrowings = Borrowing.objects.filter(
        expected_return_date_lte=today_data + datetime.timedelta(days=1),
        actual_return_date__isnull=True
    )
    if overdue_borrowings:
        for borrowing in overdue_borrowings:
            message = (
                f"User: {borrowing.user}\n"
                f"Has overdue borrowing of book:\n"
                f"{borrowing.book}\n"
                f"Expected return date was : {borrowing.expected_return_date}\n"
            )
            send_message(message)
    else:
        send_message("No borrowings overdue today!")
