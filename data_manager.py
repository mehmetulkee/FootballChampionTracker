
import json
import os
from utils import create_round_robin_fixture

class DataManager:
    def __init__(self):
        self.teams = [
            "Manchester United", "Newcastle United", "Juventus", "Manchester City", 
            "Bayern Munih", "Milan", "Atalanta", "Arsenal", "Ajax", "İnter", 
            "Roma", "PSG", "Dortmund", "Psv", "Napoli", "Feyenoord", "Liverpool", 
            "Konyaspor", "Leverkusen", "Real Madrid"
        ]
        self.matches = []
        self.fixture = []
        self.load_data()
    
    def load_data(self):
        """Veriyi yerel depolamadan yükler"""
        if os.path.exists('matches.json'):
            with open('matches.json', 'r', encoding='utf-8') as f:
                self.matches = json.load(f)
        
        if os.path.exists('fixture.json'):
            with open('fixture.json', 'r', encoding='utf-8') as f:
                self.fixture = json.load(f)
        else:
            self.generate_new_fixture()
    
    def save_data(self):
        """Veriyi yerel depolamaya kaydeder"""
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(self.matches, f, ensure_ascii=False)
        
        with open('fixture.json', 'w', encoding='utf-8') as f:
            json.dump(self.fixture, f, ensure_ascii=False)
    
    def add_match_result(self, home_team, away_team, home_goals, away_goals):
        """Maç sonucu ekler"""
        match = {
            "home_team": home_team,
            "away_team": away_team,
            "home_goals": home_goals,
            "away_goals": away_goals
        }
        
        self.matches.append(match)
        
        # Fikstürde karşılık gelen maçı işaretleme
        for i in range(len(self.fixture)):
            if self.fixture[i]["home_team"] == home_team and self.fixture[i]["away_team"] == away_team:
                self.fixture[i]["played"] = True
                break
        
        self.save_data()
    
    def generate_new_fixture(self):
        """Yeni fikstür oluşturur - her takım her hafta bir maç oynar"""
        # Mevcut maçları temizle
        self.matches = []
        # Yeni fikstür oluştur - tüm takımlar birbiriyle eşleşecek şekilde
        self.fixture = create_round_robin_fixture(self.teams)
        # Fikstür verilerini kaydet
        self.save_data()
        return len(self.fixture)
