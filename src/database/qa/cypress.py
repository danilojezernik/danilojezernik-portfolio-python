import datetime

from src.domain.language import Language

cypress = [
    Language(
        question='Cypress questions 1',
        answer='Cypress je framework, ki ga dela Google in je zelo priljubljen.',
        language='cypress',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Cypress questions 2',
        answer='Cypress je framework, ki ga dela Google in je zelo priljubljen.',
        language='cypress',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Cypress questions 3',
        answer='Cypress je framework, ki ga dela Google in je zelo priljubljen.',
        language='cypress',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
