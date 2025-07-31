import datetime

from src.domain.article import Article

fastapi = [
    Article(
        title="Uvod v Fastapi 1",
        subtitle="Zakaj je Fastapi še vedno pomemben leta 2025",
        content="Fastapi je celostni Fastapi framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Fastapi 2",
        subtitle="Zakaj je Fastapi še vedno pomemben leta 2025",
        content="Fastapi je celostni Fastapi framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Fastapi 3",
        subtitle="Zakaj je Fastapi še vedno pomemben leta 2025",
        content="Fastapi je celostni Fastapi framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
