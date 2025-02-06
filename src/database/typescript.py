import datetime

from src.domain.language import Language

typescript = [
    Language(
        question='TypeScript questions 1',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='TypeScript questions 2',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='TypeScript questions 3',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        language='typescript',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
