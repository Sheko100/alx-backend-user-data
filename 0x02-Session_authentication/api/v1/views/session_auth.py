#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - Send a response with a new session
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email:
        return jsonify({'error': 'email missing'}), 400

    if not pwd:
        return jsonify({'error': 'password missing'}), 400

    users = User.search({'email': email})
    if len(users) < 1:
        return jsonify({'error': 'no user found for this email'}), 404

    user = users[0]
    if not user.is_valid_password(pwd):
        return jsonify({'error': 'wrong password'}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    cookie_name = os.environ.get('SESSION_NAME', '_my_session_id')
    response.set_cookie(cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout

        Destroyes a session
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
