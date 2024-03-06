from src.domain.user import User

user = [
    User(
        username='danilojezernik',
        email='dani.jezernik@gmail.com',
        full_name='Danilo Jezernik',
        hashed_password='$2b$12$/4Ku22NMcxccpiFaIMDJheezk0Q0eDHGyvod3FaToy.BqfaDXM2km',
        disabled=False
    ).dict(by_alias=True)
]