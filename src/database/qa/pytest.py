import datetime

from src.domain.language import Language

pytest = [
    Language(
        question='Pytest questions 1',
        answer='Pytest je framework, ki ga dela Google in je zelo priljubljen.',
        language='pytest',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Pytest questions 2',
        answer='Pytest je framework, ki ga dela Google in je zelo priljubljen.',
        language='pytest',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Pytest questions 3',
        answer='Pytest je framework, ki ga dela Google in je zelo priljubljen.',
        language='pytest',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
