import datetime

from src.domain.language import Language

mongodb = [
    Language(
        question='MongoDb questions 1',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        language='mongodb',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='MongoDb questions 2',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        language='mongodb',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='MongoDb questions 3',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        language='mongodb',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
