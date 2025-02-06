#!/usr/bin/env python3
"""Module that defines a flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    """root route
    """
    return jsonify({'message': 'Bienvenue'}), 200


@app.route('/users', methods=['POST'])
def users():
    """Users route
    """
    email = request.form['email']
    password = request.form['password']

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Logs in
    """
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({'email': email, 'message': 'logged in'})

    response.set_cookie('session_id', session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
