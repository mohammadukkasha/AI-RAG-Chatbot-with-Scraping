from pydantic import BaseModel, HttpUrl


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WebsiteData(BaseModel):
    url: HttpUrl

class ChatMessage(BaseModel):
    message: str