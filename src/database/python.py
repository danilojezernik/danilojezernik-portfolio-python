import datetime

from src.domain.language import Language

python = [
    Language(
        question='Python questions 1',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        language='python',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Python questions 2',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        language='python',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Python questions 3',
        answer='Python je framework, ki ga dela Google in je zelo priljubljen.',
        language='python',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
