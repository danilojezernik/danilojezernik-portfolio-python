# --------------------------------------------------------------------------
# Import all the route modules for different sections of the application
# --------------------------------------------------------------------------

# General routes (index, blog, etc.)
from src.routes import (
    index, blog, login, experiences, links, contact, projects, github, book, language, dev_to_api, user
)

# QA (Questions & Answers) routes for different technologies
from src.routes.qa import (
    typescript as qa_typescript,
    python as qa_python,
    angular as qa_angular,
    javascript as qa_javascript,
    mongodb as qa_mongodb,
    vue as qa_vue,
    cypress as qa_cypress,
    django as qa_django,
)

# Article routes for different technologies
from src.routes.article import (
    typescript as article_typescript,
    python as article_python,
    angular as article_angular,
    javascript as article_javascript,
    mongodb as article_mongodb,
    vue as article_vue,
    cypress as article_cypress,
    django as article_django,
)

# --------------------------------------------------------------------------
# Define all routers in a single list to avoid repetitive app.include_router calls.
# Each tuple contains:
#   (router object, URL prefix, tags)
# --------------------------------------------------------------------------
routers = [
    # -------------------------
    # General application routes
    # -------------------------
    (index.router, '/index', ['Index']),  # Landing or home route
    (blog.router, '/blog', ['Blog']),  # Blog-related routes
    (dev_to_api.router, '/dev', ['Dev']),  # Developer tools or external API routes
    (github.router, '/github', ['Github']),  # GitHub integration routes
    (book.router, '/book', ['Book']),  # Book collection routes

    # -------------------------
    # Technologies - QA routes (Questions & Answers per technology)
    # -------------------------
    (qa_angular.router, '/qa/angular', ['Angular']),
    (qa_vue.router, '/qa/vue', ['Vue']),
    (qa_javascript.router, '/qa/javascript', ['JavaScript']),
    (qa_typescript.router, '/qa/typescript', ['TypeScript']),
    (qa_python.router, '/qa/python', ['Python']),
    (qa_mongodb.router, '/qa/mongodb', ['MongoDB']),
    (qa_cypress.router, '/qa/cypress', ['Cypress']),
    (qa_django.router, '/qa/django', ['Django']),

    # -------------------------
    # Technologies - Article routes (Articles per technology)
    # -------------------------
    (article_angular.router, '/article/angular', ['Angular']),
    (article_vue.router, '/article/vue', ['Vue']),
    (article_javascript.router, '/article/javascript', ['JavaScript']),
    (article_typescript.router, '/article/typescript', ['TypeScript']),
    (article_python.router, '/article/python', ['Python']),
    (article_mongodb.router, '/article/mongodb', ['MongoDB']),
    (article_cypress.router, '/article/cypress', ['Cypress']),
    (article_django.router, '/article/django', ['Django']),

    # -------------------------
    # Language-related routes
    # -------------------------
    (language.router, '/language', ['Language']),

    # -------------------------
    # Other resource routes
    # -------------------------
    (experiences.router, '/experiences', ['Experiences']),  # Professional experiences
    (links.router, '/links', ['Links']),  # External links or resources
    (projects.router, '/projects', ['Projects']),  # Project portfolio
    (user.router, '/user', ['User']),  # User management
    (login.router, '/login', ['Login']),  # Authentication/login
    (contact.router, '/contact', ['Contact']),  # Contact form/messages
]
