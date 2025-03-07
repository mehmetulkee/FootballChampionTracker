import streamlit as st
import pandas as pd
import plotly.express as px
from data_manager import DataManager
from utils import calculate_points

# Sayfa yapılandırması
st.set_page_config(
    page_title="Futbol Ligi Yönetim Sistemi",
    page_icon="⚽",
    layout="wide"
)

# Veri yöneticisi
@st.cache_resource
def get_data_manager():
    return DataManager()

data_manager = get_data_manager()

# Ana başlık
st.title("⚽ Futbol Ligi Yönetim Sistemi")

# Sidebar menü
menu = st.sidebar.selectbox(
    "Menü",
    ["Puan Durumu", "Maç Sonucu Gir", "Fikstür", "İstatistikler"]
)

if menu == "Puan Durumu":
    st.header("Puan Durumu")

    # Puan durumu hesaplama
    standings = calculate_points(data_manager.matches, data_manager.teams)

    # DataFrame oluşturma ve sıralama
    df_standings = pd.DataFrame.from_dict(standings, orient='index')
    df_standings = df_standings.reset_index()
    df_standings.columns = ['Takım', 'Puan', 'Oynadığı', 'Galibiyet', 'Beraberlik',
                          'Mağlubiyet', 'Attığı Gol', 'Yediği Gol', 'Averaj']

    # Sıralama işlemi
    df_standings = df_standings.sort_values(
        by=['Puan', 'Averaj', 'Attığı Gol'],
        ascending=[False, False, False]
    )

    # Sıra numarası ekleme
    df_standings.index = range(1, len(df_standings) + 1)
    df_standings.index.name = 'Sıra'

    st.dataframe(df_standings, use_container_width=True)

elif menu == "Maç Sonucu Gir":
    st.header("Maç Sonucu Girişi")

    # Maç seçimi için container
    with st.container():
        st.markdown("""
        <style>
        .match-container {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2,1,2])

        with col1:
            home_team = st.selectbox("Ev Sahibi Takım", data_manager.teams, key="home_team")
            home_goals = st.number_input("Gol", min_value=0, value=0, key="home_goals")

        with col2:
            st.markdown("<h2 style='text-align: center; margin-top: 30px;'>VS</h2>", unsafe_allow_html=True)

        with col3:
            away_team = st.selectbox("Deplasman Takım", 
                                   [t for t in data_manager.teams if t != home_team],
                                   key="away_team")
            away_goals = st.number_input("Gol", min_value=0, value=0, key="away_goals")

    # Maç sonucu önizleme
    if home_team and away_team:
        st.markdown("### Maç Sonucu Önizleme")
        col1, col2, col3 = st.columns([2,1,2])

        with col1:
            st.markdown(f"### {home_team}")
            st.markdown(f"## {home_goals}")

        with col2:
            st.markdown("<h2 style='text-align: center;'>-</h2>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"### {away_team}")
            st.markdown(f"## {away_goals}")

        # Sonuç açıklaması
        if home_goals > away_goals:
            winner = home_team
            points = "3 puan kazandı!"
        elif away_goals > home_goals:
            winner = away_team
            points = "3 puan kazandı!"
        else:
            winner = "Beraberlik"
            points = "Her iki takım 1'er puan kazandı!"

        st.markdown(f"**Sonuç:** {winner} {points}")

        if st.button("Sonucu Kaydet", type="primary"):
            if home_team != away_team:
                data_manager.add_match_result(home_team, away_team, home_goals, away_goals)
                st.success(f"Maç sonucu kaydedildi! {home_team} {home_goals} - {away_goals} {away_team}")

                # Güncel puan durumunu göster
                st.markdown("### Güncel Puan Durumu")
                new_standings = calculate_points(data_manager.matches, data_manager.teams)
                df_new = pd.DataFrame.from_dict(new_standings, orient='index')
                df_new = df_new.reset_index()
                df_new.columns = ['Takım', 'Puan', 'Oynadığı', 'Galibiyet', 'Beraberlik',
                              'Mağlubiyet', 'Attığı Gol', 'Yediği Gol', 'Averaj']
                df_new = df_new.sort_values(by=['Puan', 'Averaj', 'Attığı Gol'], 
                                          ascending=[False, False, False])
                st.dataframe(df_new, use_container_width=True)
            else:
                st.error("Aynı takımı iki kez seçemezsiniz!")

elif menu == "Fikstür":
    st.header("Fikstür")

    if st.button("Yeni Fikstür Oluştur"):
        data_manager.generate_new_fixture()
        st.success("Yeni fikstür oluşturuldu!")

    # Fikstür gösterimi
    if data_manager.fixture:
        st.write("### Maç Programı")
        current_week = None
        for i, match in enumerate(data_manager.fixture, 1):
            week = (i - 1) // 10 + 1  # Her haftada 10 maç
            if week != current_week:
                st.write(f"\n**{week}. Hafta**")
                current_week = week
            st.write(f"{match['home_team']} 🆚 {match['away_team']}")
    else:
        st.info("Henüz fikstür oluşturulmamış.")

elif menu == "İstatistikler":
    st.header("Detaylı İstatistikler")

    # İstatistik hesaplama
    standings = calculate_points(data_manager.matches, data_manager.teams)
    df_stats = pd.DataFrame.from_dict(standings, orient='index').reset_index()
    df_stats.columns = ['Takım', 'Puan', 'Oynadığı', 'Galibiyet', 'Beraberlik',
                       'Mağlubiyet', 'Attığı Gol', 'Yediği Gol', 'Averaj']

    col1, col2 = st.columns(2)

    with col1:
        # En çok gol atanlar grafiği
        fig_goals_for = px.bar(
            df_stats.nlargest(5, 'Attığı Gol'),
            x='Takım',
            y='Attığı Gol',
            title="En Çok Gol Atan Takımlar"
        )
        st.plotly_chart(fig_goals_for, use_container_width=True)

    with col2:
        # En çok gol yiyenler grafiği
        fig_goals_against = px.bar(
            df_stats.nlargest(5, 'Yediği Gol'),
            x='Takım',
            y='Yediği Gol',
            title="En Çok Gol Yiyen Takımlar"
        )
        st.plotly_chart(fig_goals_against, use_container_width=True)

    # Genel istatistikler
    col3, col4 = st.columns(2)

    with col3:
        # En çok galibiyet alanlar
        st.subheader("En Çok Galibiyet Alan Takımlar")
        win_stats = df_stats[['Takım', 'Galibiyet']].nlargest(5, 'Galibiyet')
        st.dataframe(win_stats, use_container_width=True)

    with col4:
        # En çok beraberlik yapanlar
        st.subheader("En Çok Beraberlik Yapan Takımlar")
        draw_stats = df_stats[['Takım', 'Beraberlik']].nlargest(5, 'Beraberlik')
        st.dataframe(draw_stats, use_container_width=True)