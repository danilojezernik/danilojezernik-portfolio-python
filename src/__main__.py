# Fast API imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import subprocess
import sys

from src import env
from src.domain.language import Language

# Import domain for output.txt
from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.contact import Contact
from src.domain.experiences import Experiences
from src.domain.language_data import LanguageData
from src.domain.links import Links
from src.domain.projects import Projects
from src.domain.article import Article
from src.domain.dev_api import DevAritcle, User


from src.services import db
from src.services.routers import routers
from src.tags_metadata import tags_metadata
from src.utils.domain_to_txt import write_fields_to_txt

app = FastAPI(openapi_tags=tags_metadata)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Check health for this initialization
@app.get('/healthy')
def health_check():
    return {'status': 'healthy'}

# Loop through and register all routers
for router, prefix, tags in routers:
    app.include_router(router, prefix=prefix, tags=tags)


def run_tests():
    """Run pytest and return True if all tests pass."""
    result = subprocess.run(["pytest", "--html=test/html_report/report.html", "--self-contained-html"])
    return result.returncode == 0  # 0 means success, non-zero means failure

if __name__ == '__main__':

    yes = input('Type "y" if you want to drop the entire DATABASE: ').strip().lower()
    if yes == 'y':
        print('drop_all_collections() initialized')
        db.drop_all_collections()
        # optionally re-seed here
    else:
        print('Database drop and seed skipped')

    # Confirm if you want to drop and seed a database
    yes = input('Type "y" if you want to run drop and seed: ').strip().lower()
    if yes == 'y':
        print('drop() and seed() initialized')
        db.drop()
        db.seed()
    else:
        print('Database drop and seed skipped')

    # Confirm if you want to drop and seed users database
    drop_user = input('If you want to drop user type "y": ').strip().lower()
    if drop_user == 'y':
        db.drop_user()
        db.seed_user()
    else:
        print('User drop and seed skipped')

    # Confirm if you want to write fields to output.txt
    yes_doc = input('Type "y" if you want to write the document and press enter: ').strip().lower()
    if yes_doc == 'y':
        print('Writing fields to output.txt...')
        write_fields_to_txt(
            [Blog, Experiences, Contact, Links, Projects, Book, Language, Article, DevAritcle, User, LanguageData])
        print('Done! Fields have been written to output.txt')
    else:
        print('Document writing aborted')

    if run_tests():
        print("✅ All tests passed! Starting FastAPI application...")
        uvicorn.run(app, host="127.0.0.1", port=env.PORT)
    else:
        print("❌ Tests failed! Fix issues before running the application.")
        sys.exit(1)
