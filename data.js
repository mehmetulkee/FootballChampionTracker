
// Takımlar
const teams = [
    "Arsenal", "Atalanta", "Ajax", "Barcelona", "Benfica", "Beşiktaş", 
    "Chelsea", "Fenerbahçe", "Galatasaray", "İnter", "Juventus", 
    "Liverpool", "Manchester City", "Manchester United", "Milan", 
    "Napoli", "Porto", "Real Madrid", "Roma"
];

// Maçlar dizisi
let matches = [];

// Fikstür
let fixture = [];

// Veriyi yerel depolamadan yükle
function loadData() {
    const savedMatches = localStorage.getItem('matches');
    const savedFixture = localStorage.getItem('fixture');
    
    if (savedMatches) {
        matches = JSON.parse(savedMatches);
    }
    
    if (savedFixture) {
        fixture = JSON.parse(savedFixture);
    } else {
        // Örnek fikstür verisi
        fetch('fixture.json')
            .then(response => response.json())
            .then(data => {
                fixture = data;
                localStorage.setItem('fixture', JSON.stringify(fixture));
                renderFixture();
            })
            .catch(error => {
                console.error('Fikstür yüklenirken hata oluştu:', error);
            });
    }
}

// Veriyi yerel depolamaya kaydet
function saveData() {
    localStorage.setItem('matches', JSON.stringify(matches));
    localStorage.setItem('fixture', JSON.stringify(fixture));
}

// Puan durumu hesaplama
function calculatePoints() {
    const standings = {};
    
    // Takımlar için başlangıç değerleri
    teams.forEach(team => {
        standings[team] = {
            points: 0,
            played: 0,
            won: 0,
            drawn: 0,
            lost: 0,
            goals_for: 0,
            goals_against: 0,
            goal_diff: 0
        };
    });
    
    // Maç sonuçlarına göre puan hesaplama
    matches.forEach(match => {
        const home = match.home_team;
        const away = match.away_team;
        const homeGoals = match.home_goals;
        const awayGoals = match.away_goals;
        
        // Maç sayısı
        standings[home].played += 1;
        standings[away].played += 1;
        
        // Gol istatistikleri
        standings[home].goals_for += homeGoals;
        standings[home].goals_against += awayGoals;
        standings[away].goals_for += awayGoals;
        standings[away].goals_against += homeGoals;
        
        // Galibiyet/Beraberlik/Mağlubiyet ve puanlar
        if (homeGoals > awayGoals) {  // Ev sahibi kazandı
            standings[home].won += 1;
            standings[home].points += 3;
            standings[away].lost += 1;
        } else if (homeGoals < awayGoals) {  // Deplasman kazandı
            standings[away].won += 1;
            standings[away].points += 3;
            standings[home].lost += 1;
        } else {  // Beraberlik
            standings[home].drawn += 1;
            standings[away].drawn += 1;
            standings[home].points += 1;
            standings[away].points += 1;
        }
        
        // Averaj hesaplama
        standings[home].goal_diff = standings[home].goals_for - standings[home].goals_against;
        standings[away].goal_diff = standings[away].goals_for - standings[away].goals_against;
    });
    
    return standings;
}

// Rastgele fikstür oluşturucu
function generateFixture() {
    // Takımları kopyala ve karıştır
    const shuffledTeams = [...teams].sort(() => Math.random() - 0.5);
    
    // Tüm olası eşleşmeleri oluştur
    const newFixture = [];
    for (let i = 0; i < shuffledTeams.length; i++) {
        for (let j = i + 1; j < shuffledTeams.length; j++) {
            newFixture.push({
                home_team: shuffledTeams[i],
                away_team: shuffledTeams[j],
                played: false
            });
            newFixture.push({
                home_team: shuffledTeams[j],
                away_team: shuffledTeams[i],
                played: false
            });
        }
    }
    
    // Fikstürü karıştır
    fixture = newFixture.sort(() => Math.random() - 0.5);
    saveData();
    renderFixture();
}

// Maç sonucunu ekle
function addMatchResult(homeTeam, awayTeam, homeGoals, awayGoals) {
    const match = {
        home_team: homeTeam,
        away_team: awayTeam,
        home_goals: homeGoals,
        away_goals: awayGoals
    };
    
    matches.push(match);
    
    // Fikstürde karşılık gelen maçı işaretleme
    for (let i = 0; i < fixture.length; i++) {
        if (fixture[i].home_team === homeTeam && fixture[i].away_team === awayTeam) {
            fixture[i].played = true;
            break;
        }
    }
    
    saveData();
    
    // Tüm görünümleri güncelle
    renderStandings();
    renderMatches();
    renderFixture();
    renderStatistics();
}
