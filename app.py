"""
RetailPulse Latam — Simulador de Estrés Operativo
Autor: Desarrollado para Alejandro Ovalle | aovalle.com
Versión MVP: 1.0
Stack: Python + Streamlit + Plotly Express
Deploy: Streamlit Community Cloud (tier gratuito)
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL DE LA APP
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="RetailPulse Latam | Simulador de Estrés Operativo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PREMIUM — DISEÑO CORPORATIVO OSCURO
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

  /* ── BASE ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }
  .stApp {
    background: #080C14;
    color: #E8EDF5;
  }

  /* ── SIDEBAR ── */
  [data-testid="stSidebar"] {
    background: #0D1420 !important;
    border-right: 1px solid #1E2A3A;
  }
  [data-testid="stSidebar"] .stMarkdown h3 {
    color: #4FC3F7;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 1.5rem;
    margin-bottom: 0.25rem;
    border-bottom: 1px solid #1E2A3A;
    padding-bottom: 0.4rem;
  }
  .stSlider > div > div > div { background: #1E2A3A !important; }
  .stSlider > div > div > div > div { background: #4FC3F7 !important; }

  /* ── TÍTULOS ── */
  h1 { color: #FFFFFF !important; font-weight: 700 !important; letter-spacing: -0.02em; }
  h2 { color: #CBD5E1 !important; font-weight: 500 !important; }
  h3 { color: #94A3B8 !important; }

  /* ── METRIC CARDS ── */
  .metric-card {
    background: #0D1420;
    border: 1px solid #1E2A3A;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
  }
  .metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4FC3F7, #0288D1);
  }
  .metric-card.danger::before { background: linear-gradient(90deg, #F87171, #DC2626); }
  .metric-card.warning::before { background: linear-gradient(90deg, #FBBF24, #D97706); }
  .metric-card.success::before { background: linear-gradient(90deg, #34D399, #059669); }
  .metric-card .label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #64748B;
    margin-bottom: 0.5rem;
  }
  .metric-card .value {
    font-family: 'DM Mono', monospace;
    font-size: 1.6rem;
    font-weight: 500;
    color: #F1F5F9;
    line-height: 1;
  }
  .metric-card .delta {
    font-size: 0.75rem;
    margin-top: 0.4rem;
    color: #64748B;
  }
  .metric-card .delta.negative { color: #F87171; }
  .metric-card .delta.positive { color: #34D399; }

  /* ── SCENARIO CARDS ── */
  .scenario-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background: #0D1420;
    border: 1px solid #1E2A3A;
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.5rem;
  }
  .scenario-header .icon { font-size: 1.4rem; }
  .scenario-header .title { font-weight: 600; color: #CBD5E1; font-size: 0.95rem; }
  .scenario-header .subtitle { font-size: 0.75rem; color: #475569; }

  /* ── DIAGNOSIS BOX ── */
  .diagnosis-box {
    background: #0D1420;
    border: 1px solid #DC2626;
    border-left: 4px solid #DC2626;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-top: 1rem;
  }
  .diagnosis-box.warning {
    border-color: #D97706;
    border-left-color: #D97706;
  }
  .diagnosis-box.ok {
    border-color: #059669;
    border-left-color: #059669;
  }
  .diagnosis-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
  }
  .diagnosis-box .diagnosis-title { color: #F87171; }
  .diagnosis-box.warning .diagnosis-title { color: #FBBF24; }
  .diagnosis-box.ok .diagnosis-title { color: #34D399; }

  /* ── DIVIDERS ── */
  .section-divider {
    border: none;
    border-top: 1px solid #1E2A3A;
    margin: 2rem 0;
  }

  /* ── BADGE ── */
  .badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }
  .badge-red { background: #450A0A; color: #F87171; }
  .badge-yellow { background: #451A03; color: #FBBF24; }
  .badge-blue { background: #0C2340; color: #4FC3F7; }
  .badge-green { background: #052E16; color: #34D399; }

  /* ── FOOTER ── */
  .footer-cta {
    background: linear-gradient(135deg, #0D1420, #0C2340);
    border: 1px solid #1E2A3A;
    border-radius: 12px;
    padding: 1.75rem 2rem;
    text-align: center;
    margin-top: 2rem;
  }

  /* ── STREAMLIT OVERRIDES ── */
  .stNumberInput input {
    background: #0D1420 !important;
    border: 1px solid #1E2A3A !important;
    color: #E8EDF5 !important;
    font-family: 'DM Mono', monospace !important;
  }
  .stSelectbox select, .stSelectbox > div > div {
    background: #0D1420 !important;
    border: 1px solid #1E2A3A !important;
    color: #E8EDF5 !important;
  }
  div[data-testid="stExpander"] {
    background: #0D1420 !important;
    border: 1px solid #1E2A3A !important;
    border-radius: 8px;
  }
  .streamlit-expanderHeader { color: #94A3B8 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MODELO MATEMÁTICO — FUNCIONES PURAS
# ─────────────────────────────────────────────────────────────────────────────

def calcular_baseline(trafico, cr_base, aov_clp, cpc_clp, margen_bruto_pct):
    """
    Calcula el estado financiero base del ecommerce (sin eventos de estrés).

    Parámetros
    ----------
    trafico       : int   — visitas mensuales estimadas
    cr_base       : float — tasa de conversión base (0-1)
    aov_clp       : int   — ticket promedio en CLP
    cpc_clp       : int   — costo por clic promedio en CLP
    margen_bruto  : float — margen bruto sobre ventas (0-1)

    Retorna
    -------
    dict con métricas baseline
    """
    pedidos          = trafico * cr_base
    ingresos         = pedidos * aov_clp
    gasto_ads        = trafico * cpc_clp
    margen_bruto_clp = ingresos * margen_bruto_pct
    contribucion     = margen_bruto_clp - gasto_ads
    roas             = ingresos / gasto_ads if gasto_ads > 0 else 0
    cac              = gasto_ads / pedidos  if pedidos  > 0 else 0
    ltv_estimado     = aov_clp * 2.4        # LTV = AOV × frecuencia media chilena (2.4x/año)
    ltv_cac_ratio    = ltv_estimado / cac   if cac      > 0 else 0

    return {
        "trafico"          : trafico,
        "pedidos"          : pedidos,
        "ingresos"         : ingresos,
        "gasto_ads"        : gasto_ads,
        "margen_bruto_clp" : margen_bruto_clp,
        "contribucion"     : contribucion,
        "roas"             : roas,
        "cac"              : cac,
        "ltv_estimado"     : ltv_estimado,
        "ltv_cac_ratio"    : ltv_cac_ratio,
        "cr_base"          : cr_base,
        "aov_clp"          : aov_clp,
        "cpc_clp"          : cpc_clp,
    }


def escenario_caida_pasarela(baseline, duracion_minutos=30, hora_pico=True):
    """
    EVENTO A — Caída de Webpay / Mercado Pago en hora pico de Cyber.

    Modelo:
    - Hora pico Cyber = top 2h del día concentran ~25% del tráfico diario.
    - En un Cyber de 48h, la hora pico tiene un multiplicador de tráfico 4x.
    - Durante la caída, CR cae a 0 (checkout bloqueado).
    - Recovery parcial post-caída: 15% de los usuarios reintenta vs 85% abandona.
    - Costo de Oportunidad = pedidos_perdidos × AOV
    - Gasto en Ads durante la caída NO se pausa → pérdida directa.
    """
    # Tráfico por minuto en hora pico (multiplicador Cyber)
    multiplicador_cyber = 4.0 if hora_pico else 2.0
    trafico_por_minuto  = (baseline["trafico"] / (30 * 24 * 60)) * multiplicador_cyber
    trafico_afectado    = trafico_por_minuto * duracion_minutos

    # Pedidos que no pudieron completarse
    pedidos_perdidos    = trafico_afectado * baseline["cr_base"]

    # El 15% reintenta y convierte, el 85% abandona definitivamente
    tasa_recuperacion   = 0.15
    pedidos_recuperados = pedidos_perdidos * tasa_recuperacion
    pedidos_netos_perd  = pedidos_perdidos * (1 - tasa_recuperacion)

    ingreso_perdido     = pedidos_netos_perd * baseline["aov_clp"]

    # Ads siguen corriendo durante la caída → dinero quemado sin retorno
    gasto_ads_quemado   = trafico_afectado * baseline["cpc_clp"]

    costo_total_evento  = ingreso_perdido + gasto_ads_quemado
    impacto_margen      = ingreso_perdido * (baseline["margen_bruto_clp"] / baseline["ingresos"]) if baseline["ingresos"] > 0 else 0

    return {
        "nombre"            : "Caída de Pasarela de Pago",
        "trafico_afectado"  : trafico_afectado,
        "pedidos_perdidos"  : pedidos_netos_perd,
        "ingreso_perdido"   : ingreso_perdido,
        "gasto_quemado_ads" : gasto_ads_quemado,
        "costo_total"       : costo_total_evento,
        "impacto_margen"    : impacto_margen,
        "detalle"           : f"~{trafico_afectado:,.0f} visitas sin posibilidad de comprar · {pedidos_netos_perd:,.1f} pedidos perdidos netos",
    }


def escenario_quiebre_stock_logistico(baseline, tasa_reclamo_base=0.03, multiplicador_reclamo=2.0,
                                       costo_devolucion_clp=8500, pct_ventas_regiones=0.38):
    """
    EVENTO B — Quiebre de stock / retraso logístico en Regiones.

    Modelo:
    - El 38% de ventas ecommerce Chile proviene de regiones fuera de RM (dato ACEC 2023).
    - Retraso logístico duplica tasa de reclamos (de ~3% base a ~6%).
    - Cada devolución tiene un costo operativo promedio de $8.500 CLP.
    - El 60% de clientes con mala experiencia logística no recompra (impacto LTV).
    - CR del sitio cae un 12% por reseñas negativas en redes sociales (efecto reputacional).
    """
    pedidos_regiones      = baseline["pedidos"] * pct_ventas_regiones
    tasa_reclamo_estres   = tasa_reclamo_base * multiplicador_reclamo
    reclamos_adicionales  = pedidos_regiones * (tasa_reclamo_estres - tasa_reclamo_base)

    # Costo directo de devoluciones
    costo_devoluciones    = reclamos_adicionales * costo_devolucion_clp

    # Impacto reputacional → reducción de CR del sitio
    impacto_cr_pct        = 0.12
    pedidos_perdidos_cr   = baseline["pedidos"] * impacto_cr_pct
    ingreso_perdido_cr    = pedidos_perdidos_cr * baseline["aov_clp"]

    # Impacto LTV — 60% de clientes afectados no recompra
    clientes_afectados    = reclamos_adicionales * 0.60
    ltv_perdido           = clientes_afectados * baseline["ltv_estimado"]

    costo_total_evento    = costo_devoluciones + ingreso_perdido_cr

    return {
        "nombre"             : "Quiebre Stock / Retraso Logístico",
        "reclamos_adicional" : reclamos_adicionales,
        "costo_devoluciones" : costo_devoluciones,
        "ingreso_perdido_cr" : ingreso_perdido_cr,
        "ltv_perdido"        : ltv_perdido,
        "costo_total"        : costo_total_evento,
        "detalle"            : f"~{reclamos_adicionales:,.0f} reclamos adicionales · CR del sitio cae {impacto_cr_pct*100:.0f}% por reputación",
    }


def escenario_inflacion_cac(baseline, incremento_cpc_pct=0.50):
    """
    EVENTO C — Inflación del CAC por saturación de subasta en Cyber.

    Modelo:
    - CPC sube un 50% durante Cyber/BF (promedio observado Meta/Google Chile).
    - El gasto total de Ads sube proporcionalmente (misma estrategia de puja).
    - El ROAS colapsa porque el ingreso no crece al mismo ritmo que el gasto.
    - Para mantener el mismo ROAS base, se requiere un CR mínimo nuevo.
    - Se calcula el CR mínimo de equilibrio y el GAP vs CR actual.
    """
    cpc_estres          = baseline["cpc_clp"] * (1 + incremento_cpc_pct)
    gasto_ads_estres    = baseline["trafico"] * cpc_estres
    incremento_gasto    = gasto_ads_estres - baseline["gasto_ads"]

    # ROAS post-estrés (asumiendo mismo nivel de ingresos)
    roas_estres         = baseline["ingresos"] / gasto_ads_estres if gasto_ads_estres > 0 else 0

    # Margen de contribución post-estrés
    contribucion_estres = baseline["margen_bruto_clp"] - gasto_ads_estres

    # CAC estresado
    cac_estres          = gasto_ads_estres / baseline["pedidos"] if baseline["pedidos"] > 0 else 0

    # CR mínimo necesario para mantener ROAS original
    # ROAS_base = (trafico × CR_min × AOV) / (trafico × CPC_estres)
    # CR_min = ROAS_base × CPC_estres / AOV
    cr_minimo_equilibrio = (baseline["roas"] * cpc_estres) / baseline["aov_clp"] if baseline["aov_clp"] > 0 else 0
    gap_cr               = cr_minimo_equilibrio - baseline["cr_base"]

    costo_total_evento  = max(0, incremento_gasto - (contribucion_estres - baseline["contribucion"]))

    return {
        "nombre"                : "Inflación CAC (CPC +50%)",
        "cpc_estres"            : cpc_estres,
        "gasto_ads_estres"      : gasto_ads_estres,
        "incremento_gasto"      : incremento_gasto,
        "roas_estres"           : roas_estres,
        "contribucion_estres"   : contribucion_estres,
        "cac_estres"            : cac_estres,
        "cr_minimo_equilibrio"  : cr_minimo_equilibrio,
        "gap_cr"                : gap_cr,
        "costo_total"           : abs(contribucion_estres - baseline["contribucion"]),
        "detalle"               : f"CPC sube de ${baseline['cpc_clp']:,.0f} a ${cpc_estres:,.0f} CLP · ROAS cae de {baseline['roas']:.2f}x a {roas_estres:.2f}x",
    }


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE FORMATO
# ─────────────────────────────────────────────────────────────────────────────

def fmt_clp(valor):
    """Formatea un número como moneda CLP abreviada."""
    if abs(valor) >= 1_000_000:
        return f"${valor/1_000_000:,.1f}M CLP"
    elif abs(valor) >= 1_000:
        return f"${valor/1_000:,.0f}K CLP"
    else:
        return f"${valor:,.0f} CLP"


def metric_card(label, value, delta=None, card_type="default"):
    delta_html = ""
    if delta is not None:
        cls = "negative" if delta < 0 else "positive"
        arrow = "↓" if delta < 0 else "↑"
        delta_html = f'<div class="delta {cls}">{arrow} {fmt_clp(abs(delta))} vs. baseline</div>'
    return f"""
    <div class="metric-card {card_type}">
        <div class="label">{label}</div>
        <div class="value">{value}</div>
        {delta_html}
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# LÓGICA DE DIAGNÓSTICO CONDICIONAL
# ─────────────────────────────────────────────────────────────────────────────

def generar_diagnostico(baseline, ea, eb, ec, umbral_alerta_clp=5_000_000):
    """
    Genera un diagnóstico ejecutivo condicional basado en los resultados
    del simulador. Si la pérdida supera umbrales, escala el mensaje de alerta
    y conecta con los servicios de consultoría.
    """
    perdida_total = ea["costo_total"] + eb["costo_total"] + ec["costo_total"]
    roas_ok       = baseline["roas"] >= 3.0
    ltv_cac_ok    = baseline["ltv_cac_ratio"] >= 3.0
    cr_critico    = baseline["cr_base"] < 0.015  # < 1.5% CR es crítico en Chile

    diagnosticos = []

    # ── DIAGNÓSTICO PASARELA ──
    if ea["costo_total"] > 2_000_000:
        diagnosticos.append({
            "nivel"  : "danger",
            "titulo" : "⚠️ RIESGO CRÍTICO: Checkout sin Redundancia",
            "cuerpo" : (
                f"Tu tienda puede perder <strong>{fmt_clp(ea['costo_total'])}</strong> en solo 30 minutos de caída "
                f"de Webpay/MercadoPago. Esto no es teórico: en CyberDay 2023, cortes de 15-45 min fueron "
                f"reportados por múltiples retailers chilenos. <br><br>"
                f"<strong>Acción urgente:</strong> Implementar una segunda pasarela activa (Transbank + Kushki o Flow) "
                f"con failover automático. Esta configuración puede completarse en 48-72 horas con la arquitectura correcta."
            ),
            "cta": True
        })

    # ── DIAGNÓSTICO LOGÍSTICO ──
    if eb["ltv_perdido"] > 5_000_000:
        diagnosticos.append({
            "nivel"  : "warning",
            "titulo" : "📦 ALERTA: Canibalización de LTV por Experiencia Logística",
            "cuerpo" : (
                f"El retraso en regiones proyecta una pérdida de LTV de <strong>{fmt_clp(eb['ltv_perdido'])}</strong>. "
                f"Con una base de clientes que no recompra, tu CAC actual de <strong>{fmt_clp(baseline['cac'])}</strong> "
                f"se vuelve insostenible. Cada peso invertido en Ads se diluye al no retener al cliente.<br><br>"
                f"<strong>Acción recomendada:</strong> Segmentar SLA de despacho por región, activar notificaciones "
                f"proactivas de estado de pedido (WhatsApp/email) y establecer un proceso de reclamo que resuelva en < 24h."
            ),
            "cta": True
        })

    # ── DIAGNÓSTICO CAC / ROAS ──
    if not roas_ok or ec["roas_estres"] < 2.0:
        diagnosticos.append({
            "nivel"  : "warning",
            "titulo" : "📊 ALERTA: ROAS en Zona de Quiebre Durante Cyber",
            "cuerpo" : (
                f"Con el CPC inflacionado, tu ROAS cae a <strong>{ec['roas_estres']:.2f}x</strong>. "
                f"Para ser rentable en Cyber necesitas un CR mínimo de "
                f"<strong>{ec['cr_minimo_equilibrio']*100:.2f}%</strong>. "
                f"Tu CR actual es <strong>{baseline['cr_base']*100:.2f}%</strong> "
                f"(GAP de {ec['gap_cr']*100:.2f} puntos porcentuales).<br><br>"
                f"<strong>Acción recomendada:</strong> Optimizar el funnel de conversión ANTES de activar pauta. "
                f"Un incremento de CR del 0.5% en Cyber puede ser equivalente a triplicar el presupuesto de Ads."
            ),
            "cta": True
        })

    # ── DIAGNÓSTICO LTV/CAC ──
    if not ltv_cac_ok:
        diagnosticos.append({
            "nivel"  : "danger",
            "titulo" : "🚨 RATIO LTV/CAC POR DEBAJO DEL UMBRAL SALUDABLE",
            "cuerpo" : (
                f"Tu ratio LTV/CAC es <strong>{baseline['ltv_cac_ratio']:.1f}x</strong>. "
                f"El benchmark saludable para ecommerce en LatAm es ≥ 3.0x. "
                f"Estás gastando demasiado en adquisición relativo al valor que genera cada cliente.<br><br>"
                f"<strong>Diagnóstico estructural:</strong> El problema no es el canal de adquisición, "
                f"es la arquitectura de retención. Sin un programa de fidelización y CX post-compra, "
                f"cada Cyber endeuda más la operación."
            ),
            "cta": True
        })

    # ── DIAGNÓSTICO CR CRÍTICO ──
    if cr_critico:
        diagnosticos.append({
            "nivel"  : "danger",
            "titulo" : "🔴 CR CRÍTICO: Tráfico sin Convertir = Dinero Quemado",
            "cuerpo" : (
                f"Una tasa de conversión de <strong>{baseline['cr_base']*100:.2f}%</strong> significa que "
                f"<strong>más del 98.5% de tus visitantes se van sin comprar</strong>. "
                f"Antes de invertir más en Ads para Cyber, debes resolver qué está bloqueando la conversión.<br><br>"
                f"<strong>Levers a revisar:</strong> Velocidad de carga mobile, claridad de propuesta de valor, "
                f"UX del checkout, confianza en la pasarela y medios de pago disponibles."
            ),
            "cta": True
        })

    # ── ESTADO SALUDABLE ──
    if not diagnosticos:
        diagnosticos.append({
            "nivel"  : "ok",
            "titulo" : "✅ OPERACIÓN SALUDABLE — Optimiza para Escalar",
            "cuerpo" : (
                f"Tus métricas base están dentro de rangos saludables. El simulador no detecta zonas de riesgo crítico "
                f"con los parámetros actuales. El siguiente nivel es pasar de una operación estable a una "
                f"<strong>operación de alto rendimiento</strong> con optimización continua de CX y retención."
            ),
            "cta": False
        })

    return diagnosticos, perdida_total


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICOS
# ─────────────────────────────────────────────────────────────────────────────

PLOTLY_THEME = dict(
    paper_bgcolor="#080C14",
    plot_bgcolor="#080C14",
    font=dict(family="DM Sans", color="#94A3B8", size=12),
    margin=dict(l=20, r=20, t=40, b=20),
)


def grafico_impacto_waterfall(baseline, ea, eb, ec):
    """Waterfall chart: Ingresos base → pérdidas por evento → bottom line estrés."""
    valores = [
        baseline["ingresos"],
        -ea["ingreso_perdido"],
        -eb["ingreso_perdido_cr"],
        -ec["costo_total"],
    ]
    ingresos_estres = baseline["ingresos"] - ea["ingreso_perdido"] - eb["ingreso_perdido_cr"] - ec["costo_total"]

    labels  = ["Ingresos Base", "Caída Pasarela", "Fricción Logística", "Inflación CAC"]
    colors  = ["#4FC3F7", "#F87171", "#FBBF24", "#FB923C"]
    measure = ["absolute", "relative", "relative", "relative"]

    fig = go.Figure(go.Waterfall(
        orientation  = "v",
        measure      = measure,
        x            = labels,
        y            = valores,
        connector    = dict(line=dict(color="#1E2A3A", width=1)),
        increasing   = dict(marker_color="#34D399"),
        decreasing   = dict(marker_color="#F87171"),
        totals       = dict(marker_color="#4FC3F7"),
        text         = [fmt_clp(v) for v in valores],
        textposition = "outside",
        textfont     = dict(color="#CBD5E1", size=11),
    ))

    fig.update_layout(
        title=dict(text="Impacto en Ingresos — Escenarios de Estrés Acumulados", font=dict(size=14, color="#CBD5E1")),
        showlegend=False,
        **PLOTLY_THEME
    )
    fig.update_yaxes(gridcolor="#1E2A3A", zerolinecolor="#1E2A3A")
    fig.update_xaxes(gridcolor="#1E2A3A")
    return fig


def grafico_roas_comparativo(baseline, ec):
    """Bar chart comparando ROAS baseline vs ROAS estresado."""
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name   = "ROAS Baseline",
        x      = ["ROAS Actual"],
        y      = [baseline["roas"]],
        marker = dict(color="#4FC3F7", line=dict(color="#0288D1", width=1)),
        text   = [f"{baseline['roas']:.2f}x"],
        textposition="outside",
        textfont=dict(color="#CBD5E1"),
        width  = 0.35,
    ))

    fig.add_trace(go.Bar(
        name   = "ROAS en Cyber (CPC +50%)",
        x      = ["ROAS en Estrés"],
        y      = [ec["roas_estres"]],
        marker = dict(color="#F87171", line=dict(color="#DC2626", width=1)),
        text   = [f"{ec['roas_estres']:.2f}x"],
        textposition="outside",
        textfont=dict(color="#CBD5E1"),
        width  = 0.35,
    ))

    fig.add_hline(y=3.0, line_dash="dot", line_color="#34D399",
                  annotation_text="Umbral saludable (3x)", annotation_position="top left",
                  annotation_font_color="#34D399")

    fig.update_layout(
        title=dict(text="ROAS: Condiciones Normales vs. Saturación Cyber", font=dict(size=14, color="#CBD5E1")),
        barmode="group",
        showlegend=True,
        legend=dict(font=dict(color="#94A3B8"), bgcolor="#0D1420", bordercolor="#1E2A3A"),
        **PLOTLY_THEME
    )
    fig.update_yaxes(gridcolor="#1E2A3A", zerolinecolor="#1E2A3A", title="ROAS (x)", title_font=dict(color="#64748B"))
    fig.update_xaxes(gridcolor="#1E2A3A")
    return fig


def grafico_costo_eventos_donut(ea, eb, ec):
    """Donut chart con la distribución del costo total de los 3 eventos."""
    labels = ["Caída Pasarela", "Fricción Logística", "Inflación CAC"]
    values = [ea["costo_total"], eb["costo_total"], ec["costo_total"]]
    colors = ["#F87171", "#FBBF24", "#FB923C"]

    fig = go.Figure(go.Pie(
        labels       = labels,
        values       = values,
        hole         = 0.65,
        marker       = dict(colors=colors, line=dict(color="#080C14", width=2)),
        textinfo     = "percent",
        textfont     = dict(size=12, color="#CBD5E1"),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} CLP<extra></extra>",
    ))

    total = sum(values)
    fig.add_annotation(
        text     = f"<b>{fmt_clp(total)}</b><br><span style='font-size:11px;color:#64748B'>pérdida total</span>",
        x        = 0.5, y=0.5,
        font     = dict(size=13, color="#F1F5F9"),
        showarrow=False,
        align    = "center",
    )

    fig.update_layout(
        title      = dict(text="Distribución de Costo — 3 Eventos de Estrés", font=dict(size=14, color="#CBD5E1")),
        showlegend = True,
        legend     = dict(font=dict(color="#94A3B8"), bgcolor="#0D1420", bordercolor="#1E2A3A"),
        **PLOTLY_THEME
    )
    return fig


def grafico_funnel_conversion(trafico, pedidos_base, pedidos_estres_a, pedidos_estres_bc):
    """Funnel comparativo: conversión baseline vs estrés."""
    fig = go.Figure()

    etapas = ["Tráfico Total", "Llegan al Checkout", "Completan Pago", "Pedidos Netos"]

    base_vals   = [trafico, trafico * 0.35, trafico * 0.35 * 0.60, pedidos_base]
    estres_vals = [trafico, trafico * 0.35, trafico * 0.35 * 0.30, pedidos_estres_bc]

    fig.add_trace(go.Funnel(
        name            = "Condición Normal",
        y               = etapas,
        x               = base_vals,
        textinfo        = "value+percent initial",
        marker          = dict(color=["#0C2340","#0D3B5A","#0E5280","#4FC3F7"]),
        connector       = dict(line=dict(color="#1E2A3A", dash="dot", width=1)),
        textfont        = dict(color="#CBD5E1"),
    ))

    fig.add_trace(go.Funnel(
        name            = "Con Estrés Operativo",
        y               = etapas,
        x               = estres_vals,
        textinfo        = "value+percent initial",
        marker          = dict(color=["#3B0A0A","#5C1010","#7C1717","#F87171"]),
        connector       = dict(line=dict(color="#1E2A3A", dash="dot", width=1)),
        textfont        = dict(color="#CBD5E1"),
    ))

    fig.update_layout(
        title      = dict(text="Funnel de Conversión: Normal vs. Estrés", font=dict(size=14, color="#CBD5E1")),
        showlegend = True,
        legend     = dict(font=dict(color="#94A3B8"), bgcolor="#0D1420", bordercolor="#1E2A3A"),
        **PLOTLY_THEME
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — PARÁMETROS DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 1.1rem; font-weight: 700; color: #F1F5F9; letter-spacing: -0.01em;">
            ⚡ RetailPulse Latam
        </div>
        <div style="font-size: 0.7rem; color: #475569; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.2rem;">
            Simulador de Estrés Operativo
        </div>
    </div>
    <hr style="border: none; border-top: 1px solid #1E2A3A; margin: 0.5rem 0 1rem 0;" />
    """, unsafe_allow_html=True)

    # ── MÉTRICAS BASE ──
    st.markdown("### 📊 Métricas Base")

    trafico = st.slider(
        "Tráfico Mensual Estimado",
        min_value=5_000, max_value=500_000, value=50_000, step=5_000,
        format="%d visitas",
        help="Visitas únicas mensuales a tu tienda online"
    )

    cr_base_pct = st.slider(
        "Tasa de Conversión Base (%)",
        min_value=0.1, max_value=8.0, value=1.8, step=0.1,
        format="%.1f%%",
        help="% de visitantes que generan un pedido. Promedio Chile: 1.5-2.5%"
    )
    cr_base = cr_base_pct / 100

    aov_clp = st.number_input(
        "Ticket Promedio — AOV (CLP)",
        min_value=5_000, max_value=500_000, value=65_000, step=5_000,
        format="%d",
        help="Valor promedio de cada pedido en pesos chilenos"
    )

    cpc_clp = st.number_input(
        "CPC Promedio Ads (CLP)",
        min_value=10, max_value=3_000, value=180, step=10,
        format="%d",
        help="Costo por clic promedio en Meta/Google Ads en Chile"
    )

    margen_bruto_pct = st.slider(
        "Margen Bruto sobre Venta (%)",
        min_value=5.0, max_value=70.0, value=35.0, step=1.0,
        format="%.0f%%",
        help="% de margen bruto después de costo de producto"
    )
    margen_bruto = margen_bruto_pct / 100

    # ── ESCENARIOS ──
    st.markdown("### 🔥 Escenarios de Estrés")

    activar_a = st.checkbox("Evento A: Caída Pasarela (30 min)", value=True)
    activar_b = st.checkbox("Evento B: Quiebre Stock / Logística", value=True)
    activar_c = st.checkbox("Evento C: CAC +50% (Cyber Bid War)", value=True)

    st.markdown("### ⚙️ Parámetros Avanzados")
    with st.expander("Personalizar supuestos"):
        pct_regiones = st.slider("% Ventas desde Regiones", 10, 60, 38, 1,
                                  help="Default: 38% (dato ACEC Chile)") / 100
        costo_devolucion = st.number_input("Costo Operativo por Devolución (CLP)",
                                            1_000, 50_000, 8_500, 500)
        hora_pico_cyber  = st.checkbox("Caída en hora pico Cyber (4x tráfico)", value=True)

    st.markdown("""
    <hr style="border: none; border-top: 1px solid #1E2A3A; margin: 1.5rem 0 1rem 0;" />
    <div style="font-size: 0.65rem; color: #334155; text-align: center; line-height: 1.6;">
        Modelo v1.0 · Datos contextualizados para Chile<br>
        <a href="https://www.aovalle.com" style="color: #4FC3F7; text-decoration: none;">aovalle.com</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULOS PRINCIPALES
# ─────────────────────────────────────────────────────────────────────────────

baseline = calcular_baseline(trafico, cr_base, aov_clp, cpc_clp, margen_bruto)

# Ejecutar escenarios (siempre se calculan para los gráficos, pero se filtran en UI)
ea = escenario_caida_pasarela(baseline, duracion_minutos=30, hora_pico=hora_pico_cyber)
eb = escenario_quiebre_stock_logistico(baseline, costo_devolucion_clp=costo_devolucion,
                                        pct_ventas_regiones=pct_regiones)
ec = escenario_inflacion_cac(baseline, incremento_cpc_pct=0.50)

# Si un escenario está desactivado, costo = 0 para el total
ea_activo = ea if activar_a else {**ea, "costo_total": 0, "ingreso_perdido": 0, "gasto_quemado_ads": 0}
eb_activo = eb if activar_b else {**eb, "costo_total": 0, "ingreso_perdido_cr": 0, "ltv_perdido": 0}
ec_activo = ec if activar_c else {**ec, "costo_total": 0}

diagnosticos, perdida_total = generar_diagnostico(baseline, ea_activo, eb_activo, ec_activo)

pedidos_estres = baseline["pedidos"] - ea_activo.get("pedidos_perdidos", 0) - eb_activo.get("pedidos_perdidos_cr", 0) if activar_a or activar_b else baseline["pedidos"]


# ─────────────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────────────

# ── HEADER ──
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2rem; margin-bottom: 0.25rem;">
        Simulador de Estrés Operativo
    </h1>
    <p style="color: #475569; font-size: 0.9rem; margin: 0;">
        Cuantifica el impacto financiero de los eventos críticos de Cyber en tu ecommerce · 
        <span style="color: #4FC3F7;">Mercado Chileno · CLP</span>
    </p>
</div>
""", unsafe_allow_html=True)

# ── MÉTRICAS BASELINE (fila 1) ──
st.markdown("#### 📈 Estado Operativo Base")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(metric_card("Ingresos Mensuales", fmt_clp(baseline["ingresos"])), unsafe_allow_html=True)
with col2:
    st.markdown(metric_card("Pedidos / Mes", f"{baseline['pedidos']:,.0f}"), unsafe_allow_html=True)
with col3:
    roas_type = "success" if baseline["roas"] >= 3 else "warning" if baseline["roas"] >= 2 else "danger"
    st.markdown(metric_card("ROAS", f"{baseline['roas']:.2f}x", card_type=roas_type), unsafe_allow_html=True)
with col4:
    ltv_type = "success" if baseline["ltv_cac_ratio"] >= 3 else "warning" if baseline["ltv_cac_ratio"] >= 2 else "danger"
    st.markdown(metric_card("LTV / CAC", f"{baseline['ltv_cac_ratio']:.1f}x", card_type=ltv_type), unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.markdown(metric_card("Margen Contribución", fmt_clp(baseline["contribucion"])), unsafe_allow_html=True)
with col6:
    st.markdown(metric_card("CAC Actual", fmt_clp(baseline["cac"])), unsafe_allow_html=True)
with col7:
    st.markdown(metric_card("LTV Estimado", fmt_clp(baseline["ltv_estimado"])), unsafe_allow_html=True)
with col8:
    st.markdown(metric_card("Gasto Ads / Mes", fmt_clp(baseline["gasto_ads"])), unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── ESCENARIOS DE ESTRÉS ──
st.markdown("#### ⚡ Resultados — Escenarios de Estrés Activos")

s_col1, s_col2, s_col3 = st.columns(3)

with s_col1:
    estado_a = "🔴 ACTIVO" if activar_a else "⚪ Desactivado"
    badge_a  = "badge-red" if activar_a else "badge-blue"
    st.markdown(f"""
    <div class="scenario-header">
        <div class="icon">🔌</div>
        <div>
            <div class="title">Caída de Pasarela</div>
            <div class="subtitle">Webpay / MercadoPago · 30 min pico</div>
        </div>
        <span class="badge {badge_a}" style="margin-left:auto">{estado_a}</span>
    </div>
    """, unsafe_allow_html=True)
    if activar_a:
        st.markdown(metric_card("Ingresos Perdidos", fmt_clp(ea["ingreso_perdido"]),
                                 delta=-ea["ingreso_perdido"], card_type="danger"), unsafe_allow_html=True)
        st.markdown(metric_card("Ads Quemados Sin Retorno", fmt_clp(ea["gasto_quemado_ads"]),
                                 card_type="danger"), unsafe_allow_html=True)
        st.markdown(metric_card("Costo Total Evento A", fmt_clp(ea["costo_total"]),
                                 card_type="danger"), unsafe_allow_html=True)
        st.caption(ea["detalle"])

with s_col2:
    estado_b = "🟡 ACTIVO" if activar_b else "⚪ Desactivado"
    badge_b  = "badge-yellow" if activar_b else "badge-blue"
    st.markdown(f"""
    <div class="scenario-header">
        <div class="icon">📦</div>
        <div>
            <div class="title">Fricción Logística</div>
            <div class="subtitle">Stock / Regiones · Devoluciones x2</div>
        </div>
        <span class="badge {badge_b}" style="margin-left:auto">{estado_b}</span>
    </div>
    """, unsafe_allow_html=True)
    if activar_b:
        st.markdown(metric_card("Costo Devoluciones", fmt_clp(eb["costo_devoluciones"]),
                                 delta=-eb["costo_devoluciones"], card_type="warning"), unsafe_allow_html=True)
        st.markdown(metric_card("Ingresos Perdidos (CR↓)", fmt_clp(eb["ingreso_perdido_cr"]),
                                 delta=-eb["ingreso_perdido_cr"], card_type="warning"), unsafe_allow_html=True)
        st.markdown(metric_card("LTV en Riesgo", fmt_clp(eb["ltv_perdido"]),
                                 card_type="warning"), unsafe_allow_html=True)
        st.caption(eb["detalle"])

with s_col3:
    estado_c = "🟠 ACTIVO" if activar_c else "⚪ Desactivado"
    badge_c  = "badge-yellow" if activar_c else "badge-blue"
    st.markdown(f"""
    <div class="scenario-header">
        <div class="icon">📊</div>
        <div>
            <div class="title">Inflación CAC</div>
            <div class="subtitle">CPC +50% · Saturación Cyber</div>
        </div>
        <span class="badge {badge_c}" style="margin-left:auto">{estado_c}</span>
    </div>
    """, unsafe_allow_html=True)
    if activar_c:
        st.markdown(metric_card("Nuevo CPC Estimado", fmt_clp(ec["cpc_estres"])),
                    unsafe_allow_html=True)
        st.markdown(metric_card("ROAS en Estrés", f"{ec['roas_estres']:.2f}x",
                                 card_type="danger" if ec["roas_estres"] < 2 else "warning"), unsafe_allow_html=True)
        st.markdown(metric_card("CR Mínimo para Equilibrio", f"{ec['cr_minimo_equilibrio']*100:.2f}%",
                                 card_type="warning"), unsafe_allow_html=True)
        st.caption(ec["detalle"])

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── IMPACTO TOTAL ──
perdida_total_activa = ea_activo["costo_total"] + eb_activo["costo_total"] + ec_activo["costo_total"]
pct_ingresos_perdidos = (perdida_total_activa / baseline["ingresos"] * 100) if baseline["ingresos"] > 0 else 0

st.markdown("#### 💸 Impacto Financiero Total Estimado")

t_col1, t_col2, t_col3 = st.columns([2, 1, 1])
with t_col1:
    tipo_impacto = "danger" if pct_ingresos_perdidos > 20 else "warning" if pct_ingresos_perdidos > 10 else "default"
    st.markdown(metric_card(
        "PÉRDIDA TOTAL PROYECTADA (3 EVENTOS)",
        fmt_clp(perdida_total_activa),
        card_type=tipo_impacto
    ), unsafe_allow_html=True)
with t_col2:
    st.markdown(metric_card(
        "% de Ingresos en Riesgo",
        f"{pct_ingresos_perdidos:.1f}%",
        card_type=tipo_impacto
    ), unsafe_allow_html=True)
with t_col3:
    contribucion_estres = baseline["contribucion"] - perdida_total_activa
    st.markdown(metric_card(
        "Margen Contribución Post-Estrés",
        fmt_clp(contribucion_estres),
        delta=contribucion_estres - baseline["contribucion"],
        card_type="danger" if contribucion_estres < 0 else "warning"
    ), unsafe_allow_html=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── VISUALIZACIONES ──
st.markdown("#### 📊 Análisis Visual")

viz_col1, viz_col2 = st.columns(2)
with viz_col1:
    st.plotly_chart(grafico_impacto_waterfall(baseline, ea_activo, eb_activo, ec_activo),
                    use_container_width=True)
with viz_col2:
    st.plotly_chart(grafico_roas_comparativo(baseline, ec),
                    use_container_width=True)

viz_col3, viz_col4 = st.columns(2)
with viz_col3:
    st.plotly_chart(grafico_costo_eventos_donut(ea_activo, eb_activo, ec_activo),
                    use_container_width=True)
with viz_col4:
    pedidos_estres_bc = baseline["pedidos"] * (1 - 0.12) if activar_b else baseline["pedidos"]
    st.plotly_chart(grafico_funnel_conversion(
        trafico,
        baseline["pedidos"],
        ea_activo.get("pedidos_perdidos", 0),
        pedidos_estres_bc
    ), use_container_width=True)

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── DIAGNÓSTICO EJECUTIVO ──
st.markdown("#### 🧠 Diagnóstico Ejecutivo")

for diag in diagnosticos:
    nivel = diag["nivel"]
    box_class = "diagnosis-box" + (" warning" if nivel == "warning" else " ok" if nivel == "ok" else "")

    # Renderizar el box del diagnóstico SIN el CTA adentro.
    # Streamlit sanitiza <a> anidados dentro de divs con estilos inline
    # (los convierte en texto plano). Solución: dos st.markdown() separados.
    st.markdown(f"""
    <div class="{box_class}">
        <div class="diagnosis-title">{diag["titulo"]}</div>
        <div style="font-size: 0.875rem; color: #94A3B8; line-height: 1.7;">
            {diag["cuerpo"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CTA como markdown nativo — Streamlit renderiza links Markdown sin sanitizar
    if diag["cta"]:
        st.markdown(
            '<div style="'
            'margin-top: -0.5rem; margin-bottom: 1rem; '
            'padding: 0.6rem 1.5rem; '
            'background: #0D1420; '
            'border: 1px solid #1E2A3A; border-top: none; '
            'border-radius: 0 0 8px 8px;'
            '">'
            '<a href="https://www.aovalle.com" target="_blank" '
            'style="color: #4FC3F7; font-size: 0.8rem; font-weight: 600; '
            'text-decoration: none; letter-spacing: 0.05em;">'
            '→ Solicitar diagnóstico personalizado · aovalle.com ↗'
            '</a>'
            '</div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ── TABLA RESUMEN ──
with st.expander("📋 Ver tabla resumen de todos los parámetros y resultados"):
    resumen_data = {
        "Métrica": [
            "Tráfico Mensual", "CR Base", "AOV", "CPC Ads",
            "Margen Bruto %", "Ingresos Mensuales", "Gasto Ads",
            "Margen Contribución", "ROAS", "CAC", "LTV Estimado", "LTV/CAC",
            "—", "Pérdida Evento A", "Pérdida Evento B", "Pérdida Evento C",
            "PÉRDIDA TOTAL", "% Ingresos Afectados"
        ],
        "Valor": [
            f"{trafico:,}", f"{cr_base_pct:.1f}%", fmt_clp(aov_clp), fmt_clp(cpc_clp),
            f"{margen_bruto_pct:.0f}%", fmt_clp(baseline["ingresos"]), fmt_clp(baseline["gasto_ads"]),
            fmt_clp(baseline["contribucion"]), f"{baseline['roas']:.2f}x",
            fmt_clp(baseline["cac"]), fmt_clp(baseline["ltv_estimado"]),
            f"{baseline['ltv_cac_ratio']:.1f}x",
            "—",
            fmt_clp(ea_activo["costo_total"]) if activar_a else "Desactivado",
            fmt_clp(eb_activo["costo_total"]) if activar_b else "Desactivado",
            fmt_clp(ec_activo["costo_total"]) if activar_c else "Desactivado",
            fmt_clp(perdida_total_activa), f"{pct_ingresos_perdidos:.1f}%"
        ]
    }
    df_resumen = pd.DataFrame(resumen_data)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)

# ── FOOTER CTA ──
st.markdown(f"""
<div class="footer-cta">
    <div style="font-size: 0.65rem; color: #4FC3F7; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.5rem;">
        ¿TU TIENDA ESTÁ LISTA PARA EL PRÓXIMO CYBER?
    </div>
    <div style="font-size: 1.25rem; font-weight: 700; color: #F1F5F9; margin-bottom: 0.75rem;">
        Este simulador proyecta <span style="color: #F87171;">{fmt_clp(perdida_total_activa)}</span> en riesgo con tus métricas actuales.
    </div>
    <div style="font-size: 0.875rem; color: #64748B; max-width: 600px; margin: 0 auto 1.25rem auto; line-height: 1.7;">
        Alejandro Ovalle trabaja con gerentes de ecommerce chilenos para eliminar los puntos de fricción 
        antes de que se conviertan en pérdidas reales. Diagnóstico estratégico + plan de acción concreto.
    </div>
    <a href="https://www.aovalle.com" target="_blank"
       style="display: inline-block; background: #4FC3F7; color: #080C14; font-weight: 700;
              font-size: 0.85rem; padding: 0.65rem 1.75rem; border-radius: 6px; text-decoration: none;
              letter-spacing: 0.05em; text-transform: uppercase;">
       Solicitar Diagnóstico → aovalle.com
    </a>
    <div style="font-size: 0.65rem; color: #334155; margin-top: 1.5rem;">
        RetailPulse Latam · Herramienta de simulación estratégica · linkedin.com/in/ovallealejandro
    </div>
</div>
""", unsafe_allow_html=True)
