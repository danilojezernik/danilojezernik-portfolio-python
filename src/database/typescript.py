import datetime

from src.domain.typescript import TypeScript

typescript = [
    TypeScript(
        question='TypeScript questions 1',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='typescript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    TypeScript(
        question='TypeScript questions 2',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='typescript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    TypeScript(
        question='TypeScript questions 3',
        answer='TypeScript je framework, ki ga dela Google in je zelo priljubljen.',
        image='typescript.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
