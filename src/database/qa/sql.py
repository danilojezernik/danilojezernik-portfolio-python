import datetime

from src.domain.language import Language

sql = [
    Language(
        question='Sql questions 1',
        answer='Sql je framework, ki ga dela Google in je zelo priljubljen.',
        language='sql',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Sql questions 2',
        answer='Sql je framework, ki ga dela Google in je zelo priljubljen.',
        language='sql',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Sql questions 3',
        answer='Sql je framework, ki ga dela Google in je zelo priljubljen.',
        language='sql',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
