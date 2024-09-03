import datetime

from src.domain.contact import Contact

contact = [
    Contact(
        full_name='Tester',
        email='dani.jezernik@gmail.com',
        message='Testiram ali je email prišel',
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]