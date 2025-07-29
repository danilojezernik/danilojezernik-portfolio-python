import datetime

from src.domain.language import Language

nuxt = [
    Language(
        question='Nuxt questions 1',
        answer='Nuxt je framework, ki ga dela Google in je zelo priljubljen.',
        language='nuxt',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Nuxt questions 2',
        answer='Nuxt je framework, ki ga dela Google in je zelo priljubljen.',
        language='nuxt',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Language(
        question='Nuxt questions 3',
        answer='Nuxt je framework, ki ga dela Google in je zelo priljubljen.',
        language='nuxt',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
