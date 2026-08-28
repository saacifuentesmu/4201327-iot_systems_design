# IoT Systems Design / Diseño de Sistemas IoT

**ESP32-C6 • Zephyr • OpenThread • ISO/IEC 30141:2024**

Eight hands-on labs building a Thread mesh sensor network — from the radio up to a
dashboard — designed and documented against ISO/IEC 30141:2024.

### → [Start the course](en/) · [Setup guide](en/0_0_setup.md)

> 🇪🇸 El curso está completo en inglés (`en/`). La traducción al español (`es/`)
> está planeada.

---

## Course map

| | |
|---|---|
| [Course overview](en/README.md) | Start here — labs, deliverables, assessment |
| [Setup](en/0_0_setup.md) | Install Zephyr, build Hello World on the ESP32-C6 |
| [Project scenario](en/1_project_scenario.md) | GreenField Technologies — your role and stakeholders |
| [ISO architecture](en/2_iso_architecture.md) | The ISO/IEC 30141:2024 framework |
| [Deliverable templates](en/3_deliverables_template.md) | DDR and ADR formats |
| [Labs 1–8](en/labs/) | Weekly guides · [SOPs](en/labs/sops/) for step-by-step detail |
| [References](en/references.md) · [Glossary](en/glossary.md) | Lookups |

**Arc:** weeks 1–2 physical and link layer (SCD) · 3–4 mesh and CoAP (SCD + ASD) ·
5–6 border router and security (SCD + OMD + RAID) · 7–8 dashboard and integration
(all six domains).

## Tools

Host-side Python utilities, shared by both languages: a
[CoAP client](tools/coap_client.py), dashboards for
[HTTP](tools/dashboard_http.py), [MQTT](tools/dashboard_mqtt.py) and
[CoAP](tools/dashboard_coap.py), an [OTA server](tools/ota_server.py), and
[end-to-end tests](tools/test_e2e.py).

## Reference standard

**ISO/IEC 30141:2024** — *Internet of Things (IoT) Reference Architecture*. The
course is aligned to it. It is copyrighted and **not** redistributed here; get it
from [ISO](https://www.iso.org/search.html?q=ISO%2FIEC%2030141).

The standard's six **viewpoints** (Foundational, Business, Usage, Functional,
Trustworthiness, Construction) are not the same thing as the Functional viewpoint's
six **domains** (PED, SCD, ASD, OMD, UD, RAID) — [2_iso_architecture.md](en/2_iso_architecture.md)
keeps them straight.
