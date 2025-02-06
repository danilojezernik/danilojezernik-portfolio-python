import datetime

from src.domain.language import Language

javascript = [
    Language(
        question='JavaScript questions 1',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='javascript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='JavaScript questions 2',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='javascript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='JavaScript questions 3',
        answer='JavaScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='javascript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
