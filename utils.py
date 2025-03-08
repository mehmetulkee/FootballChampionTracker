
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
    # Takım sayısının çift olduğunu kontrol et
    original_teams = teams.copy()
    if len(teams) % 2 != 0:
        # Takım sayısı tek ise, bir takım bay geçer
        teams = teams + ["Bay"]
    
    n = len(teams)
    fixtures = []
    
    # Takımları sabit ve dönen olarak iki gruba ayır
    # İlk yarı fikstür (n-1 hafta sürer)
    teams_copy = teams.copy()
    
    for week in range(1, n):
        # Bu haftanın maçları
        week_matches = []
        
        # İlk takım sabit, diğerleri döner
        for i in range(n // 2):
            home_team = teams_copy[i]
            away_team = teams_copy[n - 1 - i]
            
            # Eğer takımlardan biri "Bay" ise maçı ekleme
            if home_team != "Bay" and away_team != "Bay":
                match = {
                    "home_team": home_team,
                    "away_team": away_team,
                    "played": False,
                    "week": week
                }
                week_matches.append(match)
        
        # Takımları döndürme (ilk takım sabit kalır)
        # Rotasyon: Sabit ilk takım kalır, son takım ikinci sıraya gelir,
        # diğerleri bir yer ilerler
        teams_copy = [teams_copy[0]] + [teams_copy[-1]] + teams_copy[1:-1]
        
        # Bu haftanın maçlarını ekle
        fixtures.extend(week_matches)
    
    # Maçları haftalara göre sırala
    fixtures.sort(key=lambda x: x["week"])
    
    # Ev ve deplasman karışımı için ikinci yarı deplasman
    # İkinci devreyi otomatik olarak oluşturmuyoruz, sadece tek devre
    
    return fixtures
