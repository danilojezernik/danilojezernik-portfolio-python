import datetime

from src.domain.article import Article

typescript = [
    Article(
        title="Uvod v TypeScript 1",
        subtitle="Zakaj je TypeScript še vedno pomemben leta 2025",
        content="TypeScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v TypeScript 2",
        subtitle="Zakaj je TypeScript še vedno pomemben leta 2025",
        content="TypeScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v TypeScript 3",
        subtitle="Zakaj je TypeScript še vedno pomemben leta 2025",
        content="TypeScript je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
