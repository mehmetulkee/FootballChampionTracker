
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
        self.goal_scorers = []
        self.assist_makers = []
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
            
        if os.path.exists('goal_scorers.json'):
            with open('goal_scorers.json', 'r', encoding='utf-8') as f:
                self.goal_scorers = json.load(f)
        
        if os.path.exists('assist_makers.json'):
            with open('assist_makers.json', 'r', encoding='utf-8') as f:
                self.assist_makers = json.load(f)
    
    def save_data(self):
        """Veriyi yerel depolamaya kaydeder"""
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(self.matches, f, ensure_ascii=False)
        
        with open('fixture.json', 'w', encoding='utf-8') as f:
            json.dump(self.fixture, f, ensure_ascii=False)
            
        with open('goal_scorers.json', 'w', encoding='utf-8') as f:
            json.dump(self.goal_scorers, f, ensure_ascii=False)
            
        with open('assist_makers.json', 'w', encoding='utf-8') as f:
            json.dump(self.assist_makers, f, ensure_ascii=False)
    
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
        
    def add_goal_scorer(self, player_name, team, goals):
        """Gol kralı listesine yeni oyuncu ekler veya mevcut oyuncunun gol sayısını günceller"""
        # Eğer oyuncu zaten varsa, gol sayısını güncelle
        for scorer in self.goal_scorers:
            if scorer["player_name"] == player_name and scorer["team"] == team:
                scorer["goals"] = goals
                self.save_data()
                return
        
        # Yoksa yeni oyuncu ekle
        self.goal_scorers.append({
            "player_name": player_name,
            "team": team,
            "goals": goals
        })
        self.save_data()
        
    def add_assist_maker(self, player_name, team, assists):
        """Asist kralı listesine yeni oyuncu ekler veya mevcut oyuncunun asist sayısını günceller"""
        # Eğer oyuncu zaten varsa, asist sayısını güncelle
        for assist_maker in self.assist_makers:
            if assist_maker["player_name"] == player_name and assist_maker["team"] == team:
                assist_maker["assists"] = assists
                self.save_data()
                return
        
        # Yoksa yeni oyuncu ekle
        self.assist_makers.append({
            "player_name": player_name,
            "team": team,
            "assists": assists
        })
        self.save_data()
