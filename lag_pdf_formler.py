# -*- coding: utf-8 -*-
"""
Genererer en PDF som forklarer alle formlene, konstantene og symbolene
som brukes til aa beregne hydrogen-fjerningsraten i index.html.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# ---------------------------------------------------------------------------
# Hjelpefunksjoner for sidelayout
# ---------------------------------------------------------------------------

BLUE = "#0a4d8c"
DARK = "#1a1a1a"
GRAY = "#555555"


def new_page(pdf, title=None):
    fig = plt.figure(figsize=(8.27, 11.69))  # A4 staaende
    fig.subplots_adjust(left=0.08, right=0.94, top=0.94, bottom=0.06)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    if title:
        ax.text(0.08, 0.955, title, fontsize=17, fontweight="bold", color=BLUE,
                va="top", ha="left")
        ax.plot([0.08, 0.92], [0.935, 0.935], color=BLUE, lw=1.2)
    return fig, ax


def txt(ax, x, y, s, size=10.5, color=DARK, weight="normal", style="normal",
        family="sans-serif", ha="left"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            fontstyle=style, family=family, va="top", ha=ha, wrap=True)


def math(ax, x, y, s, size=13, color=DARK, ha="left"):
    ax.text(x, y, s, fontsize=size, color=color, va="top", ha=ha,
            usetex=False)


# ---------------------------------------------------------------------------
# PDF-innhold
# ---------------------------------------------------------------------------

pdf_path = "Hydrogen_fjerningsrate_formler.pdf"

with PdfPages(pdf_path) as pdf:

    # ===================== FORSIDE =====================
    fig, ax = new_page(pdf)
    ax.text(0.5, 0.72, "Hydrogen-fjerningsrate", fontsize=28, fontweight="bold",
            color=BLUE, ha="center", va="center")
    ax.text(0.5, 0.66, "Formler, konstanter og symbolforklaring", fontsize=15,
            color=GRAY, ha="center", va="center")
    ax.plot([0.2, 0.8], [0.62, 0.62], color=BLUE, lw=1.5)
    ax.text(0.5, 0.55,
            "Dokumentasjon av massetransport-modellen som brukes i\n"
            "avgassings-simuleringen (index.html, funksjonen calcRemovalRate).",
            fontsize=11, color=DARK, ha="center", va="center")
    ax.text(0.5, 0.30,
            "Modellen bygger paa:\n"
            "  -  Sieverts' lov (loeselighetslikevekt)\n"
            "  -  Higbie penetrasjonsteori (massetransport, 1935)\n"
            "  -  Mendelson-ligningen (bobleoppstigning)\n"
            "  -  Arrhenius-ligningen (diffusjon og loeselighet)",
            fontsize=11.5, color=DARK, ha="center", va="center")
    ax.text(0.5, 0.06, "Norsk Hydro ASA  -  Hydrogenfjerning visualisering",
            fontsize=9, color=GRAY, ha="center", va="center", style="italic")
    pdf.savefig(fig)
    plt.close(fig)

    # ===================== SIDE 1: Hovedformel =====================
    fig, ax = new_page(pdf, "1.  Hovedformelen for fjerningsraten")
    y = 0.90
    txt(ax, 0.08, y,
        "Fjerningsraten beregnes i funksjonen calcRemovalRate() i index.html. Den uttrykker hvor",
        size=10.5)
    txt(ax, 0.08, y-0.025,
        "raskt hydrogenkonsentrasjonen i smelten synker, drevet av massetransport til argonboblene:",
        size=10.5)

    # rammeboks rundt hovedformel
    ax.add_patch(plt.Rectangle((0.10, 0.735), 0.80, 0.075, fill=True,
                 facecolor="#eef4fb", edgecolor=BLUE, lw=1.3))
    math(ax, 0.5, 0.795,
         r"$\dfrac{dC_H}{dt} \;=\; -\,\dfrac{k_L \cdot A \cdot \Delta C}{V_{smelte}}$",
         size=20, ha="center")

    txt(ax, 0.08, 0.70, "I koden:", size=10.5, weight="bold")
    txt(ax, 0.10, 0.675,
        "removalRate = kL * totalArea * drivingForce / (params.meltMass / RHO_AL);",
        size=9.5, family="monospace", color="#333333")

    txt(ax, 0.08, 0.63, "Hva hver stoerrelse betyr:", size=11.5, weight="bold", color=BLUE)

    rows = [
        (r"$\dfrac{dC_H}{dt}$", "Fjerningsrate", "Endring i hydrogeninnhold per tid  [ml/100g per s]"),
        (r"$k_L$", "Massetransportkoeffisient", "Hvor lett H vandrer over grenseflaten  [m/s]"),
        (r"$A$", "Totalt grenseflateareal", "Samlet boble-overflate tilgjengelig for transport  [m^2]"),
        (r"$\Delta C$", "Drivkraft", "Konsentrasjonsforskjell melom smelte og boble  [ml/100g]"),
        (r"$V_{smelte}$", "Smeltevolum", "Volumet av flytende aluminium  [m^3]"),
        (r"$C_H$", "H-konsentrasjon", "Naavaerende hydrogeninnhold i smelten  [ml/100g]"),
    ]
    yy = 0.595
    for sym, name, desc in rows:
        math(ax, 0.12, yy, sym, size=14, ha="center")
        txt(ax, 0.20, yy+0.012, name, size=10.5, weight="bold")
        txt(ax, 0.20, yy-0.010, desc, size=9.5, color=GRAY)
        yy -= 0.055

    txt(ax, 0.08, 0.25,
        "Smeltevolumet finnes fra masse og tetthet:", size=10.5)
    math(ax, 0.5, 0.225, r"$V_{smelte} = \dfrac{m_{smelte}}{\rho_{Al}}$", size=16, ha="center")
    txt(ax, 0.08, 0.15,
        "Raten integreres over tid med Euler-metoden (linje 1319-1320 i index.html):", size=10.5)
    math(ax, 0.5, 0.115, r"$C_H(t+\Delta t) = C_H(t) - \text{rate}\cdot\Delta t$", size=15, ha="center")
    pdf.savefig(fig)
    plt.close(fig)

    # ===================== SIDE 2: Drivkraft og Sieverts =====================
    fig, ax = new_page(pdf, "2.  Drivkraften og Sieverts' lov")
    txt(ax, 0.08, 0.90,
        "Drivkraften er forskjellen mellom hydrogen loest i smelten og likevektsverdien mot boblen.",
        size=10.5)
    math(ax, 0.5, 0.845, r"$\Delta C = C_H - K_T\,\sqrt{P_{H_2,\,boble}}$", size=18, ha="center")

    txt(ax, 0.08, 0.78, "Sieverts' lov", size=12, weight="bold", color=BLUE)
    txt(ax, 0.08, 0.755,
        "Loeseligheten av toatomige gasser (H2) i metall er proporsjonal med kvadratroten av",
        size=10.5)
    txt(ax, 0.08, 0.780-0.045,
        "partialtrykket. Snudd om gir dette likevekts-partialtrykket over smelten:", size=10.5)
    math(ax, 0.5, 0.685, r"$S = K_T\sqrt{P_{H_2}} \;\;\Longrightarrow\;\; P_{H_2} = \left(\dfrac{S}{K_T}\right)^{2}$",
         size=16, ha="center")

    txt(ax, 0.08, 0.60, "Likevektskonstanten (temperaturavhengig, Arrhenius / van't Hoff)",
        size=12, weight="bold", color=BLUE)
    math(ax, 0.5, 0.555, r"$K_T = K_0 \cdot \exp\!\left(-\dfrac{\Delta H}{R\,T}\right)$", size=16, ha="center")

    txt(ax, 0.08, 0.47, "I koden (linje 1097-1103):", size=10.5, weight="bold")
    code = ("KT     = K0_liquid * Math.exp(-dH_liquid / (R * T_K));\n"
            "PH2_eq = Math.pow(h2_current / KT, 2);            // atm\n"
            "PH2_bubble_avg = PH2_eq * 0.2;                    // boble ~20% av likevekt\n"
            "drivingForce   = h2_current - KT * Math.sqrt(PH2_bubble_avg);")
    for i, line in enumerate(code.split("\n")):
        txt(ax, 0.10, 0.445 - i*0.028, line, size=9, family="monospace", color="#333333")

    txt(ax, 0.08, 0.31, "Faktoren 0,2 (20 %)", size=11.5, weight="bold", color=BLUE)
    txt(ax, 0.08, 0.285,
        "En fersk argonboble starter med PH2 = 0. Under den korte oppstigningen rekker den ikke",
        size=10.5)
    txt(ax, 0.08, 0.310-0.045,
        "aa naa likevekt med smelten. Modellen antar at boblen i snitt bare naar ~20 % av",
        size=10.5)
    txt(ax, 0.08, 0.310-0.070,
        "likevektstrykket. Lav verdi = stor drivkraft = effektiv avgassing.",
        size=10.5)

    txt(ax, 0.08, 0.17, "Symboler paa denne siden:", size=11, weight="bold", color=BLUE)
    syms = [
        (r"$S,\;C_H$", "Loest hydrogen i smelten  [ml/100g]"),
        (r"$P_{H_2}$", "Partialtrykk av H2  [atm]"),
        (r"$K_T$", "Sieverts-konstant ved temperatur T"),
        (r"$K_0$", "Pre-eksponentiell konstant"),
        (r"$\Delta H$", "Loesnings-entalpi  [J/mol]"),
    ]
    yy = 0.135
    for sym, desc in syms:
        math(ax, 0.13, yy, sym, size=12, ha="center")
        txt(ax, 0.24, yy, desc, size=9.5, color=GRAY)
        yy -= 0.028
    pdf.savefig(fig)
    plt.close(fig)

    # ===================== SIDE 3: Massetransport (Higbie) =====================
    fig, ax = new_page(pdf, "3.  Massetransportkoeffisient (Higbie 1935)")
    txt(ax, 0.08, 0.90,
        "Hvor raskt hydrogen krysser grenseflaten smelte/boble bestemmes av Higbie penetrasjonsteori:",
        size=10.5)
    ax.add_patch(plt.Rectangle((0.14, 0.795), 0.72, 0.065, fill=True,
                 facecolor="#eef4fb", edgecolor=BLUE, lw=1.2))
    math(ax, 0.5, 0.845, r"$k_L = 2\,\sqrt{\dfrac{D_H}{\pi\,t_c}}$", size=20, ha="center")

    txt(ax, 0.08, 0.75, "Kontakttiden t_c er tiden en smelte-'pakke' er i kontakt med boblen:", size=10.5)
    math(ax, 0.5, 0.71, r"$t_c = \dfrac{d}{v}$", size=16, ha="center")

    txt(ax, 0.08, 0.64, "Diffusiviteten til H i flytende Al (Arrhenius, Eichenauer et al.):",
        size=10.5)
    math(ax, 0.5, 0.60, r"$D_H = D_0 \cdot \exp\!\left(-\dfrac{E_a}{R\,T}\right)$", size=16, ha="center")

    txt(ax, 0.08, 0.52, "I koden (massTransferCoeff + diffusivityH):", size=10.5, weight="bold")
    code = ("D_H_Al      = D0 * Math.exp(-Ea / (R * T));   // D0=1.22e-4, Ea=54000\n"
            "contactTime = diameter / velocity;\n"
            "kL          = 2 * Math.sqrt(D_H_Al / (Math.PI * contactTime));")
    for i, line in enumerate(code.split("\n")):
        txt(ax, 0.10, 0.49 - i*0.028, line, size=9, family="monospace", color="#333333")

    txt(ax, 0.08, 0.37, "Symboler:", size=11, weight="bold", color=BLUE)
    syms = [
        (r"$k_L$", "Massetransportkoeffisient  [m/s]"),
        (r"$D_H$", "Diffusivitet av H i flytende Al  [m^2/s]"),
        (r"$D_0$", "Pre-eksponentiell diffusjonsfaktor = 1,22e-4 m^2/s"),
        (r"$E_a$", "Aktiveringsenergi for diffusjon = 54000 J/mol"),
        (r"$t_c$", "Kontakttid (boble mot smelte)  [s]"),
        (r"$d$", "Boblediameter  [m]"),
        (r"$v$", "Boblens stigehastighet  [m/s]"),
        (r"$\pi$", "3,14159..."),
    ]
    yy = 0.335
    for sym, desc in syms:
        math(ax, 0.13, yy, sym, size=12, ha="center")
        txt(ax, 0.24, yy, desc, size=9.5, color=GRAY)
        yy -= 0.030
    pdf.savefig(fig)
    plt.close(fig)

    # ===================== SIDE 4: Areal og bobler + Mendelson =====================
    fig, ax = new_page(pdf, "4.  Grenseflateareal og bobleoppstigning")
    txt(ax, 0.08, 0.90, "Totalt grenseflateareal", size=12, weight="bold", color=BLUE)
    txt(ax, 0.08, 0.875,
        "Samlet overflate = antall bobler per sekund x areal per boble x oppholdstid:", size=10.5)
    math(ax, 0.5, 0.83, r"$A = n_{bobler}\cdot A_{boble}\cdot t_{opphold}$", size=17, ha="center")

    txt(ax, 0.08, 0.76, "Antall bobler per sekund (argonstrom delt paa volum per boble):", size=10.5)
    math(ax, 0.5, 0.715,
         r"$n_{bobler} = \dfrac{Q}{V_{boble}}, \qquad V_{boble} = \dfrac{\pi}{6}d^{3}$",
         size=15, ha="center")

    txt(ax, 0.08, 0.64, "Areal per boble (kuleoverflate) og oppholdstid:", size=10.5)
    math(ax, 0.5, 0.60,
         r"$A_{boble} = \pi d^{2}, \qquad t_{opphold} = \dfrac{h}{v}$", size=15, ha="center")

    txt(ax, 0.08, 0.52, "Bobleoppstigning - Mendelson-ligningen", size=12, weight="bold", color=BLUE)
    txt(ax, 0.08, 0.495, "Stigehastigheten for mm-store bobler i flytende Al:", size=10.5)
    math(ax, 0.5, 0.45,
         r"$v = \sqrt{\dfrac{2\,\sigma}{\rho_{Al}\,d} + \dfrac{g\,d}{2}}$", size=17, ha="center")

    txt(ax, 0.08, 0.37, "I koden (linje 1114-1127, riseVelocity):", size=10.5, weight="bold")
    code = ("V_bubble     = (Math.PI/6) * Math.pow(bubbleDiam, 3);\n"
            "flowRate_m3s = flowRate / 1000 / 60;      // L/min -> m3/s\n"
            "nBubbles     = flowRate_m3s / V_bubble;\n"
            "A_bubble     = Math.PI * Math.pow(bubbleDiam, 2);\n"
            "residenceTime= depth / riseVelocity(bubbleDiam);\n"
            "totalArea    = nBubbles * A_bubble * residenceTime;")
    for i, line in enumerate(code.split("\n")):
        txt(ax, 0.10, 0.345 - i*0.026, line, size=9, family="monospace", color="#333333")

    txt(ax, 0.08, 0.16, "Symboler:", size=11, weight="bold", color=BLUE)
    syms = [
        (r"$Q$", "Argon-volumstrom  [m^3/s]  (input i L/min)"),
        (r"$V_{boble}$", "Volum per boble  [m^3]"),
        (r"$\sigma$", "Overflatespenning flytende Al = 0,87 N/m"),
        (r"$g$", "Tyngdeakselerasjon = 9,81 m/s^2"),
        (r"$h$", "Badedybde  [m]"),
    ]
    yy = 0.13
    for sym, desc in syms:
        math(ax, 0.13, yy, sym, size=12, ha="center")
        txt(ax, 0.26, yy, desc, size=9.5, color=GRAY)
        yy -= 0.028
    pdf.savefig(fig)
    plt.close(fig)

    # ===================== SIDE 5: Konstanttabell =====================
    fig, ax = new_page(pdf, "5.  Alle konstanter og tallverdier")
    txt(ax, 0.08, 0.90,
        "Tabellen samler alle faste tall og konstanter fra index.html med enhet og betydning.",
        size=10.5)

    header = ["Symbol / navn", "Verdi", "Enhet", "Betydning"]
    data = [
        ("R", "8,314", "J/(mol K)", "Universell gasskonstant"),
        ("K0_liquid", "419,8", "ml/100g", "Sieverts pre-faktor, fl. Al (Anyalebechi 2022)"),
        ("dH_liquid", "49534", "J/mol", "Loesnings-entalpi H i fl. Al"),
        ("K0_solid", "67,14", "ml/100g", "Sieverts pre-faktor, fast Al"),
        ("dH_solid", "57079", "J/mol", "Loesnings-entalpi H i fast Al"),
        ("D0", "1,22e-4", "m^2/s", "Pre-eksp. diffusjonsfaktor (Eichenauer)"),
        ("Ea", "54000", "J/mol", "Aktiveringsenergi for H-diffusjon"),
        ("RHO_AL", "2350", "kg/m^3", "Tetthet flytende aluminium"),
        ("GRAVITY (g)", "9,81", "m/s^2", "Tyngdeakselerasjon"),
        ("P_ATM", "101325", "Pa", "Atmosfaeretrykk"),
        ("sigma", "0,87", "N/m", "Overflatespenning flytende Al"),
        ("T_melt", "660,3", "grader C", "Smeltepunkt rent Al"),
        ("faktor 0,2", "0,2", "-", "Boble naar ~20% av likevektstrykk"),
    ]

    x_cols = [0.09, 0.32, 0.46, 0.60]
    y0 = 0.83
    # header
    for xc, htext in zip(x_cols, header):
        txt(ax, xc, y0, htext, size=10, weight="bold", color=BLUE)
    ax.plot([0.08, 0.92], [y0-0.012, y0-0.012], color=BLUE, lw=1)
    yy = y0 - 0.035
    for name, val, unit, desc in data:
        txt(ax, x_cols[0], yy, name, size=9.5, family="monospace")
        txt(ax, x_cols[1], yy, val, size=9.5)
        txt(ax, x_cols[2], yy, unit, size=9.5)
        txt(ax, x_cols[3], yy, desc, size=9)
        yy -= 0.038

    txt(ax, 0.08, yy-0.02, "Legeringskorreksjon (Sigworth eq. 4):", size=11, weight="bold", color=BLUE)
    math(ax, 0.5, yy-0.055,
         r"$C_{alloy} = 10^{\,-\sum e_i\,C_i \;-\;\sum r_i\,C_i^{2}}$", size=15, ha="center")
    txt(ax, 0.08, yy-0.11,
        "e-faktorer (positiv = senker loeselighet):  Si +0,03,  Mg -0,01,  Mn +0,06,",
        size=9.5, color=GRAY)
    txt(ax, 0.08, yy-0.135,
        "Cu +0,03,  Fe 0,  Zn +0,007,  Ti -0,14.   r-faktorer: Si -0,0008, Cu -0,0004.",
        size=9.5, color=GRAY)
    pdf.savefig(fig)
    plt.close(fig)

    # metadata
    d = pdf.infodict()
    d["Title"] = "Hydrogen-fjerningsrate - formler og konstanter"
    d["Author"] = "Norsk Hydro ASA"
    d["Subject"] = "Massetransport-modell for avgassing"

print("PDF laget:", pdf_path)
