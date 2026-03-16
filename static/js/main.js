/* FarmSphere — Shared JS */
document.addEventListener('DOMContentLoaded', () => {
    // Nav burger
    const burger = document.getElementById('navBurger');
    const menu   = document.getElementById('navMenu');
    burger?.addEventListener('click', () => menu.classList.toggle('open'));
    menu?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => menu.classList.remove('open')));

    // Scroll shrink
    const nb = document.getElementById('navbar');
    window.addEventListener('scroll', () => nb.classList.toggle('scrolled', window.scrollY > 20));

    // Intersection fade-in
    const io = new IntersectionObserver(entries => {
        entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('[data-fade]').forEach(el => io.observe(el));
});

// ── Fetch wrapper ──────────────────────────────────────
async function apiFetch(url, opts = {}) {
    const res = await fetch(url, opts);
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return res.json();
}

// ── Loading state ──────────────────────────────────────
function setLoading(btn, on) {
    if (on) {
        btn.disabled = true;
        btn._orig = btn.innerHTML;
        btn.innerHTML = '<span class="spin"></span> Loading…';
    } else {
        btn.disabled = false;
        btn.innerHTML = btn._orig || 'Submit';
    }
}

// ── Weather icon map ───────────────────────────────────
function wxEmoji(icon) {
    const m = { '01d':'☀️','01n':'🌙','02d':'⛅','02n':'⛅','03d':'☁️','03n':'☁️','04d':'☁️','04n':'☁️',
                '09d':'🌧️','09n':'🌧️','10d':'🌦️','10n':'🌧️','11d':'⛈️','11n':'⛈️','13d':'❄️','50d':'🌫️' };
    return m[icon] || '🌤️';
}

// ── Toast ──────────────────────────────────────────────
function toast(msg, type = 'success') {
    document.querySelector('.fs-toast')?.remove();
    const t = document.createElement('div');
    const c = { success:'#22c55e', error:'#ef4444', warning:'#f59e0b', info:'#38bdf8' };
    t.className = 'fs-toast';
    Object.assign(t.style, {
        position:'fixed', bottom:'24px', right:'24px', zIndex:9999,
        background:'rgba(14,34,24,.95)', border:`1px solid ${c[type]}40`,
        color: c[type], padding:'12px 20px', borderRadius:'12px',
        fontSize:'.875rem', fontWeight:'500', boxShadow:'0 8px 32px rgba(0,0,0,.4)',
        backdropFilter:'blur(12px)', animation:'fadeIn .3s ease', maxWidth:'340px',
        fontFamily:"'DM Sans',sans-serif"
    });
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 4000);
}

// ── Chart defaults ─────────────────────────────────────
if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#9dc8a8';
    Chart.defaults.borderColor = 'rgba(74,222,128,.08)';
    Chart.defaults.font.family = "'DM Sans',sans-serif";
}
