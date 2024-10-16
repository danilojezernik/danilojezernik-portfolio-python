import datetime

from src.domain.user import User

user = [
    User(
        username='danilojezernik',
        email='dani.jezernik@gmail.com',
        full_name='Danilo Jezernik',
        profession='Software inženir',
        technology='JavaScript, Python, MongoDB, FastAPI,...',
        description='Sem zavzet softvare developer in imam nekaj izkušenj',
        hashed_password='$2b$12$/4Ku22NMcxccpiFaIMDJheezk0Q0eDHGyvod3FaToy.BqfaDXM2km',
        role='admin',
        facebook='facebook',
        instagram='instagram',
        youtube='youtube',
        twitter='twitter',
        github='github',
        www='www',
        disabled=False,
        confirmed=False,
        registered=True,
        blog_notification=False,
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True),
    User(
        username='danitest',
        email='dani.jezernik@gmail.com',
        full_name='Danilo Jezernik',
        profession='Software inženir',
        technology='JavaScript, Python, MongoDB, FastAPI,...',
        description='Sem zavzet softvare developer in imam nekaj izkušenj',
        hashed_password='$2b$12$/4Ku22NMcxccpiFaIMDJheezk0Q0eDHGyvod3FaToy.BqfaDXM2km',
        role='visitor',
        facebook='facebook',
        instagram='instagram',
        youtube='youtube',
        twitter='twitter',
        github='github',
        www='www',
        disabled=False,
        confirmed=False,
        registered=True,
        blog_notification=False,
        datum_vnosa=datetime.datetime.now()
    ).dict(by_alias=True)
]
