/* FarmSphere — Disease Detection JS */
const leafInput  = document.getElementById('leafInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const uploadZone = document.getElementById('uploadZone');

// Drag & drop
uploadZone?.addEventListener('dragover', e => { e.preventDefault(); uploadZone.classList.add('dz-over'); });
uploadZone?.addEventListener('dragleave', () => uploadZone.classList.remove('dz-over'));
uploadZone?.addEventListener('drop', e => {
    e.preventDefault(); uploadZone.classList.remove('dz-over');
    if (e.dataTransfer.files[0]) handleFile(e.dataTransfer.files[0]);
});
uploadZone?.addEventListener('click', e => { if (e.target.tagName !== 'BUTTON') leafInput.click(); });
leafInput?.addEventListener('change', () => { if (leafInput.files[0]) handleFile(leafInput.files[0]); });

function handleFile(file) {
    if (!file.type.startsWith('image/')) { toast('Please upload an image file', 'error'); return; }
    const reader = new FileReader();
    reader.onload = e => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('uzIdle').style.display    = 'none';
        document.getElementById('uzPreview').style.display = 'block';
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

async function analyzeDisease() {
    if (!leafInput.files[0]) return;
    setLoading(analyzeBtn, true);

    const fd = new FormData();
    fd.append('image', leafInput.files[0]);

    try {
        const d = await apiFetch('/api/disease/upload', { method:'POST', body:fd });
        if (!d.success) throw new Error(d.error);

        document.getElementById('placeholderCard').style.display = 'none';
        document.getElementById('diseaseResult').style.display   = 'block';

        document.getElementById('rhName').textContent = d.disease;
        document.getElementById('rhIcon').textContent = d.disease === 'Healthy' ? '🌿' : '🔴';

        // Severity badge
        const sev = { 'Healthy':'badge-green','Leaf Spot':'badge-amber','Early Blight':'badge-amber',
                       'Late Blight':'badge-red','Powdery Mildew':'badge-amber' };
        const badge = document.getElementById('rhSeverity');
        badge.className = 'badge ' + (sev[d.disease] || 'badge-amber');
        badge.textContent = d.disease === 'Healthy' ? 'No Disease' : 'Disease Detected';

        document.getElementById('confPct').textContent = d.confidence + '%';
        setTimeout(() => {
            const fill = document.getElementById('confFill');
            fill.style.width = d.confidence + '%';
            fill.style.background = d.confidence > 80 ? '#22c55e' : d.confidence > 60 ? '#f59e0b' : '#ef4444';
        }, 80);

        document.getElementById('infoTreatment').textContent = d.treatment  || '—';
        document.getElementById('infoFertilizer').textContent = d.fertilizer || '—';
        document.getElementById('infoPrevention').textContent = d.prevention || '—';

        const rh = document.getElementById('resultHeader');
        rh.className = 'result-header card ' + (d.disease === 'Healthy' ? 'rh-healthy' : 'rh-disease');

        toast(`Analysis complete: ${d.disease} (${d.confidence}%)`, 'success');
    } catch (err) {
        toast('Analysis failed: ' + err.message, 'error');
    } finally {
        setLoading(analyzeBtn, false);
        analyzeBtn.innerHTML = '🔬 Analyze Disease';
    }
}

function resetUpload() {
    leafInput.value = '';
    document.getElementById('previewImg').src = '';
    document.getElementById('uzIdle').style.display    = 'block';
    document.getElementById('uzPreview').style.display = 'none';
    analyzeBtn.disabled = true;
    document.getElementById('diseaseResult').style.display   = 'none';
    document.getElementById('placeholderCard').style.display = 'block';
    document.getElementById('confFill').style.width = '0%';
}
