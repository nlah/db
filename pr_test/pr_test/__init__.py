"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
import pr_test.views
