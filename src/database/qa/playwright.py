import datetime

from src.domain.language import Language

playwright = [
    Language(
        question='Playwright questions 1',
        answer='Playwright je framework, ki ga dela Google in je zelo priljubljen.',
        language='playwright',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Playwright questions 2',
        answer='Playwright je framework, ki ga dela Google in je zelo priljubljen.',
        language='playwright',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Playwright questions 3',
        answer='Playwright je framework, ki ga dela Google in je zelo priljubljen.',
        language='playwright',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
