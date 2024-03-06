import datetime

from src.domain.blog import Blog

blog = [
    Blog(
        naslov='Test Naslov 1',
        kategorija='angular',
        podnaslov='Test Podnaslov 1',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 1'
    ).dict(by_alias=True),
    Blog(
        naslov='Test Naslov 2',
        kategorija='angular',
        podnaslov='Test Podnaslov 2',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 2'
    ).dict(by_alias=True),
    Blog(
        naslov='Test Naslov 3',
        kategorija='angular',
        podnaslov='Test Podnaslov 3',
        datum_vnosa=datetime.datetime.now(),
        vsebina='Test Vsebina 3'
    ).dict(by_alias=True),
]
