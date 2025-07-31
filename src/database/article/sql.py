import datetime

from src.domain.article import Article

sql = [
    Article(
        title="Uvod v Sql 1",
        subtitle="Zakaj je Sql še vedno pomemben leta 2025",
        content="Sql je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Sql 2",
        subtitle="Zakaj je Sql še vedno pomemben leta 2025",
        content="Sql je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Sql 3",
        subtitle="Zakaj je Sql še vedno pomemben leta 2025",
        content="Sql je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
