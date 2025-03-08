
import random
import itertools
from typing import List, Dict, Any

def calculate_points(matches, teams):
    """Maç sonuçlarına göre puan durumunu hesaplar"""
    standings = {}
    
    # Takımlar için başlangıç değerleri
    for team in teams:
        standings[team] = {
            'points': 0,
            'played': 0,
            'won': 0,
            'drawn': 0,
            'lost': 0,
            'goals_for': 0,
            'goals_against': 0,
            'goal_diff': 0
        }
    
    # Maç sonuçlarına göre puan hesaplama
    for match in matches:
        home = match['home_team']
        away = match['away_team']
        home_goals = match['home_goals']
        away_goals = match['away_goals']
        
        # Maç sayısı
        standings[home]['played'] += 1
        standings[away]['played'] += 1
        
        # Gol istatistikleri
        standings[home]['goals_for'] += home_goals
        standings[home]['goals_against'] += away_goals
        standings[away]['goals_for'] += away_goals
        standings[away]['goals_against'] += home_goals
        
        # Galibiyet/Beraberlik/Mağlubiyet ve puanlar
        if home_goals > away_goals:  # Ev sahibi kazandı
            standings[home]['won'] += 1
            standings[home]['points'] += 3
            standings[away]['lost'] += 1
        elif home_goals < away_goals:  # Deplasman kazandı
            standings[away]['won'] += 1
            standings[away]['points'] += 3
            standings[home]['lost'] += 1
        else:  # Beraberlik
            standings[home]['drawn'] += 1
            standings[away]['drawn'] += 1
            standings[home]['points'] += 1
            standings[away]['points'] += 1
        
        # Averaj hesaplama
        standings[home]['goal_diff'] = standings[home]['goals_for'] - standings[home]['goals_against']
        standings[away]['goal_diff'] = standings[away]['goals_for'] - standings[away]['goals_against']
    
    return standings

def create_round_robin_fixture(teams: List[str]) -> List[Dict[str, Any]]:
    """
    Round Robin algoritması ile fikstür oluşturur.
    Her takım her hafta sadece bir maç oynar ve 
    tüm takımlar birbiriyle eşleşir (N-1 hafta içinde).
    """
    # Takım sayısı tek ise, "Bay" takımı ekleyelim
    if len(teams) % 2 != 0:
        teams = teams + ["Bay"]
    
    n = len(teams)
    matches = []
    
    # Bu algoritma, her takımın her hafta yalnızca bir maç oynamasını sağlar
    # İlk takım sabit kalır, diğerleri rotasyon yapar
    team_rotation = teams.copy()
    
    for round_num in range(1, n):
        # İlk eleman sabit kalır, diğerleri rotasyon yapar
        fixed_team = team_rotation[0]
        rotating_teams = team_rotation[1:]
        
        # Bu haftaki eşleşmeleri oluştur
        weekly_matches = []
        for i in range(n // 2):
            home_team = rotating_teams[i]
            away_team = rotating_teams[n - 2 - i]
            
            # İlk maçı sabit takımla yapar
            if i == 0:
                home_team = fixed_team
            
            # Bay geçen takım varsa, onu içeren maçları ekleme
            if home_team != "Bay" and away_team != "Bay":
                match = {
                    "home_team": home_team,
                    "away_team": away_team,
                    "played": False,
                    "week": round_num
                }
                weekly_matches.append(match)
        
        # Rotasyon: Son eleman ikinci pozisyona gelir
        team_rotation = [team_rotation[0]] + [team_rotation[-1]] + team_rotation[1:-1]
        
        matches.extend(weekly_matches)
    
    # Kalan haftalarda da (n'den 2n-1'e kadar) her takımın eşleşmesi için
    # ilk yarının maçlarını ev/deplasman değiştirerek kopyala
    for round_num in range(n, 2*n-1):
        for i, match in enumerate(matches[:n//2]):
            if round_num - n + 1 == i + 1:  # Bu haftaya ait maçları sadece ekle
                new_match = {
                    "home_team": match["away_team"],
                    "away_team": match["home_team"],
                    "played": False,
                    "week": round_num
                }
                matches.append(new_match)
    
    # Maçları haftalara göre sırala
    matches.sort(key=lambda x: x["week"])
    
    return matches
