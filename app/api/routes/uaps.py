from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import InsulinType, User
from app.schemas import UapsOut
from app.services import uaps_service


router = APIRouter(
    prefix="/api/uaps",
    tags=["uaps"],
)


@router.get(
    "",
    response_model=list[UapsOut],
)
def consultar_disponibilidade(
    tipo: InsulinType | None = Query(None, description="Regular, NPH, Glargina ou Lispro"),
    apresentacao: str | None = Query(None, description='Ex.: "100 UI/mL"'),
    apenas_disponiveis: bool = Query(True, description="Se True, oculta UAPS sem estoque da insulina buscada"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pares = uaps_service.listar_uaps_com_disponibilidade(
        db,
        tipo=tipo,
        apresentacao=apresentacao,
        apenas_disponiveis=apenas_disponiveis,
    )

    resposta = []
    for uaps, estoque in pares:
        item = UapsOut.model_validate(uaps)
        ids_filtrados = {e.id_estoque for e in estoque}
        item.estoque = [e for e in item.estoque if e.id_estoque in ids_filtrados]
        resposta.append(item)

    return resposta