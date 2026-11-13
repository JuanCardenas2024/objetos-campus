from pathlib import Path
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.auth import verificar_admin

router = APIRouter()
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)


@router.get("/")
def inicio():
    return RedirectResponse("/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
def login(
    request: Request,
    rol: str = Form(...),
    usuario: str = Form(""),
    password: str = Form(""),
):
    if rol == "admin":
        if not verificar_admin(usuario.strip(), password):
            return templates.TemplateResponse(
                request, "login.html",
                {"error": "Usuario o contraseña incorrectos."},
                status_code=401,
            )
        request.session["rol"] = "admin"
        request.session["usuario"] = usuario.strip()
        return RedirectResponse("/admin", status_code=303)

    if rol == "encontro":
        request.session["rol"] = "encontro"
        return RedirectResponse("/reportes/hallazgo", status_code=303)

    if rol == "perdio":
        request.session["rol"] = "perdio"
        return RedirectResponse("/reportes/extravio", status_code=303)

    return templates.TemplateResponse(
        request, "login.html",
        {"error": "Seleccione quién es usted."},
        status_code=400,
    )


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)