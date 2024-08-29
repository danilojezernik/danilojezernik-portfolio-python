import datetime

from src.domain.angular import Angular

angular = [
    Angular(
        question='Angular questions 1',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        image='angular1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Angular(
        question='Angular questions 2',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        image='angular1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Angular(
        question='Angular questions 3',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        image='angular1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
