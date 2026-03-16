/* FarmSphere — Weather JS */
let tChart = null, rChart = null;

document.addEventListener('DOMContentLoaded', () => loadWeather());
document.getElementById('cityInput')?.addEventListener('keypress', e => { if (e.key === 'Enter') loadWeather(); });

async function loadWeather() {
    const city = document.getElementById('cityInput').value.trim() || 'Pune';
    const alertEl = document.getElementById('weatherAlert');
    alertEl.className = 'alert alert-info';
    alertEl.textContent = `Loading weather for ${city}…`;
    document.getElementById('weatherHero').style.display = 'none';

    const fd = new FormData(); fd.append('city', city);
    try {
        const d = await apiFetch('/api/weather', { method:'POST', body:fd });
        if (!d.success) throw new Error(d.error);
        renderWeather(d.data, alertEl);

        const fd2 = new FormData(); fd2.append('city', city);
        const f = await apiFetch('/api/forecast', { method:'POST', body:fd2 });
        if (f.success) renderForecast(f.data);
    } catch (e) {
        alertEl.className = 'alert alert-danger';
        alertEl.textContent = '❌ Could not load weather. Check city name.';
    }
}

function renderWeather(w, alertEl) {
    alertEl.className = 'alert alert-success';
    alertEl.textContent = `✅ Loaded for ${w.city}${w.country ? ', '+w.country : ''}`;
    document.getElementById('weatherHero').style.display = 'flex';

    set('whIcon', wxEmoji(w.icon || '02d'));
    set('whTemp', (w.temperature ?? '--') + '°C');
    set('whDesc', w.condition || '--');
    set('whCity', [w.city, w.country].filter(Boolean).join(', '));
    set('wFeels', (w.feels_like ?? '--') + '°C');
    set('wHumid', (w.humidity ?? '--') + '%');
    set('wWind',  (w.wind_speed ?? '--') + ' km/h');
    set('wPress', (w.pressure ?? '--') + ' hPa');
    set('wVis',   (w.visibility ?? '--') + ' km');
    set('wDew',   (w.dew_point ?? '--') + '°C');
}

function renderForecast(list) {
    const grid = document.getElementById('forecastGrid');
    grid.innerHTML = list.map((f, i) => `
        <div class="fc-card ${i===0?'fc-today':''}">
            <div class="fc-day">${f.day}</div>
            <div class="fc-icon">${wxEmoji(f.icon || '01d')}</div>
            <div class="fc-high">${f.high_temp}°</div>
            <div class="fc-low">${f.low_temp}°</div>
            <div class="fc-rain">💧 ${f.rain_probability}%</div>
        </div>`).join('');

    buildCharts(list);
}

function buildCharts(list) {
    const labels = list.map(f => f.day);
    const highs  = list.map(f => f.high_temp);
    const lows   = list.map(f => f.low_temp);
    const rains  = list.map(f => f.rain_probability);
    const base   = { responsive:true,
        plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12, font:{ size:11 } } } },
        scales:{ x:{ grid:{ color:'rgba(74,222,128,.05)' } }, y:{ grid:{ color:'rgba(74,222,128,.05)' } } }
    };

    tChart?.destroy();
    tChart = new Chart(document.getElementById('tempChart'), {
        type:'line', data:{ labels, datasets:[
            { label:'High °C', data:highs, borderColor:'#f97316', backgroundColor:'rgba(249,115,22,.1)', fill:true, tension:.4, borderWidth:2 },
            { label:'Low °C',  data:lows,  borderColor:'#38bdf8', fill:false, tension:.4, borderWidth:2 }
        ]}, options:{ ...base, scales:{ ...base.scales, y:{ ticks:{ callback: v => v+'°' } } } }
    });

    rChart?.destroy();
    rChart = new Chart(document.getElementById('rainChart'), {
        type:'bar', data:{ labels, datasets:[{
            label:'Rain %', data:rains, borderRadius:6,
            backgroundColor: rains.map(r => r>60?'rgba(56,189,248,.7)':r>30?'rgba(56,189,248,.4)':'rgba(56,189,248,.2)')
        }]}, options:{ ...base, scales:{ ...base.scales, y:{ max:100, ticks:{ callback: v => v+'%' } } } }
    });
}

function set(id, v) { const e = document.getElementById(id); if (e) e.textContent = v; }
