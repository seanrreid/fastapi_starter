import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select

import config

from models.stuff import Stuff

from db import get_session

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}

# DELETE THE ROUTES BELOW
# DEMO PURPOSES ONLY

# READ data


@app.get("/stuff")
async def get_all_stuff(session: Session = Depends(get_session)):
    statement = select(Stuff)
    results = session.exec(statement).all()
    return results

# READ specific data


@app.get("/stuff/{id}")
async def get_single_stuff(id: str, session: Session = Depends(get_session)):
    statement = select(Stuff).where(Stuff.id == id)
    result = session.exec(statement).one()
    return result

# CREATE data


@app.post("/stuff/add")
async def add_stuff(payload: Stuff, session: Session = Depends(get_session)):
    new_stuff = Stuff(title=payload.title, description=payload.description)
    session.add(new_stuff)
    session.commit()
    session.refresh(new_stuff)
    return {"message": f"Added new stuff with ID: {new_stuff.id}"}

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
