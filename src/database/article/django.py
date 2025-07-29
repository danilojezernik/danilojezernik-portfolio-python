import datetime

from src.domain.article import Article

django = [
    Article(
        title="Uvod v Django 1",
        subtitle="Zakaj je Django še vedno pomemben leta 2025",
        content="Django je celostni Django framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Django 2",
        subtitle="Zakaj je Django še vedno pomemben leta 2025",
        content="Django je celostni Django framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Django 3",
        subtitle="Zakaj je Django še vedno pomemben leta 2025",
        content="Django je celostni Django framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
