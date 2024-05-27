# Fast API imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import env
from src.domain.blog import Blog
from src.domain.experiences import Experiences

# Imported routes
from src.routes import index, blog, email, login, user, experiences, links, register, contact, projects, newsletter, \
    subscriber, comments

from src.services import db

from src.tags_metadata import tags_metadata

app = FastAPI(openapi_tags=tags_metadata)

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(index.router, prefix='/index', tags=['Index'])
app.include_router(blog.router, prefix='/blog', tags=['Blog'])

app.include_router(comments.router, prefix='/comments', tags=['Comment'])
app.include_router(experiences.router, prefix='/experiences', tags=['Experiences'])
app.include_router(links.router, prefix='/links', tags=['Links'])
app.include_router(email.router, prefix='/email', tags=['Email'])
app.include_router(projects.router, prefix='/projects', tags=['Projects'])

app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(login.router, prefix='/login', tags=['Login'])
app.include_router(register.router, prefix="/register", tags=["Register"])

app.include_router(contact.router, prefix='/contact', tags=['Contact'])
app.include_router(newsletter.router, prefix='/newsletter', tags=['Newsletter'])
app.include_router(subscriber.router, prefix='/subscriber', tags=['Subscriber'])


# Function to write fields to a text file
def write_fields_to_txt(models):
    with open('output.txt', 'w') as f:
        for model in models:
            model_name = model.__name__
            f.write(f"{model_name}:\n")
            for field in model.__fields__.keys():
                f.write(f"  {field}\n")
            f.write("\n")


if __name__ == '__main__':

    # Confirm if you want to drop and seed database
    yes = input('Type "d" if you want to run drop and seed?')
    yes_doc = input('Type "doc" if you want to write the document and press enter: ')

    true = 'd'

    if yes == true:
        print('drop() and seed() initialized')
        db.drop()
        db.seed()
        drop_user = input('If you want to drop user type "d"')
        true = 'd'
        if drop_user == true:
            db.drop_user()
            db.seed_user()
        else:
            print('User pass')
            pass
    else:
        print('All pass')
        pass

    if yes_doc == 'doc':
        print('Writing fields to output.txt...')
        write_fields_to_txt([Blog, Experiences])
        print('Done! Fields have been written to output.txt')
    else:
        print('Operation aborted')

    # Test connection to database for docker
    try:
        db.client.admin.command('ping')
        print("Database connection successful")
    except Exception as e:
        print(f"Database connection failed: {e}")

    uvicorn.run(app, host="127.0.0.1", port=env.PORT)
