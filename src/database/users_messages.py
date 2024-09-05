import datetime

from src.domain.users_messages import Messages

message_reg = [
    Messages(
        user_id='user_id_1',
        full_name_sender='user_id_1',
        email_sender='samhara.sadhaka@gmail.com',
        message='user_id_1',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Messages(
        user_id='user_id_2',
        full_name_sender='user_id_2',
        email_sender='danilo.jezernik@gmail.com',
        message='user_id_2',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]