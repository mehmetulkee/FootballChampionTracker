
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
    Her takım her hafta sadece bir maç oynar.
    """
    if len(teams) % 2 != 0:
        # Takım sayısı tek ise, bir takım bay geçer
        teams = teams + ["Bay"]
    
    n = len(teams)
    matches = []
    fixtures = []
    
    # İlk yarı fikstür (1-19 hafta)
    for week in range(n - 1):
        week_matches = []
        for i in range(n // 2):
            match = {
                "home_team": teams[i],
                "away_team": teams[n - 1 - i],
                "played": False,
                "week": week + 1
            }
            week_matches.append(match)
        
        fixtures.extend(week_matches)
        
        # Takımları döndür (ilk takım sabit kalır)
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
    
    # Fikstürü haftalara göre sırala
    fixtures.sort(key=lambda x: x["week"])
    
    return fixtures
