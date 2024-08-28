## Authentication Overview

This project implements authentication and authorization using FastAPI. The following files and folders are involved in handling user authentication, token management, and role-based access control.

## Authentication-Related Files and Folders

### 1. `src/services/security.py`
Contains essential functions for:
- **Password Verification:** `verify_password`
- **User Authentication:** `authenticate_user`
- **Token Creation:** `create_access_token`
- **Token Validation:** `get_payload`, `get_current_user`
- **Role-Based Access Control:** `require_role`

### 2. `src/domain/user.py`
Defines the `User` model, which includes:
- **User Data Fields:** `username`, `email`, `full_name`, `hashed_password`, `role`, etc.

### 3. `src/domain/user_in_db.py`
Defines `UserInDB`, a model for representing user data as stored in the database, including:
- **Hashed Password:** `hashed_password`

### 4. `src/domain/token.py`
Defines the `Token` model used for returning:
- **Access Token:** `access_token`
- **Token Type:** `token_type`
- **User Role:** `role`

### 5. `src/domain/token_data.py`
Defines `TokenData`, which is used for decoding JWT token data:
- **Username:** `username`

### 6. `src/routes/login.py`
Contains the route for user authentication:
- **POST `/token/`**: Endpoint to obtain an access token using username and password.

### 7. `src/routes/register.py`
Handles user registration:
- **POST `/register/`**: Endpoint to register a new user by hashing the password and saving user data.

### 8. `src/services/db.py`
Provides database operations:
- **User Retrieval:** `get_user`
- **User Insertion:** `register_user`

## Authentication Flow

1. **User Registration:**
    - User provides a username and password.
    - Password is hashed using bcrypt.
    - User data is stored in the database.

2. **User Authentication:**
    - User provides username and password.
    - Password is verified against the stored hashed password.
    - If valid, an access token is created and returned.

3. **Token Handling:**
    - Tokens are JWTs (JSON Web Tokens) encoded with user information and expiration time.
    - Tokens are validated to ensure they are not expired and are correctly signed.
    - User roles are extracted from tokens to enforce role-based access control.

4. **Role-Based Access Control:**
    - Certain routes are protected and require specific roles to access.
    - Role checks are performed to ensure users have the necessary permissions.

For more details on each component and its functionality, please refer to the corresponding file in the project.

### Components

1. **Password Verification**
2. **User Retrieval**
3. **User Authentication**
4. **Token Management**
5. **Token Validation**
6. **Role-Based Access Control**
7. **User Registration**

### 1. Password Verification

**Function Name:** `verify_password`

**Purpose:** Verifies a plain password against a hashed password.

**Parameters:**
- `plain_password` (str): The plain password to be verified.
- `hashed_password` (str): The hashed password to compare against.

**Behavior:**
- Uses `passlib` library's `CryptContext` to compare passwords.
- Returns `True` if passwords match, otherwise `False`.

### 2. User Retrieval

**Function Name:** `get_user`

**Purpose:** Retrieves a user from the database based on the username.

**Parameters:**
- `username` (str): The username of the user to retrieve.

**Behavior:**
- Queries the database to find a user with the given username.
- Returns a `UserInDB` instance if found, otherwise `None`.

### 3. User Authentication

**Function Name:** `authenticate_user`

**Purpose:** Authenticates a user by validating their username and password.

**Parameters:**
- `username` (str): The username of the user.
- `password` (str): The password of the user.

**Behavior:**
- Retrieves the user using `get_user`.
- Verifies the password using `verify_password`.
- Returns the `User` instance if authentication succeeds, otherwise `None`.

### 4. Token Management

**Function Name:** `create_access_token`

**Purpose:** Creates a JWT access token for an authenticated user.

**Parameters:**
- `data` (dict): Dictionary containing user information to be encoded in the token.
- `expires_delta` (Optional[timedelta]): Optional expiration time for the token.

**Behavior:**
- Sets the token expiration time.
- Encodes the data into a JWT using a secret key and algorithm.
- Returns the encoded JWT.

### 5. Token Validation

**Function Name:** `get_payload`

**Purpose:** Extracts and decodes the payload from a JWT token.

**Parameters:**
- `token` (str): The JWT token to decode.

**Behavior:**
- Decodes the token using the secret key and algorithm.
- Raises an `HTTPException` if token validation fails.
- Returns the decoded payload as a dictionary.

**Exception:**
- `HTTPException` if token validation fails.

### 6. Role-Based Access Control

**Function Name:** `require_role`

**Purpose:** Enforces role-based access control.

**Parameters:**
- `required_role` (str): The role required to access a specific endpoint.

**Behavior:**
- Checks if the current user has the required role.
- Raises `HTTPException` with a 403 status code if the role check fails.
- Returns the `User` object if the role check passes.

### 7. User Registration

**Function Name:** `register_user`

**Purpose:** Registers a new user by hashing their password and saving their data.

**Parameters:**
- `user` (User): The user data to be registered.

**Behavior:**
- Hashes the user's password using `make_hash`.
- Creates a `User` instance with the hashed password.
- Saves the user data to the database.

### Example Usage in Routes

#### Example Route with Role-Based Access Control

**Route:** `GET /admin/`

**Purpose:** Retrieves all blogs from the database. Requires the user to have admin privileges.

**Implementation:**
```python
@router.get('/admin/', operation_id='get_all_blogs_private')
async def get_all_blogs_private(current_user: str = Depends(get_current_user)) -> list[Blog]:
    # Logic to retrieve and return all blogs
```

**Dependencies**:
- `get_current_user`: Extracts the current user from the token. 
- `require_role('admin')`: Ensures the user has the admin role.

**Example Route with Authentication**
**Route:** `POST /`

**Purpose**: Adds a new blog to the database. Requires the user to be authenticated as an admin.

**Implementation:**
```python
@router.post('/', operation_id='add_new_blog_private')
async def add_new_blog(blog: Blog, current_user: User = Depends(require_role('admin'))) -> Blog | None:
# Logic to add a new blog and send notifications
```

**Dependencies**:
- `require_role('admin')`: Ensures the user has the admin role.

Feel free to customize any sections as needed to better fit the specifics of your project.