"""
charts.py
=========
Plotly chart builders for the dashboard, following a consistent
design system:

- validated categorical palette (light + dark selected separately)
- one axis per chart, recessive hairline grid, no chart junk
- thin marks, rounded bars, unified hover layer
- text in ink tokens, never in series colors
"""

import pandas as pd
import plotly.graph_objects as go

# Validated palette (see dataviz reference; both modes pass the validator).
_P = {
    "light": {
        "surface": "rgba(0,0,0,0)",
        "ink": "#0b0b0b", "ink2": "#52514e", "muted": "#898781",
        "grid": "#e1e0d9", "axis": "#c3c2b7",
        "blue": "#2a78d6", "aqua": "#1baf7a", "yellow": "#eda100",
        "red": "#e34948", "orange": "#eb6834", "violet": "#4a3aa7",
    },
    "dark": {
        "surface": "rgba(0,0,0,0)",
        "ink": "#ffffff", "ink2": "#c3c2b7", "muted": "#898781",
        "grid": "#2c2c2a", "axis": "#383835",
        "blue": "#3987e5", "aqua": "#199e70", "yellow": "#c98500",
        "red": "#e66767", "orange": "#d95926", "violet": "#9085e9",
    },
}

FONT = 'system-ui, -apple-system, "Segoe UI", sans-serif'


def _theme(dark: bool) -> dict:
    return _P["dark" if dark else "light"]


def _base_layout(fig: go.Figure, t: dict, title: str, y_title: str = "",
                 y_range=None, showlegend=False):
    fig.update_layout(
        title=dict(text=title, font=dict(family=FONT, size=15, color=t["ink"]),
                   x=0, xanchor="left"),
        font=dict(family=FONT, size=12, color=t["ink2"]),
        paper_bgcolor=t["surface"], plot_bgcolor=t["surface"],
        margin=dict(l=8, r=8, t=44, b=8),
        height=300,
        showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0,
                    font=dict(color=t["ink2"], size=11),
                    bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
        hoverlabel=dict(font=dict(family=FONT, size=12)),
    )
    fig.update_xaxes(showgrid=False, linecolor=t["axis"], tickcolor=t["axis"],
                     tickfont=dict(color=t["muted"]))
    fig.update_yaxes(title=dict(text=y_title, font=dict(color=t["muted"], size=11)),
                     gridcolor=t["grid"], gridwidth=1, zeroline=False,
                     showline=False, tickfont=dict(color=t["muted"]),
                     range=y_range)
    return fig


def _empty(t: dict, title: str, msg: str = "No data yet — log a workout and it appears here."):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False,
                       font=dict(family=FONT, size=13, color=t["muted"]))
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return _base_layout(fig, t, title)


def bar(df: pd.DataFrame, x: str, y: str, title: str, color_key: str = "blue",
        y_title: str = "", dark: bool = True, pct: bool = False,
        hover_fmt: str = "%{y:.0f}"):
    t = _theme(dark)
    if df is None or df.empty:
        return _empty(t, title)
    is_dt = pd.api.types.is_datetime64_any_dtype(df[x])
    fig = go.Figure(go.Bar(
        x=df[x], y=df[y],
        marker=dict(color=t[color_key], cornerradius=4,
                    line=dict(width=0)),
        # fixed ~16h bar width on date axes so a lone data point stays a bar
        width=16 * 3600 * 1000 if is_dt else None,
        hovertemplate=hover_fmt + "<extra></extra>",
    ))
    fig.update_layout(bargap=0.35)
    fig = _base_layout(fig, t, title, y_title,
                       y_range=[0, 105] if pct else None)
    if is_dt:
        fig.update_xaxes(tickformat="%d %b", hoverformat="%a %d %b")
    return fig


def line(df: pd.DataFrame, x: str, y: str, title: str, color_key: str = "blue",
         y_title: str = "", dark: bool = True, y_range=None,
         hover_fmt: str = "%{y:.1f}", fill: bool = False):
    t = _theme(dark)
    if df is None or df.empty:
        return _empty(t, title)
    hx = t[color_key].lstrip("#")
    rgba = f"rgba({int(hx[0:2],16)},{int(hx[2:4],16)},{int(hx[4:6],16)},0.10)"
    fig = go.Figure(go.Scatter(
        x=df[x], y=df[y], mode="lines+markers",
        line=dict(color=t[color_key], width=2),
        marker=dict(size=7, color=t[color_key],
                    line=dict(width=2, color="#1a1a19" if dark else "#fcfcfb")),
        fill="tozeroy" if fill else None,
        fillcolor=rgba if fill else None,
        hovertemplate=hover_fmt + "<extra></extra>",
    ))
    fig = _base_layout(fig, t, title, y_title, y_range=y_range)
    if pd.api.types.is_datetime64_any_dtype(df[x]):
        fig.update_xaxes(tickformat="%d %b", hoverformat="%a %d %b")
    return fig


def pain_chart(df: pd.DataFrame, dark: bool = True, title: str | None = None):
    """Average daily pain with the 3/10 caution and 5/10 stop guides."""
    t = _theme(dark)
    title = title or "Pain trend (session average, 0-10)"
    if df is None or df.empty:
        return _empty(t, title, "Log pain scores during workouts to see the trend.")
    fig = go.Figure(go.Scatter(
        x=df["log_date"], y=df["avg_pain"], mode="lines+markers",
        name="Avg pain",
        line=dict(color=t["red"], width=2),
        marker=dict(size=7, color=t["red"],
                    line=dict(width=2, color="#1a1a19" if dark else "#fcfcfb")),
        hovertemplate="avg %{y:.1f}/10<extra></extra>",
    ))
    fig.add_hline(y=3, line=dict(color=t["muted"], width=1, dash="dot"),
                  annotation_text="modify ≥3", annotation_position="right",
                  annotation_font=dict(size=10, color=t["muted"]))
    fig.add_hline(y=5, line=dict(color=t["red"], width=1, dash="dot"),
                  annotation_text="stop ≥5", annotation_position="right",
                  annotation_font=dict(size=10, color=t["muted"]))
    fig = _base_layout(fig, t, title, "pain /10", y_range=[0, 10])
    fig.update_xaxes(tickformat="%d %b", hoverformat="%a %d %b")
    return fig


def weight_chart(df: pd.DataFrame, dark: bool = True, title: str | None = None):
    t = _theme(dark)
    title = title or "Body weight (kg)"
    if df is None or df.empty:
        return _empty(t, title, "Log your body weight in the Recovery tab.")
    fig = go.Figure(go.Scatter(
        x=df["log_date"], y=df["weight_kg"], mode="lines+markers",
        line=dict(color=t["blue"], width=2, shape="spline", smoothing=0.6),
        marker=dict(size=7, color=t["blue"],
                    line=dict(width=2, color="#1a1a19" if dark else "#fcfcfb")),
        hovertemplate="%{y:.1f} kg<extra></extra>",
    ))
    lo = df["weight_kg"].min() - 1.5
    hi = df["weight_kg"].max() + 1.5
    fig = _base_layout(fig, t, title, "kg", y_range=[lo, hi])
    fig.update_xaxes(tickformat="%d %b", hoverformat="%a %d %b")
    return fig
