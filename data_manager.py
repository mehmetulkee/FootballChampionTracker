import pandas as pd
from typing import List, Dict
import json
import os

class DataManager:
    def __init__(self):
        self.teams = [
            "Manchester City", "Manchester United", "Arsenal", "Chelsea", "Liverpool",
            "Benfica", "Juventus", "Milan", "İnter", "Real Madrid",
            "Barcelona", "Atalanta", "Napoli", "Ajax", "Beşiktaş",
            "Galatasaray", "Leverkusen", "Roma", "Porto", "Fenerbahçe"
        ]
        
        # Veri dosyaları
        self.matches_file = "matches.json"
        self.fixture_file = "fixture.json"
        
        # Veri yapıları
        self.matches = self._load_matches()
        self.fixture = self._load_fixture()
    
    def _load_matches(self) -> List[Dict]:
        """Maç verilerini yükler"""
        if os.path.exists(self.matches_file):
            with open(self.matches_file, 'r') as f:
                return json.load(f)
        return []
    
    def _load_fixture(self) -> List[Dict]:
        """Fikstür verilerini yükler"""
        if os.path.exists(self.fixture_file):
            with open(self.fixture_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_matches(self):
        """Maç verilerini kaydeder"""
        with open(self.matches_file, 'w') as f:
            json.dump(self.matches, f)
    
    def save_fixture(self):
        """Fikstür verilerini kaydeder"""
        with open(self.fixture_file, 'w') as f:
            json.dump(self.fixture, f)
    
    def add_match_result(self, home_team: str, away_team: str, home_goals: int, away_goals: int):
        """Yeni maç sonucu ekler"""
        match = {
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'played': True
        }
        self.matches.append(match)
        self.save_matches()
    
    def generate_new_fixture(self):
        """Yeni fikstür oluşturur"""
        from utils import generate_fixture
        matches = generate_fixture(self.teams)
        self.fixture = [{'home_team': home, 'away_team': away, 'played': False} 
                       for home, away in matches]
        self.save_fixture()
