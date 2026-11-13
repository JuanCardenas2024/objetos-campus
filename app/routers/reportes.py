from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.datalake.storage import subir_foto
from app.db.reportes import insertar_reporte
from app.db.sedes import listar_sedes
from app.db.usuarios import obtener_o_crear_usuario

router = APIRouter(prefix="/reportes")
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)

ROLES = {"docente", "estudiante", "personal"}
TIPOS = {"hallazgo", "extravio"}


def validar(rol, cargo, correo, sede, sedes_validas, fecha, hora, contenido, tipo):
    errores = []
    if rol not in ROLES:
        errores.append("Seleccione un rol válido.")
    if rol == "personal" and not cargo.strip():
        errores.append("Escriba el cargo del personal universitario.")
    if "@" not in correo:
        errores.append("El correo institucional no es válido.")
    if sede not in sedes_validas:
        errores.append("Seleccione una sede válida.")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        errores.append("La fecha no es válida.")
    if hora:
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            errores.append("La hora no es válida.")
    if tipo == "hallazgo":
        if not hora:
            errores.append("La hora es obligatoria en objetos encontrados.")
        if not contenido:
            errores.append("Debe adjuntar una foto del objeto encontrado.")
    return errores


def _render(request, tipo, errores=None, exito=None):
    return templates.TemplateResponse(
        request,
        "formulario.html",
        {
            "tipo": tipo,
            "errores": errores or [],
            "exito": exito,
            "sedes": listar_sedes(),
        },
    )


@router.get("/{tipo}", response_class=HTMLResponse)
def formulario(request: Request, tipo: str):
    if tipo not in TIPOS:
        raise HTTPException(status_code=404)
    return _render(request, tipo)


@router.post("/{tipo}", response_class=HTMLResponse)
async def enviar(
    request: Request,
    tipo: str,
    rol: str = Form(...),
    cargo_personal: str = Form(""),
    nombre_completo: str = Form(...),
    correo_institucional: str = Form(...),
    identificacion: str = Form(...),
    telefono: str = Form(...),
    sede: str = Form(...),
    objeto: str = Form(...),
    descripcion: str = Form(...),
    fecha: str = Form(...),
    hora: str = Form(""),
    foto: UploadFile | None = File(None),
):
    if tipo not in TIPOS:
        raise HTTPException(status_code=404)

    contenido = await foto.read() if foto and foto.filename else b""
    sedes_validas = {s["nombre"] for s in listar_sedes()}

    errores = validar(rol, cargo_personal, correo_institucional, sede,
                      sedes_validas, fecha, hora, contenido, tipo)
    if errores:
        return _render(request, tipo, errores=errores)

    foto_url = None
    if contenido:
        try:
            foto_url = subir_foto(contenido, foto.content_type or "")
        except ValueError as e:
            return _render(request, tipo, errores=[str(e)])

    usuario_id = obtener_o_crear_usuario(
        tipo=rol,
        cargo_personal=cargo_personal.strip() or None,
        nombre_completo=nombre_completo.strip(),
        correo=correo_institucional.strip(),
        identificacion=identificacion.strip(),
        telefono=telefono.strip(),
    )

    documento = {
        "tipo": tipo,
        "objeto": objeto.strip(),
        "descripcion": descripcion.strip(),
        "sede": sede,
        "fecha": datetime.strptime(fecha, "%Y-%m-%d"),
        "usuario_id": usuario_id,
        "estado": "pendiente",
    }
    if hora:
        documento["hora"] = hora
    if foto_url:
        documento["foto_url"] = foto_url

    reporte_id = insertar_reporte(documento)
    return _render(request, tipo, exito=reporte_id)