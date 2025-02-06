import datetime

from src.domain.language import Language

vue = [
    Language(
        question='Vue questions 1',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Vue questions 2',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Vue questions 3',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
