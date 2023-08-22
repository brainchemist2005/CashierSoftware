from flask import Flask, render_template, request, redirect, g, url_for
from database import Database

app = Flask(__name__, static_url_path="", static_folder="static")

