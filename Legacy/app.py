# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 21:29:54 2019

@author: zfern
"""

from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
    return "This is a test."

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=80)