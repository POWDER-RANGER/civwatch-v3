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


---

## Public platform status — October 2026

**CIVINTELLIGENCE is live on the public web and its REST/API surface is active.**

**Public site:** https://civintelligence.onrender.com

The web platform is now the working reference implementation for the CIVWATCH ecosystem: the core application, public-data surfaces, evidence/provenance model, specialized pillars, and integration boundaries are being exercised through the deployed CIVINTELLIGENCE service.

### Applications are next

With the web application and REST contracts now active, the remaining client work is primarily **productization and platform packaging**, not rebuilding the intelligence platform from scratch. Native applications for the major target platforms are planned and will be coming soon.

The application layer can consume the same stable contracts already used by the web experience:

- **Android**
- **iOS**
- **Windows**
- **Linux**
- additional platform clients as the shared API contract matures

The existing Flutter client and service boundaries give the ecosystem a head start. Mobile/desktop applications can progressively adopt the established authentication, API, provenance, map, evidence, and desk contracts rather than duplicating backend intelligence.

### How quickly this came together

The current milestone is notable because the ecosystem moved from a multi-repository architecture and integration plan to a functioning public platform in a short development window. The difficult architectural work — ownership boundaries, public-data ingestion, REST contracts, evidence/provenance rules, Watchtower/Cell Titan integration, and the user-facing desk model — is already substantially established.

That means the next step should be treated as **client delivery on top of an operating platform**. The web application is the reference surface; native clients become additional presentation and interaction layers over the same CIVINTELLIGENCE contracts.

> **Build once at the platform layer. Deliver many clients at the edge.**

### Ecosystem rule

CIVINTELLIGENCE remains the system of record. Specialized repositories retain clear ownership of their domains, while clients consume stable public/service contracts. Legacy and predecessor repositories remain valuable migration/reference material but are not silently represented as unified production capabilities.

**Status discipline:** live means exposed and usable; available means implemented and integrated; in progress means actively being built; planned means not yet shipped. No synthetic or unavailable source is represented as live evidence.
