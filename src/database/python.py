import datetime

from src.domain.python import Python

python = [
    Python(
        question='Python questions 1',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        image='python.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Python(
        question='Python questions 2',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        image='python.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Python(
        question='Python questions 3',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        image='python.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
