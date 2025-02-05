# Fast API imports
from sys import prefix

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import env
from src.domain.angular import Angular
# Import domain for output.txt
from src.domain.blog import Blog
from src.domain.book import Book
from src.domain.contact import Contact
from src.domain.experiences import Experiences
from src.domain.javascript import JavaScript
from src.domain.links import Links
from src.domain.mongodb import MongoDb
from src.domain.newsletter import Newsletter
from src.domain.projects import Projects
from src.domain.python import Python
from src.domain.typescript import TypeScript
from src.domain.vue import Vue
# Imported routes
from src.routes import index, blog, login, experiences, links, contact, projects, github, book, angular, vue, \
    typescript, javascript, mongodb, python, language, dev_to_api, user
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

# Technologies
app.include_router(angular.router, prefix='/angular', tags=['Angular'])
app.include_router(language.router, prefix='/language')
app.include_router(vue.router, prefix='/vue', tags=['Vue'])
app.include_router(javascript.router, prefix='/javascript', tags=['JavaScript'])
app.include_router(typescript.router, prefix='/typescript', tags=['TypeScript'])
app.include_router(python.router, prefix='/python', tags=['Python'])
app.include_router(mongodb.router, prefix='/mongodb', tags=['MongoDB'])

app.include_router(experiences.router, prefix='/experiences', tags=['Experiences'])
app.include_router(links.router, prefix='/links', tags=['Links'])
app.include_router(projects.router, prefix='/projects', tags=['Projects'])

app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(login.router, prefix='/login', tags=['Login'])

app.include_router(contact.router, prefix='/contact', tags=['Contact'])

if __name__ == '__main__':

    # Confirm if you want to drop and seed database
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
            [Blog, Experiences, Contact, Links, Newsletter, Projects, Book, Angular, Vue,
             JavaScript, TypeScript, Python, MongoDb])
        print('Done! Fields have been written to output.txt')
    else:
        print('Document writing aborted')

    uvicorn.run(app, host="127.0.0.1", port=env.PORT)
