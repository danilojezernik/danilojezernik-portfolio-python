import datetime

from src.domain.email_data import EmailData

sent_email_data = [
    EmailData(
        full_name='Danilo',
        sender_email='dani.jezernik@gmail.com',
        message='neki se deal',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    EmailData(
        full_name='Dani',
        sender_email='danilo.jezernik@gmail.com',
        message='neki se deal',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]