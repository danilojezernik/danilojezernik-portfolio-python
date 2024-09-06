# Import necessary modules and functions
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from cryptography.fernet import Fernet
import json

from src.domain.user import User
from src import env
from src.domain.user_in_db import UserInDB
from src.domain.token_data import TokenData
from src.services import db

# Initialize a password context with bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
role_cipher = Fernet(env.ROLE_ENCRYPTION_KEY)

# Define OAuth2 password bearer scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to verify the provided plain password against the hashed password
def verify_password(plain_password, hashed_password):
    """
    This function verifies the provided plain password against the hashed password.

    Parameters:
    - plain_password: The plain password to verify.
    - hashed_password: The hashed password to compare against.

    Behavior:
    - It uses the verify method from the passlib context to compare the plain password with the hashed password.
    - Returns True if the plain password matches the hashed password, otherwise returns False.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Function to get a user from the database based on the provided username
def get_user(username: str):
    """
    This function retrieves a user from the database based on the provided username.

    Parameters:
    - username (str): Username of the user to retrieve.

    Behavior:
    - It queries the database to find a user with the given username using the find_one method.
    - If a user is found, it constructs a UserInDB instance using the retrieved data and returns it.
    - If no user is found, it returns None.
    """
    user = db.process.user.find_one({"username": username})
    if user:
        return UserInDB(**user)


# Function to authenticate a user based on the provided username and password
def authenticate_user(username: str, password: str):
    """
    This function authenticates a user by validating the provided username and password.

    Parameters:
    - username (str): Username of the user to authenticate.
    - password (str): Password of the user to authenticate.

    Behavior:
    - It retrieves the user based on the provided username using the get_user function.
    - If a user is found and the provided password matches the stored hashed password, the user is considered authenticated and returned.
    - If no user is found or the password doesn't match, it returns None, indicating authentication failure.
    """

    user = get_user(username)
    if user and user.registered is not False and verify_password(password, user.hashed_password):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    This function is responsible for creating an access token (JWT) using the jwt. Encode function from the jose library.

    Parameters:
    - data: A dictionary containing the data to be encoded into the token (e.g., user information).
    - expires_delta: An optional parameter indicating the expiration time for the token.

    Behavior:
    - Calculates the expiration time for the token based on the provided expires_delta or defaults to 15 minutes if no expiration is provided.
    - Updates the data dictionary with the expiration time.
    - Encodes the updated data into a JWT using the jwt.encode function with the provided SECRET_KEY and ALGORITHM.

    Returns:
    - The encoded JWT (access token) as the result of the function.
    """

    # Make a copy of the data to encode
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=60))


    # Update the data with the expiration time
    to_encode.update({"exp": expire})

    # Encrypt the role before adding it to the token
    if 'role' in to_encode:
        decrypted_role = decrypt_role(to_encode['role'])
        to_encode["role"] = decrypted_role

        # Encode the data into a JWT using the provided SECRET_KEY and algorithm
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)

    # Return the encoded JWT (access token)
    return encoded_jwt


async def get_payload(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Extracts and decodes the payload from the JWT token.

    Parameters:
    - token: The JWT token.

    Returns:
    - The decoded payload as a dictionary.

    Raises:
    - HTTPException if token validation fails.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=["HS256"])

    except JWTError:
        raise credentials_exception

    print(f'payload: {payload}')
    return payload

def test_encryption_decryption():
    test_role = "admin"
    encrypted_role = role_cipher.encrypt(json.dumps(test_role).encode())
    print(f"Encrypted Role: {encrypted_role.decode()}")

    decrypted_role = json.loads(role_cipher.decrypt(encrypted_role).decode())
    print(f"Decrypted Role: {decrypted_role}")

test_encryption_decryption()

def decrypt_role(encrypted_role: str) -> str:
    try:
        decrypted_role = json.loads(role_cipher.decrypt(encrypted_role.encode()).decode())
        return decrypted_role
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to decrypt role")



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Asynchronously retrieves the current user based on the provided token.

    Steps:
    1. Decodes the token to extract the username and encrypted role.
    2. Decrypts the role from the token.
    3. Retrieves the user from the database using the decoded username.
    4. Adds the decrypted role to the user object.
    5. Returns the user object with the decrypted role.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        role: str = payload.get("role")

        decrypted_role = decrypt_role_if_encrypted(role)

        print(f"Decrypted role: {role}")
        if username is None or role is None:
            raise credentials_exception


        token_data = TokenData(username=username, role=decrypted_role)

    except JWTError:
        raise credentials_exception

    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception

    # Assign decrypted role to the user object
    user.role = decrypted_role
    print(f"Decrypted Role after JWT Decode: {decrypted_role}")  # Debugging output
    return user


def decrypt_role_if_encrypted(role: str) -> str:
    """
    Decrypts the role if it is encrypted, otherwise returns it as-is.
    """
    try:
        # Check if the role is already in plaintext (adjust logic as needed)
        if role == "admin" or role == "visitor":  # Assume roles like 'admin' or 'user' are plaintext
            return role
        else:
            # If not, attempt to decrypt it
            return json.loads(role_cipher.decrypt(role.encode()).decode())
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to decrypt role")


# This function is a decorator that checks if the current user has the required role.
def require_role(required_role: str):
    """
    A decorator function to enforce role-based access control.

    Args:
        required_role (str): The role required to access the endpoint.

    Returns:
        Callable: A function that performs the role check and returns the current user
                  if they have the required role, otherwise raises an HTTP 403 Forbidden error.
    """

    def role_checker(current_user: User = Depends(get_current_user)):
        """
        Checks if the current user has the required role.

        Args:
            current_user (User): The user object obtained from the authentication system.

        Raises:
            HTTPException: If the current user's role does not match the required role,
                           a 403 Forbidden error is raised.

        Returns:
            User: The current user object if the role check passes.
        """
        # Check if the user's role matches the required role
        if required_role not in current_user.role:  # Check if required_role is in user's roles
            print(current_user.role)
            # If the role does not match, raise a 403 Forbidden error
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        # Return the current user object if the role check passes
        return current_user

    # Return the role_checker function which will be used as a dependency
    return role_checker


# Has a password
def make_hash(password):
    return pwd_context.hash(password)


# Register new user function
def register_user(user: User):
    """
    This function registers a new user by creating a User instance with hashed password.

    Parameters:
    - user_data (User): Registration data containing username and password.

    Returns:
    - User: The registered user with hashed password.
    """
    hashed_password = make_hash(user.hashed_password)
    user_data = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        role=user.role
    )

    # Save user to database
    db.process.user.insert_one(user_data.dict(by_alias=True))

    return user_data
