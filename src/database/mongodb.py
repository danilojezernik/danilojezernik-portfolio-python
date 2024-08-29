import datetime

from src.domain.mongodb import MongoDb

mongodb = [
    MongoDb(
        question='MongoDb questions 1',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        image='mongodb.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    MongoDb(
        question='MongoDb questions 2',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        image='mongodb.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    MongoDb(
        question='MongoDb questions 3',
        answer='MongoDb je framework, ki ga dela Google in je zelo priljubljen.',
        image='mongodb.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
