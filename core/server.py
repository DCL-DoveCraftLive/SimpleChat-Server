# from flask import Flask
from utils.singleton import Singleton


@Singleton
class ChatServer:

    def __init__(self):
        pass