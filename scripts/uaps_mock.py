import random
from datetime import date, datetime, timedelta, timezone

from app.database import SessionLocal
from app.models import AvailabilityLevel, EstoqueUaps, InsulinType, Uaps

random.seed(42)

INSULINAS = [InsulinType.REGULAR, InsulinType.NPH, InsulinType.GLARGINA, InsulinType.LISPRO]
APRESENTACAO = "100 UI/mL"

BAIRROS_FICTICIOS = [f"Bairro Fictício {c}" for c in "ABCDEFGHIJ"]
LAT_BASE, LON_BASE = -3.70, -38.50
HOJE = date.today()

FAIXAS = {
    AvailabilityLevel.ALTO:         {"faixa": (50, 120), "dias_validade": (240, 540)},
    AvailabilityLevel.MEDIO:        {"faixa": (20, 49),  "dias_validade": (180, 400)},
    AvailabilityLevel.BAIXO:        {"faixa": (1, 19),   "dias_validade": (90, 300)},
    AvailabilityLevel.CRITICO:      {"faixa": (1, 8),    "dias_validade": (5, 20)},
    AvailabilityLevel.INDISPONIVEL: {"faixa": (0, 0),    "dias_validade": (30, 300)},
}

PLANO_POR_UAPS = {
    1: AvailabilityLevel.ALTO, 2: AvailabilityLevel.ALTO,
    3: AvailabilityLevel.MEDIO, 4: AvailabilityLevel.MEDIO,
    5: AvailabilityLevel.BAIXO, 6: AvailabilityLevel.BAIXO,
    7: AvailabilityLevel.CRITICO,
    8: AvailabilityLevel.INDISPONIVEL,
}


def seed(db):
    # idempotente: limpa a base mockada antes de repovoar
    db.query(EstoqueUaps).delete()
    db.query(Uaps).delete()

    uaps_objs = []
    for i in range(1, 11):
        uaps = Uaps(
            id_uaps=i,
            nome=f"UAPS Modelo {i:02d}",
            bairro=BAIRROS_FICTICIOS[(i - 1) % len(BAIRROS_FICTICIOS)],
            endereco=f"Rua Modelo, {i * 100}",
            latitude=round(LAT_BASE + random.uniform(-0.05, 0.05), 6),
            longitude=round(LON_BASE + random.uniform(-0.05, 0.05), 6),
            ativa=(i != 10),
        )
        db.add(uaps)
        uaps_objs.append(uaps)
    db.flush()

    id_estoque = 100
    for uaps in uaps_objs:
        if not uaps.ativa:
            continue
        for idx, tipo in enumerate(INSULINAS):
            if uaps.id_uaps == 9:
                nivel = list(AvailabilityLevel)[idx % len(AvailabilityLevel)]
            else:
                nivel = PLANO_POR_UAPS.get(uaps.id_uaps, AvailabilityLevel.MEDIO)

            fmin, fmax = FAIXAS[nivel]["faixa"]
            dmin, dmax = FAIXAS[nivel]["dias_validade"]
            quantidade = random.randint(fmin, fmax)
            validade = HOJE + timedelta(days=random.randint(dmin, dmax))

            id_estoque += 1
            db.add(EstoqueUaps(
                id_estoque=id_estoque,
                id_uaps=uaps.id_uaps,
                tipo=tipo,
                apresentacao=APRESENTACAO,
                quantidade_disponivel=quantidade,
                nivel_disponibilidade=nivel,
                lote=f"MOCK-{tipo.value.upper()}-{id_estoque:03d}",
                validade=validade,
                updated_at=datetime.now(timezone.utc),
            ))

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
        print("Base fictícia de UAPS e estoques semeada com sucesso.")
    finally:
        db.close()