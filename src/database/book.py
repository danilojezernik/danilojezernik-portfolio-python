import datetime

from src.domain.book import Book

book = [
    Book(
        naslov='Test Knjiga 1',
        tehnologija='angular',
        podnaslov='Test Podnaslov 1',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 1',
        image='test1.jpg'
    ).dict(by_alias=True),
    Book(
        naslov='Test Knjiga 2',
        tehnologija='angular',
        podnaslov='Test Podnaslov 2',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 2',
        image='test2.jpg'
    ).dict(by_alias=True),
    Book(
        naslov='Test Knjiga 3',
        tehnologija='angular',
        podnaslov='Test Podnaslov 3',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 3',
        image='test3.jpg'
    ).dict(by_alias=True),
]
