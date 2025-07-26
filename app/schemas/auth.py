from pydantic import BaseModel, model_validator


class UserLoginDTO(BaseModel):
    username: str
    password: str


class UserDTO(BaseModel):
    username: str
    password: str


class TokenDTO(BaseModel):
    access_token: str
    token_type: str
    username: str


class UserRegisterDTO(BaseModel):
    username: str
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegisterDTO':
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
