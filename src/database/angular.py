import datetime

from src.domain.language import Language

angular = [
    Language(
        question='Angular questions 1',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Angular questions 2',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Angular questions 3',
        answer='Angular je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
