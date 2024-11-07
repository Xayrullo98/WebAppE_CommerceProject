import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI

from download_file import download_file_func
from read_file import read_file_func
from routes import auth, users, branch, trades , orders, products,basket, sold_products

from db import Base, engine
from utils.functions import FERGANA_WAREHOUSE_FILE_NAME, NAMANGAN_WAREHOUSE_FILE_NAME, NAMANGAN_WAREHOUSE_ID, \
    FERGANA_WAREHOUSE_ID

FERGANA_FILE_NAME=os.environ.get("FERGANA_WAREHOUSE_FILE_NAME",'downloaded_file')
NAMANGAN_FILE_NAME=os.environ.get("NAMANGAN_WAREHOUSE_FILE_NAME")

Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Meros web app",
    responses={200: {'description': 'Ok'}, 201: {'description': 'Created'}, 400: {'description': 'Bad Request'},
               401: {'desription': 'Unauthorized'}}
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(
    auth.login_router,
    prefix='/auth',
    tags=['User auth section'],

)

app.include_router(
    branch.router_branch,
    prefix='/branch',
    tags=['Branch section'],

)


app.include_router(
    users.router_user,
    prefix='/user',
    tags=['User section'],

)


app.include_router(
    orders.router_order,
    prefix='/order',
    tags=['Order  section'],

)

app.include_router(
    trades.router_product,
    prefix='/trade',
    tags=['Trade  section'],

)

app.include_router(
    basket.router_basket,
    prefix='/basket',
    tags=['Basket  section'],

)


app.include_router(
    products.router_product,
    prefix='/products',
    tags=['Products  section'],

)

 
app.include_router(
    sold_products.router_sold_product,
    prefix='/sold_products',
    tags=['Sold Products  section'],

)

scheduler = BackgroundScheduler()

scheduler.add_job(download_file_func, 'interval', seconds=15, args=(f'{FERGANA_WAREHOUSE_ID}', FERGANA_WAREHOUSE_FILE_NAME))
scheduler.add_job(download_file_func, 'interval', seconds=15, args=(f'{NAMANGAN_WAREHOUSE_ID}', NAMANGAN_WAREHOUSE_FILE_NAME))

scheduler.add_job(read_file_func, 'interval', seconds=15, args=(f'{FERGANA_WAREHOUSE_FILE_NAME}', 1))
scheduler.add_job(read_file_func, 'interval', seconds=15, args=(f'{NAMANGAN_WAREHOUSE_FILE_NAME}', 2))





scheduler.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    scheduler.shutdown()

