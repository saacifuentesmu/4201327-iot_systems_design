#!/usr/bin/env python3
"""Figures for the session-7 deck (07_fleet.md).

    python3 fleet_figs.py       # writes fleet_*.svg here

fleet_dashboard.png is a screenshot of tools/fleet's Grafana dashboard on the course
bench (2026-10-23, three ESP32-C6 nodes), taken during the Lab 7 drills;
fleet_dashboard.svg embeds it with its callouts. The pet-tracker and truck figures draw
two production architectures in outline; the signal traces are shapes, not data.
fleet_upload.svg rounds a typical FTP upload from a production tracker's log; its
hatched bars are computed with a 150 ms round trip, not measured.
"""
import base64
import math
from pathlib import Path

from figlib import C, GRID, INK, MUTED, PAL, PANEL, T, box, line, poly, rect, save, svg, text

HERE = Path(__file__).resolve().parent
TH, RAID, SCD, UD, OMD, TW = (PAL[k] for k in ("Thread", "RAID", "SCD", "UD", "OMD", "Trustworthiness"))


MARKERS = "<defs>" + "".join(
    f'<marker id="a-{k}" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="12" refX="13" refY="6" '
    f'orient="auto"><path d="M0 0 L14 6 L0 12 Z" fill="{v}"/></marker>'
    for k, v in {"ink": INK, "muted": MUTED, **C}.items()) + "</defs>"
MKEY = {INK: "ink", MUTED: "muted", **{v: k for k, v in C.items()}}


def arr(x1, y1, x2, y2, stroke=INK, sw=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" '
            f'stroke-width="{sw}"{d} marker-end="url(#a-{MKEY[stroke]})"/>')


def parr(points, stroke=INK, sw=2.5, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (f'<polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{sw}"{d} '
            f'marker-end="url(#a-{MKEY[stroke]})"/>')


def fig(w, h, body):
    return svg(w, h, [MARKERS] + body)


def circle(cx, cy, r, fill, stroke="none", sw=0):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def badge(cx, cy, n, col):
    return circle(cx, cy, 15, C[col]) + "\n" + text(cx, cy + 6, n, 17, 800, "#fff", "middle")


def pill(x, y, w, label, col):
    return "\n".join([rect(x, y, w, 30, T[col], C[col], 2, 15), circle(x + 18, y + 15, 6, C[col]),
                      text(x + 32, y + 21, label, 16, 700, C[col])])


def paths():
    body = [text(20, 34, "Labs 3–6: one node, one shell, inside the mesh", 21, 700, MUTED)]
    body.append(box(20, 50, 150, 56, "node", SCD, 20))
    body.append(line(170, 78, 300, 78, MUTED, 3, arrow=True))
    body.append(box(300, 50, 170, 56, "your shell", "gray", 20))
    body.append(text(20, 160, "Lab 7: the whole fleet, out of the mesh", 21, 700, INK))
    hops = [("nodes", SCD, "CoAPS · CBOR"), ("bridge", RAID, "MQTT · JSON"), ("broker", "gray", "subscribe"),
            ("Telegraf", "gray", "points"), ("InfluxDB", "gray", "Flux queries"), ("Grafana", UD, "")]
    x = 20
    for i, (name, col, proto) in enumerate(hops):
        body.append(box(x, 180, 140, 60, name, col, 20))
        if proto:
            body.append(line(x + 140, 210, x + 175, 210, INK, 3, arrow=True))
            body.append(text(x + 157, 268, proto, 16, 400, MUTED, "middle"))
        x += 175
    body.append(text(20, 320, "the mesh speaks CoAP over IPv6; everything right of the bridge is ordinary IT",
                     19, 400, MUTED))
    return svg(1080, 336, body)


def loop():
    steps = [("telemetry", "batt, rssi, up, hsfail"),
             ("baseline", "normal for this node?"),
             ("compare", "outside the band?"),
             ("alert", "a red light, a ticket")]
    body, x = [], 20
    for i, (name, sub) in enumerate(steps):
        col = TW if name == "alert" else OMD
        body.append(box(x, 40, 230, 80, name, col, 22))
        body.append(text(x + 115, 152, sub, 18, 400, INK, "middle"))
        if i < 3:
            body.append(line(x + 232, 80, x + 268, 80, INK, 3, arrow=True))
        x += 270
    body.append(text(20, 200, "the lab's lights are fixed thresholds; a fleet compares each node with its own history",
                     19, 400, MUTED))
    return svg(1100, 216, body)


def audiences():
    body = [box(20, 115, 160, 90, "node 4", SCD, 24)]
    body.append(poly([(180, 145), (200, 145), (200, 93), (214, 93)], MUTED, 2))
    body.append(poly([(180, 175), (200, 175), (200, 233), (214, 233)], MUTED, 2))
    lanes = [(80, UD, "business data", "soil 24.5 °C", 24, "changes in minutes",
              "Daniela (farmer)", "is my soil OK?"),
             (220, OMD, "telemetry", "battery 3100 mV", 120, "changes over hours",
              "Edwin, Gustavo (ops)", "is the node OK?")]
    for y, col, name, example, step, rate, who, asks in lanes:
        body.append(text(220, y - 22, name, 21, 700, C[col]))
        body.append(text(220 + 13.5 * len(name) + 14, y - 22, example, 19, 400, INK))
        body.append(line(220, y + 30, 700, y + 30, GRID, 2))
        for x in range(222, 700, step):
            body.append(rect(x, y, 9, 28, C[col], C[col], 0, 2))
        body.append(text(700, y + 54, rate, 16, 400, MUTED, "end"))
        body.append(arr(712, y + 14, 756, y + 14, C[col], 3))
        body.append(box(760, y - 18, 320, 66, who, col, 21, asks))
    body.append(text(20, 318, "one node, two audiences: send each stream at the rate its reader needs",
                     19, 400, MUTED))
    return fig(1100, 330, body)


def signals():
    x0, x1, h = 220, 760, 46

    def trace(f, top, t0, t1, n=60):
        return [(x0 + (x1 - x0) * (t0 + (t1 - t0) * i / n), top + h * f(t0 + (t1 - t0) * i / n))
                for i in range(n + 1)]

    def wiggle(t):
        return 0.05 * math.sin(41 * t) + 0.04 * math.sin(97 * t)

    rows = [
        ("battery", "health", OMD, "a fault; dying soon",
         lambda t: 0.1 + 0.25 * t if t < 0.72 else 0.28 + 2.4 * (t - 0.72), 0.72),
        ("link RSSI", "health", OMD, "moved, blocked, jammed",
         lambda t: 0.3 + wiggle(t) + (0.4 if t >= 0.6 else 0), 0.6),
        ("uptime", "health", OMD, "it rebooted",
         lambda t: 0.95 - 0.85 * t / 0.66 if t < 0.66 else 0.95 - 0.85 * (t - 0.66) / 0.66, 0.66),
        ("failed handshakes", "security", TW, "wrong key, or key guessing",
         lambda t: 0.95 if t < 0.6 else 0.95 - 0.2 * min(4, 1 + int((t - 0.6) / 0.09)), 0.6),
    ]
    body = [text(20, 30, "signal", 17, 700, MUTED), text(x0, 30, "normal, then the change", 17, 700, MUTED),
            text(800, 30, "changes when", 17, 700, MUTED)]
    for i, (name, kind, col, when, f, tc) in enumerate(rows):
        top = 52 + i * 82
        normal = trace(f, top, 0, tc - 0.001)
        body.append(text(20, top + 24, name, 21, 700, INK))
        body.append(text(20, top + 47, kind, 16, 600, C[col]))
        body.append(poly(normal, MUTED, 3))
        body.append(poly([normal[-1]] + trace(f, top, tc, 1), C[col], 4))
        body.append(text(800, top + 32, when, 20, 400, INK))
        body.append(line(20, top + 68, 1080, top + 68, GRID, 1))
    top = 52 + 4 * 82
    body.append(text(20, top + 24, "reports", 21, 700, INK))
    body.append(text(20, top + 47, "security", 16, 600, C[TW]))
    for k in range(12):
        body.append(rect(x0 + 2 + k * 26, top + 8, 7, 30, MUTED, MUTED, 0, 2))
    body.append(rect(x0 + 330, top + 4, x1 - x0 - 330, 38, T[TW], C[TW], 2, 6, "6 4"))
    body.append(text((x0 + 330 + x1) / 2, top + 29, "silence", 18, 700, C[TW], "middle"))
    body.append(text(800, top + 32, "any of these, or theft", 20, 400, INK))
    return fig(1100, 470, body)


def fanout():
    ny = [60, 128, 196, 264]
    cons = [("phone", "gray"), ("laptop", "gray"), ("Grafana", UD)]
    cy = [84, 162, 240]
    body = [text(20, 30, "each consumer to each node", 22, 700, INK)]
    for y in ny:
        for c in cy:
            body.append(line(150, y + 22, 378, c + 22, MUTED, 2))
    for i, y in enumerate(ny):
        body.append(box(30, y, 120, 44, f"node {i + 1}", SCD, 19))
    for (name, col), y in zip(cons, cy):
        body.append(box(380, y, 140, 44, name, col, 19))
    body.append(text(20, 352, "12 DTLS sessions", 21, 800, C[TW]))
    body.append(text(20, 380, "each node answers every consumer", 18, 400, INK))
    body.append(text(20, 406, "an IPv4-only phone can't reach the mesh", 18, 400, INK))

    body.append(line(570, 20, 570, 410, GRID, 2, "6 6"))
    body.append(text(610, 30, "a broker in between", 22, 700, INK))
    for i, y in enumerate(ny):
        body.append(box(610, y, 110, 44, f"node {i + 1}", SCD, 19))
        body.append(line(720, y + 22, 780, 184, MUTED, 2))
    body.append(box(780, 150, 110, 68, "bridge", RAID, 20))
    body.append(arr(890, 184, 920, 184))
    body.append(box(920, 150, 110, 68, "broker", "gray", 20))
    for (name, col), y in zip(cons, cy):
        body.append(arr(1030, 184, 1066, y + 22, MUTED, 2))
        body.append(box(1066, y, 124, 44, name, col, 19))
    body.append(text(610, 352, "4 DTLS sessions + 3 subscriptions", 21, 800, INK))
    body.append(text(610, 380, "each node reports once; the broker fans out", 18, 400, INK))
    body.append(text(610, 406, "consumers know a topic; any TCP client connects", 18, 400, INK))
    return fig(1200, 420, body)


def brokers():
    body = [rect(20, 50, 290, 250, T[TH], C[TH], 2, 18, "8 6"),
            text(40, 80, "Thread mesh", 19, 700, C[TH])]
    body.append(poly([(100, 127), (225, 182), (100, 247), (100, 127)], C[TH], 2, dash="5 5"))
    for x, y in [(50, 105), (175, 160), (50, 225)]:
        body.append(box(x, y, 100, 44, "node", SCD, 19))
    body.append(arr(310, 175, 380, 175, INK, 3))
    body.append(text(344, 160, "CoAPS", 16, 600, MUTED, "middle"))
    body.append(box(380, 130, 190, 90, "bridge", RAID, 24, "the architecture"))
    body.append(arr(570, 175, 650, 175, INK, 3))
    body.append(text(609, 160, "MQTT", 16, 600, MUTED, "middle"))
    cards = ["Mosquitto (Lab 7)", "AWS IoT Core", "HiveMQ Cloud", "ThingsBoard"]
    for i, name in enumerate(cards):
        y = 60 + i * 60
        lab = i == 0
        body.append(rect(650, y, 300, 48, T["gray"] if lab else "#fff", INK if lab else GRID, 3 if lab else 2, 10))
        body.append(text(668, y + 31, name, 19, 700 if lab else 400, INK))
    body.append(poly([(964, 60), (976, 60), (976, 288), (964, 288)], MUTED, 2))
    body.append(text(990, 160, "the broker:", 20, 700, INK))
    body.append(text(990, 186, "a setting", 20, 700, INK))
    body.append(text(990, 220, "change the host,", 17, 400, MUTED))
    body.append(text(990, 242, "the port, three", 17, 400, MUTED))
    body.append(text(990, 264, "certificate files", 17, 400, MUTED))
    body.append(text(20, 345, "all of them speak MQTT; none speaks CoAP over Thread, so each needs the same bridge",
                     19, 400, MUTED))
    return fig(1150, 360, body)


def dashboard():
    png = (HERE / "fleet_dashboard.png").read_bytes()
    w, s = 1060, 1060 / 1585
    data = base64.b64encode(png).decode()
    body = [f'<image x="20" y="20" width="{w}" height="{195 * s:.1f}" href="data:image/png;base64,{data}"/>',
            rect(20, 20, w, 195 * s, "none", GRID, 2, 4)]
    notes = [((640, 64), 250, TW, "east: silent past 150 s, red", "a heartbeat detector"),
             ((1095, 114), 630, TW, "north: 4 failed handshakes", "one probe, counted four times"),
             ((1480, 64), 975, OMD, "uptime only grows", "a drop means a reboot")]
    for (px, py), tx, col, head, sub in notes:
        x, y = 20 + px * s, 20 + py * s
        body.append(circle(x, y, 7, "none", C[col], 3))
        body.append(poly([(x, y + 8), (x, 176), (tx, 196)], C[col], 2))
        body.append(text(tx, 222, head, 19, 700, C[col], "middle"))
        body.append(text(tx, 248, sub, 17, 400, INK, "middle"))
    return fig(1100, 262, body)


def scales():
    cols = [("thing", SCD, 125, 175), ("bridge", RAID, 435, 175), ("ingest", "gray", 720, 185),
            ("store", "gray", 935, 135), ("view", UD, 1095, 140)]
    body = [rect(425, 52, 195, 400, T[RAID], "none", 0, 12)]
    for name, col, x, w in cols:
        body.append(text(x + w / 2, 40, name, 20, 800, C[col], "middle"))
    rows = [
        (90, "Lab 7", "your team", ["ESP32-C6 node", ("bridge", "laptop, Pi, gateway"), "Mosquitto", "InfluxDB", "Grafana"],
         ["Thread · CoAPS", "LAN · MQTT"]),
        (240, "Pets", "GPS collars", [("collar", "Wi-Fi · BLE · LTE-M"), ("owner's phone", "BLE path only"),
                                      ("cloud ingest", "MQTT · CoAP · HTTPS"), "DynamoDB", ("console", "staff only")],
         ["BLE", "HTTPS"]),
        (375, "Trucks", "telematics", ["vehicle ECUs", ("gateway", "telematics unit"), None, None, "web portal"],
         ["CAN · J1939", "cellular"]),
    ]
    for y, name, sub, cells, links in rows:
        body.append(text(10, y + 30, name, 22, 800, INK))
        body.append(text(10, y + 54, sub, 16, 400, MUTED))
        for (_, col, x, w), cell in zip(cols, cells):
            if cell is None:
                continue
            label, s = cell if isinstance(cell, tuple) else (cell, "")
            body.append(box(x, y, w, 64, label, col, 18, s))
        if cells[2] is None:
            body.append(box(720, y, 350, 64, "vendor cloud", "gray", 18, "ingest and store, one name"))
        else:
            body.append(arr(905, y + 32, 935, y + 32))
        for (x1, x2), label in zip([(300, 435), (610, 720)], links):
            body.append(arr(x1, y + 32, x2, y + 32))
            body.append(text((x1 + x2) / 2, y + 22, label, 14, 600, MUTED, "middle"))
        body.append(arr(1070, y + 32, 1095, y + 32))
    y = 240
    body.append(parr([(212, y), (212, y - 30), (812, y - 30), (812, y)], C[RAID], 2.5, "8 5"))
    body.append(text(512, y - 38, "Wi-Fi (CoAP), LTE-M (MQTT-SN): the collar speaks IP; the cloud ingest translates",
                     16, 600, C[RAID], "middle"))
    body.append(text(10, 476, "the names change with the business; the five jobs stay", 19, 400, MUTED))
    return fig(1240, 486, body)


def tracker():
    body = [box(20, 90, 140, 290, "collar", SCD, 24, "on the dog")]
    for y, label, ingest in [(120, "Wi-Fi · CoAP", "CoAP server"), (235, "LTE-M · MQTT-SN", "AWS IoT Core"),
                             (350, None, "app API")]:
        body.append(box(470, y - 28, 160, 56, ingest, "gray", 19))
        body.append(arr(630, y, 680, y))
        if label:
            body.append(arr(160, y, 470, y))
            body.append(text(314, y - 12, label, 17, 600, MUTED, "middle"))
    y = 350
    body.append(arr(160, y, 230, y))
    body.append(text(195, y - 12, "BLE", 17, 600, MUTED, "middle"))
    body.append(box(230, y - 30, 172, 60, "owner's phone", RAID, 18, "the bridge here"))
    body.append(arr(402, y, 470, y))
    body.append(text(436, y - 12, "HTTPS", 15, 600, MUTED, "middle"))

    body.append(rect(680, 92, 150, 286, T["gray"], MUTED, 2, 10))
    body.append(text(755, 200, "telemetry", 20, 700, MUTED, "middle"))
    body.append(text(755, 225, "tables", 20, 700, MUTED, "middle"))
    body.append(rect(694, 250, 122, 64, T[RAID], C[RAID], 2, 8))
    body.append(text(755, 276, "one key set", 16, 700, C[RAID], "middle"))
    body.append(text(755, 298, "three paths", 16, 700, C[RAID], "middle"))
    body.append(arr(830, 235, 865, 235))
    body.append(box(865, 200, 160, 70, "collector", "gray", 20, "polls by activity"))
    body.append(arr(1025, 235, 1050, 235))
    body.append(box(1050, 200, 140, 70, "console", UD, 21, "staff login"))
    body.append(pill(1062, 284, 116, "Live 3s", "c3"))
    body.append(text(1120, 342, "the console", 15, 400, MUTED, "middle"))
    body.append(text(1120, 360, "times itself", 15, 400, MUTED, "middle"))

    body.append(box(865, 20, 325, 70, "health checks", OMD, 20, "every minute, inside and out"))
    body.append(parr([(865, 55), (550, 55), (550, 92)], C[OMD], 2, "6 5"))
    body.append(arr(1120, 90, 1120, 200, C[OMD], 2, "6 5"))
    body.append(text(20, 425, "three radios, three protocols, one meaning per field", 20, 700, INK))
    body.append(text(20, 452, "and the console is a product too: it has its own health page", 18, 400, MUTED))
    return fig(1200, 466, body)


def trucks():
    body = [rect(20, 70, 460, 250, PANEL, MUTED, 2, 18, "8 6"),
            text(40, 102, "vehicle", 19, 700, MUTED)]
    body.append(box(40, 150, 170, 90, "ECUs", SCD, 21, "engine, brakes"))
    body.append(arr(210, 195, 320, 195))
    body.append(text(265, 182, "CAN · J1939", 15, 600, MUTED, "middle"))
    body.append(box(320, 150, 140, 90, "gateway", RAID, 21, "GPS + modem"))
    body.append(arr(460, 195, 570, 195))
    body.append(text(522, 182, "cellular", 16, 600, MUTED, "middle"))
    body.append(box(570, 160, 170, 70, "vendor cloud", "gray", 20))
    body.append(arr(740, 195, 790, 195))
    body.append(box(790, 160, 150, 70, "web portal", UD, 20))
    for y, who, asks in [(60, "dispatcher", "where is each truck?"), (160, "mechanic", "which engine faulted?"),
                         (260, "fleet manager", "idling, inspections")]:
        body.append(arr(940, 195, 985, y + 35, C[UD], 2))
        body.append(box(985, y, 205, 70, who, UD, 19, asks))
    body.append(text(20, 390, "the ECUs never speak IP: the gateway parses and re-encodes, like your bridge", 19, 700, INK))
    body.append(text(20, 418, "each alert goes to the role that can act on it", 18, 400, MUTED))
    return fig(1200, 432, body)


def console():
    body = [rect(20, 20, 760, 460, "#fff", MUTED, 2, 12), rect(20, 20, 760, 44, PANEL, "none", 0, 12),
            line(20, 64, 780, 64, GRID, 2)]
    for k in range(3):
        body.append(circle(44 + 18 * k, 42, 6, GRID))
    body.append(rect(110, 30, 420, 24, "#fff", GRID, 2, 12))
    body.append(rect(124, 41, 11, 9, MUTED, "none", 0, 1))
    body.append(f'<path d="M126 41 v-3 a3.5 3.5 0 0 1 7 0 v3" fill="none" stroke="{MUTED}" stroke-width="2"/>')
    body.append(rect(145, 38, 180, 8, GRID, "none", 0, 4))
    x = 40
    for i, tab in enumerate(["Status", "Device", "Timeline", "Battery", "Health"]):
        w = 16 + 9 * len(tab)
        body.append(rect(x, 76, w, 26, INK if i == 0 else PANEL, GRID, 1, 13))
        body.append(text(x + w / 2, 94, tab, 14, 600, "#fff" if i == 0 else MUTED, "middle"))
        x += w + 8
    body.append(pill(650, 74, 110, "Live 3s", "c3"))

    body.append(rect(40, 118, 430, 342, "#fff", GRID, 2, 8))
    body.append(rect(40, 118, 430, 30, PANEL, "none", 0, 8))
    for hx, h in [(70, "device"), (170, "last seen"), (270, "path"), (340, "fw"), (395, "battery")]:
        body.append(text(hx, 138, h, 13, 700, MUTED))
    for r, st in enumerate(["c3", "c3", "c5", "c3", "c7", "c3", "c3", "c3", "c3"]):
        y = 156 + r * 33
        if st == "c5":
            body.append(rect(42, y - 4, 426, 30, T["c5"], "none", 0, 4))
        body.append(circle(56, y + 11, 6, C[st]))
        for bx, bw in [(70, 70 + 13 * (r % 3)), (170, 60), (270, 40), (340, 36), (395, 30 + 9 * ((r * 5) % 4))]:
            body.append(rect(bx, y + 6, bw, 10, GRID, "none", 0, 5))

    body.append(rect(490, 118, 270, 172, "#fff", GRID, 2, 8))
    body.append(text(505, 140, "one device", 14, 700, MUTED))
    body.append(line(505, 220, 745, 220, GRID, 1))
    body.append(poly([(505, 160), (560, 170), (600, 168), (650, 186), (700, 196), (745, 212)], C[OMD], 3))
    for sx, sw, col in [(505, 60, "c4"), (570, 30, "gray"), (605, 80, "c4"), (690, 25, "c1"), (720, 25, "c4")]:
        body.append(rect(sx, 236, sw, 14, T[col], C[col], 1, 3))
    body.append(rect(505, 262, 200, 8, GRID, "none", 0, 4))
    body.append(rect(505, 276, 150, 8, GRID, "none", 0, 4))

    body.append(rect(490, 304, 270, 156, "#fff", GRID, 2, 8))
    body.append(text(505, 326, "service health", 14, 700, MUTED))
    for k in range(30):
        col = "c5" if k == 19 else "c7" if k in (8, 24) else "c3"
        body.append(rect(505 + k * 8.3, 350, 5.5, 46, C[col], "none", 0, 2))
    body.append(rect(505, 412, 240, 32, T["c5"], C["c5"], 1, 6))
    body.append(rect(515, 424, 140, 8, C["c5"], "none", 0, 4))

    for n, (cx, cy) in enumerate([(632, 89), (40, 118), (760, 118), (760, 304), (548, 42)], 1):
        body.append(badge(cx, cy, str(n), OMD))
    legend = [("Live 3s", ["the console times its own data:", "a frozen screen turns red"]),
              ("Fleet table", ["last seen per path, firmware,", "battery; sort and filter"]),
              ("Device page", ["one device's whole story:", "trend, connections, messages"]),
              ("Incidents", ["open after 3 failed checks,", "close after 2 good ones"]),
              ("Login", ["a role per person;", "read-only cloud keys"])]
    for i, (head, lines_) in enumerate(legend):
        y = 52 + i * 88
        body.append(badge(822, y, str(i + 1), OMD))
        body.append(text(848, y + 7, head, 20, 700, INK))
        for j, ln in enumerate(lines_):
            body.append(text(848, y + 32 + 22 * j, ln, 17, 400, MUTED))
    return fig(1200, 500, body)


def acting():
    steps = [("see", OMD, "Lab 7: the dashboard", "a person reads red"),
             ("recover", SCD, "Lab 8: watchdog, fail-safe", "the node fixes itself"),
             ("update", TW, "Lab 8 stretch: signed OTA", "200 nodes, one key")]
    body, x = [], 20
    for i, (name, col, sub, note) in enumerate(steps):
        body.append(box(x, 20, 320, 90, name, col, 26, sub))
        body.append(text(x + 160, 142, note, 18, 400, MUTED, "middle"))
        if i < 2:
            body.append(arr(x + 322, 65, x + 368, 65, INK, 3))
        x += 370
    return fig(1100, 160, body)



def upload():
    x0, k, h, rtt = 330, 0.26, 34, 150
    defs = ("<defs>" + "".join(
        f'<pattern id="h-{n}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        f'<rect width="8" height="8" fill="#fff"/><rect width="4" height="8" fill="{c}"/></pattern>'
        for n, c in (("w", MUTED), ("d", C[RAID]))) + "</defs>")
    body = [defs]

    def bar(y, segs, hatch=False, labels=None):
        x = x0
        for i, (ms, kind) in enumerate(segs):
            w = ms * k
            fill = (f"url(#h-{kind})" if hatch else (MUTED if kind == "w" else C[RAID]))
            body.append(rect(x, y, max(w, 1.5), h, fill, "#fff", 1, 0))
            if labels:
                body.append(text(x + w / 2, y + h + 17, labels[i], 14, 600, MUTED, "middle"))
            x += w
        return x

    def row(y, name, sub):
        body.append(text(20, y + 15, name, 19, 700, INK))
        body.append(text(20, y + 36, sub, 16, 400, MUTED))

    body.append(text(20, 26, "a typical upload, rounded from a production log", 17, 700, MUTED))
    y = 44
    row(y, "data file, ~350 KB", "FTP · 40% waiting")
    end = bar(y, [(600, "w"), (1700, "d"), (500, "w")],
              labels=["setup: 4 round trips", "data", "finish: 3"])
    body.append(text(end + 10, y + 24, "≈ 3 s", 19, 700, INK))
    y = 122
    row(y, "log file, ~5 KB", "FTP · almost all waiting")
    end = bar(y, [(800, "w"), (5, "d"), (500, "w")])
    body.append(text(end + 10, y + 24, "≈ 1.3 s", 19, 700, INK))

    body.append(line(20, 186, 1180, 186, GRID, 1))
    body.append(text(20, 214, f"computed with a {rtt} ms round trip", 17, 700, MUTED))
    y = 232
    row(y, "data file, ~350 KB", "CoAP, 1 KB blocks, one at a time")
    bar(y, [(3000, "w")], hatch=True)
    body.append(rect(1086, y - 4, 14, h + 8, "#fff", "none", 0))
    body.append(line(1086, y - 4, 1092, y + h + 4, INK, 2))
    body.append(line(1094, y - 4, 1100, y + h + 4, INK, 2))
    body.append(rect(1100, y, 20, h, "url(#h-w)", "#fff", 1, 0))
    body.append(text(1128, y + 24, "≈ 1 min", 19, 700, C[TW]))
    y = 300
    row(y, "data file, ~350 KB", "one connection kept open")
    end = bar(y, [(rtt, "w"), (1700, "d")], hatch=True)
    body.append(text(end + 10, y + 24, "≈ 2 s", 19, 700, INK))
    y = 368
    row(y, "log file, ~5 KB", "sent on that same connection")
    end = bar(y, [(rtt, "w"), (5, "d")], hatch=True)
    body.append(text(end + 10, y + 24, "≈ 0.2 s", 19, 700, INK))

    lx = 20
    for fill, label in [(MUTED, "waiting for a reply"), (C[RAID], "moving bytes"), ("url(#h-w)", "computed")]:
        body.append(rect(lx, 438, 22, 16, fill, MUTED if fill.startswith("url") else "none", 1, 2))
        body.append(text(lx + 30, 452, label, 16, 400, INK))
        lx += 70 + 9 * len(label)
    body.append(text(1180, 452, "time ≈ round trips × RTT + bytes ÷ rate", 18, 700, INK, "end"))
    return fig(1220, 470, body)

if __name__ == "__main__":
    figs = [("fleet_paths.svg", paths), ("fleet_loop.svg", loop), ("fleet_audiences.svg", audiences),
            ("fleet_signals.svg", signals), ("fleet_fanout.svg", fanout), ("fleet_brokers.svg", brokers),
            ("fleet_dashboard.svg", dashboard), ("fleet_scales.svg", scales), ("fleet_tracker.svg", tracker),
            ("fleet_trucks.svg", trucks), ("fleet_console.svg", console), ("fleet_acting.svg", acting),
            ("fleet_upload.svg", upload)]
    for name, f in figs:
        print(save(HERE, name, f()))
