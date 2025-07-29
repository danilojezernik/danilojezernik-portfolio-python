import datetime

from src.domain.language import Language

django = [
    Language(
        question='Django questions 1',
        answer='Django je framework, ki ga dela Google in je zelo priljubljen.',
        language='django',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Django questions 2',
        answer='Django je framework, ki ga dela Google in je zelo priljubljen.',
        language='django',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Django questions 3',
        answer='Django je framework, ki ga dela Google in je zelo priljubljen.',
        language='django',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
