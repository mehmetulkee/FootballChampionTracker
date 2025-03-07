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

# CSS stilleri
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
        margin-bottom: 2rem;
        background: linear-gradient(to right, #f0f2f6, #ffffff);
        border-radius: 10px;
    }
    .stat-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .match-result {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Veri yöneticisi
@st.cache_resource
def get_data_manager():
    return DataManager()

data_manager = get_data_manager()

# Admin kontrolü için session state başlatma
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Admin girişi
with st.sidebar:
    if not st.session_state.is_admin:
        admin_password = st.text_input("Admin Şifresi", type="password")
        if admin_password == "admin123":  # Basit bir şifre kontrolü
            st.session_state.is_admin = True
            st.success("Admin girişi başarılı!")
    else:
        if st.button("Çıkış Yap"):
            st.session_state.is_admin = False
            st.rerun()

# Ana başlık
st.markdown("<h1 class='main-header'>⚽ Futbol Ligi Yönetim Sistemi</h1>", unsafe_allow_html=True)

# Sidebar menü
menu_options = ["Puan Durumu", "Oynanan Maçlar", "Fikstür", "İstatistikler"]
if st.session_state.is_admin:
    menu_options.insert(1, "Maç Sonucu Gir")

menu = st.sidebar.selectbox("Menü", menu_options)

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

elif menu == "Oynanan Maçlar":
    st.header("Oynanan Maçlar")

    if data_manager.matches:
        for match in reversed(data_manager.matches):  # En son maçlar üstte
            with st.container():
                st.markdown(f"""
                <div class='match-result'>
                    <h3 style='text-align: center;'>
                        {match['home_team']} {match['home_goals']} - {match['away_goals']} {match['away_team']}
                    </h3>
                    <p style='text-align: center;'>
                        {match['home_goals'] > match['away_goals'] and '🏆 ' + match['home_team'] + ' kazandı!' or
                         match['home_goals'] < match['away_goals'] and '🏆 ' + match['away_team'] + ' kazandı!' or
                         '🤝 Berabere'}
                    </p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Henüz oynanmış maç bulunmamaktadır.")

elif menu == "Maç Sonucu Gir" and st.session_state.is_admin:
    st.header("Maç Sonucu Girişi")

    # Maç seçimi için container
    with st.container():
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
            st.markdown(f"""
            <div class='stat-card' style='text-align: center;'>
                <h3>{home_team}</h3>
                <h2 style='color: #1f77b4;'>{home_goals}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<h2 style='text-align: center;'>-</h2>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class='stat-card' style='text-align: center;'>
                <h3>{away_team}</h3>
                <h2 style='color: #1f77b4;'>{away_goals}</h2>
            </div>
            """, unsafe_allow_html=True)

        # Sonuç açıklaması
        if home_goals > away_goals:
            winner = home_team
            points = "3 puan kazandı! 🏆"
        elif away_goals > home_goals:
            winner = away_team
            points = "3 puan kazandı! 🏆"
        else:
            winner = "Beraberlik"
            points = "Her iki takım 1'er puan kazandı! 🤝"

        st.markdown(f"""
        <div class='stat-card' style='text-align: center;'>
            <h3>Sonuç</h3>
            <p>{winner} {points}</p>
        </div>
        """, unsafe_allow_html=True)

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

    if st.session_state.is_admin and st.button("Yeni Fikstür Oluştur"):
        data_manager.generate_new_fixture()
        st.success("Yeni fikstür oluşturuldu!")

    # Fikstür gösterimi
    if data_manager.fixture:
        st.write("### Maç Programı")
        current_week = None
        for i, match in enumerate(data_manager.fixture, 1):
            week = (i - 1) // 10 + 1  # Her haftada 10 maç
            if week != current_week:
                st.markdown(f"""
                <div class='stat-card'>
                    <h3>{week}. Hafta</h3>
                </div>
                """, unsafe_allow_html=True)
                current_week = week
            st.markdown(f"""
            <div class='match-result'>
                {match['home_team']} 🆚 {match['away_team']}
            </div>
            """, unsafe_allow_html=True)
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
            title="En Çok Gol Atan Takımlar",
            color='Takım',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_goals_for.update_layout(showlegend=False)
        st.plotly_chart(fig_goals_for, use_container_width=True)

    with col2:
        # En çok gol yiyenler grafiği
        fig_goals_against = px.bar(
            df_stats.nlargest(5, 'Yediği Gol'),
            x='Takım',
            y='Yediği Gol',
            title="En Çok Gol Yiyen Takımlar",
            color='Takım',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_goals_against.update_layout(showlegend=False)
        st.plotly_chart(fig_goals_against, use_container_width=True)

    # Genel istatistikler
    col3, col4 = st.columns(2)

    with col3:
        # En çok galibiyet alanlar
        st.markdown("""
        <div class='stat-card'>
            <h3>En Çok Galibiyet Alan Takımlar</h3>
        </div>
        """, unsafe_allow_html=True)
        win_stats = df_stats[['Takım', 'Galibiyet']].nlargest(5, 'Galibiyet')
        st.dataframe(win_stats, use_container_width=True)

    with col4:
        # En çok beraberlik yapanlar
        st.markdown("""
        <div class='stat-card'>
            <h3>En Çok Beraberlik Yapan Takımlar</h3>
        </div>
        """, unsafe_allow_html=True)
        draw_stats = df_stats[['Takım', 'Beraberlik']].nlargest(5, 'Beraberlik')
        st.dataframe(draw_stats, use_container_width=True)