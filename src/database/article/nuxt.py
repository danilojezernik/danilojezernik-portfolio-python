import datetime

from src.domain.article import Article

nuxt = [
    Article(
        title="Uvod v Nuxt 1",
        subtitle="Zakaj je Nuxt še vedno pomemben leta 2025",
        content="Nuxt je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Nuxt 2",
        subtitle="Zakaj je Nuxt še vedno pomemben leta 2025",
        content="Nuxt je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
    Article(
        title="Uvod v Nuxt 3",
        subtitle="Zakaj je Nuxt še vedno pomemben leta 2025",
        content="Nuxt je celostni TypeScript framework, ki ga uporablja veliko podjetij za gradnjo robustnih aplikacij...",
        author="Danilo Jezernik",
        datum_vnosa=datetime.datetime.now(),
    ).dict(by_alias=True),
]
