import datetime

from src.domain.language_data import LanguageData

language_data = [
    LanguageData(
        tag= "test",
        count= 1234567,
        last_updated=datetime.datetime.now(),
    ).dict(by_alias=True)
]