"""
Backward compatibility facade for backend.models.
All database models, schema setup, and query functions have been modularized under backend.models.
"""

from backend.models import *
from backend.models import __all__ as _models_all

__all__ = _models_all
