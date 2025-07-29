import datetime

from src.domain.language import Language

docker = [
    Language(
        question='Docker questions 1',
        answer='Docker je framework, ki ga dela Google in je zelo priljubljen.',
        language='docker',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Docker questions 2',
        answer='Docker je framework, ki ga dela Google in je zelo priljubljen.',
        language='docker',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Docker questions 3',
        answer='Docker je framework, ki ga dela Google in je zelo priljubljen.',
        language='docker',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
