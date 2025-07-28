import datetime

from src.domain.article import Article

cypress = [
    Article(
        title="Uvod v Cypress 1",
        subtitle="Zakaj je Cypress še vedno pomemben leta 2025",
        content="Cypress je celostni Cypress framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Cypress 2",
        subtitle="Zakaj je Cypress še vedno pomemben leta 2025",
        content="Cypress je celostni Cypress framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Cypress 3",
        subtitle="Zakaj je Cypress še vedno pomemben leta 2025",
        content="Cypress je celostni Cypress framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
