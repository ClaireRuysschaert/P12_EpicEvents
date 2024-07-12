from datetime import timedelta, datetime, timezone
import os
from typing import Union, Tuple
import click
from dotenv import load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

load_dotenv()

postgresql = {
    "pguser": os.getenv('PGUSER'),
    "pgpasswd": os.getenv('PGPASSWORD'),
    "pghost": os.getenv('PGHOST'),
    "pgport": os.getenv('PGPORT'),
    "pgdb": os.getenv('PGDATABASE'),
}

def generate_jwt_token(user_login) -> str:
    """
    Generate a JWT token for the user that wants to loggin.
    The token payload contains the user_id, department_id, and expiration time.
    It will expire in 1 hour.
    """
    payload = {
        'user_id': user_login.staff_id,
        'department_id': user_login.department_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    secret = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    token = jwt.encode(payload, secret, algorithm)
    return token

def decode_jwt_token(token) -> Tuple[int, int, datetime]:
    """
    Decode the JWT token and return the user_id and department_id.
    """
    secret = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    user_id = jwt.decode(token, secret, algorithm)['user_id']
    department_id = jwt.decode(token, secret, algorithm)['department_id']
    return user_id, department_id

def is_jwt_token_valid(token: str) -> bool:
    """
    Verify if the JWT token is valid.
    """
    secret = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    try:
        user_id = jwt.decode(token, secret, algorithm)['user_id']
        if user_id:
            return True
    except ExpiredSignatureError:
        click.echo("Token has expired. Please log in again.")
        return False
    except InvalidTokenError:
        click.echo("Invalid token. Please log in again.")
        return False
