# APIs for Projects That I build for strong static data
- This provide CRUD operation APIs for my applications

# Flask + Vercel

This example shows how to use Flask 3 on Vercel with Serverless Functions using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python).

## Demo

https://gameboard-dev.vercel.app/

## How it Works

This example uses the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions.

## Running Locally

```bash
pip install -r .\requirements.txt
$env:FLASK_ENV = "development"
$env:FLASK_APP = "api\index.py"
flask run
```

Your Flask application is now available at `http://localhost:5000`.

