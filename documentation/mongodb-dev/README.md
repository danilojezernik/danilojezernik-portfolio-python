# Development MongoDB Configuration

This document explains how to set up and use a development version of MongoDB for the application.

## Overview

The application now supports using a local MongoDB instance for development purposes. This makes it easier to develop and test without affecting the production database.

## Configuration

The following environment variables have been added to control the MongoDB connection:

- `ENV`: Set to "development" to use the development MongoDB connection, or "production" to use the production MongoDB connection.
- `DB_DEV`: The connection string for the development MongoDB instance. Defaults to "mongodb://localhost:27017" if not specified.

## How It Works

When the application starts, it checks the `ENV` environment variable:

- If `ENV` is set to "development", the application uses the MongoDB connection specified in `DB_DEV`.
- If `ENV` is set to anything else (or not set), the application uses the MongoDB connection specified in `DB_MAIN`.

## Setup Instructions

1. Make sure you have MongoDB installed locally. You can download it from [the MongoDB website](https://www.mongodb.com/try/download/community).

2. Start your local MongoDB instance:
   ```
   mongod --dbpath /path/to/data/directory
   ```

3. Set the environment variables in your `.env` file:
   ```
   ENV=development
   DB_DEV=mongodb://localhost:27017
   DB_PROCESS=development
   ```

4. Run the application. You should see a message indicating that the development MongoDB connection is being used.

## Switching Between Development and Production

To switch between development and production MongoDB:

- For development: Set `ENV=development` in your `.env` file.
- For production: Set `ENV=production` in your `.env` file.

## Troubleshooting

If you encounter issues connecting to the local MongoDB instance:

1. Make sure MongoDB is running locally.
2. Check that the connection string in `DB_DEV` is correct.
3. Ensure that the MongoDB port (default: 27017) is not blocked by a firewall.
