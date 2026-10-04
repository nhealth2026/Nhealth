"""
Nhealth - Healthcare at Home
Flask Application Factory & Backend Package Initialization
"""

import os
import jinja2
from datetime import datetime, date
from flask import Flask
from flask.json.provider import DefaultJSONProvider

from .config import Config
from .routes import register_routes
from .models import init_db


class CustomJSONProvider(DefaultJSONProvider):
    """Serialize datetime and date objects to ISO 8601 strings."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def create_app(config_class=Config):
    """Application factory for Nhealth Flask backend."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    frontend_dir = os.path.join(base_dir, 'frontend')
    static_dir = os.path.join(frontend_dir, 'static')
    template_dir = os.path.join(frontend_dir, 'templates')

    app = Flask(
        __name__,
        static_folder=static_dir,
        template_folder=template_dir
    )

    # Use custom JSON provider
    app.json = CustomJSONProvider(app)

    # Load configuration
    app.config.from_object(config_class)

    # Set up multi-path Jinja ChoiceLoader so both 'index.html' and 'pages/index.html' work seamlessly
    template_folders = [
        template_dir,
        os.path.join(template_dir, 'pages'),
        os.path.join(template_dir, 'auth'),
        os.path.join(template_dir, 'dashboards'),
        # Fallback to root templates/ if present
        os.path.join(base_dir, 'templates')
    ]
    app.jinja_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(f) for f in template_folders if os.path.exists(f)
    ])

    # Security & cache headers
    @app.after_request
    def add_security_and_cache_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response

    # Register all modular route blueprints
    register_routes(app)

    # Initialize database connection pool & tables
    init_db()

    return app
