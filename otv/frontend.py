from flask import Blueprint, render_template, flash, redirect, url_for, g

frontend = Blueprint("frontend", __name__)

@frontend.route("/")
def index_page():
    return("")