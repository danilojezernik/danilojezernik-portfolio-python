# Fast API imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import env

# Imported routes
from src.routes import index, blog, email, login, user

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
app.include_router(user.router, prefix='/user', tags=['User'])
app.include_router(blog.router, prefix='/blog', tags=['Blog'])
app.include_router(email.router, prefix='/email', tags=['Email'])
app.include_router(login.router, prefix='/login', tags=['Login'])

if __name__ == '__main__':

    # Confirm if you want to drop and seed database
    yes = input('Type "d" if you want to run drop and seed?')
    true = 'd'

    if yes == true:
        print('drop() and seed() initialized')
        db.drop()
        db.seed()
    else:
        print('pass')
        pass

    uvicorn.run(app, host="127.0.0.1", port=env.PORT)
