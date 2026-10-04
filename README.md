# CIVWATCH V3

**Predecessor/reference RF dashboard for the CIVWATCH ecosystem.**

CIVWATCH v3 is an earlier standalone RF observability implementation covering cellular, Wi-Fi, D2D, and transport-domain visualization with a cryptographic evidence concept and matrix-style dashboard.

> **Current role:** predecessor/reference implementation.
> **Canonical RF service:** [CIVWATCH Cell Titan](https://github.com/POWDER-RANGER/civwatch-cell-titan).
> **System of record:** [CivilianIntelligence](https://github.com/POWDER-RANGER/CivilianIntelligence).

## Why this repository remains

This repository is retained for:

- historical RF UI work
- comparison during Cell Titan evolution
- reusable visualization ideas
- migration/reference of earlier RF concepts

New integrations should use Cell Titan rather than create new production dependencies on v3.

## Historical feature set

| Area | Reference implementation |
|---|---|
| Cellular | LTE / 5G-oriented RF dashboard |
| Wi-Fi | 802.11-oriented visualization |
| D2D | Sidelink-oriented concepts |
| Transport | Bluetooth / BLE / NFC-oriented concepts |
| Evidence | Cryptographic chain concept |
| UI | Matrix-style live topology dashboard |
| Sensors | Earlier ADB/federated sensor model |

These describe the predecessor implementation and are **not** a claim that every feature is accepted in unified production.

## Quick start

Reference-only local execution:

~~~bash
cp .env.example .env
./launch.sh
# historically served on localhost:8000
~~~

Review configuration before exposing the service beyond localhost.

## Migration path

~~~text
CIVINTELLIGENCE
        |
        +---- Cell Titan  <-- current RF pillar
        |
        +---- Watchtower  <-- current geospatial pillar
        |
        +---- civwatch-app
~~~

## Related repositories

- [CivilianIntelligence](https://github.com/POWDER-RANGER/CivilianIntelligence)
- [Cell Titan](https://github.com/POWDER-RANGER/civwatch-cell-titan)
- [Watchtower](https://github.com/POWDER-RANGER/civwatch-watchtower)
- [CIVWATCH](https://github.com/POWDER-RANGER/CIVWATCH)

## License

MIT
