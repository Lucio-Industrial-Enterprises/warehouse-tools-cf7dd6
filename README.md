# Warehouse tools

Small Python utilities for warehouse order and shipping workflows.

Run the tests with `python3 -m unittest discover -s tests -v`.

## Shipping

`shipping_quote(weight_kg, zone, service="standard")` returns a shipping quote
in dollars.

| Parameter   | Values                      | Description                        |
|-------------|-----------------------------|------------------------------------|
| `weight_kg` | positive float              | Parcel weight in kilograms         |
| `zone`      | `"local"`, `"regional"`    | Delivery zone                      |
| `service`   | `"standard"`, `"express"`  | Service level (default: standard)  |

Express shipping adds **$7** to the standard quote for the given zone.

```python
from warehouse.rates import shipping_quote

shipping_quote(2, "local")                     # → 8.0  (standard)
shipping_quote(2, "local", service="express")  # → 15.0 (express)
```

### CLI

```
python -m warehouse.cli <weight_kg> <zone> [--service {standard,express}]
```

Examples:

```
python -m warehouse.cli 2 local                    # $8.00
python -m warehouse.cli 2 local --service express  # $15.00
```
