from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# Подключаем статику и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 1. Главная страница
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# 1. Главная страница
@app.get("/about", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse(request=request, name="about.html")

@app.get("/first", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse(request=request, name="product_one.html")

@app.get("/admin", response_class=HTMLResponse)
async def read_about(request: Request):
    return templates.TemplateResponse(request=request, name="admin_one.html")

# 3. Обработка формы
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    order: str = Form(...)
):
    try:
        response = requests.get(f"http://127.0.0.1:8080/add_application?name={username}&email={email}&order={order}&phone={phone}")
        if response.status_code == 200:
        # username и email берутся из атрибутов name="..." в HTML
            return templates.TemplateResponse(
                request=request,
                name="result.html",
                context={"name": username, "email": email, "order": order, "phone": phone}
        )
    except requests.exceptions.RequestException as e:
        return

# 3. Обработка формы
@app.post("/passord", response_class=HTMLResponse)
async def admin_passord(
    request: Request,
    password: str = Form(...),
):
    if password == "36863686":
        return admin_panel(request)
    else:
        return templates.TemplateResponse(request=request, name="index.html")

@app.get("/edit/{item_id}", response_class=HTMLResponse)
async def edit_form(
    request: Request,
    item_id: int
):
    try:
        response = requests.get(f"http://127.0.0.1:8080/pay_order?id={item_id}")
        if response.status_code == 200:
            return admin_panel(request)
    except requests.exceptions.RequestException as e:
        return

def admin_panel(request: Request):
    result = []
    try:
        response = requests.get(f"http://127.0.0.1:8080/get_orders")
        if response.status_code == 200:
            result = response.json()
    except requests.exceptions.RequestException as e:
        return
    result_client = []
    try:
        response = requests.get(f"http://127.0.0.1:8080/get_clients")
        if response.status_code == 200:
            result_client = response.json()
    except requests.exceptions.RequestException as e:
        return
    total_price = 0
    for item in result:
        total_price += item["Price"]
    return templates.TemplateResponse(request=request,
                                      name="admin.html",
                                      context={"result": result,
                                               "result_client": result_client,
                                               "total_client": len(result_client),
                                               "total_orders": len(result),
                                               "total_price" : total_price,})