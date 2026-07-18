from ninja import Schema


class UserAuthSchema(Schema):
    user_name: str
    password: str


class UserOutSchema(Schema):
    id: int
    user_name: str


class MessageSchema(Schema):
    detail: str