from datetime import datetime
from pathlib import Path
from bson.errors import InvalidId
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.datalake.storage import subir_foto
from app.db.reportes import (
    actualizar_reclamo, listar_reportes, marcar_reclamado,
    obtener_reporte, revertir_reclamo,
)
from app.db.usuarios import buscar_usuario_id_por_correo, obtener_usuarios

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(
    directory=Path(__file__).resolve().parent.parent / "templates"
)

SECCIONES = {
    "encontrados": ("Objetos encontrados", {"tipo": "hallazgo"}),
    "perdidos": ("Objetos perdidos", {"tipo": "extravio"}),
    "reclamados": ("Objetos reclamados", {"estado": "reclamado"}),
}


def _es_admin(request: Request) -> bool:
    return request.session.get("rol") == "admin"


def _reporte_o_404(reporte_id: str) -> dict:
    try:
        reporte = obtener_reporte(reporte_id)
    except InvalidId:
        reporte = None
    if not reporte:
        raise HTTPException(status_code=404)
    return reporte


def _validar_entrega(nombre: str, correo: str) -> list[str]:
    errores = []
    if not nombre.strip():
        errores.append("Escriba el nombre de quien recibe el objeto.")
    if "@" not in correo:
        errores.append("El correo de quien recibe no es válido.")
    return errores


async def _subir_foto_entrega(foto):
    # Devuelve (url, error). Si no hay foto, ambos son None.
    if not foto or not foto.filename:
        return None, None
    contenido = await foto.read()
    try:
        return subir_foto(contenido, foto.content_type or ""), None
    except ValueError as e:
        return None, str(e)


def _render_entregar(request, reporte, accion, titulo, reclamo=None, errores=None):
    return templates.TemplateResponse(
        request,
        "entregar.html",
        {
            "reporte": reporte,
            "accion": accion,
            "titulo": titulo,
            "reclamo": reclamo or {},
            "errores": errores or [],
            "usuario": request.session.get("usuario"),
        },
    )


@router.get("", response_class=HTMLResponse)
def inicio(request: Request):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    return RedirectResponse("/admin/encontrados", status_code=303)


@router.get("/foto/{ruta:path}")
def foto(request: Request, ruta: str):
    if not _es_admin(request):
        raise HTTPException(status_code=401)

    base = Path(settings.DATALAKE_PATH).resolve()
    archivo = (base / ruta).resolve()
    if base not in archivo.parents or not archivo.is_file():
        raise HTTPException(status_code=404)
    return FileResponse(archivo)


# ---------- CREAR: marcar un objeto como entregado ----------

@router.get("/entregar/{reporte_id}", response_class=HTMLResponse)
def entregar_form(request: Request, reporte_id: str):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    reporte = _reporte_o_404(reporte_id)
    return _render_entregar(
        request, reporte,
        accion=f"/admin/entregar/{reporte_id}",
        titulo="Marcar como entregado",
    )


@router.post("/entregar/{reporte_id}", response_class=HTMLResponse)
async def entregar(
    request: Request,
    reporte_id: str,
    nombre_receptor: str = Form(""),
    correo_receptor: str = Form(""),
    foto_entrega: UploadFile | None = File(None),
):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    reporte = _reporte_o_404(reporte_id)
    accion = f"/admin/entregar/{reporte_id}"

    if reporte.get("estado") == "reclamado":
        return _render_entregar(request, reporte, accion,
                                "Marcar como entregado",
                                errores=["Este objeto ya fue entregado."])

    errores = _validar_entrega(nombre_receptor, correo_receptor)
    foto_url, error_foto = await _subir_foto_entrega(foto_entrega)
    if error_foto:
        errores.append(error_foto)
    if errores:
        return _render_entregar(request, reporte, accion,
                                "Marcar como entregado", errores=errores)

    marcar_reclamado(reporte_id, {
        "nombre_receptor": nombre_receptor.strip(),
        "correo_receptor": correo_receptor.strip(),
        "receptor_usuario_id": buscar_usuario_id_por_correo(correo_receptor.strip()),
        "foto_entrega_url": foto_url,
        "fecha_entrega": datetime.now(),
        "entregado_por": request.session.get("usuario"),
    })
    return RedirectResponse("/admin/reclamados", status_code=303)


# ---------- ACTUALIZAR: editar la entrega ----------

@router.get("/reclamados/{reporte_id}/editar", response_class=HTMLResponse)
def editar_form(request: Request, reporte_id: str):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    reporte = _reporte_o_404(reporte_id)
    if reporte.get("estado") != "reclamado":
        return RedirectResponse("/admin/encontrados", status_code=303)
    return _render_entregar(
        request, reporte,
        accion=f"/admin/reclamados/{reporte_id}/editar",
        titulo="Editar entrega",
        reclamo=reporte.get("reclamo"),
    )


@router.post("/reclamados/{reporte_id}/editar", response_class=HTMLResponse)
async def editar(
    request: Request,
    reporte_id: str,
    nombre_receptor: str = Form(""),
    correo_receptor: str = Form(""),
    foto_entrega: UploadFile | None = File(None),
):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    reporte = _reporte_o_404(reporte_id)
    accion = f"/admin/reclamados/{reporte_id}/editar"

    errores = _validar_entrega(nombre_receptor, correo_receptor)
    foto_url, error_foto = await _subir_foto_entrega(foto_entrega)
    if error_foto:
        errores.append(error_foto)
    if errores:
        return _render_entregar(request, reporte, accion, "Editar entrega",
                                reclamo=reporte.get("reclamo"), errores=errores)

    campos = {
        "nombre_receptor": nombre_receptor.strip(),
        "correo_receptor": correo_receptor.strip(),
        "receptor_usuario_id": buscar_usuario_id_por_correo(correo_receptor.strip()),
    }
    if foto_url:
        campos["foto_entrega_url"] = foto_url

    actualizar_reclamo(reporte_id, campos)
    return RedirectResponse("/admin/reclamados", status_code=303)


# ---------- ELIMINAR: deshacer la entrega ----------

@router.post("/reclamados/{reporte_id}/eliminar")
def eliminar(request: Request, reporte_id: str):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    _reporte_o_404(reporte_id)
    revertir_reclamo(reporte_id)
    return RedirectResponse("/admin/reclamados", status_code=303)


# ---------- LEER: listados ----------

@router.get("/{seccion}", response_class=HTMLResponse)
def seccion_admin(request: Request, seccion: str):
    if not _es_admin(request):
        return RedirectResponse("/login", status_code=303)
    if seccion not in SECCIONES:
        raise HTTPException(status_code=404)

    titulo, filtro = SECCIONES[seccion]
    reportes = listar_reportes(filtro)
    personas = obtener_usuarios([r.get("usuario_id") for r in reportes])

    for r in reportes:
        r["id"] = str(r["_id"])
        r["persona"] = personas.get(r.get("usuario_id"), {})

    return templates.TemplateResponse(
        request,
        "admin_lista.html",
        {
            "titulo": titulo,
            "seccion": seccion,
            "reportes": reportes,
            "usuario": request.session.get("usuario"),
        },
    )