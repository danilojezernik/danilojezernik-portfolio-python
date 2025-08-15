import datetime

from src.domain.article import Article

playwright = [
    Article(
        title="Uvod v Playwright 1",
        subtitle="Zakaj je Playwright še vedno pomemben leta 2025",
        content="Playwright je celostni Playwright framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Playwright 2",
        subtitle="Zakaj je Playwright še vedno pomemben leta 2025",
        content="Playwright je celostni Playwright framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Playwright 3",
        subtitle="Zakaj je Playwright še vedno pomemben leta 2025",
        content="Playwright je celostni Playwright framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
