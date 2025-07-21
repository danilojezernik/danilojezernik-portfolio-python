import datetime

from src.domain.article import Article

javascript = [
    Article(
        title="Uvod v JavaScript 1",
        subtitle="Zakaj je JavaScript še vedno pomemben leta 2025",
        content="JavaScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v JavaScript 2",
        subtitle="Zakaj je JavaScript še vedno pomemben leta 2025",
        content="JavaScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v JavaScript 3",
        subtitle="Zakaj je JavaScript še vedno pomemben leta 2025",
        content="JavaScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
