## BackEnd API

A simple Django-based REST API for managing users and posts, with authentication and authorization controls.

### Features

- JWT-based authentication (dj-ninja-auth)
- Role-Based Access Control (RBAC) for admin operations
- Discretionary Access Control (DAC) to restrict users to their own resources
- CRUD operations for users and posts

### Technologies

- Django 5.2
- Django Ninja & Ninja Extra
- dj-ninja-auth (JWT)
- SQLite3 (default)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BackEnd.git
   cd BackEnd
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Configuration

- Update `SECRET_KEY` in `settings.py` for production.
- Adjust `ALLOWED_HOSTS`, database settings, and other security settings as needed.

### Authentication & Authorization

This API uses JWT tokens for authentication (via `dj-ninja-auth`).

**Role-Based Access Control (RBAC):**
- **Admin**: Access to all user and post management endpoints under `/api/admin/*`.
  - Implemented using `permissions.IsAdminUser` on the `AdminController`.
- **Authenticated User**: Access to own profile and own posts under `/api/me/*`.
  - Implemented using `permissions.IsAuthenticated` on the `UserController`.

**Discretionary Access Control (DAC):**
- Users can only update, delete, or view resources they own (their own posts and profile).
  - The `UserController` methods filter by `request.user` to ensure ownership.
  - Eg. when updating or deleting a post, the query includes `filter(user=request.user)`.

### API Endpoints

#### Auth

- `POST /api/register` - Create a new user and return user data.
- `POST /api/token` - Obtain JWT token.
- `POST /api/token/refresh` - Refresh JWT token.

#### Users (`/api/me`)

- `GET /api/me` - Get current user.
- `PATCH /api/me` - Update current user.
- `DELETE /api/me` - Delete current user.

#### User Posts (`/api/me/posts`)

- `GET /api/me/posts` - List current user's posts.
- `POST /api/me/posts` - Create a new post for current user.
- `PATCH /api/me/posts/{id}` - Update a post (ownership enforced).
- `DELETE /api/me/posts/{id}` - Delete a post (ownership enforced).

#### Posts (`/api/posts`)

- `GET /api/posts` - List all published posts.

#### Admin (`/api/admin`)

- `GET /api/admin/users` - List all users.
- `GET /api/admin/users/{id}` - Get a user by ID.
- `PATCH /api/admin/users/{id}` - Update a user by ID.
- `DELETE /api/admin/users/{id}` - Delete a user by ID.
- `GET /api/admin/posts` - List all posts (including unpublished).
- `GET /api/admin/posts/{id}` - Get a post by ID.
- `PATCH /api/admin/posts/{id}` - Update a post by ID.
- `DELETE /api/admin/posts/{id}` - Delete a post by ID.

### Docker
#### Build the image
docker build -t backend:latest .

#### Run the container
docker run -d -p 8000:8000 --env-file .env backend:latest


### Contributing

Feel free to open issues or submit pull requests.

### License

MIT License

