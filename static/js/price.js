/* FarmSphere — Price Prediction JS */
let trendChart = null;

// Set default season based on current month
document.addEventListener('DOMContentLoaded', () => {
    const m = new Date().getMonth() + 1;
    const sel = document.getElementById('seasonSel');
    if (sel) sel.value = (m >= 6 && m <= 11) ? 'Kharif' : (m >= 11 || m <= 4) ? 'Rabi' : 'Zaid';
});

async function predictPrice() {
    const crop   = document.getElementById('cropSel').value;
    const market = document.getElementById('marketSel').value;
    const season = document.getElementById('seasonSel').value;
    const btn    = document.getElementById('predictBtn');

    setLoading(btn, true);

    const fd = new FormData();
    fd.append('crop', crop);
    fd.append('market', market);
    fd.append('season', season);

    try {
        const d = await apiFetch('/api/price/predict', { method:'POST', body:fd });
        if (!d.success) throw new Error(d.error);

        document.getElementById('pricePlaceholder').style.display = 'none';
        document.getElementById('priceResult').style.display      = 'block';

        // Main price
        document.getElementById('priceBig').textContent  = '₹' + Number(d.predicted_price).toLocaleString('en-IN');
        document.getElementById('priceCtx').textContent  = `${d.crop} · ${d.market} · ${d.season}`;

        // Badge
        const badge = document.getElementById('priceBadge');
        const pct   = d.percentage_vs_msp;
        badge.className = 'badge ' + (pct >= 0 ? 'badge-green' : 'badge-red');
        badge.textContent = (pct >= 0 ? '↑ +' : '↓ ') + Math.abs(pct).toFixed(1) + '% vs MSP';

        // vs MSP
        const diff = d.difference_from_msp;
        const vsMSP = document.getElementById('vsMSP');
        vsMSP.textContent  = (diff >= 0 ? '+' : '') + '₹' + Math.abs(diff).toLocaleString('en-IN');
        vsMSP.style.color  = diff >= 0 ? 'var(--green-400)' : '#f87171';

        // Insight alert
        const ins = document.getElementById('priceInsight');
        if (pct > 10) {
            ins.className = 'alert alert-success';
            ins.textContent = `🟢 Sell Now — Price is ${pct.toFixed(1)}% above MSP. Excellent selling opportunity.`;
        } else if (pct > 2) {
            ins.className = 'alert alert-info';
            ins.textContent = `🟡 Good Time — Price is moderately above MSP. Consider selling in batches.`;
        } else if (pct > -5) {
            ins.className = 'alert alert-warning';
            ins.textContent = `🟠 Hold — Price near MSP. Wait 3–4 weeks for seasonal uptick.`;
        } else {
            ins.className = 'alert alert-danger';
            ins.textContent = `🔴 Store — Price below MSP. Explore government procurement or wait for recovery.`;
        }

        document.getElementById('trendTitle').textContent = `${d.crop} — Annual Price Trend`;

        // Trend chart
        if (trendChart) trendChart.destroy();
        const labels = d.trend.map(t => t.month);
        const prices = d.trend.map(t => t.price);
        const mspLine = prices.map(() => d.msp);

        trendChart = new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels,
                datasets: [
                    {
                        label: `${d.crop} ₹/Q`,
                        data: prices,
                        borderColor: '#22c55e',
                        backgroundColor: 'rgba(34,197,94,.08)',
                        fill: true,
                        tension: 0.4,
                        pointRadius: 4,
                        pointBackgroundColor: '#22c55e',
                        borderWidth: 2
                    },
                    {
                        label: 'MSP',
                        data: mspLine,
                        borderColor: '#f97316',
                        borderDash: [6, 4],
                        pointRadius: 0,
                        borderWidth: 1.5,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position:'bottom', labels:{ boxWidth:12, font:{ size:11 } } },
                    tooltip: { callbacks: { label: ctx => ' ₹' + ctx.parsed.y.toLocaleString('en-IN') } }
                },
                scales: {
                    x: { grid:{ color:'rgba(74,222,128,.05)' } },
                    y: {
                        grid: { color:'rgba(74,222,128,.05)' },
                        ticks: { callback: v => '₹' + (v/1000).toFixed(1) + 'K' }
                    }
                }
            }
        });

        toast(`Predicted: ₹${Number(d.predicted_price).toLocaleString('en-IN')}/quintal`, 'success');
    } catch (err) {
        toast('Prediction failed: ' + err.message, 'error');
    } finally {
        setLoading(btn, false);
        btn.innerHTML = '📈 Predict Price';
    }
}
