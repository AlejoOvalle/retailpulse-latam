"""
RetailPulse Latam — Simulador P&L Ecommerce
Autor: Desarrollado para Alejandro Ovalle | aovalle.com
Versión: 2.0
Stack: Python + Streamlit + Plotly
Deploy: Streamlit Community Cloud (tier gratuito)

ARQUITECTURA v2.0
─────────────────
• Modo Gerente / Modo PyME (selector en sidebar)
• Full P&L por canal (Orgánico, Paid, Email, Marketplace)
• Punto de equilibrio dinámico
• Retención & Ciclo de Vida del Cliente (Cohort simplificado)
• Módulo Cyber opcional (herencia v1.0)
• Diagnósticos condicionales por área
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# 🔐 ACCESO — Edita el password aquí
# ─────────────────────────────────────────────────────────────────────────────
APP_PASSWORD = "retailpulse2025"   # ← CAMBIA ESTE VALOR

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="RetailPulse Latam | Simulador P&L Ecommerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 🔐 PANTALLA DE LOGIN
# ─────────────────────────────────────────────────────────────────────────────

def pantalla_login():
    st.markdown("""
    <style>
      .login-wrap {
        display: flex; flex-direction: column; align-items: center;
        justify-content: center; min-height: 70vh; text-align: center;
      }
      .login-logo {
        font-size: 2.2rem; font-weight: 700; color: #F1F5F9;
        letter-spacing: -0.02em; margin-bottom: 0.25rem;
      }
      .login-sub {
        font-size: 0.75rem; color: #38BDF8; letter-spacing: 0.15em;
        text-transform: uppercase; margin-bottom: 2.5rem;
      }
      .login-box {
        background: #0D1420; border: 1px solid #1A2535;
        border-radius: 12px; padding: 2rem 2.5rem;
        width: 100%; max-width: 380px;
      }
      .login-box label { color: #94A3B8 !important; font-size: 0.8rem !important; }
      .login-error {
        background: #450A0A; border: 1px solid #DC2626;
        border-radius: 6px; padding: 0.6rem 1rem;
        color: #F87171; font-size: 0.82rem; margin-top: 0.75rem;
      }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 0.9, 1])
    with col_c:
        st.markdown("""
        <div style="text-align:center; padding-top: 5vh;">
          <img src="data:image/png;base64,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"
               style="height:56px; width:auto; margin-bottom:1.25rem; border-radius:10px;"
               alt="aovalle.com logo" />
          <div style="font-size:2.2rem; font-weight:700; color:#F1F5F9;
                      letter-spacing:-0.02em; margin-bottom:0.2rem;">
            RetailPulse Latam | Chile
          </div>
          <div style="font-size:0.7rem; color:#38BDF8; letter-spacing:0.15em;
                      text-transform:uppercase; margin-bottom:2.5rem;">
            Simulador P&L · Ecommerce · v2.0 Beta
          </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style="background:#0D1420; border:1px solid #1A2535;
                        border-radius:12px; padding:1.75rem 2rem;">
              <div style="font-size:0.75rem; color:#64748B; font-weight:600;
                          letter-spacing:0.1em; text-transform:uppercase;
                          margin-bottom:1rem;">Acceso restringido</div>
            """, unsafe_allow_html=True)

            password_input = st.text_input(
                "Contraseña de acceso",
                type="password",
                placeholder="Ingresa el password...",
                label_visibility="collapsed",
            )
            st.markdown('<div style="height:1rem;"></div>', unsafe_allow_html=True)
            ingresar = st.button("Ingresar →", use_container_width=True, type="primary")

            st.markdown("</div>", unsafe_allow_html=True)

        if ingresar:
            if password_input == APP_PASSWORD:
                st.session_state["autenticado"] = True
                st.rerun()
            else:
                st.markdown("""
                <div class="login-error">
                  🔒 Password incorrecto. Intenta nuevamente.
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; margin-top:2rem;
                    font-size:0.65rem; color:#1E2D3D;">
          aovalle.com · Acceso exclusivo para clientes
        </div>
        """, unsafe_allow_html=True)


# ── Control de acceso ──
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    pantalla_login()
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,400&family=DM+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Roboto', sans-serif; }

  .stApp { background: #333333; color: #E8EDF5; }

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {
    background: #0B1017 !important;
    border-right: 1px solid #1A2535;
  }
  [data-testid="stSidebar"] .stMarkdown h3 {
    color: #38BDF8;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 1.6rem;
    margin-bottom: 0.3rem;
    padding-bottom: 0.35rem;
    border-bottom: 1px solid #1A2535;
  }
  .stSlider > div > div > div { background: #1A2535 !important; }
  .stSlider > div > div > div > div { background: #38BDF8 !important; }

  /* ── HEADINGS ── */
  h1 { color: #F1F5F9 !important; font-weight: 700 !important; letter-spacing: -0.025em !important; }
  h2 { color: #CBD5E1 !important; font-weight: 600 !important; }
  h3 { color: #94A3B8 !important; font-weight: 500 !important; }

  /* ── MODO BADGE ── */
  .modo-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
  }
  .modo-gerente { background: #0C2340; color: #38BDF8; border: 1px solid #1E3A5F; }
  .modo-pyme    { background: #1A2E0F; color: #86EFAC; border: 1px solid #2D4A1E; }

  /* ── METRIC CARDS ── */
  .metric-card {
    background: #0D1420;
    border: 1px solid #1A2535;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    position: relative;
    overflow: hidden;
    height: 100%;
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #38BDF8, #0284C7);
  }
  .metric-card.danger::before  { background: linear-gradient(90deg, #F87171, #DC2626); }
  .metric-card.warning::before { background: linear-gradient(90deg, #FBBF24, #D97706); }
  .metric-card.success::before { background: linear-gradient(90deg, #34D399, #059669); }
  .metric-card.purple::before  { background: linear-gradient(90deg, #C084FC, #9333EA); }
  .metric-card .label {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #475569; margin-bottom: 0.45rem;
  }
  .metric-card .value {
    font-family: 'DM Mono', monospace;
    font-size: 1.5rem; font-weight: 500; color: #F1F5F9; line-height: 1.1;
  }
  .metric-card .value.sm { font-size: 1.15rem; }
  .metric-card .sub {
    font-size: 0.72rem; color: #64748B; margin-top: 0.35rem; line-height: 1.4;
  }
  .metric-card .delta { font-size: 0.72rem; margin-top: 0.3rem; }
  .metric-card .delta.neg { color: #F87171; }
  .metric-card .delta.pos { color: #34D399; }

  /* ── SECTION TABS ── */
  .section-tab {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.5rem 1.1rem;
    border-radius: 6px 6px 0 0;
    font-size: 0.78rem; font-weight: 600;
    background: #0D1420; border: 1px solid #1A2535;
    border-bottom: none; color: #64748B;
  }
  .section-tab.active { background: #111827; color: #38BDF8; border-color: #38BDF8; }

  /* ── CANAL ROWS ── */
  .canal-row {
    background: #0D1420;
    border: 1px solid #1A2535;
    border-radius: 8px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.4rem;
    display: flex; align-items: center; gap: 1rem;
  }
  .canal-dot {
    width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
  }
  .canal-name { font-size: 0.8rem; font-weight: 600; color: #CBD5E1; min-width: 110px; }
  .canal-bar-bg {
    flex: 1; background: #1A2535; border-radius: 3px; height: 6px; position: relative;
  }
  .canal-bar-fill {
    position: absolute; left: 0; top: 0; height: 6px; border-radius: 3px;
  }
  .canal-val { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #94A3B8; min-width: 90px; text-align: right; }
  .canal-roas {
    font-family: 'DM Mono', monospace; font-size: 0.75rem;
    padding: 0.15rem 0.5rem; border-radius: 4px; min-width: 52px; text-align: center;
  }
  .roas-ok      { background: #052E16; color: #34D399; }
  .roas-warning { background: #451A03; color: #FBBF24; }
  .roas-danger  { background: #450A0A; color: #F87171; }

  /* ── P&L TABLE ── */
  .pnl-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
  .pnl-table td { padding: 0.55rem 0.75rem; border-bottom: 1px solid #1A2535; }
  .pnl-table tr:last-child td { border-bottom: none; }
  .pnl-table .pnl-label { color: #94A3B8; }
  .pnl-table .pnl-val { font-family: 'DM Mono', monospace; text-align: right; color: #E2E8F0; }
  .pnl-table .pnl-total td { border-top: 1px solid #38BDF8; padding-top: 0.7rem; }
  .pnl-table .pnl-total .pnl-label { color: #38BDF8; font-weight: 700; }
  .pnl-table .pnl-total .pnl-val   { color: #38BDF8; font-weight: 700; }
  .pnl-table .pnl-neg { color: #F87171 !important; }
  .pnl-table .pnl-pos { color: #34D399 !important; }
  .pnl-section td { background: #0B1017; color: #475569 !important;
    font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; padding-top: 0.9rem; }

  /* ── DIAGNOSIS BOX ── */
  .diag-box {
    background: #0D1420;
    border: 1px solid #DC2626; border-left: 4px solid #DC2626;
    border-radius: 8px; padding: 1.1rem 1.3rem; margin-top: 0.75rem;
  }
  .diag-box.warning { border-color: #D97706; border-left-color: #D97706; }
  .diag-box.ok      { border-color: #059669; border-left-color: #059669; }
  .diag-box.purple  { border-color: #9333EA; border-left-color: #9333EA; }
  .diag-title {
    font-size: 0.65rem; font-weight: 800; letter-spacing: 0.14em;
    text-transform: uppercase; margin-bottom: 0.5rem;
  }
  .diag-box .diag-title         { color: #F87171; }
  .diag-box.warning .diag-title { color: #FBBF24; }
  .diag-box.ok .diag-title      { color: #34D399; }
  .diag-box.purple .diag-title  { color: #C084FC; }
  .diag-body { font-size: 0.85rem; color: #94A3B8; line-height: 1.75; }

  /* ── EQUILIBRIO BAR ── */
  .eq-bar-bg {
    background: #1A2535; border-radius: 4px; height: 10px;
    position: relative; overflow: hidden; margin: 0.5rem 0;
  }
  .eq-bar-fill {
    position: absolute; left: 0; top: 0; height: 10px;
    border-radius: 4px; transition: width 0.3s;
  }
  .eq-marker {
    position: absolute; top: -3px; width: 2px; height: 16px;
    background: #F1F5F9;
  }

  /* ── DIVIDER ── */
  .sdiv { border: none; border-top: 1px solid #1A2535; margin: 1.75rem 0; }

  /* ── FOOTER ── */
  .footer-cta {
    background: linear-gradient(135deg, #0D1420 0%, #0C1E35 100%);
    border: 1px solid #1A2535; border-radius: 12px;
    padding: 1.75rem 2rem; text-align: center; margin-top: 2rem;
  }

  /* ── INPUTS ── */
  .stNumberInput input {
    background: #0D1420 !important; border: 1px solid #1A2535 !important;
    color: #E8EDF5 !important; font-family: 'DM Mono', monospace !important;
    border-radius: 6px !important;
  }
  div[data-testid="stExpander"] {
    background: #0D1420 !important; border: 1px solid #1A2535 !important;
    border-radius: 8px !important;
  }
  .streamlit-expanderHeader { color: #94A3B8 !important; }
  .stTabs [data-baseweb="tab-list"] { background: transparent; gap: 4px; }
  .stTabs [data-baseweb="tab"] {
    background: #0D1420 !important; border: 1px solid #1A2535 !important;
    color: #64748B !important; border-radius: 6px 6px 0 0 !important;
    font-size: 0.8rem !important; padding: 0.5rem 1rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: #111827 !important; color: #38BDF8 !important;
    border-color: #38BDF8 !important;
  }
  .stTabs [data-baseweb="tab-panel"] {
    background: #0D1420; border: 1px solid #1A2535;
    border-radius: 0 8px 8px 8px; padding: 1.25rem;
  }

  /* ── FONDO PRINCIPAL — forzar azul oscuro en todos los contenedores ── */
  .stApp,
  .stAppViewContainer,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stMainBlockContainer"],
  .main .block-container,
  section.main,
  .stMainBlockContainer {
    background-color: #080C14 !important;
    background: #080C14 !important;
  }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fmt_clp(v, decimals=1):
    if abs(v) >= 1_000_000_000:
        return f"${v/1_000_000_000:,.{decimals}f}B"
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:,.{decimals}f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:,.0f}K"
    return f"${v:,.0f}"

def fmt_pct(v, d=1): return f"{v*100:.{d}f}%"
def fmt_x(v, d=2):   return f"{v:.{d}f}x"

def mc(label, value, sub=None, delta=None, kind="default", sm=False):
    sub_html   = f'<div class="sub">{sub}</div>'  if sub   else ""
    val_cls    = "value sm" if sm else "value"
    delta_html = ""
    if delta is not None:
        cls   = "neg" if delta < 0 else "pos"
        arrow = "↓" if delta < 0 else "↑"
        delta_html = f'<div class="delta {cls}">{arrow} {fmt_clp(abs(delta))}</div>'
    return f"""
    <div class="metric-card {kind}">
        <div class="label">{label}</div>
        <div class="{val_cls}">{value}</div>
        {sub_html}{delta_html}
    </div>"""

THEME = dict(
    paper_bgcolor="#0c1320", plot_bgcolor="#0c1320",
    font=dict(family="DM Sans", color="#94A3B8", size=11),
    margin=dict(l=16, r=16, t=36, b=16),
)


# ─────────────────────────────────────────────────────────────────────────────
# MODELO MATEMÁTICO
# ─────────────────────────────────────────────────────────────────────────────

CANALES_DEF = {
    "Orgánico/SEO":   {"color": "#38BDF8", "dot": "#38BDF8"},
    "Paid Ads":       {"color": "#F87171", "dot": "#F87171"},
    "Email/CRM":      {"color": "#34D399", "dot": "#34D399"},
    "Marketplace":    {"color": "#FBBF24", "dot": "#FBBF24"},
    "Directo/Otros":  {"color": "#C084FC", "dot": "#C084FC"},
}

# Comisiones reales por marketplace chileno (rango típico, usamos punto medio)
MARKETPLACE_COMISIONES = {
    "Mercado Libre":    {"min": 13.0, "max": 17.0, "default": 15.0},
    "Falabella.com":    {"min": 15.0, "max": 20.0, "default": 17.5},
    "Lider (Walmart)":  {"min": 12.0, "max": 18.0, "default": 15.0},
    "Ripley":           {"min": 15.0, "max": 20.0, "default": 17.0},
    "Paris":            {"min": 15.0, "max": 18.0, "default": 16.5},
    "Personalizado":    {"min":  0.0, "max": 40.0, "default": 15.0},
}

# Eventos comerciales digitales Chile — multiplicadores reales
# Fuente: ACEC, IAB Chile, datos históricos CyberDay / Black Friday Chile
EVENTOS_CYBER_CL = {
    "CyberDay (Mayo)":       {"multiplicador": 4.0, "inflacion_cpc": 0.50, "mes": "Mayo"},
    "CyberDay (Octubre)":    {"multiplicador": 3.5, "inflacion_cpc": 0.45, "mes": "Octubre"},
    "Black Friday":          {"multiplicador": 3.0, "inflacion_cpc": 0.40, "mes": "Noviembre"},
    "Cyber Monday":          {"multiplicador": 2.5, "inflacion_cpc": 0.35, "mes": "Noviembre"},
    "Hot Sale Chile":        {"multiplicador": 2.8, "inflacion_cpc": 0.35, "mes": "Junio"},
    "Fiestas Patrias":       {"multiplicador": 2.2, "inflacion_cpc": 0.25, "mes": "Septiembre"},
    "Navidad / Año Nuevo":   {"multiplicador": 2.5, "inflacion_cpc": 0.30, "mes": "Diciembre"},
    "Día de la Madre":       {"multiplicador": 2.0, "inflacion_cpc": 0.20, "mes": "Mayo"},
    "Día del Padre":         {"multiplicador": 1.8, "inflacion_cpc": 0.15, "mes": "Junio"},
    "Personalizado":         {"multiplicador": 2.0, "inflacion_cpc": 0.25, "mes": "—"},
}

# Pasarelas de pago Chile — comisión % + cargo fijo (2025)
# Fuente: tarifarios públicos Transbank, Getnet, Kushki, Flow, Khipu
PASARELAS_CL = {
    "Webpay (Transbank)":  {"pct": 1.49, "fijo_clp":    0, "label": "1.49% (negociable volumen)"},
    "Getnet":              {"pct": 1.95, "fijo_clp":    0, "label": "~1.95%"},
    "Mercado Pago":        {"pct": 3.49, "fijo_clp":    0, "label": "3.49% tarjeta / 0% QR"},
    "Flow":                {"pct": 1.95, "fijo_clp":  150, "label": "1.95% + $150 CLP"},
    "Kushki":              {"pct": 2.20, "fijo_clp":    0, "label": "~2.20% (negociable)"},
    "Khipu":               {"pct": 1.40, "fijo_clp":    0, "label": "1.40% (transferencia)"},
    "PayPal":              {"pct": 3.99, "fijo_clp":  200, "label": "3.99% + $0.30 USD"},
    "Personalizado":       {"pct": 2.00, "fijo_clp":    0, "label": "Editable"},
}

def calcular_canal(trafico, cr, aov, cpc, margen_pct,
                   es_marketplace=False, comision_pct=0.0, nombre_mp=None,
                   inversion=0):
    """
    P&L completo de un canal individual.

    Lógica de costo de adquisición por tipo de canal:
    ─────────────────────────────────────────────────
    • Paid Ads:           gasto = trafico × cpc  (costo variable por clic)
    • Orgánico/SEO,
      Email/CRM,
      Directo/Otros:      gasto = inversion      (costo fijo mensual: agencia, plataforma)
    • Marketplace:        gasto = comision_pct × ingresos (% sobre venta)

    Esta distinción elimina el sesgo de aplicar CPC a canales sin costo por clic,
    alineado con los estándares de P&L multicanal (Google, HubSpot, Shopify).
    """
    pedidos      = trafico * cr
    ingresos     = pedidos * aov
    cogs         = ingresos * (1 - margen_pct)
    margen_bruto = ingresos * margen_pct

    if es_marketplace:
        comision_pagada = ingresos * comision_pct
        ingresos_netos  = ingresos - comision_pagada
        gasto_ads       = comision_pagada
        contribucion    = margen_bruto - comision_pagada
        roas            = ingresos / comision_pagada if comision_pagada > 0 else 0
        cac             = comision_pagada / pedidos  if pedidos > 0 else 0
    else:
        comision_pagada = 0.0
        ingresos_netos  = ingresos
        # Paid Ads → costo variable (CPC × tráfico)
        # Resto    → costo fijo mensual (inversión en canal)
        gasto_ads       = (trafico * cpc) if cpc > 0 else inversion
        contribucion    = margen_bruto - gasto_ads
        roas            = ingresos / gasto_ads if gasto_ads > 0 else 0
        cac             = gasto_ads / pedidos  if pedidos  > 0 else 0

    return dict(
        trafico=trafico, cr=cr, aov=aov, cpc=cpc, inversion=inversion,
        pedidos=pedidos, ingresos=ingresos, ingresos_netos=ingresos_netos,
        cogs=cogs, margen_bruto=margen_bruto,
        gasto_ads=gasto_ads, comision_pagada=comision_pagada,
        contribucion=contribucion, roas=roas, cac=cac,
        es_marketplace=es_marketplace, comision_pct=comision_pct,
        nombre_mp=nombre_mp,
    )

def calcular_pl_global(canales_data, costos_fijos, costo_logistica_unitario, tasa_devolucion):
    """Consolida el P&L completo desde los canales."""
    total_ingresos          = sum(c["ingresos"]         for c in canales_data.values())
    total_pedidos           = sum(c["pedidos"]           for c in canales_data.values())
    total_margen_bruto      = sum(c["margen_bruto"]      for c in canales_data.values())
    total_gasto_ads         = sum(c["gasto_ads"]         for c in canales_data.values()
                                  if not c.get("es_marketplace"))
    total_comisiones_mp     = sum(c["comision_pagada"]   for c in canales_data.values()
                                  if c.get("es_marketplace"))

    costo_logistica    = total_pedidos * costo_logistica_unitario
    devoluciones_netas = total_pedidos * tasa_devolucion * (
        total_ingresos / total_pedidos if total_pedidos > 0 else 0
    )
    # EBITDA separa ads y comisiones para transparencia en el P&L
    ebitda_operativo   = (total_margen_bruto
                          - total_gasto_ads
                          - total_comisiones_mp
                          - costo_logistica
                          - costos_fijos
                          - devoluciones_netas)

    total_costo_adquisicion = total_gasto_ads + total_comisiones_mp
    margen_contribucion = total_margen_bruto - total_costo_adquisicion
    punto_equilibrio_pedidos = (
        (costos_fijos + costo_logistica + devoluciones_netas) /
        ((total_ingresos - total_costo_adquisicion) / total_pedidos)
        if total_pedidos > 0 and total_ingresos > total_costo_adquisicion else 0
    )
    punto_equilibrio_ingresos = punto_equilibrio_pedidos * (
        total_ingresos / total_pedidos if total_pedidos > 0 else 0
    )

    ltv_promedio = (total_ingresos / total_pedidos if total_pedidos > 0 else 0) * 2.4
    cac_promedio = total_costo_adquisicion / total_pedidos if total_pedidos > 0 else 0
    ltv_cac      = ltv_promedio / cac_promedio if cac_promedio > 0 else 0
    roas_global  = total_ingresos / total_costo_adquisicion if total_costo_adquisicion > 0 else 0

    return dict(
        total_ingresos=total_ingresos,
        total_pedidos=total_pedidos,
        total_margen_bruto=total_margen_bruto,
        total_gasto_ads=total_gasto_ads,
        total_comisiones_mp=total_comisiones_mp,
        total_costo_adquisicion=total_costo_adquisicion,
        costo_logistica=costo_logistica,
        devoluciones_netas=devoluciones_netas,
        costos_fijos=costos_fijos,
        ebitda_operativo=ebitda_operativo,
        margen_contribucion=margen_contribucion,
        punto_equilibrio_pedidos=punto_equilibrio_pedidos,
        punto_equilibrio_ingresos=punto_equilibrio_ingresos,
        ltv_promedio=ltv_promedio,
        cac_promedio=cac_promedio,
        ltv_cac=ltv_cac,
        roas_global=roas_global,
        margen_neto_pct=ebitda_operativo / total_ingresos if total_ingresos > 0 else 0,
    )

def calcular_retencion(aov, frecuencia_anual, tasa_churn_mensual, cohorte_size, meses=12):
    """
    Modelo de cohorte simplificado mensual.
    Retorna lista mensual de: clientes activos, ingresos, LTV acumulado.
    """
    rows = []
    clientes = cohorte_size
    ltv_acum = 0
    for m in range(1, meses + 1):
        ing_mes  = clientes * (aov * frecuencia_anual / 12)
        ltv_acum += ing_mes / cohorte_size if cohorte_size > 0 else 0
        rows.append(dict(mes=m, clientes=clientes, ingresos=ing_mes, ltv_acum=ltv_acum))
        clientes *= (1 - tasa_churn_mensual)
    return rows

# ── ESCENARIOS CYBER (heredados v1.0) ──
def cyber_caida_pasarela(total_pedidos, total_ingresos, trafico_total, aov_promedio,
                         cr_promedio, cpc_promedio, hora_pico=True,
                         evento="CyberDay (Mayo)", pasarela="Webpay (Transbank)"):
    """
    Caída de pasarela durante evento digital chileno.
    El multiplicador de tráfico y la inflación CPC varían por evento.
    La comisión de la pasarela se pierde sobre los ingresos no procesados.
    """
    evento_data   = EVENTOS_CYBER_CL.get(evento, {"multiplicador": 4.0, "inflacion_cpc": 0.50})
    pasarela_data = PASARELAS_CL.get(pasarela, {"pct": 1.49, "fijo_clp": 0})
    multiplicador = evento_data["multiplicador"] if hora_pico else evento_data["multiplicador"] * 0.6
    tpm            = (trafico_total / (30 * 24 * 60)) * multiplicador
    afectados      = tpm * 30
    perdidos_bruto = afectados * cr_promedio
    perdidos_netos = perdidos_bruto * 0.85
    ingreso_perdido = perdidos_netos * aov_promedio
    ads_quemados    = afectados * cpc_promedio
    # Comisión pasarela que tampoco se cobra (ingresos no procesados)
    com_no_cobrada  = ingreso_perdido * (pasarela_data["pct"] / 100)
    return dict(
        ingreso_perdido=ingreso_perdido,
        ads_quemados=ads_quemados,
        com_no_cobrada=com_no_cobrada,
        costo_total=ingreso_perdido + ads_quemados,
        evento=evento, pasarela=pasarela,
        multiplicador=multiplicador,
    )

def cyber_logistica(total_pedidos, ltv_promedio, pct_regiones=0.38, costo_dev=8500):
    pedidos_reg = total_pedidos * pct_regiones
    reclamos_extra = pedidos_reg * 0.03
    cost_dev = reclamos_extra * costo_dev
    ingreso_cr = total_pedidos * 0.12 * (ltv_promedio / 2.4)
    ltv_riesgo = reclamos_extra * 0.60 * ltv_promedio
    return dict(costo_devoluciones=cost_dev, ingreso_perdido_cr=ingreso_cr,
                ltv_perdido=ltv_riesgo, costo_total=cost_dev + ingreso_cr)

def cyber_cac(total_ingresos, total_gasto_ads, total_pedidos, trafico_total,
              incremento_cpc_pct=0.50):
    """Inflación CAC con porcentaje real del evento seleccionado."""
    gasto_nuevo = total_gasto_ads * (1 + incremento_cpc_pct)
    roas_nuevo  = total_ingresos / gasto_nuevo if gasto_nuevo > 0 else 0
    costo_total = gasto_nuevo - total_gasto_ads
    return dict(gasto_nuevo=gasto_nuevo, roas_nuevo=roas_nuevo,
                costo_total=costo_total, incremento_pct=incremento_cpc_pct)


# ─────────────────────────────────────────────────────────────────────────────
# DIAGNÓSTICOS
# ─────────────────────────────────────────────────────────────────────────────

def diagnosticos_pl(pl, canales_data, modo):
    diags = []
    es_pyme = (modo == "PyME")

    # 1. EBITDA negativo
    if pl["ebitda_operativo"] < 0:
        if es_pyme:
            diags.append(dict(nivel="danger", titulo="🔴 Tu tienda está perdiendo dinero este mes",
                cuerpo=(f"Después de todos los costos, el negocio tiene un resultado de "
                        f"<strong>{fmt_clp(pl['ebitda_operativo'])}</strong>. "
                        f"Esto significa que por cada peso que entra, el negocio gasta más de lo que gana.<br><br>"
                        f"<strong>Qué revisar primero:</strong> Los costos fijos y el gasto en publicidad son las palancas más rápidas. "
                        f"Antes de invertir más en Ads, asegúrate de que cada venta sea rentable por sí sola."), cta=True))
        else:
            diags.append(dict(nivel="danger", titulo="🔴 EBITDA OPERATIVO NEGATIVO",
                cuerpo=(f"El resultado operativo es <strong>{fmt_clp(pl['ebitda_operativo'])}</strong>. "
                        f"La operación está destruyendo valor. La suma de costos fijos ({fmt_clp(pl['costos_fijos'])}), "
                        f"logística ({fmt_clp(pl['costo_logistica'])}) y costo de adquisición ({fmt_clp(pl['total_costo_adquisicion'])}) "
                        f"supera el margen bruto generado.<br><br>"
                        f"<strong>Lever inmediato:</strong> Auditar el mix de canales. "
                        f"Identificar cuál canal tiene contribución negativa y pausarlo es más urgente que optimizar campañas."), cta=True))

    # 2. LTV/CAC crítico
    if pl["ltv_cac"] < 2.0:
        if es_pyme:
            diags.append(dict(nivel="danger", titulo="🚨 Gastas demasiado para conseguir cada cliente",
                cuerpo=(f"Por cada peso que gastas en publicidad para traer un cliente, ese cliente te genera "
                        f"<strong>{fmt_x(pl['ltv_cac'])}</strong> veces ese valor en el tiempo. "
                        f"Lo mínimo saludable es 3 veces. Tu modelo de negocio necesita clientes que vuelvan a comprar.<br><br>"
                        f"<strong>Acción concreta:</strong> Implementa un programa simple de recompra: descuento en segunda compra, "
                        f"WhatsApp post-despacho, o email automático a los 15 días."), cta=True))
        else:
            diags.append(dict(nivel="danger", titulo="🚨 LTV/CAC POR DEBAJO DEL UMBRAL CRÍTICO (< 2x)",
                cuerpo=(f"Ratio LTV/CAC actual: <strong>{fmt_x(pl['ltv_cac'])}</strong>. "
                        f"Umbral de viabilidad mínima: 2.0x. Benchmark saludable LatAm: ≥ 3.0x. "
                        f"CAC promedio consolidado: <strong>{fmt_clp(pl['cac_promedio'])}</strong>.<br><br>"
                        f"<strong>Diagnóstico:</strong> El problema no es el canal de adquisición, es la frecuencia de recompra. "
                        f"Con frecuencia anual ≤ 1.5x, el LTV nunca alcanza a amortizar un CAC de performance marketing."), cta=True))
    elif pl["ltv_cac"] < 3.0:
        diags.append(dict(nivel="warning", titulo="⚠️ LTV/CAC EN ZONA DE ALERTA (2x–3x)",
            cuerpo=(f"Ratio <strong>{fmt_x(pl['ltv_cac'])}</strong>. "
                    f"Viable pero frágil: cualquier aumento de CPC o campaña de retención fallida destruye el margen.<br><br>"
                    f"<strong>Prioridad:</strong> Incrementar la frecuencia de recompra en 0.3x–0.5x antes de escalar inversión en Ads."), cta=True))

    # 3. Canal con ROAS < 1.5
    for nombre, canal in canales_data.items():
        if canal["gasto_ads"] > 0 and canal["roas"] < 1.5:
            diags.append(dict(nivel="danger",
                titulo=f"📉 Canal {nombre}: ROAS {canal['roas']:.2f}x — Destruyendo Margen",
                cuerpo=(f"El canal <strong>{nombre}</strong> genera <strong>{fmt_clp(canal['ingresos'])}</strong> en ingresos "
                        f"gastando <strong>{fmt_clp(canal['gasto_ads'])}</strong> en adquisición. "
                        f"Contribución neta: <strong>{fmt_clp(canal['contribucion'])}</strong>.<br><br>"
                        f"<strong>Decisión binaria:</strong> Pausar o redirigir el presupuesto hacia el canal de mayor ROAS "
                        f"hasta resolver la estructura de la campaña."), cta=True))

    # 4. Punto de equilibrio
    cobertura = pl["total_pedidos"] / pl["punto_equilibrio_pedidos"] if pl["punto_equilibrio_pedidos"] > 0 else 0
    if cobertura < 1.1:
        diags.append(dict(nivel="warning", titulo="⚡ OPERACIÓN CERCA DEL PUNTO DE EQUILIBRIO",
            cuerpo=(f"Estás operando al <strong>{cobertura*100:.0f}%</strong> del punto de equilibrio. "
                    f"Necesitas <strong>{pl['punto_equilibrio_pedidos']:,.0f} pedidos/mes</strong> para cubrir todos los costos. "
                    f"Tienes <strong>{pl['total_pedidos']:,.0f}</strong>. "
                    f"Un mes con menor demanda puede generar pérdidas operativas.<br><br>"
                    f"<strong>Colchón mínimo recomendado:</strong> Operar al 120%+ del punto de equilibrio antes de escalar."), cta=True))

    # 5. Margen neto
    if pl["margen_neto_pct"] > 0.12:
        diags.append(dict(nivel="ok", titulo="✅ MARGEN NETO SALUDABLE — Preparado para Escalar",
            cuerpo=(f"Margen neto sobre ventas: <strong>{pl['margen_neto_pct']*100:.1f}%</strong>. "
                    f"La operación es rentable y tiene capacidad de reinversión. "
                    f"El siguiente paso es identificar el canal con mejor LTV para escalar inversión de forma asimétrica."), cta=False))

    if not diags:
        diags.append(dict(nivel="ok", titulo="✅ MÉTRICAS EN RANGO OPERATIVO NORMAL",
            cuerpo="No se detectan alertas críticas con los parámetros actuales. Usa el módulo de Retención para identificar la próxima palanca de crecimiento.", cta=False))

    return diags


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────

def grafico_pl_waterfall(pl):
    # Construir dinámicamente según si hay comisiones marketplace
    tiene_mp = pl.get("total_comisiones_mp", 0) > 0
    labels = ["Ingresos Brutos", "COGS", "Gasto Ads"]
    vals   = [
        pl["total_ingresos"],
        -(pl["total_ingresos"] - pl["total_margen_bruto"]),
        -pl["total_gasto_ads"],
    ]
    if tiene_mp:
        labels.append("Comisiones MP")
        vals.append(-pl["total_comisiones_mp"])
    labels += ["Logística", "Devoluciones", "Costos Fijos", "EBITDA"]
    vals   += [
        -pl["costo_logistica"],
        -pl["devoluciones_netas"],
        -pl["costos_fijos"],
    ]
    ebitda = pl["ebitda_operativo"]
    measure = ["absolute"] + ["relative"] * (len(labels) - 2) + ["total"]
    vals.append(ebitda)
    base_colors = ["#38BDF8","#F87171","#F87171"]
    if tiene_mp:
        base_colors.append("#FBBF24")   # amarillo para comisiones MP
    base_colors += ["#FBBF24","#FBBF24","#FB923C"]
    colors_bar = base_colors + ["#34D399" if ebitda >= 0 else "#F87171"]
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=measure, x=labels, y=vals,
        connector=dict(line=dict(color="#1A2535", width=1)),
        increasing=dict(marker_color="#34D399"),
        decreasing=dict(marker_color="#F87171"),
        totals=dict(marker_color="#34D399" if ebitda >= 0 else "#F87171"),
        text=[fmt_clp(v) for v in vals], textposition="outside",
        textfont=dict(color="#CBD5E1", size=10),
    ))
    fig.update_layout(title=dict(text="P&L Cascada — De Ingresos a EBITDA", font=dict(size=13, color="#CBD5E1")),
                      showlegend=False, **THEME)
    fig.update_yaxes(gridcolor="#1A2535", zerolinecolor="#1A2535")
    fig.update_xaxes(gridcolor="#1A2535")
    return fig

def hex_rgba(hex_color, alpha=1.0):
    """Convierte #RRGGBB → rgba(r,g,b,a). Plotly no acepta hex de 8 dígitos."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def grafico_mix_canales(canales_data):
    nombres  = list(canales_data.keys())
    ingresos = [c["ingresos"] for c in canales_data.values()]
    contribs = [c["contribucion"] for c in canales_data.values()]
    colores  = [CANALES_DEF[n]["color"] for n in nombres]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Ingresos", x=nombres, y=ingresos,
                         marker_color=[hex_rgba(c, 0.5) for c in colores],
                         text=[fmt_clp(v) for v in ingresos], textposition="outside",
                         textfont=dict(size=10, color="#94A3B8")))
    fig.add_trace(go.Bar(name="Contribución Neta", x=nombres, y=contribs,
                         marker_color=colores,
                         text=[fmt_clp(v) for v in contribs], textposition="outside",
                         textfont=dict(size=10, color="#CBD5E1")))
    fig.update_layout(title=dict(text="Ingresos vs. Contribución por Canal", font=dict(size=13, color="#CBD5E1")),
                      barmode="group", legend=dict(font=dict(color="#94A3B8"), bgcolor="#0D1420"),
                      **THEME)
    fig.update_yaxes(gridcolor="#1A2535", zerolinecolor="#1A2535")
    fig.update_xaxes(gridcolor="#1A2535")
    return fig

def grafico_roas_canales(canales_data):
    nombres = list(canales_data.keys())
    roas    = [c["roas"] for c in canales_data.values()]
    colores = ["#34D399" if r >= 3 else "#FBBF24" if r >= 1.5 else "#F87171" for r in roas]
    fig = go.Figure(go.Bar(
        x=nombres, y=roas, marker_color=colores,
        text=[f"{r:.2f}x" for r in roas], textposition="outside",
        textfont=dict(size=11, color="#CBD5E1"),
    ))
    fig.add_hline(y=3.0, line_dash="dot", line_color="#34D399",
                  annotation_text="Óptimo ≥ 3x", annotation_font_color="#34D399", annotation_position="top right")
    fig.add_hline(y=1.5, line_dash="dot", line_color="#FBBF24",
                  annotation_text="Mínimo 1.5x", annotation_font_color="#FBBF24", annotation_position="bottom right")
    fig.update_layout(title=dict(text="ROAS por Canal", font=dict(size=13, color="#CBD5E1")),
                      showlegend=False, **THEME)
    fig.update_yaxes(gridcolor="#1A2535", zerolinecolor="#1A2535", title="ROAS", title_font=dict(color="#475569"))
    fig.update_xaxes(gridcolor="#1A2535")
    return fig

def grafico_retencion(cohorte_rows):
    df = pd.DataFrame(cohorte_rows)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["mes"], y=df["clientes"], mode="lines+markers", name="Clientes Activos",
        line=dict(color="#38BDF8", width=2), marker=dict(size=5),
        fill="tozeroy", fillcolor="rgba(56,189,248,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=df["mes"], y=df["ltv_acum"], mode="lines+markers", name="LTV Acumulado / Cliente",
        line=dict(color="#34D399", width=2, dash="dot"), marker=dict(size=5),
        yaxis="y2",
    ))
    fig.update_layout(
        title=dict(text="Cohorte: Retención de Clientes & LTV Acumulado (12 meses)", font=dict(size=13, color="#CBD5E1")),
        legend=dict(font=dict(color="#94A3B8"), bgcolor="#0D1420"),
        yaxis=dict(title="Clientes activos", gridcolor="#1A2535", color="#94A3B8"),
        yaxis2=dict(title="LTV acum. (CLP)", overlaying="y", side="right", color="#34D399", gridcolor="rgba(0,0,0,0)"),
        **THEME,
    )
    return fig

def grafico_waterfall_cyber(pl, cyber_a, cyber_b, cyber_c, activos):
    ea = cyber_a if activos[0] else {"ingreso_perdido": 0, "ads_quemados": 0, "costo_total": 0}
    eb = cyber_b if activos[1] else {"costo_total": 0, "ingreso_perdido_cr": 0}
    ec = cyber_c if activos[2] else {"costo_total": 0}
    vals   = [pl["total_ingresos"], -ea["costo_total"], -eb["costo_total"], -ec["costo_total"]]
    labels = ["Ingresos Base", "Caída Pasarela", "Fricción Logística", "Inflación CAC"]
    fig = go.Figure(go.Waterfall(
        orientation="v", measure=["absolute","relative","relative","relative"],
        x=labels, y=vals,
        connector=dict(line=dict(color="#1A2535", width=1)),
        decreasing=dict(marker_color="#F87171"),
        totals=dict(marker_color="#38BDF8"),
        text=[fmt_clp(v) for v in vals], textposition="outside",
        textfont=dict(color="#CBD5E1", size=10),
    ))
    fig.update_layout(title=dict(text="Impacto Cyber sobre Ingresos Base", font=dict(size=13, color="#CBD5E1")),
                      showlegend=False, **THEME)
    fig.update_yaxes(gridcolor="#1A2535", zerolinecolor="#1A2535")
    return fig

def grafico_equilibrio(pl):
    pe_ing  = pl["punto_equilibrio_ingresos"]
    ing_act = pl["total_ingresos"]
    maximo  = max(pe_ing, ing_act) * 1.3
    pct_pe  = min(pe_ing / maximo, 1.0)
    pct_act = min(ing_act / maximo, 1.0)
    color   = "#34D399" if ing_act >= pe_ing * 1.1 else "#FBBF24" if ing_act >= pe_ing else "#F87171"
    return pct_pe, pct_act, color


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding:0.9rem 0 0.4rem 0;">
    <img src="data:image/png;base64,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"
               style="height:56px; width:auto; margin-bottom:1.25rem; border-radius:10px;"
               alt="aovalle.com logo" />
      <div style="font-size:1.05rem;font-weight:700;color:#F1F5F9;letter-spacing:-0.01em;">
        📊 RetailPulse Latam | Chile
      </div>
      <div style="font-size:0.65rem;color:#38BDF8;letter-spacing:0.14em;text-transform:uppercase;margin-top:0.15rem;">
        Simulador P&L · Ecommerce · v2.0 Beta
      </div>
    </div>
    <hr style="border:none;border-top:1px solid #1A2535;margin:0.5rem 0 0.3rem 0;"/>
    """, unsafe_allow_html=True)

    modo = st.radio("Modo de uso", ["Gerente Ecommerce", "Dueño PyME"],
                    horizontal=True, label_visibility="collapsed")
    es_pyme = (modo == "Dueño PyME")

    if es_pyme:
        st.markdown('<div class="modo-badge modo-pyme">🏪 Modo PyME — Lenguaje simple</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="modo-badge modo-gerente">💼 Modo Gerente — Métricas técnicas</div>', unsafe_allow_html=True)

    # ── CANALES ──
    st.markdown("### 📡 Canales de Venta")

    canales_activos = {}
    canales_input   = {}

    nombres_canales = list(CANALES_DEF.keys())

    # Valores default por canal
    # CANALES:
    # - Paid Ads: usa CPC (costo por clic) — gasto variable ligado al tráfico
    # - Orgánico/SEO, Email/CRM, Directo/Otros: usa inversión mensual fija
    #   (agencia SEO, plataforma de email, etc.) — costo fijo por canal
    # - Marketplace: comisión % sobre venta (lógica propia)
    defaults = {
        "Orgánico/SEO":  dict(tr=15000, cr=2.2, aov=58000, cpc=0, inversion=350000),
        "Paid Ads":      dict(tr=20000, cr=1.6, aov=65000, cpc=190, inversion=0),
        "Email/CRM":     dict(tr=8000,  cr=3.1, aov=72000, cpc=0,   inversion=80000),
        "Marketplace":   dict(tr=5000,  cr=4.5, aov=42000, cpc=0,   inversion=0),
        "Directo/Otros": dict(tr=4000,  cr=1.9, aov=55000, cpc=0,   inversion=0),
    }

    label_tr       = "Visitas/mes"          if es_pyme else "Tráfico mensual"
    label_cr       = "% que compran"        if es_pyme else "CR (%)"
    label_aov      = "Precio promedio"      if es_pyme else "AOV (CLP)"
    label_cpc      = "Costo por clic (CLP)" if es_pyme else "CPC (CLP)"
    label_inversion= "Inversión mensual en canal (CLP)" if es_pyme else "Inversión mensual canal (CLP)"

    for nombre in nombres_canales:
        d = defaults[nombre]
        with st.expander(f"{nombre}", expanded=(nombre in ["Orgánico/SEO","Paid Ads"])):
            activo = st.checkbox("Incluir canal", value=(nombre in ["Orgánico/SEO","Paid Ads","Email/CRM"]),
                                 key=f"act_{nombre}")
            if activo:
                tr  = st.number_input(label_tr, 0, 500000, d["tr"], 1000, key=f"tr_{nombre}")
                cr  = st.slider(label_cr, 0.1, 10.0, d["cr"], 0.1, key=f"cr_{nombre}",
                                format="%.1f%%") / 100
                aov = st.number_input(label_aov, 1000, 500000, d["aov"], 1000, key=f"aov_{nombre}")

                if nombre == "Marketplace":
                    # ── Selector de marketplace chileno ──
                    mp_nombres = list(MARKETPLACE_COMISIONES.keys())
                    mp_sel = st.selectbox(
                        "Marketplace" if not es_pyme else "¿En qué tienda vendes?",
                        mp_nombres, index=0, key="mp_selector"
                    )
                    mp_data   = MARKETPLACE_COMISIONES[mp_sel]
                    mp_com_def = mp_data["default"]
                    # Mostrar rango referencial
                    st.markdown(
                        f'<div style="font-size:0.68rem;color:#64748B;margin:-0.3rem 0 0.4rem 0;">'
                        f'Comisión típica: {mp_data["min"]:.0f}% – {mp_data["max"]:.0f}%</div>',
                        unsafe_allow_html=True
                    )
                    comision_mp = st.slider(
                        "Comisión del marketplace (%)" if not es_pyme else "% que cobra la plataforma",
                        mp_data["min"], mp_data["max"], mp_com_def, 0.5,
                        format="%.1f%%", key="mp_comision"
                    ) / 100
                    canales_activos[nombre] = True
                    canales_input[nombre]   = dict(
                        tr=tr, cr=cr, aov=aov, cpc=0,
                        es_marketplace=True,
                        comision_pct=comision_mp,
                        nombre_mp=mp_sel,
                    )
                else:
                    if nombre == "Paid Ads":
                        # Paid Ads: CPC variable ligado al volumen de tráfico
                        cpc = st.number_input(label_cpc, 0, 5000, d["cpc"], 10, key=f"cpc_{nombre}")
                        inversion = 0
                        st.markdown(
                            '<div style="font-size:0.68rem;color:#64748B;margin:-0.3rem 0 0.4rem 0;">'
                            'Costo variable · Se calcula como Tráfico × CPC</div>',
                            unsafe_allow_html=True
                        )
                    else:
                        # Orgánico/SEO, Email/CRM, Directo/Otros:
                        # Inversión mensual fija (agencia, plataforma, retainer)
                        # No hay costo por clic — el tráfico no tiene costo variable unitario
                        inversion = st.number_input(
                            label_inversion, 0, 50_000_000,
                            d.get("inversion", 0), 50000,
                            key=f"inv_{nombre}"
                        )
                        cpc = 0
                        st.markdown(
                            '<div style="font-size:0.68rem;color:#64748B;margin:-0.3rem 0 0.4rem 0;">'
                            'Costo fijo mensual · Incluye agencia SEO, plataforma email, etc.</div>',
                            unsafe_allow_html=True
                        )
                    canales_activos[nombre] = True
                    canales_input[nombre]   = dict(
                        tr=tr, cr=cr, aov=aov, cpc=cpc,
                        inversion=inversion,
                        es_marketplace=False, comision_pct=0.0, nombre_mp=None
                    )

    # ── COSTOS ──
    st.markdown("### 🏗️ Estructura de Costos")

    margen_bruto_global = st.slider(
        "Margen bruto promedio (%)" if not es_pyme else "Ganancia por cada venta (%)",
        5.0, 80.0, 38.0, 1.0, format="%.0f%%") / 100

    costos_fijos = st.number_input(
        "Costos fijos mensuales (CLP)" if not es_pyme else "Gastos fijos del negocio (CLP)",
        0, 100_000_000, 3_500_000, 100_000)

    costo_logistica = st.number_input(
        "Costo logístico por pedido (CLP)" if not es_pyme else "Envío por pedido (CLP)",
        0, 30_000, 4_200, 100)

    tasa_devolucion = st.slider(
        "Tasa de devolución (%)" if not es_pyme else "% pedidos devueltos",
        0.0, 15.0, 3.5, 0.5, format="%.1f%%") / 100

    # ── RETENCIÓN ──
    st.markdown("### 🔁 Retención & Ciclo de Vida")

    frecuencia_anual = st.slider(
        "Recompras por cliente / año" if not es_pyme else "Veces que vuelve a comprar al año",
        1.0, 12.0, 2.4, 0.1)

    churn_mensual = st.slider(
        "Churn mensual (%)" if not es_pyme else "% clientes que no vuelven por mes",
        1.0, 30.0, 8.0, 0.5, format="%.1f%%") / 100

    cohorte_size = st.number_input(
        "Nuevos clientes por mes" if not es_pyme else "Clientes nuevos por mes",
        10, 50000, 500, 50)

    # ── CYBER ──
    st.markdown("### ⚡ Módulo Eventos Digitales")
    activar_cyber = st.checkbox("Activar escenarios de evento", value=False)
    cyber_a_on = cyber_b_on = cyber_c_on = False
    evento_cyber_sel = "CyberDay (Mayo)"
    pasarela_sel     = "Webpay (Transbank)"
    if activar_cyber:
        evento_cyber_sel = st.selectbox(
            "Evento a simular",
            list(EVENTOS_CYBER_CL.keys()), index=0,
            help="Cada evento tiene su propio multiplicador de tráfico e inflación de CPC"
        )
        ev = EVENTOS_CYBER_CL[evento_cyber_sel]
        st.markdown(
            f'<div style="font-size:0.68rem;color:#64748B;margin:-0.3rem 0 0.6rem 0;">'
            f'Tráfico ×{ev["multiplicador"]} · CPC +{ev["inflacion_cpc"]*100:.0f}% · {ev["mes"]}</div>',
            unsafe_allow_html=True
        )
        pasarela_sel = st.selectbox(
            "Pasarela principal",
            list(PASARELAS_CL.keys()), index=0,
            help="Afecta el cálculo de ingresos perdidos por caída de checkout"
        )
        pas = PASARELAS_CL[pasarela_sel]
        st.markdown(
            f'<div style="font-size:0.68rem;color:#64748B;margin:-0.3rem 0 0.6rem 0;">'
            f'Comisión: {pas["label"]}</div>',
            unsafe_allow_html=True
        )
        cyber_a_on = st.checkbox("A: Caída pasarela (30 min pico)", value=True)
        cyber_b_on = st.checkbox("B: Fricción logística regiones",  value=True)
        cyber_c_on = st.checkbox("C: Inflación CAC (saturación subasta)", value=True)

    st.markdown("""
    <hr style="border:none;border-top:1px solid #1A2535;margin:1.2rem 0 0.8rem 0;"/>
    <div style="font-size:0.62rem;color:#2D3748;text-align:center;line-height:1.6;">
      RetailPulse Latam v2.0 · Chile<br>
      <a href="https://www.aovalle.com" style="color:#38BDF8;text-decoration:none;">aovalle.com</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS PRINCIPALES
# ─────────────────────────────────────────────────────────────────────────────

if not canales_input:
    st.warning("Activa al menos un canal de venta en el sidebar para comenzar.")
    st.stop()

# P&L por canal
canales_data = {
    nombre: calcular_canal(
        v["tr"], v["cr"], v["aov"], v["cpc"], margen_bruto_global,
        es_marketplace=v.get("es_marketplace", False),
        comision_pct=v.get("comision_pct", 0.0),
        nombre_mp=v.get("nombre_mp"),
        inversion=v.get("inversion", 0),
    )
    for nombre, v in canales_input.items()
}

# P&L global
pl = calcular_pl_global(canales_data, costos_fijos, costo_logistica, tasa_devolucion)

# Retención
cohorte_rows = calcular_retencion(
    pl["total_ingresos"] / pl["total_pedidos"] if pl["total_pedidos"] > 0 else 50000,
    frecuencia_anual, churn_mensual, cohorte_size
)
ltv_12m = cohorte_rows[-1]["ltv_acum"] if cohorte_rows else 0

# Cyber
if activar_cyber and pl["total_pedidos"] > 0:
    aov_p    = pl["total_ingresos"] / pl["total_pedidos"]
    tr_tot   = sum(v["tr"] for v in canales_input.values())
    cpc_p    = pl["total_gasto_ads"] / tr_tot if tr_tot > 0 else 0
    cr_p     = pl["total_pedidos"] / tr_tot    if tr_tot > 0 else 0
    inflacion_cpc = EVENTOS_CYBER_CL[evento_cyber_sel]["inflacion_cpc"]
    cyber_a = cyber_caida_pasarela(
        pl["total_pedidos"], pl["total_ingresos"], tr_tot, aov_p, cr_p, cpc_p,
        evento=evento_cyber_sel, pasarela=pasarela_sel
    )
    cyber_b = cyber_logistica(pl["total_pedidos"], pl["ltv_promedio"])
    cyber_c = cyber_cac(pl["total_ingresos"], pl["total_gasto_ads"],
                        pl["total_pedidos"], tr_tot,
                        incremento_cpc_pct=inflacion_cpc)
else:
    evento_cyber_sel = "CyberDay (Mayo)"
    pasarela_sel     = "Webpay (Transbank)"
    cyber_a = cyber_b = cyber_c = dict(costo_total=0, ingreso_perdido=0, ads_quemados=0,
                                        ingreso_perdido_cr=0, ltv_perdido=0, gasto_nuevo=0,
                                        roas_nuevo=0, com_no_cobrada=0, multiplicador=0,
                                        incremento_pct=0)

cyber_perdida_total = (
    (cyber_a["costo_total"] if cyber_a_on else 0) +
    (cyber_b["costo_total"] if cyber_b_on else 0) +
    (cyber_c["costo_total"] if cyber_c_on else 0)
)

# Diagnósticos
diags = diagnosticos_pl(pl, canales_data, modo)
pct_pe, pct_act, color_eq = grafico_equilibrio(pl)


# ─────────────────────────────────────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

# ── HEADER ──
badge_html = (
    '<span style="background:#1A2E0F;color:#86EFAC;border:1px solid #2D4A1E;'
    'padding:0.2rem 0.7rem;border-radius:999px;font-size:0.65rem;font-weight:700;'
    'letter-spacing:0.1em;text-transform:uppercase;margin-left:0.75rem;">🏪 Modo PyME</span>'
    if es_pyme else
    '<span style="background:#0C2340;color:#38BDF8;border:1px solid #1E3A5F;'
    'padding:0.2rem 0.7rem;border-radius:999px;font-size:0.65rem;font-weight:700;'
    'letter-spacing:0.1em;text-transform:uppercase;margin-left:0.75rem;">💼 Modo Gerente</span>'
)

titulo = "Simulador P&L de tu Tienda Online" if es_pyme else "Simulador Full P&L Ecommerce"
subtitulo = "Visualiza cuánto gana tu negocio, dónde se va el dinero y cuándo empiezas a ser rentable." if es_pyme else "P&L multicanal · Punto de equilibrio · Retención · Ciclo de vida · Módulo Cyber · Mercado Chileno · CLP"

st.markdown(f"""
<div style="margin-bottom:1.75rem;">
  <div style="display:flex;align-items:center;flex-wrap:wrap;gap:0.5rem;">
    <h1 style="font-size:1.85rem;margin:0;">{titulo}</h1>
    {badge_html}
  </div>
  <p style="color:#475569;font-size:0.85rem;margin:0.4rem 0 0 0;">{subtitulo}</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS PRINCIPALES
# ══════════════════════════════════════════════════════════════════════════════

tab_pl, tab_canales, tab_retencion, tab_cyber = st.tabs([
    "📋 P&L Global",
    "📡 Canales",
    "🔁 Retención & LTV",
    "⚡ Módulo Cyber",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — P&L GLOBAL
# ─────────────────────────────────────────────────────────────────────────────

with tab_pl:

    # KPIs fila 1
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(mc(
            "Ingresos Mensuales" if es_pyme else "GMV Mensual",
            fmt_clp(pl["total_ingresos"]),
            sub=f"{pl['total_pedidos']:,.0f} pedidos"
        ), unsafe_allow_html=True)
    with k2:
        mb_pct = pl["total_margen_bruto"] / pl["total_ingresos"] if pl["total_ingresos"] > 0 else 0
        st.markdown(mc(
            "Ganancia Bruta" if es_pyme else "Margen Bruto",
            fmt_clp(pl["total_margen_bruto"]),
            sub=f"{mb_pct*100:.1f}% sobre ingresos",
        ), unsafe_allow_html=True)
    with k3:
        ebitda_kind = "success" if pl["ebitda_operativo"] > 0 else "danger"
        st.markdown(mc(
            "Resultado del Negocio" if es_pyme else "EBITDA Operativo",
            fmt_clp(pl["ebitda_operativo"]),
            sub=f"{pl['margen_neto_pct']*100:.1f}% margen neto",
            kind=ebitda_kind,
        ), unsafe_allow_html=True)
    with k4:
        roas_kind = "success" if pl["roas_global"] >= 3 else "warning" if pl["roas_global"] >= 1.5 else "danger"
        st.markdown(mc(
            "Rentabilidad de Ads" if es_pyme else "ROAS Global",
            fmt_x(pl["roas_global"]),
            sub=f"Gasto ads: {fmt_clp(pl['total_gasto_ads'])}",
            kind=roas_kind,
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    # KPIs fila 2
    k5, k6, k7, k8 = st.columns(4)
    with k5:
        ltv_kind = "success" if pl["ltv_cac"] >= 3 else "warning" if pl["ltv_cac"] >= 2 else "danger"
        st.markdown(mc(
            "Por cuánto recuperas cada cliente" if es_pyme else "LTV / CAC",
            fmt_x(pl["ltv_cac"]),
            sub=f"LTV {fmt_clp(pl['ltv_promedio'])}  ·  CAC {fmt_clp(pl['cac_promedio'])}",
            kind=ltv_kind,
        ), unsafe_allow_html=True)
    with k6:
        st.markdown(mc(
            "Cuánto te cuesta cada envío" if es_pyme else "Costo Logístico Total",
            fmt_clp(pl["costo_logistica"]),
            sub=f"${costo_logistica:,}/pedido · {pl['total_pedidos']:,.0f} envíos",
        ), unsafe_allow_html=True)
    with k7:
        st.markdown(mc(
            "Ventas mínimas para no perder" if es_pyme else "Punto de Equilibrio (Ingresos)",
            fmt_clp(pl["punto_equilibrio_ingresos"]),
            sub=f"{pl['punto_equilibrio_pedidos']:,.0f} pedidos mínimos",
        ), unsafe_allow_html=True)
    with k8:
        cobertura_pe = pl["total_pedidos"] / pl["punto_equilibrio_pedidos"] if pl["punto_equilibrio_pedidos"] > 0 else 0
        pe_kind = "success" if cobertura_pe >= 1.2 else "warning" if cobertura_pe >= 1.0 else "danger"
        st.markdown(mc(
            "Qué tan lejos estás de perder" if es_pyme else "Cobertura del Punto de Equilibrio",
            f"{cobertura_pe*100:.0f}%",
            sub="≥120% = zona segura",
            kind=pe_kind,
        ), unsafe_allow_html=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # ── PUNTO DE EQUILIBRIO VISUAL ──
    label_pe = "¿Cuánto necesitas vender para no perder dinero?" if es_pyme else "Punto de Equilibrio — Posición Actual"
    st.markdown(f"#### {label_pe}")

    dist_pe  = pl["total_ingresos"] - pl["punto_equilibrio_ingresos"]
    color_text = "#34D399" if dist_pe >= 0 else "#F87171"
    signo      = "por encima" if dist_pe >= 0 else "por debajo"

    st.markdown(f"""
    <div style="background:#0D1420;border:1px solid #1A2535;border-radius:10px;padding:1.2rem 1.5rem;margin-bottom:1rem;">
      <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:0.6rem;">
        <span style="font-size:0.72rem;color:#475569;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;">
          Ingresos actuales vs. punto de equilibrio
        </span>
        <span style="font-family:'DM Mono',monospace;font-size:0.85rem;color:{color_text};">
          {fmt_clp(abs(dist_pe))} {signo} del equilibrio
        </span>
      </div>
      <div class="eq-bar-bg">
        <div class="eq-bar-fill" style="width:{pct_act*100:.1f}%;background:{color_text};"></div>
        <div class="eq-marker" style="left:{pct_pe*100:.1f}%;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;margin-top:0.4rem;">
        <span style="font-size:0.7rem;color:#475569;">$0</span>
        <span style="font-size:0.7rem;color:#94A3B8;">
          PE: {fmt_clp(pl['punto_equilibrio_ingresos'])}
          <span style="color:#475569"> · </span>
          Actual: <span style="color:{color_text};">{fmt_clp(pl['total_ingresos'])}</span>
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # ── P&L TABLA + WATERFALL ──
    pl_col, wf_col = st.columns([1, 1.6])

    with pl_col:
        st.markdown("#### Estado de Resultados" if not es_pyme else "#### Resumen del Negocio")
        margen_contribucion_pct = pl["margen_contribucion"] / pl["total_ingresos"] if pl["total_ingresos"] > 0 else 0
        neg_cls = lambda v: "pnl-neg" if v < 0 else "pnl-pos" if v > 0 else ""
        # Fila de comisiones marketplace (condicional)
        mp_row_html = (
            f'<tr><td class="pnl-label">Comisiones Marketplace</td>'
            f'<td class="pnl-val pnl-neg">−{fmt_clp(pl["total_comisiones_mp"])}</td></tr>'
        ) if pl.get("total_comisiones_mp", 0) > 0 else ""

        st.markdown(f"""
        <table class="pnl-table">
          <tr class="pnl-section"><td colspan="2">INGRESOS</td></tr>
          <tr><td class="pnl-label">Ventas brutas</td>
              <td class="pnl-val">{fmt_clp(pl['total_ingresos'])}</td></tr>
          <tr><td class="pnl-label">Devoluciones</td>
              <td class="pnl-val pnl-neg">−{fmt_clp(pl['devoluciones_netas'])}</td></tr>

          <tr class="pnl-section"><td colspan="2">COSTOS VARIABLES</td></tr>
          <tr><td class="pnl-label">Costo mercadería (COGS)</td>
              <td class="pnl-val pnl-neg">−{fmt_clp(pl['total_ingresos'] - pl['total_margen_bruto'])}</td></tr>
          <tr><td class="pnl-label">Logística & despacho</td>
              <td class="pnl-val pnl-neg">−{fmt_clp(pl['costo_logistica'])}</td></tr>
          <tr><td class="pnl-label">Gasto en Ads</td>
              <td class="pnl-val pnl-neg">−{fmt_clp(pl['total_gasto_ads'])}</td></tr>
          {mp_row_html}

          <tr class="pnl-total">
            <td class="pnl-label">Margen de Contribución</td>
            <td class="pnl-val {neg_cls(pl['margen_contribucion'])}">{fmt_clp(pl['margen_contribucion'])}</td>
          </tr>
          <tr><td class="pnl-label" style="font-size:0.72rem;color:#475569;">
            % sobre ingresos</td>
            <td class="pnl-val" style="font-size:0.72rem;color:#64748B;">{margen_contribucion_pct*100:.1f}%</td>
          </tr>

          <tr class="pnl-section"><td colspan="2">COSTOS FIJOS</td></tr>
          <tr><td class="pnl-label">Plataforma & operación</td>
              <td class="pnl-val pnl-neg">−{fmt_clp(pl['costos_fijos'])}</td></tr>

          <tr class="pnl-total">
            <td class="pnl-label">EBITDA Operativo</td>
            <td class="pnl-val {neg_cls(pl['ebitda_operativo'])}">{fmt_clp(pl['ebitda_operativo'])}</td>
          </tr>
          <tr><td class="pnl-label" style="font-size:0.72rem;color:#475569;">Margen neto</td>
              <td class="pnl-val" style="font-size:0.72rem;color:#64748B;">{pl['margen_neto_pct']*100:.1f}%</td>
          </tr>
        </table>
        """, unsafe_allow_html=True)

    with wf_col:
        st.plotly_chart(grafico_pl_waterfall(pl), use_container_width=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # ── DIAGNÓSTICOS ──
    titulo_diag = "¿Qué está bien y qué hay que mejorar?" if es_pyme else "Diagnóstico Ejecutivo"
    st.markdown(f"#### {titulo_diag}")

    for diag in diags:
        nivel = diag["nivel"]
        box_cls = "diag-box" + (" warning" if nivel == "warning" else " ok" if nivel == "ok" else " purple" if nivel == "purple" else "")
        st.markdown(f"""
        <div class="{box_cls}">
          <div class="diag-title">{diag['titulo']}</div>
          <div class="diag-body">{diag['cuerpo']}</div>
        </div>
        """, unsafe_allow_html=True)
        if diag.get("cta"):
            st.markdown(
                '<div style="margin-top:-0.5rem;margin-bottom:0.75rem;padding:0.55rem 1.3rem;'
                'background:#0D1420;border:1px solid #1A2535;border-top:none;border-radius:0 0 8px 8px;">'
                '<a href="https://www.aovalle.com" target="_blank" '
                'style="color:#38BDF8;font-size:0.78rem;font-weight:600;text-decoration:none;letter-spacing:0.04em;">'
                '→ Solicitar diagnóstico personalizado · aovalle.com ↗</a></div>',
                unsafe_allow_html=True,
            )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — CANALES
# ─────────────────────────────────────────────────────────────────────────────

with tab_canales:

    st.markdown("#### Rendimiento por Canal")

    # Canal rows visuales
    max_ingresos = max((c["ingresos"] for c in canales_data.values()), default=1)
    for nombre, canal in canales_data.items():
        color  = CANALES_DEF[nombre]["color"]
        pct    = canal["ingresos"] / max_ingresos if max_ingresos > 0 else 0
        contrib_color = "#34D399" if canal["contribucion"] >= 0 else "#F87171"

        if canal.get("es_marketplace"):
            # Badge especial: muestra comisión en lugar de ROAS
            mp_label   = canal.get("nombre_mp", "Marketplace")
            com_pct    = canal.get("comision_pct", 0) * 100
            roas_c     = canal["roas"]
            badge_html = (
                f'<div class="canal-roas roas-warning" style="min-width:80px;font-size:0.68rem;">' +
                f'COM {com_pct:.1f}%</div>'
            )
            extra_info = (
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.72rem;' +
                f'color:#64748B;min-width:130px;text-align:right;">' +
                f'{mp_label} · ROAS <span style="color:#FBBF24;">{roas_c:.1f}x</span></div>'
            )
        else:
            roas_c     = canal["roas"]
            roas_cls   = "roas-ok" if roas_c >= 3 else "roas-warning" if roas_c >= 1.5 else "roas-danger"
            badge_html = f'<div class="canal-roas {roas_cls}">ROAS {roas_c:.1f}x</div>'
            extra_info = (
                f'<div style="font-family:\'DM Mono\',monospace;font-size:0.72rem;' +
                f'color:#64748B;min-width:90px;text-align:right;">' +
                f'Contrib: <span style="color:{contrib_color};">{fmt_clp(canal["contribucion"])}</span></div>'
            )

        st.markdown(f"""
        <div class="canal-row">
          <div class="canal-dot" style="background:{color};"></div>
          <div class="canal-name">{nombre}</div>
          <div class="canal-bar-bg">
            <div class="canal-bar-fill" style="width:{pct*100:.1f}%;background:{color};opacity:0.7;"></div>
          </div>
          <div class="canal-val">{fmt_clp(canal['ingresos'])}</div>
          {extra_info}
          {badge_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    gc1, gc2 = st.columns(2)
    with gc1:
        st.plotly_chart(grafico_mix_canales(canales_data), use_container_width=True)
    with gc2:
        st.plotly_chart(grafico_roas_canales(canales_data), use_container_width=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # Tabla detalle
    hay_mp = any(c.get("es_marketplace") for c in canales_data.values())
    with st.expander("📋 Tabla detallada por canal"):
        rows_tabla = []
        for nombre, canal in canales_data.items():
            fila = {
                "Canal":        nombre,
                "Tráfico":      f"{canal['trafico']:,}",
                "CR":           fmt_pct(canal["cr"]),
                "Pedidos":      f"{canal['pedidos']:,.0f}",
                "AOV":          fmt_clp(canal["aov"]),
                "Ingresos":     fmt_clp(canal["ingresos"]),
            }
            if canal.get("es_marketplace"):
                fila["Marketplace"]      = canal.get("nombre_mp", "—")
                fila["Comisión %"]       = fmt_pct(canal.get("comision_pct", 0))
                fila["Comisión Pagada"]  = fmt_clp(canal.get("comision_pagada", 0))
                fila["Ing. Netos"]       = fmt_clp(canal.get("ingresos_netos", canal["ingresos"]))
                fila["Costo Canal"]      = "N/A"
                fila["Tipo Costo"]       = "Comisión %"
            else:
                if hay_mp:
                    fila["Marketplace"]     = "—"
                    fila["Comisión %"]      = "—"
                    fila["Comisión Pagada"] = "—"
                    fila["Ing. Netos"]      = fmt_clp(canal["ingresos"])
                if canal.get("cpc", 0) > 0:
                    fila["Costo Canal"] = fmt_clp(canal["gasto_ads"])
                    fila["Tipo Costo"]  = f"CPC {fmt_clp(canal['cpc'])}/clic"
                elif canal.get("inversion", 0) > 0:
                    fila["Costo Canal"] = fmt_clp(canal["gasto_ads"])
                    fila["Tipo Costo"]  = "Inversión fija"
                else:
                    fila["Costo Canal"] = fmt_clp(0)
                    fila["Tipo Costo"]  = "Sin inversión"
            fila["ROAS"]         = fmt_x(canal["roas"])
            fila["CAC"]          = fmt_clp(canal["cac"])
            fila["Contribución"] = fmt_clp(canal["contribucion"])
            rows_tabla.append(fila)
        st.dataframe(pd.DataFrame(rows_tabla), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — RETENCIÓN & LTV
# ─────────────────────────────────────────────────────────────────────────────

with tab_retencion:

    r1, r2, r3, r4 = st.columns(4)
    clientes_mes12 = cohorte_rows[-1]["clientes"] if cohorte_rows else 0
    retencion_12m  = clientes_mes12 / cohorte_size if cohorte_size > 0 else 0
    with r1:
        st.markdown(mc(
            "LTV a 12 meses / cliente" if es_pyme else "LTV Cohorte 12M",
            fmt_clp(ltv_12m),
            sub="Por cliente adquirido",
        ), unsafe_allow_html=True)
    with r2:
        ltv_kind = "success" if pl["ltv_cac"] >= 3 else "warning" if pl["ltv_cac"] >= 2 else "danger"
        st.markdown(mc(
            "Relación LTV / CAC" if es_pyme else "LTV / CAC Ratio",
            fmt_x(pl["ltv_cac"]),
            sub="≥3x = saludable",
            kind=ltv_kind,
        ), unsafe_allow_html=True)
    with r3:
        churn_kind = "success" if churn_mensual <= 0.05 else "warning" if churn_mensual <= 0.10 else "danger"
        st.markdown(mc(
            "% clientes que no vuelven / mes" if es_pyme else "Churn Mensual",
            fmt_pct(churn_mensual),
            sub=f"Retención 12M: {retencion_12m*100:.0f}%",
            kind=churn_kind,
        ), unsafe_allow_html=True)
    with r4:
        st.markdown(mc(
            "Clientes activos al mes 12" if es_pyme else "Clientes Activos Mes 12",
            f"{clientes_mes12:,.0f}",
            sub=f"De {cohorte_size:,} iniciales",
            kind="purple",
        ), unsafe_allow_html=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
    st.plotly_chart(grafico_retencion(cohorte_rows), use_container_width=True)

    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

    # Tabla de cohorte
    with st.expander("📋 Ver tabla de cohorte mes a mes"):
        df_cohorte = pd.DataFrame(cohorte_rows)
        df_cohorte.columns = ["Mes", "Clientes Activos", "Ingresos Cohorte (CLP)", "LTV Acum. / Cliente (CLP)"]
        df_cohorte["Clientes Activos"] = df_cohorte["Clientes Activos"].apply(lambda v: f"{v:,.0f}")
        df_cohorte["Ingresos Cohorte (CLP)"] = df_cohorte["Ingresos Cohorte (CLP)"].apply(fmt_clp)
        df_cohorte["LTV Acum. / Cliente (CLP)"] = df_cohorte["LTV Acum. / Cliente (CLP)"].apply(fmt_clp)
        st.dataframe(df_cohorte, use_container_width=True, hide_index=True)

    # Diagnóstico retención
    st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
    st.markdown("#### Diagnóstico de Retención")

    if churn_mensual > 0.10:
        msg_churn = (
            f"Un churn de <strong>{churn_mensual*100:.1f}% mensual</strong> significa que pierdes más del 10% de tu base "
            f"cada mes. En 12 meses, solo conservas el <strong>{retencion_12m*100:.0f}%</strong> de los clientes "
            f"captados hoy. A este ritmo, el negocio necesita adquirir constantemente clientes nuevos solo para "
            f"mantener los ingresos, sin crecer.<br><br>"
            f"<strong>Palancas de retención:</strong> Email post-compra a los 7 y 30 días, programa de puntos "
            f"simple, y encuesta NPS para identificar el motivo de abandono."
            if not es_pyme else
            f"Cada mes estás perdiendo el <strong>{churn_mensual*100:.1f}%</strong> de tus clientes. "
            f"Eso significa que en un año solo quedan <strong>{retencion_12m*100:.0f} de cada 100</strong> "
            f"clientes que tuviste hoy.<br><br>"
            f"<strong>Qué hacer:</strong> Manda un WhatsApp o email a los 7 días después de la compra. "
            f"Ofrece un descuento para la segunda compra. Es la acción de mayor impacto con menor costo."
        )
        st.markdown(f'<div class="diag-box"><div class="diag-title">🔴 CHURN ELEVADO — Base de Clientes en Erosión</div><div class="diag-body">{msg_churn}</div></div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:-0.5rem;margin-bottom:0.75rem;padding:0.55rem 1.3rem;background:#0D1420;border:1px solid #1A2535;border-top:none;border-radius:0 0 8px 8px;"><a href="https://www.aovalle.com" target="_blank" style="color:#38BDF8;font-size:0.78rem;font-weight:600;text-decoration:none;">→ Diagnóstico de retención · aovalle.com ↗</a></div>', unsafe_allow_html=True)
    elif retencion_12m >= 0.40:
        st.markdown(f'<div class="diag-box ok"><div class="diag-title">✅ RETENCIÓN SALUDABLE</div><div class="diag-body">Tu tasa de retención a 12 meses es <strong>{retencion_12m*100:.0f}%</strong>. Esto es superior al benchmark promedio de ecommerce en Chile (~25-35%). El foco ahora debe ser incrementar la frecuencia de recompra para elevar el LTV por cohorte.</div></div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — CYBER
# ─────────────────────────────────────────────────────────────────────────────

with tab_cyber:

    if not activar_cyber:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;">
          <div style="font-size:2.5rem;margin-bottom:1rem;">⚡</div>
          <div style="font-size:1.1rem;font-weight:600;color:#CBD5E1;margin-bottom:0.5rem;">
            Módulo de Eventos Digitales desactivado
          </div>
          <div style="font-size:0.85rem;color:#475569;max-width:420px;margin:0 auto;">
            Activa "Escenarios de evento" en el sidebar para simular CyberDay, Black Friday,
            Hot Sale y otros eventos digitales chilenos sobre tu P&L actual.
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        ev_activo  = EVENTOS_CYBER_CL.get(evento_cyber_sel, {})
        pas_activo = PASARELAS_CL.get(pasarela_sel, {})
        st.markdown(f"""
        <div style="background:#0D1420;border:1px solid #1A2535;border-radius:8px;
                    padding:0.75rem 1.25rem;margin-bottom:1rem;
                    display:flex;gap:2rem;align-items:center;flex-wrap:wrap;">
          <div>
            <span style="font-size:0.62rem;color:#64748B;text-transform:uppercase;
                         letter-spacing:0.1em;">Evento</span><br>
            <span style="font-size:0.9rem;font-weight:600;color:#38BDF8;">
              {evento_cyber_sel}</span>
            <span style="font-size:0.75rem;color:#64748B;margin-left:0.5rem;">
              · Tráfico ×{ev_activo.get('multiplicador',4)} · {ev_activo.get('mes','—')}</span>
          </div>
          <div>
            <span style="font-size:0.62rem;color:#64748B;text-transform:uppercase;
                         letter-spacing:0.1em;">Pasarela</span><br>
            <span style="font-size:0.9rem;font-weight:600;color:#FBBF24;">
              {pasarela_sel}</span>
            <span style="font-size:0.75rem;color:#64748B;margin-left:0.5rem;">
              · {pas_activo.get('label','—')}</span>
          </div>
          <div>
            <span style="font-size:0.62rem;color:#64748B;text-transform:uppercase;
                         letter-spacing:0.1em;">Inflación CPC</span><br>
            <span style="font-size:0.9rem;font-weight:600;color:#F87171;">
              +{ev_activo.get('inflacion_cpc',0.5)*100:.0f}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("#### Impacto sobre tu P&L Mensual")

        ca1, ca2, ca3, ca4 = st.columns(4)
        with ca1:
            kind_c = "danger" if cyber_perdida_total > pl["total_ingresos"] * 0.05 else "warning"
            st.markdown(mc(
                "Pérdida Total Proyectada" if not es_pyme else "Dinero en Riesgo (Cyber)",
                fmt_clp(cyber_perdida_total),
                sub=f"{cyber_perdida_total/pl['total_ingresos']*100:.1f}% de ingresos en riesgo" if pl["total_ingresos"] > 0 else "",
                kind=kind_c,
            ), unsafe_allow_html=True)
        with ca2:
            st.markdown(mc(
                "Pérdida Evento A (Pasarela)",
                fmt_clp(cyber_a["costo_total"] if cyber_a_on else 0),
                kind="danger" if cyber_a_on else "default",
            ), unsafe_allow_html=True)
        with ca3:
            st.markdown(mc(
                "Pérdida Evento B (Logística)",
                fmt_clp(cyber_b["costo_total"] if cyber_b_on else 0),
                kind="warning" if cyber_b_on else "default",
            ), unsafe_allow_html=True)
        with ca4:
            st.markdown(mc(
                "Pérdida Evento C (CAC +50%)",
                fmt_clp(cyber_c["costo_total"] if cyber_c_on else 0),
                sub=f"ROAS en Cyber: {fmt_x(cyber_c.get('roas_nuevo', 0))}",
                kind="warning" if cyber_c_on else "default",
            ), unsafe_allow_html=True)

        st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

        ebitda_post_cyber = pl["ebitda_operativo"] - cyber_perdida_total
        cyber_w1, cyber_w2 = st.columns(2)
        with cyber_w1:
            st.plotly_chart(
                grafico_waterfall_cyber(pl, cyber_a, cyber_b, cyber_c, [cyber_a_on, cyber_b_on, cyber_c_on]),
                use_container_width=True
            )
        with cyber_w2:
            # EBITDA antes vs después del Cyber
            fig_ebitda = go.Figure()
            fig_ebitda.add_trace(go.Bar(
                x=["EBITDA Normal", "EBITDA Post-Cyber"],
                y=[pl["ebitda_operativo"], ebitda_post_cyber],
                marker_color=["#34D399" if pl["ebitda_operativo"] >= 0 else "#F87171",
                              "#34D399" if ebitda_post_cyber >= 0 else "#F87171"],
                text=[fmt_clp(pl["ebitda_operativo"]), fmt_clp(ebitda_post_cyber)],
                textposition="outside", textfont=dict(color="#CBD5E1", size=11),
                width=0.4,
            ))
            fig_ebitda.add_hline(y=0, line_color="#475569", line_width=1)
            fig_ebitda.update_layout(
                title=dict(text="EBITDA: Normal vs. Post-Cyber", font=dict(size=13, color="#CBD5E1")),
                showlegend=False, **THEME,
            )
            fig_ebitda.update_yaxes(gridcolor="#1A2535", zerolinecolor="#475569")
            st.plotly_chart(fig_ebitda, use_container_width=True)

        # Diagnósticos Cyber
        st.markdown('<hr class="sdiv">', unsafe_allow_html=True)
        st.markdown("#### Diagnóstico Cyber")

        if cyber_perdida_total > pl["total_ingresos"] * 0.10:
            st.markdown(f"""
            <div class="diag-box">
              <div class="diag-title">🚨 RIESGO ALTO: Cyber Puede Destruir Tu Margen</div>
              <div class="diag-body">
                Con los 3 eventos activos, tu operación puede perder <strong>{fmt_clp(cyber_perdida_total)}</strong>
                — el <strong>{cyber_perdida_total/pl['total_ingresos']*100:.1f}%</strong> de tus ingresos mensuales.
                Tu EBITDA post-Cyber sería <strong>{fmt_clp(ebitda_post_cyber)}</strong>.
                {'Estarías en pérdida operativa.' if ebitda_post_cyber < 0 else 'Pero el colchón es mínimo.'}<br><br>
                <strong>Prioridad antes de Cyber:</strong> Resolver redundancia de pasarela, pre-stockear regiones
                clave y establecer un tope de CPC máximo en campañas de performance.
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div style="margin-top:-0.5rem;margin-bottom:0.75rem;padding:0.55rem 1.3rem;background:#0D1420;border:1px solid #1A2535;border-top:none;border-radius:0 0 8px 8px;"><a href="https://www.aovalle.com" target="_blank" style="color:#38BDF8;font-size:0.78rem;font-weight:600;text-decoration:none;">→ Preparación Cyber · aovalle.com ↗</a></div>', unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="diag-box ok">
              <div class="diag-title">✅ EXPOSICIÓN CYBER MANEJABLE</div>
              <div class="diag-body">
                La pérdida proyectada ({fmt_clp(cyber_perdida_total)}) representa menos del 10% de tus ingresos.
                Tu operación tiene suficiente margen para absorber los eventos de estrés típicos de Cyber.
                El foco debe ser aprovechar el volumen incremental optimizando el CR pre-evento.
              </div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER CTA
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<hr class="sdiv">', unsafe_allow_html=True)

ebitda_label = fmt_clp(pl["ebitda_operativo"])
ebitda_color = "#34D399" if pl["ebitda_operativo"] >= 0 else "#F87171"

if es_pyme:
    headline = f'Tu negocio tiene un resultado de <span style="color:{ebitda_color};">{ebitda_label}</span> este mes.'
    sub_copy = "¿Quieres saber exactamente qué cambiar para mejorar ese número? Alejandro Ovalle trabaja con dueños de tiendas chilenas para convertir datos en decisiones concretas."
else:
    headline = f'EBITDA operativo: <span style="color:{ebitda_color};">{ebitda_label}</span> · LTV/CAC: {fmt_x(pl["ltv_cac"])} · ROAS global: {fmt_x(pl["roas_global"])}'
    sub_copy = "Alejandro Ovalle convierte este diagnóstico en un plan de acción ejecutable: auditoría de canales, arquitectura de retención, y optimización pre-Cyber. Clientes en Chile y LatAm."

st.markdown(f"""
<div class="footer-cta">
  <div style="font-size:0.62rem;color:#38BDF8;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.5rem;">
    CONVIERTE ESTE DIAGNÓSTICO EN CRECIMIENTO REAL
  </div>
  <div style="font-size:1.15rem;font-weight:700;color:#F1F5F9;margin-bottom:0.65rem;">
    {headline}
  </div>
  <div style="font-size:0.85rem;color:#64748B;max-width:580px;margin:0 auto 1.25rem auto;line-height:1.7;">
    {sub_copy}
  </div>
  <a href="https://www.aovalle.com" target="_blank"
     style="display:inline-block;background:#38BDF8;color:#080C14;font-weight:700;
            font-size:0.82rem;padding:0.6rem 1.75rem;border-radius:6px;text-decoration:none;
            letter-spacing:0.06em;text-transform:uppercase;">
    Solicitar Diagnóstico → aovalle.com
  </a>
  <div style="font-size:0.62rem;color:#ffffff;margin-top:1.25rem;">
    RetailPulse Latam v2.0 · Mercado Chileno · linkedin.com/in/ovallealejandro<br>
Copyright &COPY; <script>
                  document.write(new Date().getFullYear());
                </script> | <a>AOvalle.com</a> | Todos los Derechos Reservados
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TÉRMINOS Y CONDICIONES
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

col_tc_l, col_tc_c, col_tc_r = st.columns([1, 1, 1])
with col_tc_c:
    with st.popover("📄 Ver Términos y Condiciones"):

        st.caption("Última actualización: Junio de 2026")
        st.markdown("#### Términos y Condiciones de Uso | RetailPulse LATAM")

        secciones = [
            ("1. Objeto de la Aplicación y Licencia de Uso",
             "RetailPulse LATAM es un simulador interactivo de Estado de Resultados (P&L) enfocado en comercio electrónico para el mercado latinoamericano. El Propietario otorga al Usuario una licencia de uso limitada, no exclusiva, revocable, personal y no transferible para utilizar La Aplicación como herramienta de análisis, diagnóstico y simulación estratégica según el plan de licenciamiento contratado."),

            ("2. Privacidad por Diseño y No Almacenamiento (Cumplimiento Ley N° 21.719)",
             "En estricto cumplimiento del principio de minimización y privacidad por diseño consagrados en la Ley N° 21.719, La Aplicación adopta un modelo de procesamiento en tiempo de ejecución. Esto significa que El Propietario no realiza operaciones de recolección, registro, almacenamiento ni tratamiento de los datos financieros introducidos. Toda la información se procesa localmente en la sesión efímera del navegador del Usuario y se destruye automáticamente al cerrarse la sesión, garantizando la imposibilidad de accesos no autorizados o fugas de información."),

            ("3. Exclusión de Responsabilidad Financiera y Comercial",
             "RetailPulse LATAM es exclusivamente una herramienta de simulación, apoyo educativo y planificación estratégica. Los resultados, gráficos, proyecciones y cálculos generados son estimaciones matemáticas basadas en los datos suministrados por el propio Usuario. El uso de La Aplicación no constituye asesoría financiera, contable, legal, tributaria o comercial vinculante. El Propietario no será responsable por pérdidas financieras, lucro cesante, daño emergente o decisiones operativas erróneas derivadas del uso de la información visualizada."),

            ("4. Propiedad Intelectual y Restricciones",
             "Toda la propiedad intelectual asociada a RetailPulse LATAM —incluyendo código fuente (Python), arquitectura de software, algoritmos de simulación financiera, lógica de módulos, diseños e interfaces— es propiedad exclusiva de Alejandro Ovalle. Queda prohibido realizar ingeniería inversa, descompilar, extraer el código fuente, revender el acceso a terceros sin licencia corporativa, o remover los avisos de derecho de autor."),

            ("5. Modificaciones y Actualizaciones de Datos",
             "Las tarifas de pasarelas de pago, comisiones de marketplaces y multiplicadores de eventos incluidos corresponden a revisiones periódicas del mercado realizadas por El Propietario. El Propietario se reserva el derecho de actualizar o modificar la matriz de datos en cualquier momento para asegurar la vigencia de las simulaciones."),

            ("6. Ley Aplicable y Jurisdicción",
             "Estos Términos y Condiciones se rigen por las leyes de la República de Chile. Cualquier controversia será sometida a la jurisdicción de los Tribunales Ordinarios de Justicia de Santiago de Chile."),
        ]

        for titulo, cuerpo in secciones:
            st.markdown(f"**{titulo}**")
            st.markdown(cuerpo)
            st.divider()

        st.caption("© 2026 Alejandro Ovalle · aovalle.com · Todos los derechos reservados")
