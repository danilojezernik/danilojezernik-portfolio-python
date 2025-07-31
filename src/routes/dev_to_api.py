from fastapi import APIRouter, HTTPException
import httpx
from pymongo.errors import PyMongoError

from src.domain.dev_api import DevAritcle, User
from src.services import db

router = APIRouter()


@router.get('/angular', operation_id='angular_dev_news')
async def angular_dev():
    url = f'https://dev.to/api/articles?tag=angular'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_angular.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_angular.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_angular.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_angular.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/vue', operation_id='vue_dev_news')
async def vue_dev():
    url = f'https://dev.to/api/articles?tag=vue'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_vue.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_vue.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_vue.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_vue.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/nuxt', operation_id='nuxt_dev_news')
async def nuxt_dev():
    url = f'https://dev.to/api/articles?tag=nuxt'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_vue.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_vue.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_vue.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_vue.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/typescript', operation_id='typescript_dev_news')
async def typescript_dev():
    url = f'https://dev.to/api/articles?tag=typescript'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_typescript.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_typescript.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_typescript.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_typescript.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/javascript', operation_id='javascript_dev_news')
async def javascript_dev():
    url = f'https://dev.to/api/articles?tag=javascript'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_javascript.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_javascript.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_javascript.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_javascript.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/mongodb', operation_id='mongodb_dev_news')
async def mongodb_dev():
    url = f'https://dev.to/api/articles?tag=mongodb'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_mongodb.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_mongodb.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_mongodb.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_mongodb.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/python', operation_id='python_dev_news')
async def python_dev():
    url = f'https://dev.to/api/articles?tag=python'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_python.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_python.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_python.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_python.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/css', operation_id='css_dev_news')
async def css_dev():
    url = f'https://dev.to/api/articles?tag=css'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_css.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_css.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_css.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_css.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/frontend', operation_id='frontend_dev_news')
async def frontend_dev():
    url = f'https://dev.to/api/articles?tag=frontend'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_frontend.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_frontend.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_frontend.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_frontend.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/backend', operation_id='backend_dev_news')
async def backend_dev():
    url = f'https://dev.to/api/articles?tag=backend'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_backend.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_backend.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_backend.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_backend.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/webdesign', operation_id='webdesign_dev_news')
async def webdesign_dev():
    url = f'https://dev.to/api/articles?tag=webdesign'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_webdesign.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_webdesign.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_webdesign.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_webdesign.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/ai', operation_id='ai_dev_news')
async def ai_dev():
    url = f'https://dev.to/api/articles?tag=ai'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_ai.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_ai.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_ai.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_ai.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/github', operation_id='github_dev_news')
async def github_dev():
    url = f'https://dev.to/api/articles?tag=github'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_github.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_github.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_github.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_github.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/sql', operation_id='sql_dev_news')
async def sql_dev():
    url = f'https://dev.to/api/articles?tag=sql'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_sql.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_sql.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_sql.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_sql.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/cypress', operation_id='cypress_dev_news')
async def cypress_dev():
    url = f'https://dev.to/api/articles?tag=cypress'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_cypress.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_cypress.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_cypress.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_cypress.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles


@router.get('/algorithms', operation_id='algorithms_dev_news')
async def algorithms_dev():
    url = f'https://dev.to/api/articles?tag=algorithms'

    # Handle potential errors with the external HTTP request
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
    except (httpx.HTTPStatusError, httpx.RequestError) as http_err:
        # If there's an error in making the request, fall back to the database
        try:
            saved_articles = list(db.process.dev_api_algorithms.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to fetch articles from Dev.to and no data in the database: {str(http_err)}"
                )
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Error making request to Dev.to and failed to retrieve data from the database: {str(db_err)}"
            )

    # Try to parse the response JSON
    try:
        articles = response.json()
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid response format from Dev.to")

    # If no articles are returned from the API, fetch data from the database
    if not articles:
        try:
            saved_articles = list(db.process.dev_api_algorithms.find({}))
            if saved_articles:
                return saved_articles
            else:
                raise HTTPException(status_code=404, detail="No articles available in the database")
        except PyMongoError as db_err:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to retrieve articles from the database: {str(db_err)}"
            )

    # If articles are returned from the API, clear the database and insert new ones
    try:
        db.process.dev_api_algorithms.delete_many({})
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear old articles from the database: {str(db_err)}"
        )

    # Extract the fields you want to save to the database
    extracted_articles = []
    for article in articles:
        try:
            extracted = DevAritcle(
                type_of=article['type_of'],
                title=article['title'],
                description=article['description'],
                url=article['url'],
                cover_image=article['cover_image'],
                published_at=article['published_at'],
                tag_list=article['tag_list'],
                user=User(
                    name=article['user']['name'],
                    profile_image=article['user']['profile_image'],
                    website_url=article['user'].get('website_url')
                )
            )
            extracted_articles.append(extracted.dict(by_alias=True))  # Convert Pydantic model to dictionary
        except KeyError as key_err:
            raise HTTPException(
                status_code=500,
                detail=f"Missing expected field in article data: {str(key_err)}"
            )

    # Insert new articles into the database
    try:
        db.process.dev_api_algorithms.insert_many(extracted_articles)
    except PyMongoError as db_err:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save articles to the database: {str(db_err)}"
        )

    # Return the saved articles
    return extracted_articles
