/* FarmSphere — Dashboard JS */
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    initCharts();
});

async function loadDashboard() {
    try {
        const d = await apiFetch('/api/dashboard-stats?city=Pune');
        if (!d.success) return;
        const w = d.weather;
        setText('dashTemp',  w.temperature);
        setText('dashFeels', 'Feels like ' + (w.feels_like || w.temperature));
        setText('dashHumid', w.humidity);
        setText('dashWind',  'Wind: ' + w.wind_speed + ' km/h');
        setText('dashRain',  w.rain_probability);
        setText('dashCond',  w.condition);

        // Market pulse
        const mp = d.market_trends || {};
        const el = document.getElementById('marketPulse');
        if (el) el.innerHTML = Object.entries(mp).map(([k, v]) => `
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border)">
                <span style="color:var(--text-2);text-transform:capitalize">${k}</span>
                <span style="color:var(--green-400);font-weight:700;font-family:var(--ff-display)">₹${v.current}</span>
                <span class="badge ${v.trend==='up'?'badge-green':v.trend==='down'?'badge-red':'badge-amber'}">${v.change}</span>
            </div>`).join('');
    } catch (e) { console.warn('Dashboard load:', e.message); }
}

function setText(id, val) { const el = document.getElementById(id); if (el) el.textContent = val; }

function initCharts() {
    const months = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'];
    const opts = {
        responsive: true,
        plugins: { legend: { position:'bottom', labels: { boxWidth:12, font:{ size:11 } } } },
        scales: {
            x: { grid:{ color:'rgba(74,222,128,.05)' } },
            y: { grid:{ color:'rgba(74,222,128,.05)' } }
        }
    };

    // Market chart
    const mc = document.getElementById('marketChart');
    if (mc) new Chart(mc, {
        type: 'line',
        data: {
            labels: months,
            datasets: [
                { label:'Wheat', data:[2280,2250,2310,2350,2200,2180,2280,2320,2400,2500,2450,2300],
                  borderColor:'#fbbf24', backgroundColor:'rgba(251,191,36,.08)', fill:true, tension:.4, borderWidth:2, pointRadius:2 },
                { label:'Rice',  data:[2300,2280,2320,2340,2260,2200,2250,2310,2370,2430,2390,2320],
                  borderColor:'#86efac', fill:false, tension:.4, borderWidth:2, pointRadius:2 },
                { label:'Maize', data:[2090,2070,2100,2120,2060,2020,2060,2100,2140,2180,2160,2110],
                  borderColor:'#f97316', fill:false, tension:.4, borderWidth:2, pointRadius:2 },
            ]
        },
        options: { ...opts, scales: { ...opts.scales, y: { ...opts.scales.y, ticks:{ callback: v => '₹'+v } } } }
    });

    // Crop analytics donut
    const cc = document.getElementById('cropChart');
    if (cc) new Chart(cc, {
        type: 'doughnut',
        data: {
            labels: ['Healthy','At Risk','Diseased'],
            datasets: [{ data:[75,15,10], backgroundColor:['#22c55e','#f59e0b','#ef4444'], borderWidth:0 }]
        },
        options: { responsive:true, plugins:{ legend:{ position:'bottom', labels:{ boxWidth:12 } } }, cutout:'65%' }
    });
}
