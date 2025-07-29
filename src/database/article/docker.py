import datetime

from src.domain.article import Article

docker = [
    Article(
        title="Uvod v Docker 1",
        subtitle="Zakaj je Docker še vedno pomemben leta 2025",
        content="Docker je celostni Docker framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Docker 2",
        subtitle="Zakaj je Docker še vedno pomemben leta 2025",
        content="Docker je celostni Docker framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Docker 3",
        subtitle="Zakaj je Docker še vedno pomemben leta 2025",
        content="Docker je celostni Docker framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
