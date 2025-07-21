import datetime

from src.domain.article import Article

mongodb = [
    Article(
        title="Uvod v MongoDB 1",
        subtitle="Zakaj je Angular še vedno pomemben leta 2025",
        content="Angular je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Angular 2",
        subtitle="Zakaj je Angular še vedno pomemben leta 2025",
        content="Angular je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Angular 3",
        subtitle="Zakaj je Angular še vedno pomemben leta 2025",
        content="Angular je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
