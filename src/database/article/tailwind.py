import datetime

from src.domain.article import Article

tailwind = [
    Article(
        title="Uvod v Tailwind 1",
        subtitle="Zakaj je Tailwind še vedno pomemben leta 2025",
        content="Tailwind je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Tailwind 2",
        subtitle="Zakaj je Tailwind še vedno pomemben leta 2025",
        content="Tailwind je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Tailwind 3",
        subtitle="Zakaj je Tailwind še vedno pomemben leta 2025",
        content="Tailwind je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
