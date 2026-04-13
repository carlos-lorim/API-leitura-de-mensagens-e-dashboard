"""
dashboard.py — Dashboard simples de atendimento.
Rode: python dashboard.py -> http://127.0.0.1:8050
"""

import sqlite3
import datetime
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output

DB_PATH = "atendimento.db"

# ── CORES ─────────────────────────────────────────────────────────────
AZUL     = "#2563eb"
VERMELHO = "#dc2626"
AMARELO  = "#d97706"
VERDE    = "#059669"
FUNDO    = "#f5f6fa"
BRANCO   = "#ffffff"
BORDA    = "#e2e8f0"
TEXTO    = "#1e293b"
CINZA    = "#64748b"

COR_PRI = {"CRITICA": VERMELHO, "ALTA": AMARELO, "MEDIA": VERDE}
COR_INT = {"COMPRA": AZUL, "PROBLEMA_TECNICO": VERMELHO, "DUVIDA_GERAL": VERDE}


def carregar_dados():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM atendimentos ORDER BY timestamp DESC", conn)
        conn.close()
        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["data"] = df["timestamp"].dt.date
        return df
    except Exception:
        return pd.DataFrame()


def graf_base():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(color=CINZA, family="Arial", size=11),
    )


# ── APP ───────────────────────────────────────────────────────────────
app = Dash(__name__, title="Dashboard Atendimento")

app.layout = html.Div(
    style={"background": FUNDO, "minHeight": "100vh",
           "fontFamily": "Arial, sans-serif", "padding": "24px"},
    children=[

        # Cabeçalho
        html.Div(style={
            "background": BRANCO, "borderRadius": "10px",
            "padding": "20px 28px", "marginBottom": "20px",
            "border": f"1px solid {BORDA}",
            "display": "flex", "justifyContent": "space-between", "alignItems": "center",
        }, children=[
            html.Div([
                html.H1("Dashboard de Atendimento", style={
                    "margin": 0, "fontSize": "20px",
                    "fontWeight": "700", "color": TEXTO,
                }),
                html.Div(id="subtitulo", style={"color": CINZA, "fontSize": "13px", "marginTop": "2px"}),
            ]),
            html.Div(id="status-badge"),
        ]),

        # KPIs
        html.Div(id="kpis", style={
            "display": "grid",
            "gridTemplateColumns": "repeat(4, 1fr)",
            "gap": "16px", "marginBottom": "20px",
        }),

        # Gráficos — linha 1
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "2fr 1fr",
            "gap": "16px", "marginBottom": "16px",
        }, children=[
            html.Div(style={
                "background": BRANCO, "borderRadius": "10px",
                "padding": "20px", "border": f"1px solid {BORDA}",
            }, children=[
                html.Div("Atendimentos por Dia", style={
                    "fontWeight": "700", "color": TEXTO,
                    "marginBottom": "16px", "fontSize": "14px",
                }),
                dcc.Graph(id="g-linha", config={"displayModeBar": False},
                          style={"height": "200px"}),
            ]),
            html.Div(style={
                "background": BRANCO, "borderRadius": "10px",
                "padding": "20px", "border": f"1px solid {BORDA}",
            }, children=[
                html.Div("Por Intenção", style={
                    "fontWeight": "700", "color": TEXTO,
                    "marginBottom": "16px", "fontSize": "14px",
                }),
                dcc.Graph(id="g-intencao", config={"displayModeBar": False},
                          style={"height": "200px"}),
            ]),
        ]),

        # Gráficos — linha 2
        html.Div(style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr",
            "gap": "16px", "marginBottom": "20px",
        }, children=[
            html.Div(style={
                "background": BRANCO, "borderRadius": "10px",
                "padding": "20px", "border": f"1px solid {BORDA}",
            }, children=[
                html.Div("Prioridade", style={
                    "fontWeight": "700", "color": TEXTO,
                    "marginBottom": "16px", "fontSize": "14px",
                }),
                dcc.Graph(id="g-prioridade", config={"displayModeBar": False},
                          style={"height": "180px"}),
            ]),
            html.Div(style={
                "background": BRANCO, "borderRadius": "10px",
                "padding": "20px", "border": f"1px solid {BORDA}",
            }, children=[
                html.Div("Intenção × Prioridade", style={
                    "fontWeight": "700", "color": TEXTO,
                    "marginBottom": "16px", "fontSize": "14px",
                }),
                dcc.Graph(id="g-heat", config={"displayModeBar": False},
                          style={"height": "180px"}),
            ]),
        ]),

        # Tabela
        html.Div(style={
            "background": BRANCO, "borderRadius": "10px",
            "padding": "20px", "border": f"1px solid {BORDA}",
        }, children=[
            html.Div("Registros Recentes", style={
                "fontWeight": "700", "color": TEXTO,
                "marginBottom": "16px", "fontSize": "14px",
            }),
            html.Div(id="tabela"),
        ]),

        dcc.Interval(id="tick", interval=10_000, n_intervals=0),
    ]
)


@app.callback(
    Output("kpis",        "children"),
    Output("subtitulo",   "children"),
    Output("status-badge","children"),
    Output("g-linha",     "figure"),
    Output("g-intencao",  "figure"),
    Output("g-prioridade","figure"),
    Output("g-heat",      "figure"),
    Output("tabela",      "children"),
    Input("tick", "n_intervals"),
)
def atualizar(_):
    df   = carregar_dados()
    hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sub  = f"Última atualização: {hora}"
    vazio = go.Figure(layout={**graf_base(),
        "annotations": [dict(text="Sem dados", x=0.5, y=0.5,
                             showarrow=False, font=dict(color=CINZA))]})

    # SEM DADOS
    if df.empty:
        kpis = _kpis(0, 0, 0, 0)
        badge = _badge("Sem dados", CINZA)
        sem = html.P("Nenhum registro encontrado.", style={"color": CINZA, "fontSize": "13px"})
        return kpis, sub, badge, vazio, vazio, vazio, vazio, sem

    total    = len(df)
    criticos = int((df["prioridade"] == "CRITICA").sum())
    altas    = int((df["prioridade"] == "ALTA").sum())
    unicos   = int(df["cliente"].nunique())
    pct      = round(criticos / total * 100)

    # Badge
    if pct > 30:
        badge = _badge(f"⚠ {pct}% críticos", VERMELHO)
    else:
        badge = _badge("● Operação normal", VERDE)

    # KPIs
    kpis = _kpis(total, criticos, altas, unicos)

    # Gráfico linha
    por_dia = df.groupby("data").size().reset_index(name="n")
    por_dia["ds"] = por_dia["data"].astype(str)
    g_linha = go.Figure()
    g_linha.add_trace(go.Scatter(
        x=por_dia["ds"], y=por_dia["n"],
        mode="lines+markers",
        line=dict(color=AZUL, width=2),
        marker=dict(size=6, color=AZUL),
        fill="tozeroy", fillcolor="rgba(37,99,235,0.07)",
    ))
    g_linha.update_layout(**graf_base(), showlegend=False,
        xaxis=dict(gridcolor=BORDA, tickfont=dict(color=CINZA)),
        yaxis=dict(gridcolor=BORDA, tickfont=dict(color=CINZA)))

    # Donut intenção
    vi = df["intencao"].value_counts().reset_index()
    vi.columns = ["intencao", "n"]
    g_int = go.Figure(go.Pie(
        labels=[i.replace("_", " ").title() for i in vi["intencao"]],
        values=vi["n"], hole=0.55,
        marker_colors=[COR_INT.get(i, AZUL) for i in vi["intencao"]],
        textfont=dict(size=11),
    ))
    g_int.update_layout(**graf_base(), showlegend=True,
        legend=dict(orientation="v", x=0.75, y=0.5,
                    font=dict(size=10, color=CINZA)))

    # Barras prioridade
    ordem = ["CRITICA", "ALTA", "MEDIA"]
    vp    = df["prioridade"].value_counts().reindex(ordem, fill_value=0).reset_index()
    vp.columns = ["prioridade", "n"]
    pcts  = (vp["n"] / total * 100).round(1)
    g_pri = go.Figure(go.Bar(
        x=vp["n"], y=vp["prioridade"], orientation="h",
        marker_color=[COR_PRI.get(p, AZUL) for p in vp["prioridade"]],
        marker_line_width=0,
        text=[f"{v}%" for v in pcts],
        textposition="outside",
        textfont=dict(color=CINZA, size=11),
    ))
    g_pri.update_layout(**graf_base(), showlegend=False, bargap=0.4,
        xaxis=dict(showgrid=False, tickfont=dict(color=CINZA)),
        yaxis=dict(tickfont=dict(color=CINZA)))

    # Heatmap
    heat = df.groupby(["intencao", "prioridade"]).size().unstack(fill_value=0)
    g_heat = go.Figure(go.Heatmap(
        z=heat.values,
        x=list(heat.columns),
        y=[r.replace("_", " ").title() for r in heat.index],
        colorscale=[[0, "#eff6ff"], [1, AZUL]],
        showscale=False,
        text=heat.values, texttemplate="%{text}",
        textfont=dict(size=13, color=TEXTO),
        xgap=3, ygap=3,
    ))
    g_heat.update_layout(**graf_base(),
        xaxis=dict(showgrid=False, tickfont=dict(color=CINZA)),
        yaxis=dict(showgrid=False, tickfont=dict(color=CINZA)))

    # Tabela
    cols  = ["timestamp", "cliente", "intencao", "prioridade", "mensagem"]
    df_t  = df[cols].head(15).copy()
    df_t["timestamp"] = df_t["timestamp"].dt.strftime("%d/%m %H:%M")
    nomes = {"timestamp": "Horário", "cliente": "Cliente",
             "intencao": "Intenção", "prioridade": "Prioridade", "mensagem": "Mensagem"}
    tabela = dash_table.DataTable(
        data=df_t.to_dict("records"),
        columns=[{"name": nomes[c], "id": c} for c in cols],
        style_table={"overflowX": "auto"},
        style_header={
            "backgroundColor": FUNDO, "color": CINZA,
            "fontWeight": "600", "fontSize": "11px",
            "textTransform": "uppercase", "letterSpacing": "0.5px",
            "border": "none", "borderBottom": f"2px solid {BORDA}",
            "padding": "10px 14px",
        },
        style_cell={
            "backgroundColor": BRANCO, "color": TEXTO,
            "fontSize": "13px", "padding": "10px 14px",
            "border": "none", "borderBottom": f"1px solid {BORDA}",
            "textAlign": "left", "maxWidth": "280px",
            "overflow": "hidden", "textOverflow": "ellipsis",
        },
        style_data_conditional=[
            {"if": {"filter_query": '{prioridade} = "CRITICA"'},
             "color": VERMELHO, "fontWeight": "700"},
            {"if": {"filter_query": '{prioridade} = "ALTA"'},
             "color": AMARELO, "fontWeight": "600"},
            {"if": {"filter_query": '{prioridade} = "MEDIA"'},
             "color": VERDE},
            {"if": {"row_index": "odd"}, "backgroundColor": FUNDO},
        ],
        page_size=10,
        style_as_list_view=True,
    )

    return kpis, sub, badge, g_linha, g_int, g_pri, g_heat, tabela


def _kpis(total, criticos, altas, unicos):
    itens = [
        ("Total",        total,    AZUL,     "📋"),
        ("Críticos",     criticos, VERMELHO, "🔴"),
        ("Alta Prior.",  altas,    AMARELO,  "🟡"),
        ("Clientes",     unicos,   VERDE,    "👥"),
    ]
    cards = []
    for titulo, valor, cor, icone in itens:
        cards.append(html.Div(style={
            "background": BRANCO, "borderRadius": "10px",
            "padding": "20px", "border": f"1px solid {BORDA}",
            "borderTop": f"4px solid {cor}",
        }, children=[
            html.Div(style={"display": "flex", "justifyContent": "space-between",
                            "alignItems": "center", "marginBottom": "10px"}, children=[
                html.Span(titulo, style={
                    "fontSize": "11px", "textTransform": "uppercase",
                    "letterSpacing": "0.8px", "color": CINZA, "fontWeight": "600",
                }),
                html.Span(icone, style={"fontSize": "18px"}),
            ]),
            html.Div(str(valor), style={
                "fontSize": "38px", "fontWeight": "800",
                "color": cor, "lineHeight": "1",
            }),
        ]))
    return cards


def _badge(texto, cor):
    return html.Div(texto, style={
        "background": cor + "18",
        "color": cor,
        "border": f"1px solid {cor}40",
        "borderRadius": "20px",
        "padding": "6px 16px",
        "fontSize": "12px",
        "fontWeight": "600",
    })


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)