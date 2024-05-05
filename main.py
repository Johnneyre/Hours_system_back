from fastapi import FastAPI, __version__, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from routes import hours, tasks, rol, users
from fastapi.responses import HTMLResponse
from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from db.db import get_db
from sqlalchemy.orm import Session
from models.models import User
from schemas.users import UserInDB

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"])
SECRET_KEY = "perro2"
ALGORITHM = "HS256"

html = f"""
<!DOCTYPE html>
<html> 
    <head>
        <title>FastAPI on APPLINKTIC</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

ouath2_scheme = OAuth2PasswordBearer("/token")

def get_user(db, username: str):
    user_data = db.query(User).filter(User.username == username).first()
    if user_data is not None:
        user_dict = user_data.__dict__
        if 'hashed_password' not in user_dict:
            user_dict['hashed_password'] = pwd_context.hash(user_data.password)
        return UserInDB(**user_dict)
    return []

def verifiy_password(plane_password, hashed_password):
    return pwd_context.verify(plane_password, hashed_password)

def authenticate_user(db, username, password):
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="No son validos las credenciales", headers={"WWW-Authenticate": "Bearer"})
    if not verifiy_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="No son validos las credenciales", headers={"WWW-Authenticate": "Bearer"})
    return user

def create_token(data: dict, time_expire: Union[datetime, None] = None):
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=15)
    else:
        expires = datetime.utcnow() + time_expire
    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def get_user_current(token: str = Depends(ouath2_scheme), db: Session = Depends(get_db)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = token_decode.get("sub")
        if username == None:
            raise HTTPException(status_code=401, detail="No son validos las credenciales", headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401, detail="No son validos las credenciales", headers={"WWW-Authenticate": "Bearer"})
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="No son validos las credenciales", headers={"WWW-Authenticate": "Bearer"})
    return user

def get_user_disabled_current(user: User = Depends(get_user_current)):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return user

@app.get("/users/me")
def user(user: User = Depends(get_user_disabled_current)):
    return user

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user.username}, access_token_expires)
    return {
        "access_token": access_token_jwt,
        "token_type": "bearer"
    }

app.include_router(hours.router, prefix="/hours", tags=["hours"])
app.include_router(rol.router, prefix="/rol", tags=["rol"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])