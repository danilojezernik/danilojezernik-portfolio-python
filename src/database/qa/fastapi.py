import datetime

from src.domain.language import Language

fastapi = [
    Language(
        question='Fastapi questions 1',
        answer='Fastapi je framework, ki ga dela Google in je zelo priljubljen.',
        language='fastapi',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Fastapi questions 2',
        answer='Fastapi je framework, ki ga dela Google in je zelo priljubljen.',
        language='fastapi',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Fastapi questions 3',
        answer='Fastapi je framework, ki ga dela Google in je zelo priljubljen.',
        language='fastapi',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
