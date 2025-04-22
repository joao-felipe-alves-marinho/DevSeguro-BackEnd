import re

from django.core.validators import validate_email
from ninja_schema import ModelSchema, model_validator
from ninja_extra.exceptions import ValidationError

from BackEndApi.models import User, Post


class CreateUserSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'email', 'password']

    @classmethod
    @model_validator('username')
    def validate_username(cls, value: str):
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValueError("O nome de usuário deve conter apenas letras, números, pontos, sublinhados ou hífens.")
        if len(value) < 3 or len(value) > 100:
            raise ValueError("O nome de usuário deve ter entre 3 e 100 caracteres.")
        return value

    @classmethod
    @model_validator('email')
    def validate_email(cls, value: str):
        try:
            validate_email(value)
        except ValidationError:
            raise ValueError("Por favor, insira um e-mail válido.")
        if User.objects.filter(email=value).exists():
            raise ValueError("Este e-mail já está em uso.")
        return value

    @classmethod
    @model_validator('password')
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("A senha deve ter pelo menos 8 caracteres.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("A senha deve incluir pelo menos uma letra maiúscula.")
        if not re.search(r"\d", value):
            raise ValueError("A senha deve incluir pelo menos um número.")
        return value


class UpdateUserSchema(ModelSchema):
    class Config:
        model = User
        include = ['username', 'email']
        optional = '__all__'

    @classmethod
    @model_validator('username')
    def validate_username(cls, value: str):
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValueError("O nome de usuário deve conter apenas letras, números, pontos, sublinhados ou hífens.")
        if len(value) < 3 or len(value) > 100:
            raise ValueError("O nome de usuário deve ter entre 3 e 100 caracteres.")
        return value

    @classmethod
    @model_validator('email')
    def validate_email(cls, value: str):
        try:
            validate_email(value)
        except ValidationError:
            raise ValueError("Por favor, insira um e-mail válido.")
        if User.objects.filter(email=value).exists():
            raise ValueError("Este e-mail já está em uso.")
        return value


class UserSchema(ModelSchema):
    class Config:
        model = User
        include = ['id', 'username', 'email']


# ---------------------------------------------------------------------

class CreatePostSchema(ModelSchema):
    class Config:
        model = Post
        include = ['title', 'content', 'is_published']

    @classmethod
    @model_validator('title')
    def validate_title(cls, value: str):
        if len(value) < 3 or len(value) > 255:
            raise ValueError("O título deve ter entre 3 e 255 caracteres.")
        return value

    @classmethod
    @model_validator('content')
    def validate_content(cls, value: str):
        if len(value) < 10:
            raise ValueError("O conteúdo deve ter pelo menos 10 caracteres.")
        return value


class UpdatePostSchema(ModelSchema):
    class Config:
        model = Post
        include = ['title', 'content', 'is_published']
        optional = '__all__'

    @classmethod
    @model_validator('title')
    def validate_title(cls, value: str):
        if len(value) < 3 or len(value) > 255:
            raise ValueError("O título deve ter entre 3 e 255 caracteres.")
        return value

    @classmethod
    @model_validator('content')
    def validate_content(cls, value: str):
        if len(value) < 10:
            raise ValueError("O conteúdo deve ter pelo menos 10 caracteres.")
        return value

class PostSchema(ModelSchema):
    user: UserSchema

    class Config:
        model = Post
        include = ['id', 'title', 'content', 'is_published', 'created_at']
