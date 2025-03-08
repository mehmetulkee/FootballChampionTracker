
document.addEventListener('DOMContentLoaded', function() {
    // Sayfa yüklendiğinde veriyi yükle
    loadData();
    
    // Menü işlemleri
    const menuLinks = document.querySelectorAll('.menu a');
    const sections = document.querySelectorAll('.section');
    
    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Aktif menü öğesini güncelle
            menuLinks.forEach(item => item.classList.remove('active'));
            this.classList.add('active');
            
            // İlgili bölümü göster
            const targetId = this.getAttribute('href').substring(1);
            sections.forEach(section => {
                section.classList.remove('active');
                if (section.id === targetId) {
                    section.classList.add('active');
                }
            });
        });
    });
    
    // Admin girişi
    const adminPassword = document.getElementById('admin-password');
    const adminLoginBtn = document.getElementById('admin-login');
    const adminLogoutBtn = document.getElementById('admin-logout');
    const adminOnlyElements = document.querySelectorAll('.admin-only');
    const macGirisiMenu = document.createElement('li');
    const macGirisiLink = document.createElement('a');
    
    macGirisiLink.href = '#mac-girisi';
    macGirisiLink.textContent = 'Maç Sonucu Gir';
    macGirisiMenu.appendChild(macGirisiLink);
    
    adminLoginBtn.addEventListener('click', function() {
        if (adminPassword.value === "05365265029Me") {
            // Admin girişi başarılı
            adminLoginBtn.style.display = 'none';
            adminLogoutBtn.style.display = 'block';
            adminPassword.style.display = 'none';
            
            // Admin menüsünü ekle
            document.querySelector('.menu').insertBefore(macGirisiMenu, document.querySelector('.menu li:nth-child(2)'));
            
            // Admin elementlerini göster
            adminOnlyElements.forEach(el => el.style.display = 'block');
            
            alert('Admin girişi başarılı!');
        } else {
            alert('Hatalı şifre!');
        }
    });
    
    adminLogoutBtn.addEventListener('click', function() {
        adminLoginBtn.style.display = 'block';
        adminLogoutBtn.style.display = 'none';
        adminPassword.style.display = 'block';
        adminPassword.value = '';
        
        // Admin menüsünü kaldır
        document.querySelector('.menu').removeChild(macGirisiMenu);
        
        // Admin elementlerini gizle
        adminOnlyElements.forEach(el => el.style.display = 'none');
        
        // Eğer şu anda admin sayfasındaysak puan durumuna git
        if (document.getElementById('mac-girisi').classList.contains('active')) {
            document.querySelector('.menu a[href="#puan-durumu"]').click();
        }
    });
    
    // Ev sahibi ve deplasman takımları seçimlerini doldur
    const homeTeamSelect = document.getElementById('home-team');
    const awayTeamSelect = document.getElementById('away-team');
    
    teams.forEach(team => {
        const homeOption = document.createElement('option');
        homeOption.value = team;
        homeOption.textContent = team;
        homeTeamSelect.appendChild(homeOption);
    });
    
    // Ev sahibi takım değiştikçe deplasman takımı listesini güncelle
    homeTeamSelect.addEventListener('change', function() {
        const selectedHomeTeam = this.value;
        
        // Deplasman takımı seçimini temizle
        awayTeamSelect.innerHTML = '';
        
        // Ev sahibi olmayan takımları ekle
        teams.forEach(team => {
            if (team !== selectedHomeTeam) {
                const awayOption = document.createElement('option');
                awayOption.value = team;
                awayOption.textContent = team;
                awayTeamSelect.appendChild(awayOption);
            }
        });
        
        updateMatchPreview();
    });
    
    // İlk yükleme için deplasman takımını doldur
    if (teams.length > 0) {
        const firstTeam = teams[0];
        homeTeamSelect.value = firstTeam;
        
        teams.forEach(team => {
            if (team !== firstTeam) {
                const awayOption = document.createElement('option');
                awayOption.value = team;
                awayOption.textContent = team;
                awayTeamSelect.appendChild(awayOption);
            }
        });
    }
    
    // Maç önizleme güncelleme
    const homeGoalsInput = document.getElementById('home-goals');
    const awayGoalsInput = document.getElementById('away-goals');
    const matchResultPreview = document.getElementById('match-result-preview');
    const matchOutcomePreview = document.getElementById('match-outcome-preview');
    
    function updateMatchPreview() {
        const homeTeam = homeTeamSelect.value;
        const awayTeam = awayTeamSelect.value;
        const homeGoals = parseInt(homeGoalsInput.value);
        const awayGoals = parseInt(awayGoalsInput.value);
        
        matchResultPreview.textContent = `${homeTeam} ${homeGoals} - ${awayGoals} ${awayTeam}`;
        
        if (homeGoals > awayGoals) {
            matchOutcomePreview.textContent = `🏆 ${homeTeam} kazanacak ve 3 puan alacak!`;
        } else if (awayGoals > homeGoals) {
            matchOutcomePreview.textContent = `🏆 ${awayTeam} kazanacak ve 3 puan alacak!`;
        } else {
            matchOutcomePreview.textContent = `🤝 Berabere kalacak ve her iki takım 1'er puan alacak!`;
        }
    }
    
    homeGoalsInput.addEventListener('input', updateMatchPreview);
    awayGoalsInput.addEventListener('input', updateMatchPreview);
    homeTeamSelect.addEventListener('change', updateMatchPreview);
    awayTeamSelect.addEventListener('change', updateMatchPreview);
    
    // İlk yükleme için önizlemeyi güncelle
    updateMatchPreview();
    
    // Maç sonucu kaydetme
    const saveResultBtn = document.getElementById('save-result');
    
    saveResultBtn.addEventListener('click', function() {
        const homeTeam = homeTeamSelect.value;
        const awayTeam = awayTeamSelect.value;
        const homeGoals = parseInt(homeGoalsInput.value);
        const awayGoals = parseInt(awayGoalsInput.value);
        
        if (homeTeam && awayTeam && homeTeam !== awayTeam) {
            addMatchResult(homeTeam, awayTeam, homeGoals, awayGoals);
            alert(`Maç sonucu kaydedildi! ${homeTeam} ${homeGoals} - ${awayGoals} ${awayTeam}`);
            
            // Giriş alanlarını sıfırla
            homeGoalsInput.value = 0;
            awayGoalsInput.value = 0;
            updateMatchPreview();
        } else {
            alert('Lütfen farklı takımlar seçin!');
        }
    });
    
    // Yeni fikstür oluşturma
    const generateFixtureBtn = document.getElementById('generate-fixture');
    
    generateFixtureBtn.addEventListener('click', function() {
        if (confirm('Yeni bir fikstür oluşturmak istediğinize emin misiniz? Mevcut fikstür silinecektir.')) {
            generateFixture();
            alert('Yeni fikstür oluşturuldu!');
        }
    });
    
    // Tüm arayüzü ilk yükleme için render et
    renderStandings();
    renderMatches();
    renderFixture();
    renderStatistics();
});

// Puan durumunu render et
function renderStandings() {
    const standingsBody = document.getElementById('standings-body');
    const standings = calculatePoints();
    
    // Puan durumunu hesapla ve sırala
    let standingsArray = Object.entries(standings).map(([team, stats]) => {
        return { team, ...stats };
    });
    
    standingsArray.sort((a, b) => {
        if (a.points !== b.points) return b.points - a.points;
        if (a.goal_diff !== b.goal_diff) return b.goal_diff - a.goal_diff;
        return b.goals_for - a.goals_for;
    });
    
    // Tabloyu güncelle
    standingsBody.innerHTML = '';
    
    standingsArray.forEach((team, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${team.team}</td>
            <td>${team.points}</td>
            <td>${team.played}</td>
            <td>${team.won}</td>
            <td>${team.drawn}</td>
            <td>${team.lost}</td>
            <td>${team.goals_for}</td>
            <td>${team.goals_against}</td>
            <td>${team.goal_diff}</td>
        `;
        standingsBody.appendChild(row);
    });
}

// Oynanan maçları render et
function renderMatches() {
    const matchesContainer = document.getElementById('matches-container');
    
    if (matches.length === 0) {
        matchesContainer.innerHTML = '<p>Henüz oynanmış maç bulunmamaktadır.</p>';
        return;
    }
    
    matchesContainer.innerHTML = '';
    
    // En son maçlar üstte
    [...matches].reverse().forEach(match => {
        const matchItem = document.createElement('div');
        matchItem.className = 'match-item';
        
        let outcomeClass = '';
        let outcomeText = '';
        
        if (match.home_goals > match.away_goals) {
            outcomeClass = 'winner';
            outcomeText = `🏆 ${match.home_team} kazandı!`;
        } else if (match.home_goals < match.away_goals) {
            outcomeClass = 'winner';
            outcomeText = `🏆 ${match.away_team} kazandı!`;
        } else {
            outcomeClass = 'draw';
            outcomeText = '🤝 Berabere';
        }
        
        matchItem.innerHTML = `
            <div class="match-result">${match.home_team} ${match.home_goals} - ${match.away_goals} ${match.away_team}</div>
            <div class="match-outcome ${outcomeClass}">${outcomeText}</div>
        `;
        
        matchesContainer.appendChild(matchItem);
    });
}

// Fikstürü render et
function renderFixture() {
    const fixtureContainer = document.getElementById('fixture-container');
    
    if (fixture.length === 0) {
        fixtureContainer.innerHTML = '<p>Henüz fikstür oluşturulmamış.</p>';
        return;
    }
    
    fixtureContainer.innerHTML = '';
    
    // Haftalara göre gruplandır
    const fixtureByWeek = {};
    fixture.forEach(match => {
        const week = match.week || 1; // Eğer week yoksa 1 kabul et
        if (!fixtureByWeek[week]) {
            fixtureByWeek[week] = [];
        }
        fixtureByWeek[week].push(match);
    });
    
    // Haftaları sırayla göster
    const weeks = Object.keys(fixtureByWeek).sort((a, b) => a - b);
    
    weeks.forEach(week => {
        const weekFixtureDiv = document.createElement('div');
        weekFixtureDiv.className = 'fixture-week';
        weekFixtureDiv.innerHTML = `<h3>${week}. Hafta</h3>`;
        
        fixtureByWeek[week].forEach(match => {
            const matchDiv = document.createElement('div');
            matchDiv.className = 'fixture-match';
            
            if (match.played) {
                matchDiv.innerHTML = `✅ ${match.home_team} 🆚 ${match.away_team}`;
                matchDiv.style.color = '#888';
            } else {
                matchDiv.innerHTML = `⏳ ${match.home_team} 🆚 ${match.away_team}`;
            }
            
            weekFixtureDiv.appendChild(matchDiv);
        });
        
        fixtureContainer.appendChild(weekFixtureDiv);
    });
}

// İstatistikleri render et
function renderStatistics() {
    const standings = calculatePoints();
    
    // İstatistik hesaplama
    let statsArray = Object.entries(standings).map(([team, stats]) => {
        return { team, ...stats };
    });
    
    // En çok gol atanlar grafiği
    const topScorers = [...statsArray].sort((a, b) => b.goals_for - a.goals_for).slice(0, 5);
    
    const goalsForData = {
        x: topScorers.map(team => team.team),
        y: topScorers.map(team => team.goals_for),
        type: 'bar',
        marker: {
            color: '#3498db'
        }
    };
    
    const goalsForLayout = {
        title: 'En Çok Gol Atan Takımlar',
        xaxis: {
            title: 'Takım'
        },
        yaxis: {
            title: 'Attığı Gol'
        }
    };
    
    Plotly.newPlot('goals-for-chart', [goalsForData], goalsForLayout);
    
    // En çok gol yiyenler grafiği
    const topConceded = [...statsArray].sort((a, b) => b.goals_against - a.goals_against).slice(0, 5);
    
    const goalsAgainstData = {
        x: topConceded.map(team => team.team),
        y: topConceded.map(team => team.goals_against),
        type: 'bar',
        marker: {
            color: '#e74c3c'
        }
    };
    
    const goalsAgainstLayout = {
        title: 'En Çok Gol Yiyen Takımlar',
        xaxis: {
            title: 'Takım'
        },
        yaxis: {
            title: 'Yediği Gol'
        }
    };
    
    Plotly.newPlot('goals-against-chart', [goalsAgainstData], goalsAgainstLayout);
    
    // En çok galibiyet alanlar
    const topWinners = [...statsArray].sort((a, b) => b.won - a.won).slice(0, 5);
    const winStatsTable = document.querySelector('#win-stats tbody');
    
    winStatsTable.innerHTML = '';
    topWinners.forEach(team => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${team.team}</td>
            <td>${team.won}</td>
        `;
        winStatsTable.appendChild(row);
    });
    
    // En çok beraberlik yapanlar
    const topDrawers = [...statsArray].sort((a, b) => b.drawn - a.drawn).slice(0, 5);
    const drawStatsTable = document.querySelector('#draw-stats tbody');
    
    drawStatsTable.innerHTML = '';
    topDrawers.forEach(team => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${team.team}</td>
            <td>${team.drawn}</td>
        `;
        drawStatsTable.appendChild(row);
    });
}
