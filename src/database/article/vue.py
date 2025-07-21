import datetime

from src.domain.article import Article

vue = [
    Article(
        title="Uvod v Vue 1",
        subtitle="Zakaj je Vue še vedno pomemben leta 2025",
        content="Vue je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Vue 2",
        subtitle="Zakaj je Vue še vedno pomemben leta 2025",
        content="Vue je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Vue 3",
        subtitle="Zakaj je Vue še vedno pomemben leta 2025",
        content="Vue je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
