
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

// Round Robin algoritması ile fikstür oluşturma
function generateFixture() {
    let teamList = [...teams];
    
    // Takım sayısı tek ise, bir takım bay geçer
    if (teamList.length % 2 !== 0) {
        teamList.push("Bay");
    }
    
    const n = teamList.length;
    const newFixture = [];
    
    // İlk yarı fikstür (1-19 hafta)
    for (let round = 0; round < n - 1; round++) {
        for (let i = 0; i < n / 2; i++) {
            // Her takım her hafta sadece bir maç oynar
            newFixture.push({
                home_team: teamList[i],
                away_team: teamList[n - 1 - i],
                played: false,
                week: round + 1
            });
        }
        
        // Takımları döndür (ilk takım sabit kalır)
        teamList = [teamList[0], ...teamList.slice(n - 1), ...teamList.slice(1, n - 1)];
    }
    
    // Fikstürü haftalara göre sırala
    fixture = newFixture.sort((a, b) => a.week - b.week);
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
