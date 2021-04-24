from flask import Flask
from core.routes import TestRoute
from core.server import ChatServer

flask_ = Flask(__name__)

TestRoute('test').register(flask_)
ChatServer().run(flask_, debug=True)
