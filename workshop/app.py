"""Portfolio app: the notebook 4 model behind a Streamlit interface.

Run:  streamlit run app.py
"""
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import gamspy as gp

st.set_page_config(page_title="Portfolio optimizer", layout="wide")


@st.cache_data
def load_data():
    returns = pd.read_csv("data/sector_returns_simulated.csv", index_col="date")
    return returns.mean() * 252, returns.cov() * 252


def solve_portfolio(mu, cov, funds, appetite, max_funds):
    """Build and solve the Markowitz model for the chosen funds. Returns weights."""
    mu, cov = mu[funds], cov.loc[funds, funds]
    m = gp.Container()
    s = gp.Set(m, records=funds)
    s2 = gp.Alias(m, alias_with=s)
    MU = gp.Parameter(m, domain=s, records=mu.reset_index())
    COV = gp.Parameter(m, domain=[s, s2], records=cov.stack().reset_index())
    w = gp.Variable(m, domain=s, type="positive")

    budget = gp.Equation(m)
    budget[...] = gp.Sum(s, w[s]) == 1
    equations, problem = [budget], "QCP"

    if max_funds < len(funds):                      # optional cap on holdings -> MIQCP
        y = gp.Variable(m, domain=s, type="binary")
        link = gp.Equation(m, domain=s)
        cap = gp.Equation(m)
        link[s] = w[s] <= y[s]
        cap[...] = gp.Sum(s, y[s]) <= max_funds
        equations, problem = equations + [link, cap], "MIQCP"

    risk = gp.Sum((s, s2), w[s] * COV[s, s2] * w[s2])
    ret = gp.Sum(s, MU[s] * w[s])
    portfolio = gp.Model(m, equations=equations, problem=problem,
                         sense="min", objective=risk - appetite * ret)
    portfolio.solve(solver="CPLEX")
    return w.records.set_index("s")["level"].reindex(funds).fillna(0)


@st.cache_data
def frontier(funds, max_funds):
    mu, cov = load_data()
    pts = []
    for lam in [0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 3]:
        W = solve_portfolio(mu, cov, list(funds), lam, max_funds)
        pts.append({"risk": float(np.sqrt(W @ cov.loc[W.index, W.index] @ W)),
                    "return": float(mu[W.index] @ W)})
    return pd.DataFrame(pts)


mu, cov = load_data()

st.title("Portfolio optimizer")
st.caption("Markowitz mean-variance model in GAMSPy. Data: simulated returns for 12 fictional sector funds.")

with st.sidebar:
    st.header("Your choices")
    funds = st.multiselect("Funds you may invest in", mu.index.tolist(), default=mu.index.tolist())
    appetite = st.slider("Risk appetite (λ)", 0.0, 3.0, 0.5, 0.05,
                         help="0 = least risk; higher = chase return")
    max_funds = st.slider("Maximum number of funds", 1, max(len(funds), 1), max(len(funds), 1))

if len(funds) < 2:
    st.warning("Pick at least two funds.")
    st.stop()

W = solve_portfolio(mu, cov, funds, appetite, max_funds)
port_ret = float(mu[funds] @ W)
port_risk = float(np.sqrt(W @ cov.loc[funds, funds] @ W))

c1, c2, c3 = st.columns(3)
c1.metric("Expected yearly return", f"{port_ret:.1%}")
c2.metric("Risk (volatility)", f"{port_risk:.1%}")
c3.metric("Funds held", int((W > 0.005).sum()))

CHART_HEIGHT = 520


def styled(chart):
    """Make a chart tall, with large, easy-to-read labels."""
    return (chart.properties(height=CHART_HEIGHT)
            .configure_axis(labelFontSize=15, titleFontSize=16, titlePadding=12, labelLimit=250)
            .configure_legend(labelFontSize=15, symbolSize=200))


left, right = st.columns(2)
with left:
    st.subheader("Allocation")
    alloc = W[W > 0.005].rename_axis("fund").reset_index(name="weight")
    bars = alt.Chart(alloc).mark_bar(color="#F4961A").encode(
        x=alt.X("weight:Q", title="Share of portfolio", axis=alt.Axis(format="%")),
        y=alt.Y("fund:N", title=None, sort="-x"))
    st.altair_chart(styled(bars), width="stretch")
with right:
    st.subheader("Where you are on the frontier")
    front = frontier(tuple(funds), max_funds)
    front = front.assign(series="efficient frontier")
    you = pd.DataFrame([{"risk": port_risk, "return": port_ret, "series": "your portfolio"}])
    x = alt.X("risk:Q", title="Risk (volatility)", axis=alt.Axis(format="%"), scale=alt.Scale(zero=False))
    y = alt.Y("return:Q", title="Expected yearly return", axis=alt.Axis(format="%"), scale=alt.Scale(zero=False))
    series = ["efficient frontier", "your portfolio"]
    color = alt.Color("series:N", scale=alt.Scale(domain=series, range=["#8A8A8A", "#F4961A"]),
                      legend=alt.Legend(title=None, orient="bottom"))
    shape = alt.Shape("series:N", scale=alt.Scale(domain=series, range=["circle", "diamond"]))
    line = alt.Chart(front).mark_line(point=True).encode(x=x, y=y, color=color)
    dot = alt.Chart(you).mark_point(size=400, filled=True, opacity=1, stroke="black",
                                    strokeWidth=1.5).encode(x=x, y=y, color=color, shape=shape)
    st.altair_chart(styled(line + dot), width="stretch")
