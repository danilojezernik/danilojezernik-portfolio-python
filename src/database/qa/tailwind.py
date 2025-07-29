import datetime

from src.domain.language import Language

tailwind = [
    Language(
        question='Tailwind questions 1',
        answer='Tailwind je framework, ki ga dela Google in je zelo priljubljen.',
        language='tailwind',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Tailwind questions 2',
        answer='Tailwind je framework, ki ga dela Google in je zelo priljubljen.',
        language='tailwind',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Tailwind questions 3',
        answer='Tailwind je framework, ki ga dela Google in je zelo priljubljen.',
        language='tailwind',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
