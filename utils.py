import random
import itertools
from typing import List, Tuple, Dict

def generate_fixture(teams: List[str]) -> List[Tuple[str, str]]:
    """Rastgele fikstür oluşturur"""
    # Takımları karıştır
    random.shuffle(teams)

    # Tüm olası eşleşmeleri oluştur
    matches = []
    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            matches.append((teams[i], teams[j]))
            matches.append((teams[j], teams[i]))  # İç saha ve deplasman maçları

    random.shuffle(matches)
    return matches

def calculate_points(matches: List[Dict], teams: List[str] = None) -> Dict[str, Dict]:
    """Puan durumunu hesaplar"""
    standings = {}

    # Takımlar için başlangıç değerleri
    if teams:
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
        if match['played']:
            home = match['home_team']
            away = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']

            # Takımları standings'e ekle (eğer yoksa)
            for team in [home, away]:
                if team not in standings:
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