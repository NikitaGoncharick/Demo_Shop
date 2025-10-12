from tempfile import template

from fastapi import FastAPI
import uvicorn
from fastapi import Request
from fastapi.templating import Jinja2Templates



app = FastAPI()


template = Jinja2Templates(directory="../frontend/templates")

@app.get("/")
async def root(request: Request):
    return template.TemplateResponse("home.html", {"request": request})







if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)