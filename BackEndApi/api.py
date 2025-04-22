from http import HTTPStatus
from typing import List

from ninja_extra import (
    NinjaExtraAPI,
    api_controller,
    ControllerBase, route,
    permissions
)

from dj_ninja_auth.jwt.authentication import JWTAuth
from dj_ninja_auth.jwt.controller import NinjaAuthJWTController

from BackEndApi.models import User, Post
from BackEndApi.schemas import UserSchema, CreateUserSchema, UpdateUserSchema, PostSchema, CreatePostSchema, \
    UpdatePostSchema

api = NinjaExtraAPI(auth=[JWTAuth()], title="BackEnd API", version="1.0.0")


@api.post('/register', tags=['auth'], response={201: UserSchema}, auth=None, permissions=[permissions.AllowAny])
def register(request, payload: CreateUserSchema):
    """
    Register a new user.
    """
    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    return HTTPStatus.CREATED, user


@api_controller('/me', tags=['users'], permissions=[permissions.IsAuthenticated])
class UserController(ControllerBase):
    """
    Controller for user-related operations.
    """

    @route.get('', response=UserSchema)
    def me(self):
        """
        Get the current user.
        :return: UserSchema
        """
        return self.context.request.user

    @route.patch('', response=UserSchema)
    def update_me(self, payload: UpdateUserSchema):
        """
        Update the current user.
        :param payload: UpdateUserSchema
        :return: UserSchema
        """
        user = self.context.request.user
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        user.save()
        return user

    @route.delete('', response={204: None})
    def delete_me(self):
        """
        Delete the current user.
        :return: None
        """
        user = self.context.request.user
        user.delete()
        return HTTPStatus.NO_CONTENT

    @route.get('/posts', response=List[PostSchema])
    def get_posts(self):
        """
        Get all posts of the current user.
        :return: List[PostSchema]
        """
        user = self.context.request.user
        posts = Post.objects.filter(user=user).all()
        return posts

    @route.post('/posts', response=PostSchema)
    def create_post(self, payload: CreatePostSchema):
        """
        Create a new post for the current user.
        :param payload: CreatePostSchema
        :return: PostSchema
        """
        user = self.context.request.user
        post = Post.objects.create(user=user, **payload.dict())
        return post

    @route.get('/posts/{post_id}', response=PostSchema)
    def get_post(self, post_id: int):
        """
        Get a post of the current user.
        :param post_id: ID of the post to retrieve
        :return: PostSchema
        """
        user = self.context.request.user
        post = Post.objects.get(id=post_id, user=user)
        return post

    @route.patch('/posts/{post_id}', response=PostSchema)
    def update_post(self, post_id: int, payload: UpdatePostSchema):
        """
        Update a post of the current user.
        :param post_id: ID of the post to update
        :param payload: UpdatePostSchema
        :return: PostSchema
        """
        user = self.context.request.user
        post = Post.objects.get(id=post_id, user=user)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(post, attr, value)
        post.save()
        return post

    @route.delete('/posts/{post_id}', response={204: None})
    def delete_post(self, post_id: int):
        """
        Delete a post of the current user.
        :param post_id: ID of the post to delete
        :return: None
        """
        user = self.context.request.user
        post = Post.objects.get(id=post_id, user=user)
        post.delete()
        return HTTPStatus.NO_CONTENT


@api_controller('/posts', tags=['posts'], auth=None, permissions=[permissions.AllowAny])
class PostController(ControllerBase):
    """
    Controller for post-related operations.
    """

    @route.get('', response=List[PostSchema])
    def list_posts(self):
        """
        List all posts.
        :return: List[PostSchema]
        """
        posts = Post.objects.filter(is_published=True).all()
        return posts
    
    @route.get('/{post_id}', response=PostSchema)
    def get_post(self, post_id: int):
        """
        Get a post by ID.
        :param post_id: ID of the post to retrieve
        :return: PostSchema
        """
        post = Post.objects.get(id=post_id, is_published=True)
        return post


@api_controller('/admin', tags=['admin'], permissions=[permissions.IsAdminUser])
class AdminController(ControllerBase):
    """
    Controller for admin-related operations.
    """

    @route.get('/users', response=List[UserSchema])
    def list_users(self):
        """
        List all users.
        :return: List[UserSchema]
        """
        users = User.objects.all()
        return users

    @route.get('/users/{user_id}', response=UserSchema)
    def get_user(self, user_id: int):
        """
        Get a user by ID.
        :param user_id: ID of the user to retrieve
        :return: UserSchema
        """
        user = User.objects.get(id=user_id)
        return user

    @route.patch('/users/{user_id}', response=UserSchema)
    def update_user(self, user_id: int, payload: UpdateUserSchema):
        """
        Update a user by ID.
        :param user_id: ID of the user to update
        :param payload: UpdateUserSchema
        :return: UserSchema
        """
        user = User.objects.get(id=user_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(user, attr, value)
        user.save()
        return user

    @route.delete('/users/{user_id}', response={204: None})
    def delete_user(self, user_id: int):
        """
        Delete a user.
        :param user_id: ID of the user to delete
        :return: None
        """
        user = User.objects.get(id=user_id)
        user.delete()
        return HTTPStatus.NO_CONTENT

    @route.get('/posts', response=List[PostSchema])
    def list_all_posts(self):
        """
        List all posts. including unpublished ones.
        :return: List[PostSchema]
        """
        posts = Post.objects.all()
        return posts

    @route.get('/posts/{post_id}', response=PostSchema)
    def get_post(self, post_id: int):
        """
        Get a post by ID.
        :param post_id: ID of the post to retrieve
        :return: PostSchema
        """
        post = Post.objects.get(id=post_id)
        return post

    @route.patch('/posts/{post_id}', response=PostSchema)
    def update_post(self, post_id: int, payload: UpdatePostSchema):
        """
        Update a post by ID.
        :param post_id: ID of the post to update
        :param payload: UpdatePostSchema
        :return: PostSchema
        """
        post = Post.objects.get(id=post_id)
        for attr, value in payload.dict(exclude_unset=True).items():
            setattr(post, attr, value)
        post.save()
        return post

    @route.delete('/posts/{post_id}', response={204: None})
    def delete_post(self, post_id: int):
        """
        Delete a post.
        :param post_id: ID of the post to delete
        :return: None
        """
        post = Post.objects.get(id=post_id)
        post.delete()
        return HTTPStatus.NO_CONTENT


api.register_controllers(
    NinjaAuthJWTController,
    UserController,
    PostController,
    AdminController
)
