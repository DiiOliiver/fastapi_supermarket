from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
