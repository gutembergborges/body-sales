#!/usr/bin/env python3
"""Generate fixtures/clientes.json with synthetic (invented) customers.

The output keeps the exact shape of the legacy ERP "ObterClientes" response
(same 40 keys, same order, same value types), so it can be used to:
  - run the Quasar front-end against a mock API, and
  - test the importer/seeder of the new back-end.

Safety rules baked in:
  - every person and company name is invented;
  - CPF/CNPJ numbers intentionally FAIL the official check digits,
    so they can never belong to a real person or company;
  - e-mails use example.com (reserved by RFC 2606);
  - phone numbers use a fixed 0000/9000 pattern.

Usage (standard library only, deterministic):
    python3 fixtures/generate_clientes.py > fixtures/clientes.json
"""

import json
import random
import sys
from datetime import datetime, timezone

SEED = 42
TOTAL = 100

FIRST_NAMES_M = ["JOAO", "PEDRO", "LUCAS", "MATEUS", "RAFAEL", "GABRIEL", "BRUNO", "DIEGO", "FELIPE", "TIAGO"]
FIRST_NAMES_F = ["MARIA", "ANA", "JULIA", "BEATRIZ", "CAMILA", "LARISSA", "FERNANDA", "PATRICIA", "RENATA", "SOFIA"]
SURNAMES = ["SILVA", "SANTOS", "OLIVEIRA", "SOUZA", "LIMA", "PEREIRA", "COSTA", "RODRIGUES", "ALMEIDA", "NASCIMENTO"]
COMPANIES = [
    ("ACADEMIA EXEMPLO ALFA LTDA", "ACADEMIA ALFA"),
    ("LOJA MODELO SUPLEMENTOS ME", "LOJA MODELO"),
    ("ESTUDIO TESTE FITNESS LTDA", "ESTUDIO TESTE"),
    ("CENTRO FICTICIO DE TREINO EIRELI", "CENTRO FICTICIO"),
    ("EMPORIO DEMONSTRACAO NATURAL ME", "EMPORIO DEMO"),
]
STREETS = ["RUA DAS ACACIAS", "RUA DOS IPES", "AVENIDA CENTRAL", "TRAVESSA DA PAZ", "RUA PROJETADA A",
           "RUA DO SOL", "AVENIDA DAS PALMEIRAS", "RUA DAS ORQUIDEAS", "ALAMEDA DOS GIRASSOIS", "RUA NOVA"]
DISTRICTS = ["CENTRO", "JARDIM DAS FLORES", "VILA NOVA", "BAIRRO MODELO", "PARQUE VERDE", "JARDIM AMERICA"]
# Codigo_Municipio holds a city NAME in the legacy ERP, not an IBGE code.
CITIES_BA = ["SALVADOR", "LAURO DE FREITAS", "CAMACARI", "FEIRA DE SANTANA", "ALAGOINHAS", "SIMOES FILHO"]
CITIES_OTHER = [("SAO PAULO", "SP"), ("BELO HORIZONTE", "MG"), ("ARACAJU", "SE")]


def legacy_date(rng, start_year, end_year):
    """Return a date in the legacy .NET JSON format: /Date(<epoch ms>)/."""
    start = datetime(start_year, 1, 1, tzinfo=timezone.utc).timestamp()
    end = datetime(end_year, 12, 31, tzinfo=timezone.utc).timestamp()
    return f"/Date({int(rng.uniform(start, end)) * 1000})/"


def _cpf_check_digits(base):
    d1 = (sum(int(n) * w for n, w in zip(base, range(10, 1, -1))) * 10) % 11 % 10
    d2 = (sum(int(n) * w for n, w in zip(base + str(d1), range(11, 1, -1))) * 10) % 11 % 10
    return f"{d1}{d2}"


def _cnpj_check_digits(base):
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    w2 = [6] + w1
    r1 = sum(int(n) * w for n, w in zip(base, w1)) % 11
    d1 = 0 if r1 < 2 else 11 - r1
    r2 = sum(int(n) * w for n, w in zip(base + str(d1), w2)) % 11
    d2 = 0 if r2 < 2 else 11 - r2
    return f"{d1}{d2}"


def invalid_cpf(rng):
    base = "".join(str(rng.randint(0, 9)) for _ in range(9))
    valid = _cpf_check_digits(base)
    return base + f"{(int(valid) + 11) % 100:02d}"  # always differs from the valid digits


def invalid_cnpj(rng):
    base = "".join(str(rng.randint(0, 9)) for _ in range(8)) + "0001"
    valid = _cnpj_check_digits(base)
    return base + f"{(int(valid) + 11) % 100:02d}"


def maybe(rng, value, p_value, empty=None):
    """Return value with probability p_value, otherwise `empty` (None or "")."""
    return value if rng.random() < p_value else empty


def money(rng):
    return round(rng.choice([0.0, 0.0, 0.0, rng.uniform(10, 900)]), 2)


def build_customer(rng, index):
    code = f"{index:06d}"
    is_company = rng.random() < 0.08
    if is_company:
        name, trade_name = rng.choice(COMPANIES)
        sex, cpf, cnpj, kind, birth = None, None, invalid_cnpj(rng), "J", None
        email_user = trade_name.lower().replace(" ", ".")
    else:
        female = rng.random() < 0.4
        first = rng.choice(FIRST_NAMES_F if female else FIRST_NAMES_M)
        last1, last2 = rng.sample(SURNAMES, 2)
        name = trade_name = f"{first} {last1} {last2}"
        sex = maybe(rng, "F" if female else "M", 0.75)
        cpf, cnpj, kind = maybe(rng, invalid_cpf(rng), 0.92), None, "F"
        birth = maybe(rng, legacy_date(rng, 1965, 2004), 0.77)
        email_user = f"{first}.{last1}".lower()

    if rng.random() < 0.95:
        city, uf, country = rng.choice(CITIES_BA), "BA", "1058"
    elif rng.random() < 0.6:
        (city, uf), country = rng.choice(CITIES_OTHER), "1058"
    else:
        city, uf, country = None, None, None

    limit = rng.choice([0.0, 300.0, 500.0, 1000.0, 1500.0])
    return {
        "Codigo_Cliente": code,
        "Nome": name,
        "Nome_Fantasia": trade_name,
        "Cep": maybe(rng, f"4{rng.randint(0, 2599999):07d}", 0.93, rng.choice([None, ""])),
        "Endereco": maybe(rng, rng.choice(STREETS), 0.96, ""),
        "Endereco_Numero": rng.choice([str(rng.randint(1, 999)), str(rng.randint(1, 999)), "SN"]),
        "Bairro": maybe(rng, rng.choice(DISTRICTS), 0.95, ""),
        "Codigo_Municipio": city,
        "Ponto_Referencia": maybe(rng, "PROXIMO A PRACA", 0.12, rng.choice([None, ""])),
        "Caixa_Postal": None,
        "Estado_Uf": uf,
        "Codigo_Pais": country,
        "Data_Nascimento": birth,
        "Sexo": sex,
        "CNPF": cpf,
        "CNPJ": cnpj,
        "Contato": rng.choice([None, None, None, ""]),
        "Telefone": maybe(rng, f"713000{rng.randint(0, 9999):04d}", 0.4),  # 10 digits
        "Ramal": None,
        "Celular": maybe(rng, f"7190000{rng.randint(0, 9999):04d}", 0.75, ""),  # 11 digits
        "Data_Implantacao": legacy_date(rng, 2015, 2020),
        "Codigo_Grupo_Cliente": rng.choice(["0001"] * 18 + ["0003", "14"]),
        "Codigo_CNAE_Fiscal": None,
        "Email": maybe(rng, f"{email_user}{index}@example.com", 0.75, rng.choice([None, ""])),
        "Volume_Compra": None,
        "Comentario": None,
        "Observacao": rng.choice([None, None, None, ""]),
        "Ativo": "",
        "Tipo_Cadastro": kind,
        "Contato2": rng.choice([None, None, None, ""]),
        "Telefone2": None,
        "Ramal2": None,
        "Status_Inclusao": maybe(rng, "D", 0.8),
        "Insc_Estadual": rng.choice([None, None, None, ""]),
        "Limite_Credito": limit,
        "Debito_Titulo": money(rng),
        "areceber": money(rng),
        "atraso": money(rng),
        "pendente": money(rng),
        "Outras_Observacoes": f"LIMITE DE CREDITO R$ {limit:.2f}" if limit and rng.random() < 0.3 else "",
    }


def main():
    rng = random.Random(SEED)
    customers = [build_customer(rng, i) for i in range(2, TOTAL + 1)]
    # Record 000001 matches the default "CONSUMIDOR" client used in src/pages/Carrinho.vue.
    walk_in = build_customer(random.Random(0), 1)
    walk_in.update({"Nome": "CONSUMIDOR", "Nome_Fantasia": "CONSUMIDOR", "CNPF": None, "CNPJ": None,
                    "Data_Nascimento": None, "Sexo": None, "Email": None, "Tipo_Cadastro": "F"})
    json.dump([walk_in] + customers, sys.stdout, ensure_ascii=False, indent=4)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
