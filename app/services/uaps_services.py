from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import AvailabilityLevel, EstoqueUaps, InsulinType, Uaps


def listar_uaps_com_disponibilidade(
    db: Session,
    tipo: InsulinType | None = None,
    apresentacao: str | None = None,
    apenas_disponiveis: bool = True,
) -> list[tuple[Uaps, list[EstoqueUaps]]]:
    statement = (
        select(Uaps)
        .where(Uaps.ativa.is_(True))
        .options(joinedload(Uaps.estoque))
        .order_by(Uaps.id_uaps)
    )
    uaps_list = db.scalars(statement).unique().all()

    resultado: list[tuple[Uaps, list[EstoqueUaps]]] = []
    for uaps in uaps_list:
        estoque_filtrado = [
            e for e in uaps.estoque
            if (tipo is None or e.tipo == tipo)
            and (apresentacao is None or e.apresentacao == apresentacao)
            and (not apenas_disponiveis or e.nivel_disponibilidade != AvailabilityLevel.INDISPONIVEL)
        ]
        if estoque_filtrado:
            resultado.append((uaps, estoque_filtrado))

    return resultado