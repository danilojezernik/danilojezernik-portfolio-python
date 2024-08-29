import datetime

from src.domain.javascript import JavaScript

javascript = [
    JavaScript(
        question='JavaScript questions 1',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='javascript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    JavaScript(
        question='JavaScript questions 2',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='javascript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    JavaScript(
        question='JavaScript questions 3',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='javascript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
