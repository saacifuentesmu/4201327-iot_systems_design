# IoT Systems Design Labs

Bilingual (EN/ES) university course: 8 hands-on labs building a Thread mesh IoT system on ESP32-C6, aligned with ISO/IEC 30141:2024.

**Migrating from ESP-IDF to Zephyr.** `en/0_0_setup.md` is Zephyr. Labs 1-8 and the SOPs still document ESP-IDF; port them lab by lab and keep each file internally consistent.

## Structure

- `en/` — English course content (guides, labs, SOPs)
- `es/` — Spanish course content (mirrors `en/`)
- `tools/` — Python utilities (CoAP client, dashboards, OTA server, e2e tests)
- `en/labs/lab1-8.md` — Weekly lab guides
- `en/labs/sops/` — Step-by-step implementation references
- `ISO_IEC_30141_2024(en).pdf` — Reference standard

## Tech stack

- **Hardware:** ESP32-C6
- **Frameworks:** Zephyr (target), ESP-IDF (being replaced), OpenThread
- **Protocols:** Thread (802.15.4), CoAP, CBOR, DTLS, MQTT, HTTP
- **Tools:** Python 3 (aiocoap, paho-mqtt, Flask)

## Content rules

- Labs reference ISO/IEC 30141:2024. The standard defines six **viewpoints** (Foundational, Business, Usage, Functional, Trustworthiness, Construction) and the Functional viewpoint contains six **domains** (PED, SCD, ASD, OMD, UD, RAID). Do not conflate viewpoints with domains.
- Lab numbering: Lab 0 = HTTP intro, Lab 0.5 = MQTT intro, Labs 1-8 = Thread/CoAP progression.
- SOPs in `en/labs/sops/` are detailed implementation guides; lab files in `en/labs/` are higher-level with role-based context.

## Code style

- New C code targets Zephyr: `west` workflow, devicetree overlays, Kconfig fragments, `LOG_*` macros.
- Legacy ESP-IDF C follows Espressif conventions (esp_err_t returns, ESP_LOG macros, menuconfig).
- Python tools use standard library + minimal dependencies; keep them simple and self-contained.
- Firmware examples target ESP32-C6 only (`esp32c6_devkitc/esp32c6/hpcore` in Zephyr).

## Agent delegation

| Task | Agent |
|---|---|
| Writing/editing code or running commands | `coder` |
| Analyzing logs, build output, UART/RTT traces | `checker` |
| Code review before committing | `reviewer` |
| Writing tests | `tester` |
| Firmware crashes, HardFaults, linker errors | `fw-debugger` |
| Commit messages, PR descriptions | `git` |
