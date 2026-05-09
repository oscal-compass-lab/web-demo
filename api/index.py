# Vercel serverless function entry point for Flask app
from app import app

# Export the Flask app for Vercel
# Vercel will use this as the WSGI application
def handler(request, context):
    return app(request.environ, context)

# For Vercel Python runtime
app = app

# Made with Bob
