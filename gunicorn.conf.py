"""
Gunicorn WSGI Server configuration
"""

# pylint: disable=C0103 # gunicorn needs lower case variable names

bind = '127.0.0.1:8000'
backlog = 2048

