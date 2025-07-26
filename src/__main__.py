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
from src.domain.links import Links
from src.domain.projects import Projects
from src.domain.article import Article
# Imported routes
from src.routes import index, blog, login, experiences, links, contact, projects, github, book, language, dev_to_api, user
from src.routes.qa import typescript as qa_typescript, python as qa_python, angular as qa_angular, javascript as qa_javascript, mongodb as qa_mongodb, vue as qa_vue
from src.routes.article import typescript as article_typescript, python as article_python, angular as article_angular, javascript as article_javascript, mongodb as article_mongodb, vue as article_vue
from src.services import db
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

app.include_router(index.router, prefix='/index', tags=['Index'])
app.include_router(blog.router, prefix='/blog', tags=['Blog'])
app.include_router(dev_to_api.router, prefix='/dev', tags=['Dev'])
app.include_router(github.router, prefix='/github', tags=['Github'])
app.include_router(book.router, prefix='/book', tags=['Book'])

# Technologies - QA
app.include_router(qa_angular.router, prefix='/qa/angular', tags=['Angular'])
app.include_router(qa_vue.router, prefix='/qa/vue', tags=['Vue'])
app.include_router(qa_javascript.router, prefix='/qa/javascript', tags=['JavaScript'])
app.include_router(qa_typescript.router, prefix='/qa/typescript', tags=['TypeScript'])
app.include_router(qa_python.router, prefix='/qa/python', tags=['Python'])
app.include_router(qa_mongodb.router, prefix='/qa/mongodb', tags=['MongoDB'])

# Technologies - Articles
app.include_router(article_angular.router, prefix='/article/angular', tags=['Angular'])
app.include_router(article_vue.router, prefix='/article/vue', tags=['Vue'])
app.include_router(article_javascript.router, prefix='/article/javascript', tags=['JavaScript'])
app.include_router(article_typescript.router, prefix='/article/typescript', tags=['TypeScript'])
app.include_router(article_python.router, prefix='/article/python', tags=['Python'])
app.include_router(article_mongodb.router, prefix='/article/mongodb', tags=['MongoDB'])
app.include_router(language.router, prefix='/language')

app.include_router(experiences.router, prefix='/experiences', tags=['Experiences'])
app.include_router(links.router, prefix='/links', tags=['Links'])
app.include_router(projects.router, prefix='/projects', tags=['Projects'])

app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(login.router, prefix='/login', tags=['Login'])

app.include_router(contact.router, prefix='/contact', tags=['Contact'])


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
            [Blog, Experiences, Contact, Links, Projects, Book, Language, Article])
        print('Done! Fields have been written to output.txt')
    else:
        print('Document writing aborted')

    if run_tests():
        print("✅ All tests passed! Starting FastAPI application...")
        uvicorn.run(app, host="127.0.0.1", port=env.PORT)
    else:
        print("❌ Tests failed! Fix issues before running the application.")
        sys.exit(1)
