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

# Admin kontrolü için session state başlatma
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Admin girişi
with st.sidebar:
    if not st.session_state.is_admin:
        admin_password = st.text_input("Admin Şifresi", type="password")
        if admin_password == "05365265029Me":  # Yeni şifre
            st.session_state.is_admin = True
            st.success("Admin girişi başarılı!")
    else:
        if st.button("Çıkış Yap"):
            st.session_state.is_admin = False
            st.rerun()

# Ana başlık
st.title("⚽ Futbol Ligi Yönetim Sistemi")

# Sidebar menü
menu_options = ["Puan Durumu", "Oynanan Maçlar", "Fikstür", "İstatistikler", "Detaylı İstatistikler"]
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
    df_standings.insert(0, 'Sıra', range(1, len(df_standings) + 1))
    
    # Maçkolik stilinde CSS ile tablo özelleştirmesi
    st.markdown("""
    <style>
    .mackolik-table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }
    .mackolik-table th {
        background-color: #013369;
        color: white;
        text-align: center;
        padding: 8px;
        font-weight: bold;
        border: 1px solid #ddd;
    }
    .mackolik-table td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: center;
    }
    .mackolik-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .team-cell {
        text-align: left;
        font-weight: bold;
    }
    .point-cell {
        font-weight: bold;
        color: #013369;
    }
    .top-teams {
        background-color: rgba(0, 128, 0, 0.1) !important;
    }
    .bottom-teams {
        background-color: rgba(255, 0, 0, 0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # HTML tablosunu oluştur
    html_table = '<table class="mackolik-table">'
    
    # Tablo başlığı
    html_table += '''
    <thead>
        <tr>
            <th>Sıra</th>
            <th>Takım</th>
            <th>O</th>
            <th>G</th>
            <th>B</th>
            <th>M</th>
            <th>A</th>
            <th>Y</th>
            <th>Av</th>
            <th>P</th>
        </tr>
    </thead>
    <tbody>
    '''
    
    # Tablo içeriği
    for i, row in df_standings.iterrows():
        # İlk 3 takım ve son 3 takım için özel sınıf ekleme
        row_class = ""
        if i < 3:  # İlk 3 takım
            row_class = "top-teams"
        elif i >= len(df_standings) - 3 and len(df_standings) > 5:  # Son 3 takım (toplam takım sayısı 6'dan fazlaysa)
            row_class = "bottom-teams"
            
        html_table += f'<tr class="{row_class}">'
        html_table += f'<td>{row["Sıra"]}</td>'
        html_table += f'<td class="team-cell">{row["Takım"]}</td>'
        html_table += f'<td>{row["Oynadığı"]}</td>'
        html_table += f'<td>{row["Galibiyet"]}</td>'
        html_table += f'<td>{row["Beraberlik"]}</td>'
        html_table += f'<td>{row["Mağlubiyet"]}</td>'
        html_table += f'<td>{row["Attığı Gol"]}</td>'
        html_table += f'<td>{row["Yediği Gol"]}</td>'
        html_table += f'<td>{row["Averaj"]}</td>'
        html_table += f'<td class="point-cell">{row["Puan"]}</td>'
        html_table += '</tr>'
        
    html_table += '</tbody></table>'
    
    # HTML tablosunu göster
    st.markdown(html_table, unsafe_allow_html=True)
    
    # Açıklama
    st.markdown("""
    <div style="margin-top: 10px; font-size: 12px;">
        <span style="background-color: rgba(0, 128, 0, 0.1); padding: 2px 5px;">■</span> Üst sıralama
        <span style="margin-left: 20px; background-color: rgba(255, 0, 0, 0.1); padding: 2px 5px;">■</span> Alt sıralama
    </div>
    """, unsafe_allow_html=True)

elif menu == "Oynanan Maçlar":
    st.header("Oynanan Maçlar")

    if data_manager.matches:
        for match in reversed(data_manager.matches):  # En son maçlar üstte
            st.write(f"{match['home_team']} {match['home_goals']} - {match['away_goals']} {match['away_team']}")
            if match['home_goals'] > match['away_goals']:
                st.write(f"🏆 {match['home_team']} kazandı!")
            elif match['home_goals'] < match['away_goals']:
                st.write(f"🏆 {match['away_team']} kazandı!")
            else:
                st.write("🤝 Berabere")
            st.divider()
    else:
        st.info("Henüz oynanmış maç bulunmamaktadır.")

elif menu == "Maç Sonucu Gir" and st.session_state.is_admin:
    st.header("Maç Sonucu Girişi")

    col1, col2, col3 = st.columns([2,1,2])

    with col1:
        home_team = st.selectbox("Ev Sahibi Takım", data_manager.teams, key="home_team")
        home_goals = st.number_input("Gol", min_value=0, value=0, key="home_goals")

    with col2:
        st.write("##")
        st.write("VS")

    with col3:
        away_team = st.selectbox("Deplasman Takım", 
                               [t for t in data_manager.teams if t != home_team],
                               key="away_team")
        away_goals = st.number_input("Gol", min_value=0, value=0, key="away_goals")

    # Maç sonucu önizleme
    if home_team and away_team:
        st.write("### Maç Sonucu Önizleme")
        st.write(f"{home_team} {home_goals} - {away_goals} {away_team}")

        # Sonuç açıklaması
        if home_goals > away_goals:
            st.write(f"🏆 {home_team} kazanacak ve 3 puan alacak!")
        elif away_goals > home_goals:
            st.write(f"🏆 {away_team} kazanacak ve 3 puan alacak!")
        else:
            st.write("🤝 Berabere kalacak ve her iki takım 1'er puan alacak!")

        if st.button("Sonucu Kaydet", type="primary"):
            if home_team != away_team:
                data_manager.add_match_result(home_team, away_team, home_goals, away_goals)
                st.success(f"Maç sonucu kaydedildi! {home_team} {home_goals} - {away_goals} {away_team}")

                # Güncel puan durumunu göster
                st.write("### Güncel Puan Durumu")
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

    with st.container():
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write("### Maç Programı")
        with c2:
            if st.session_state.is_admin:
                if st.button("Yeni Fikstür Oluştur"):
                    data_manager.generate_new_fixture()
                    st.success("Yeni fikstür oluşturuldu!")
                    st.rerun()

    # Fikstür gösterimi
    if data_manager.fixture:
        # Haftalara göre gruplandır
        fixture_by_week = {}
        for match in data_manager.fixture:
            week = match.get('week', 1)  # Eğer week yoksa 1 kabul et
            if week not in fixture_by_week:
                fixture_by_week[week] = []
            fixture_by_week[week].append(match)
        
        # Haftaları sırayla göster, 3 küçük sütun olarak
        total_weeks = len(fixture_by_week.keys())
        
        # En çok maç sayısını bulalım (her takımın başka bir takımla eşleşmesi için)
        matches_per_week = len(data_manager.teams) // 2
        
        tabs = st.tabs([f"{week}. Hafta" for week in range(1, total_weeks + 1)])
        
        for week_idx, week in enumerate(range(1, total_weeks + 1)):
            if week in fixture_by_week:
                with tabs[week_idx]:
                    st.write(f"### {week}. Hafta Maçları")
                    
                    # Bu haftanın maçlarını göster
                    for i, match in enumerate(fixture_by_week[week]):
                        col1, col2, col3 = st.columns([2, 1, 2])
                        
                        with col1:
                            st.write(f"**{match['home_team']}**")
                        
                        with col2:
                            status = "✅" if match.get("played", False) else "⏳"
                            st.write(f"{status} 🆚")
                        
                        with col3:
                            st.write(f"**{match['away_team']}**")
                        
                        if i < len(fixture_by_week[week]) - 1:
                            st.divider()
    else:
        st.info("Henüz fikstür oluşturulmamış.")

elif menu == "İstatistikler":
    st.header("İstatistikler")
    
    # İstatistik hesaplama
    standings = calculate_points(data_manager.matches, data_manager.teams)
    df_stats = pd.DataFrame.from_dict(standings, orient='index').reset_index()
    df_stats.columns = ['Takım', 'Puan', 'Oynadığı', 'Galibiyet', 'Beraberlik',
                       'Mağlubiyet', 'Attığı Gol', 'Yediği Gol', 'Averaj']
    
    # Sıralama işlemi
    df_stats = df_stats.sort_values(
        by=['Puan', 'Averaj', 'Attığı Gol'],
        ascending=[False, False, False]
    )
    
    # İstatistik kartları
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("En Çok Gol Atan Takım", 
                 df_stats.iloc[0]['Takım'] if not df_stats.empty else "-", 
                 df_stats.iloc[0]['Attığı Gol'] if not df_stats.empty else 0)
    
    with col2:
        top_defense = df_stats.sort_values(by='Yediği Gol', ascending=True)
        st.metric("En Az Gol Yiyen Takım", 
                 top_defense.iloc[0]['Takım'] if not top_defense.empty else "-", 
                 top_defense.iloc[0]['Yediği Gol'] if not top_defense.empty else 0)
    
    with col3:
        top_winner = df_stats.sort_values(by='Galibiyet', ascending=False)
        st.metric("En Çok Galibiyet Alan", 
                 top_winner.iloc[0]['Takım'] if not top_winner.empty else "-", 
                 top_winner.iloc[0]['Galibiyet'] if not top_winner.empty else 0)
    
    with col4:
        top_draw = df_stats.sort_values(by='Beraberlik', ascending=False)
        st.metric("En Çok Beraberlik Yapan", 
                 top_draw.iloc[0]['Takım'] if not top_draw.empty else "-", 
                 top_draw.iloc[0]['Beraberlik'] if not top_draw.empty else 0)
    
    st.divider()
    
    # Oyuncu istatistikleri (ileride eklenebilir)
    st.write("### Gol Krallığı")
    
    # Örnek bir gol krallığı verisi (ileride gerçek verilerle değiştirilebilir)
    if data_manager.matches:
        st.info("Gol krallığı istatistikleri henüz eklenmemiştir.")
    else:
        st.info("Henüz maç oynanmadığı için istatistik bulunmamaktadır.")

elif menu == "Detaylı İstatistikler":
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

        # En çok galibiyet alanlar
        st.write("### En Çok Galibiyet Alan Takımlar")
        win_stats = df_stats[['Takım', 'Galibiyet']].nlargest(5, 'Galibiyet')
        st.dataframe(win_stats, use_container_width=True)

    with col2:
        # En çok gol yiyenler grafiği
        fig_goals_against = px.bar(
            df_stats.nlargest(5, 'Yediği Gol'),
            x='Takım',
            y='Yediği Gol',
            title="En Çok Gol Yiyen Takımlar"
        )
        st.plotly_chart(fig_goals_against, use_container_width=True)

        # En çok beraberlik yapanlar
        st.write("### En Çok Beraberlik Yapan Takımlar")
        draw_stats = df_stats[['Takım', 'Beraberlik']].nlargest(5, 'Beraberlik')
        st.dataframe(draw_stats, use_container_width=True)