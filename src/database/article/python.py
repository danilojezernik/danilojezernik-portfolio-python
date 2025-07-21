import datetime

from src.domain.article import Article

python = [
    Article(
        title="Uvod v Python 1",
        subtitle="Zakaj je Python še vedno pomemben leta 2025",
        content="Python je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Python 2",
        subtitle="Zakaj je Python še vedno pomemben leta 2025",
        content="Python je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Python 3",
        subtitle="Zakaj je Python še vedno pomemben leta 2025",
        content="Python je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
