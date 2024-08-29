import datetime

from src.domain.vue import Vue

vue = [
    Vue(
        question='Vue questions 1',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        image='vue1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Vue(
        question='Vue questions 2',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        image='vue1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Vue(
        question='Vue questions 3',
        answer='Vue je framework, ki ga dela Google in je zelo priljubljen.',
        image='vue1.jpg',
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True)
]
