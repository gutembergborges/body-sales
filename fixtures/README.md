# Fixtures

Synthetic test data. **Every record here is invented.** No real customer data belongs in this repository.

## `clientes.json`

100 fake customers with the exact shape of the legacy ERP `ObterClientes` response: the same 40 keys, in the same order, with the same value types.

Use it to:

- run the Quasar front-end against a mock API while the new back-end doesn't exist yet;
- test the importer or seeder of the new back-end (legacy fields → new `customers` table).

Regenerate it with the standard library only (output is deterministic, seed `42`):

```bash
python3 fixtures/generate_clientes.py > fixtures/clientes.json
```

### Safety rules

| Field | Rule |
|---|---|
| `Nome`, `Nome_Fantasia` | Invented from generic name lists; companies use obviously fictional names |
| `CNPF` (CPF), `CNPJ` | Intentionally **fail** the official check digits, so they can't match a real person or company |
| `Email` | Always `@example.com` (reserved by RFC 2606) |
| `Telefone`, `Celular` | Fixed `713000xxxx` / `7190000xxxx` patterns |

### Legacy format notes

- Dates use the old .NET JSON format: `"/Date(1546300800000)/"` (epoch milliseconds).
- `Codigo_Municipio` holds a city **name**, not an IBGE code.
- Money fields (`Limite_Credito`, `areceber`, …) are floats. The new back-end should store integer cents.
- Record `000001` is `CONSUMIDOR`, the default client used in `src/pages/Carrinho.vue`.
- Many fields are always `null` or `""` in the legacy data (`Ramal`, `Volume_Compra`, `Ativo`, …). The new `customers` table only needs a few of them.
