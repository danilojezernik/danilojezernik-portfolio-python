import datetime

from src.domain.article import Article

pytest = [
    Article(
        title="Uvod v Pytest 1",
        subtitle="Zakaj je Pytest še vedno pomemben leta 2025",
        content="Pytest je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Pytest 2",
        subtitle="Zakaj je Pytest še vedno pomemben leta 2025",
        content="Pytest je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Pytest 3",
        subtitle="Zakaj je Pytest še vedno pomemben leta 2025",
        content="Pytest je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
