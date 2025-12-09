"""
Utils Package Initialization
Firebase Firestore Database
"""
from .firebase_db import init_firebase, get_db

__all__ = [
    'init_firebase',
    'get_db'
]
