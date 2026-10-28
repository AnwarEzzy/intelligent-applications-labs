"""TP2 : tableau de bord Auto MPG et estimation Random Forest."""

import plotly.express as px
import streamlit as st

from data_processing import display_table, filter_vehicles, load_vehicles
from model import predict_consumption, train_model


COLORS = {"usa": "#d76b44", "japan": "#159b8d", "europe": "#7469b6"}
ORIGIN_NAMES = {"usa": "États-Unis", "japan": "Japon", "europe": "Europe"}

st.set_page_config(
    page_title="AutoScope · TP2",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {background: #f6f4ef; color: #193044;}
    .block-container {max-width: 1390px; padding-top: 2rem; padding-bottom: 3rem;}
    [data-testid="stSidebar"] {background: #102a3b; border-right: 0;}
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {color: #f1f7f6 !important;}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {color: #acc8c9 !important;}
    [data-testid="stSidebar"] hr {border-color: #315064;}
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid #e4e9e5; border-radius: 18px;
        padding: 1.2rem 1.35rem; box-shadow: 0 8px 24px rgba(15, 42, 59, .045);
    }
    [data-testid="stMetricLabel"] {color: #5e737c;}
    [data-testid="stMetricValue"] {color: #163949;}
    [data-testid="stTabs"] [role="tablist"] {
        background: #e7ece8; border-radius: 14px; padding: .25rem; gap: .25rem;
        border-bottom: none;
    }
    [data-testid="stTabs"] [role="tab"] {border-radius: 10px; padding: .55rem 1rem;}
    [data-testid="stTabs"] [aria-selected="true"] {background: #fff; color: #087e74;}
    .hero {
        padding: 2.2rem 2.5rem; margin-bottom: 1.5rem; border-radius: 24px;
        color: #f4fbf7; background: linear-gradient(115deg, #102a3b 0%, #174c56 62%, #147d78 100%);
        box-shadow: 0 18px 32px rgba(16, 42, 59, .12);
    }
    .hero .eyebrow {font-size: .77rem; letter-spacing: .15em; font-weight: 750; color: #a7e0d5;}
    .hero h1 {color: #fff; font-size: clamp(2rem, 4vw, 3.1rem); margin: .5rem 0 .35rem;}
    .hero p {color: #d4e9e7; margin: 0; max-width: 720px; line-height: 1.55;}
    .section-kicker {color: #087e74; font-size: .78rem; font-weight: 750; letter-spacing: .13em; margin: 1.3rem 0 .2rem;}
    .note {
        padding: .85rem 1.1rem; background: #e7f4ef; border-left: 4px solid #159b8d;
        border-radius: 10px; color: #24534e; margin: 1rem 0;
    }
    div.stFormSubmitButton > button[kind="primary"] {
        background: #087e74; border-color: #087e74; border-radius: 11px;
    }
    @media (max-width: 640px) {
        .hero {padding: 1.5rem;}
        .block-container {padding-top: 1rem;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def get_data():
    return load_vehicles()


@st.cache_resource
def get_model():
    # Les filtres d'affichage ne changent pas le jeu d'entraînement.
    return train_model(get_data())


def show_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(color="#425b65", family="Arial, sans-serif"),
        title_font=dict(color="#193044", size=17),
        margin=dict(l=22, r=20, t=65, b=25),
        height=390,
        legend_title_text="Origine",
    )
    st.plotly_chart(fig, width="stretch")


try:
    vehicles = get_data()
except (OSError, ValueError) as exc:
    st.error(f"Impossible de charger data/mpg.csv : {exc}")
    st.stop()

all_origins = sorted(vehicles["origin"].unique().tolist())
all_cylinders = sorted(int(value) for value in vehicles["cylinders"].unique())
first_year = int(vehicles["year"].min())
last_year = int(vehicles["year"].max())

with st.sidebar:
    st.caption("AUTOSCOPE / LABORATOIRE 02")
    st.title("Affiner le parc")
    st.write("Composez votre sélection pour explorer les données historiques.")
    st.divider()
    selected_origins = st.multiselect(
        "Pays ou région", all_origins, default=all_origins,
        format_func=lambda value: ORIGIN_NAMES[value],
    )
    selected_years = st.slider(
        "Période", first_year, last_year, (first_year, last_year)
    )
    selected_cylinders = st.multiselect(
        "Cylindres", all_cylinders, default=all_cylinders
    )
    minimum_mpg = st.slider(
        "Efficacité minimale (mpg)",
        float(vehicles["mpg"].min()),
        float(vehicles["mpg"].max()),
        float(vehicles["mpg"].min()),
        step=0.5,
    )
    st.divider()
    st.caption("Données : Auto MPG, 1970–1982. Les filtres s'appliquent au tableau de bord et au catalogue.")

filtered = filter_vehicles(
    vehicles, selected_origins, selected_years, selected_cylinders, minimum_mpg
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">TP 02 &nbsp;·&nbsp; DATA & MACHINE LEARNING</div>
        <h1>AutoScope</h1>
        <p>Explorer l'efficacité des voitures des années 70 et estimer leur
        consommation avec un modèle Random Forest.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

dashboard_tab, catalogue_tab, prediction_tab = st.tabs(
    ["Vue d'ensemble", "Catalogue des véhicules", "Estimation ML"]
)

with dashboard_tab:
    st.markdown('<div class="section-kicker">01 / EXPLORATION</div>', unsafe_allow_html=True)
    st.subheader("Le parc en un regard")

    if filtered.empty:
        st.warning("Aucun véhicule ne correspond à ces filtres. Élargissez la sélection dans la barre latérale.")
    else:
        kpis = st.columns(4)
        kpis[0].metric("Véhicules sélectionnés", f"{len(filtered)} / {len(vehicles)}")
        kpis[1].metric("Consommation moyenne", f"{filtered['consumption_l_100km'].mean():.1f} L/100 km")
        kpis[2].metric("Puissance moyenne", f"{filtered['horsepower'].mean():.1f} hp")
        kpis[3].metric("Efficacité moyenne", f"{filtered['mpg'].mean():.1f} mpg")

        st.markdown(
            '<div class="note"><strong>Comment lire les valeurs :</strong> une consommation '
            'en L/100 km plus basse et une efficacité en mpg plus haute indiquent '
            'un véhicule plus sobre.</div>',
            unsafe_allow_html=True,
        )

        chart_data = filtered.assign(origin_label=filtered["origin"].map(ORIGIN_NAMES))
        scatter = px.scatter(
            chart_data,
            x="weight_kg", y="consumption_l_100km", color="origin_label",
            hover_name="name",
            color_discrete_map={ORIGIN_NAMES[k]: v for k, v in COLORS.items()},
            labels={
                "weight_kg": "Poids (kg)",
                "consumption_l_100km": "Consommation (L/100 km)",
                "origin_label": "Origine",
            },
            title="Le poids influence-t-il la consommation ?",
        )
        scatter.update_traces(marker=dict(size=9, opacity=0.72))
        show_chart(scatter)

        origin_summary = (
            chart_data.groupby("origin_label", as_index=False)
            .agg(
                vehicles=("mpg", "size"),
                consumption=("consumption_l_100km", "mean"),
            )
        )
        left, right = st.columns([1.1, 0.9])
        with left:
            comparison = px.bar(
                origin_summary.sort_values("consumption"),
                x="consumption", y="origin_label", orientation="h",
                color="origin_label",
                color_discrete_map={ORIGIN_NAMES[k]: v for k, v in COLORS.items()},
                text="consumption",
                labels={"consumption": "L/100 km", "origin_label": "Origine"},
                title="Consommation moyenne par origine",
            )
            comparison.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            comparison.update_layout(showlegend=False)
            show_chart(comparison)
        with right:
            distribution = px.pie(
                origin_summary,
                values="vehicles", names="origin_label", hole=0.66,
                color="origin_label",
                color_discrete_map={ORIGIN_NAMES[k]: v for k, v in COLORS.items()},
                title="Répartition des véhicules",
            )
            distribution.update_traces(textinfo="percent+label", textposition="outside")
            show_chart(distribution)

        yearly = filtered.groupby("year", as_index=False)["mpg"].mean()
        trend = px.area(
            yearly, x="year", y="mpg",
            labels={"year": "Année du modèle", "mpg": "Efficacité moyenne (mpg)"},
            title="L'efficacité au fil des années",
        )
        trend.update_traces(line_color="#159b8d", fillcolor="rgba(21,155,141,.17)")
        show_chart(trend)
        st.caption("Les moyennes ignorent les puissances manquantes. La consommation moyenne est calculée véhicule par véhicule.")

with catalogue_tab:
    st.markdown('<div class="section-kicker">02 / DONNÉES</div>', unsafe_allow_html=True)
    st.subheader("Explorer les véhicules")
    st.write("Le tableau et la fiche suivent les filtres de la barre latérale.")
    if filtered.empty:
        st.warning("La sélection est vide. Modifiez les filtres pour voir le catalogue.")
    else:
        st.dataframe(display_table(filtered), width="stretch", hide_index=True, height=430)
        selected_index = st.selectbox(
            "Afficher la fiche d'un véhicule",
            filtered.index.tolist(),
            format_func=lambda index: (
                f"{vehicles.at[index, 'name'].title()} · {vehicles.at[index, 'year']}"
            ),
        )
        selected = vehicles.loc[selected_index]
        st.markdown(f"#### {selected['name'].title()}")
        st.caption(f"{ORIGIN_NAMES[selected['origin']]} · {selected['year']} · {int(selected['cylinders'])} cylindres")
        card_cols = st.columns(3)
        card_cols[0].metric("Consommation", f"{selected['consumption_l_100km']:.1f} L/100 km")
        card_cols[1].metric("Puissance", "Non renseignée" if selected['horsepower'] != selected['horsepower'] else f"{selected['horsepower']:.0f} hp")
        card_cols[2].metric("Poids", f"{selected['weight_kg']:.0f} kg")

with prediction_tab:
    st.markdown('<div class="section-kicker">03 / MODÈLE</div>', unsafe_allow_html=True)
    st.subheader("Simuler une voiture historique")
    st.write("Renseignez ses caractéristiques pour obtenir une estimation en L/100 km.")
    model = get_model()

    with st.form("prediction_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            year = st.slider("Année du modèle", first_year, last_year, 1976, key="predict_year")
            origin = st.selectbox("Origine du véhicule", all_origins, format_func=lambda value: ORIGIN_NAMES[value])
            cylinders = st.selectbox("Nombre de cylindres", all_cylinders, index=all_cylinders.index(4))
            displacement = st.number_input(
                "Cylindrée (pouces³)", min_value=60.0, max_value=460.0, value=140.0, step=1.0
            )
        with col_b:
            horsepower = st.number_input(
                "Puissance (hp)", min_value=40.0, max_value=240.0, value=90.0, step=1.0
            )
            weight_kg = st.number_input(
                "Poids (kg)", min_value=700.0, max_value=2400.0, value=1150.0, step=10.0
            )
            acceleration = st.number_input(
                "Accélération 0–60 mph (s)",
                min_value=8.0, max_value=25.0, value=15.0, step=0.1,
            )
        submitted = st.form_submit_button("Calculer l'estimation", type="primary")

    if submitted:
        consumption, mpg = predict_consumption(
            model,
            cylinders=cylinders,
            displacement=displacement,
            horsepower=horsepower,
            weight_kg=weight_kg,
            acceleration=acceleration,
            year=year,
            origin=origin,
        )
        st.success("Estimation calculée à partir des véhicules historiques Auto MPG.")
        result_cols = st.columns(2)
        result_cols[0].metric("Consommation estimée", f"{consumption:.1f} L/100 km")
        result_cols[1].metric("Efficacité équivalente", f"{mpg:.1f} mpg")

    with st.expander("Comment fonctionne le modèle ?"):
        st.write(
            "RandomForestRegressor utilise les cylindres, la cylindrée, la puissance, "
            "le poids, l'accélération, l'année et l'origine. Les filtres du tableau de "
            "bord ne modifient pas son entraînement."
        )
        score_cols = st.columns(3)
        score_cols[0].metric("Erreur moyenne (MAE)", f"{model.mae:.2f} L/100 km")
        score_cols[1].metric("Score R²", f"{model.r2:.2f}")
        score_cols[2].metric("Entraînement / test", f"{model.train_size} / {model.test_size}")
        st.caption("Séparation 80/20 avec graine fixe. Puissances absentes imputées dans le pipeline.")
    st.caption("Démonstration pédagogique fondée sur des voitures de 1970 à 1982 ; estimation non adaptée aux véhicules modernes.")

st.divider()
st.caption("Données : Auto MPG, Quinlan (1993), UCI Machine Learning Repository (CC BY 4.0). Copie CSV : mwaskom/seaborn-data.")
