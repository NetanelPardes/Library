from database.db_connection import DBconnection
from fastapi import FastAPI
import uvicorn
from routes.book_routes import router as book_routes
from routes.member_routes import router as member_routes
from routes.report_routes import router as report_routes


app = FastAPI()

app.include_router(book_routes)
app.include_router(member_routes)
app.include_router(report_routes)
db = DBconnection()
db.create_tables()

if __name__ == "__main__":
    uvicorn.run("main:app" ,reload=True)