/* ============================================================
   weys — app.js
   ============================================================ */
'use strict';

// ── Provider definitions ──────────────────────────────────────
const P = {
  gemini: {
    name: 'Gemini', prefix: 'AIza', free: 'aistudio.google.com',
    models: ['gemini-2.0-flash', 'gemini-2.5-flash-preview-05-20', 'gemini-1.5-flash'],
    url:     (m, k) => `https://generativelanguage.googleapis.com/v1beta/models/${m}:generateContent?key=${k}`,
    body:    (s, p, m) => ({ system_instruction: { parts: [{ text: s }] }, contents: [{ parts: [{ text: p }] }], generationConfig: { temperature: 0.2, maxOutputTokens: 1024 } }),
    headers: () => ({ 'Content-Type': 'application/json' }),
    pick:    d => d.candidates?.[0]?.content?.parts?.[0]?.text || ''
  },
  openai: {
    name: 'OpenAI', prefix: 'sk-', free: null,
    models: ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo'],
    url:     () => 'https://api.openai.com/v1/chat/completions',
    body:    (s, p, m) => ({ model: m, max_tokens: 1024, temperature: 0.2, messages: [{ role: 'system', content: s }, { role: 'user', content: p }] }),
    headers: k => ({ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + k }),
    pick:    d => d.choices?.[0]?.message?.content || ''
  },
  claude: {
    name: 'Claude', prefix: 'sk-ant-', free: null,
    models: ['claude-sonnet-4-20250514', 'claude-haiku-4-5-20251001'],
    url:     () => 'https://api.anthropic.com/v1/messages',
    body:    (s, p, m) => ({ model: m, max_tokens: 1024, system: s, messages: [{ role: 'user', content: p }] }),
    headers: k => ({ 'Content-Type': 'application/json', 'x-api-key': k, 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' }),
    pick:    d => d.content?.[0]?.text || ''
  },
  groq: {
    name: 'Groq', prefix: 'gsk_', free: 'console.groq.com',
    models: ['llama-3.3-70b-versatile', 'llama-3.1-8b-instant', 'mixtral-8x7b-32768'],
    url:     () => 'https://api.groq.com/openai/v1/chat/completions',
    body:    (s, p, m) => ({ model: m, max_tokens: 1024, temperature: 0.2, messages: [{ role: 'system', content: s }, { role: 'user', content: p }] }),
    headers: k => ({ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + k }),
    pick:    d => d.choices?.[0]?.message?.content || ''
  },
  openrouter: {
    name: 'OpenRouter', prefix: 'sk-or-', free: 'openrouter.ai',
    models: ['meta-llama/llama-3.3-70b-instruct:free', 'google/gemma-3-27b-it:free', 'deepseek/deepseek-r1:free'],
    url:     () => 'https://openrouter.ai/api/v1/chat/completions',
    body:    (s, p, m) => ({ model: m, max_tokens: 1024, temperature: 0.2, messages: [{ role: 'system', content: s }, { role: 'user', content: p }] }),
    headers: k => ({ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + k }),
    pick:    d => d.choices?.[0]?.message?.content || ''
  },
  custom: {
    name: 'Custom', prefix: null, free: null, models: [],
    url:     (m, k, b) => (b || '').replace(/\/$/, '') + '/chat/completions',
    body:    (s, p, m) => ({ model: m, max_tokens: 1024, temperature: 0.2, messages: [{ role: 'system', content: s }, { role: 'user', content: p }] }),
    headers: k => ({ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + k }),
    pick:    d => d.choices?.[0]?.message?.content || ''
  }
};

// ── Language hints ────────────────────────────────────────────
const HINTS = {
  COBOL:      'Standard COBOL: IDENTIFICATION, ENVIRONMENT, DATA, PROCEDURE DIVISION. Columns 7-72. DISPLAY for output.',
  JCL:        'IBM JCL syntax. // notation. JOB, EXEC, DD statements. Each line starts with //.',
  Java:       'Complete Java class with main method.',
  Python:     'Clean Python.',
  'C++':      'Complete C++ with includes and main.',
  JavaScript: 'Clean JavaScript.',
  Kotlin:     'Complete Kotlin with main.',
  Go:         'Complete Go, package main.',
  TypeScript: 'Complete TypeScript.',
  Rust:       'Complete Rust, fn main().'
};

// ── State ─────────────────────────────────────────────────────
let lang     = 'COBOL';
let langType = 'cobol';
let provKey  = 'gemini';
let genCode  = '';
let cfg = { provider: 'gemini', apiKey: '', model: '', customUrl: '', ip: '', delay: 50 };

// ── Ripple ────────────────────────────────────────────────────
function addRipple(e, el) {
  const r    = el.getBoundingClientRect();
  const size = Math.max(r.width, r.height) * 2;
  const rip  = document.createElement('span');
  rip.className  = 'ripple-effect';
  rip.style.cssText = `width:${size}px;height:${size}px;left:${e.clientX - r.left - size / 2}px;top:${e.clientY - r.top - size / 2}px`;
  el.appendChild(rip);
  setTimeout(() => rip.remove(), 700);

  // Keystroke particle burst on type button
  if (el.classList && el.classList.contains('type-btn')) {
    burstKeystrokes(e.clientX, e.clientY);
  }
}

// ── Slider fill updater ──────────────────────────────────────
function updateSlider(el) {
  const min = +el.min, max = +el.max;
  const pct = ((+el.value - min) / (max - min)) * 100;
  el.style.setProperty('--slider-fill', pct + '%');
  document.getElementById('delayVal').textContent = el.value + 'ms';
}

// ── Keystroke particle burst ──────────────────────────────────
function burstKeystrokes(cx, cy) {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const chars = ['{ }', '< >', '( )', '=>', ';', '_', '/*', '*/', '[]', '#!', '0', '1'];
  const n = 10;
  for (let i = 0; i < n; i++) {
    const p = document.createElement('span');
    p.className = 'keystroke-particle';
    p.textContent = chars[Math.floor(Math.random() * chars.length)];
    const angle = (Math.PI * (i / n)) + (Math.random() * .5 - .25);
    const dist  = 60 + Math.random() * 50;
    p.style.left = (cx - 8) + 'px';
    p.style.top  = (cy - 10) + 'px';
    p.style.setProperty('--px', (Math.cos(-angle) * dist) + 'px');
    p.style.setProperty('--py', (-Math.abs(Math.sin(angle)) * dist - 20) + 'px');
    document.body.appendChild(p);
    setTimeout(() => p.remove(), 950);
  }
}

// ── Boot ──────────────────────────────────────────────────────
function boot() {
  // Theme
  try {
    if (localStorage.getItem('ct_theme') === 'dark') {
      document.body.classList.add('dark');
      document.getElementById('themeBtn').textContent = '🌙';
    }
  } catch (e) {}

  // Init slider fill (works whether or not config is saved)
  updateSlider(document.getElementById('delaySlider'));

  // Config
  try {
    const s = localStorage.getItem('ct_v6');
    if (!s) { return; }
    cfg = { ...cfg, ...JSON.parse(s) };
    document.getElementById('apiKey').value      = cfg.apiKey    || '';
    document.getElementById('picoIp').value      = cfg.ip        || '';
    document.getElementById('customUrl').value   = cfg.customUrl || '';
    document.getElementById('delaySlider').value = cfg.delay     || 50;
    updateSlider(document.getElementById('delaySlider'));

    // Restore provider dropdown
    const pSel = document.getElementById('providerSelect');
    if (cfg.provider) pSel.value = cfg.provider;
    applyProvider(cfg.provider || 'gemini');
    document.getElementById('modelInput').value = cfg.model || P[cfg.provider || 'gemini'].models[0];

    // Restore language dropdown
    if (cfg.lang) {
      const lSel = document.getElementById('langSelect');
      const opt  = [...lSel.options].find(o => o.value.startsWith(cfg.lang + '|'));
      if (opt) lSel.value = opt.value;
      const [l, t] = (opt ? opt.value : 'COBOL|cobol').split('|');
      lang = l; langType = t;
      updateLangPill();
    }

    if (cfg.apiKey && cfg.ip) pingPico();
  } catch (e) {}
}

// ── Language change (from dropdown) ──────────────────────────
function onLangChange(sel) {
  const [l, t] = sel.value.split('|');
  lang = l; langType = t;
  updateLangPill();
}

function updateLangPill() {
  const pill  = document.getElementById('langPill');
  const label = document.getElementById('langPillLabel');
  pill.className = 'sel-pill lang-' + langType;
  // Animate swap
  label.style.opacity   = '0';
  label.style.transform = 'translateY(-5px)';
  setTimeout(() => {
    label.textContent     = lang;
    label.style.transition = 'all 0.2s var(--spring)';
    label.style.opacity   = '1';
    label.style.transform = 'none';
  }, 100);
}

// ── Provider change (from dropdown) ──────────────────────────
function onProviderChange(key) {
  cfg.provider = key;
  applyProvider(key);
  document.getElementById('modelInput').value = P[key].models[0] || '';
}

function applyProvider(key) {
  provKey = key;
  const p = P[key];

  // Sync dropdown
  const sel = document.getElementById('providerSelect');
  if (sel.value !== key) sel.value = key;

  // Model chips
  const chips = document.getElementById('modelChips');
  chips.innerHTML = p.models.map(m =>
    `<span class="mchip" onclick="pickModel('${m}')">${m}</span>`
  ).join('');

  // Custom URL
  document.getElementById('customUrlField').style.display = key === 'custom' ? '' : 'none';

  // Provider hint
  const h = document.getElementById('providerHint');
  h.innerHTML = p.free
    ? `Free key at <a href="https://${p.free}" target="_blank">${p.free}</a> — no credit card needed.`
    : `${p.name} API key required.`;

  // Provider pill in prompt card
  const pill  = document.getElementById('providerPill');
  const label = document.getElementById('providerPillLabel');
  pill.className = 'sel-pill provider-pill ' + key;
  label.textContent = p.name;
}

function pickModel(m) {
  document.getElementById('modelInput').value = m;
  document.querySelectorAll('.mchip').forEach(c => {
    c.classList.toggle('active', c.textContent === m);
  });
}

// ── Auto-detect provider from key prefix ─────────────────────
function autoDetect(k) {
  for (const [id, p] of Object.entries(P)) {
    if (p.prefix && k.startsWith(p.prefix)) {
      cfg.provider = id;
      applyProvider(id);
      document.getElementById('providerSelect').value = id;
      return;
    }
  }
}

// ── Save config ───────────────────────────────────────────────
function saveConfig() {
  cfg.provider  = provKey;
  cfg.lang      = lang;
  cfg.apiKey    = document.getElementById('apiKey').value.trim();
  cfg.model     = document.getElementById('modelInput').value.trim() || P[provKey].models[0];
  cfg.customUrl = document.getElementById('customUrl').value.trim();
  cfg.ip        = document.getElementById('picoIp').value.trim();
  cfg.delay     = parseInt(document.getElementById('delaySlider').value);
  try { localStorage.setItem('ct_v6', JSON.stringify(cfg)); } catch (e) {}
  closeSheet();
  applyProvider(cfg.provider);
  updateLangPill();
  pingPico();
}

// ── Sheet open / close ────────────────────────────────────────
function toggleSheet() {
  document.getElementById('sheet').classList.contains('open') ? closeSheet() : openSheet();
}
function openSheet() {
  document.getElementById('sheet').classList.add('open');
  document.getElementById('overlay').classList.add('open');
  document.getElementById('settingsBtn').classList.add('active');
}
function closeSheet() {
  document.getElementById('sheet').classList.remove('open');
  document.getElementById('overlay').classList.remove('open');
  document.getElementById('settingsBtn').classList.remove('active');
}

// ── Char counter ──────────────────────────────────────────────
function onType() {
  const val = document.getElementById('promptInput').value;
  const cc  = document.getElementById('charCount');
  cc.textContent = val.length + ' chars';
  cc.classList.toggle('active', val.length > 0);
}

// ── Pico status ───────────────────────────────────────────────
function setStatus(state, label) {
  const b = document.getElementById('picoBadge');
  b.className = 'pico-badge' + (state === 'online' ? ' online' : state === 'offline' ? ' offline' : '');
  document.getElementById('statusLabel').textContent = label;
  const d = document.getElementById('statusDot');
  d.className = 'status-dot' + (state === '' ? ' pulse' : '');
  b.style.transform = 'scale(1.08)';
  setTimeout(() => b.style.transform = '', 220);
}

async function pingPico() {
  if (!cfg.ip) { setStatus('', 'Setup'); return; }
  setStatus('', 'Checking...');
  try {
    const r = await fetch('http://' + cfg.ip + ':5000/ping', { signal: AbortSignal.timeout(3000) });
    r.ok ? setStatus('online', 'Online ✓') : setStatus('offline', 'Error');
  } catch { setStatus('offline', 'Offline'); }
}

// ── Toast ─────────────────────────────────────────────────────
let _toastT = null;
function toast(msg, type = 'info', icon = '') {
  const el = document.getElementById('toast');
  document.getElementById('toastMsg').textContent  = msg;
  document.getElementById('toastIcon').textContent = icon;
  el.className = 'toast show ' + type;
  clearTimeout(_toastT);
  _toastT = setTimeout(() => el.className = 'toast', 3800);
}

// ── Theme ─────────────────────────────────────────────────────
function toggleTheme() {
  const dark = document.body.classList.toggle('dark');
  const btn  = document.getElementById('themeBtn');
  btn.textContent    = dark ? '🌙' : '☀️';
  btn.style.transform = 'rotate(360deg) scale(1.2)';
  setTimeout(() => btn.style.transform = '', 340);
  try { localStorage.setItem('ct_theme', dark ? 'dark' : 'light'); } catch (e) {}
}

// ── Generate ──────────────────────────────────────────────────
async function generate() {
  const prompt = document.getElementById('promptInput').value.trim();
  if (!prompt)     { toast('Enter a prompt first', 'err', '⚠️'); document.getElementById('promptInput').focus(); return; }
  if (!cfg.apiKey) { toast('Add your API key in Settings', 'err', '🔑'); openSheet(); return; }

  const btn = document.getElementById('genBtn');
  btn.disabled = true;
  document.getElementById('spinner').classList.add('on');
  document.getElementById('genTxt').textContent = 'Generating...';

  // Show skeleton
  document.getElementById('codeCard').classList.add('show');
  document.getElementById('skelLines').classList.add('show');
  document.getElementById('codeBlock').style.display = 'none';
  document.getElementById('progWrap').classList.add('on');

  toast('Asking ' + P[cfg.provider].name + '...', 'info', '⚡');

  const sys =
    `You are a ${lang} code generator.\nSTRICT RULES:\n` +
    `- Output ONLY raw ${lang} code. Nothing else.\n` +
    `- No explanation. No markdown. No backticks.\n` +
    `- Start directly with the first line of code.\n` +
    `- Complete and ready to use.\n` +
    (HINTS[lang] || '');

  const prov  = P[cfg.provider];
  const model = cfg.model || prov.models[0];

  try {
    const res  = await fetch(prov.url(model, cfg.apiKey, cfg.customUrl), {
      method: 'POST', headers: prov.headers(cfg.apiKey),
      body: JSON.stringify(prov.body(sys, prompt, model))
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error?.message || data.error?.msg || 'API error ' + res.status);

    let c = prov.pick(data).replace(/^```[\w]*\r?\n?/, '').replace(/\r?\n?```$/, '').trim();
    if (!c) throw new Error('Empty response — try rephrasing your prompt');

    genCode = c;
    document.getElementById('skelLines').classList.remove('show');
    document.getElementById('codeBlock').style.display = '';
    document.getElementById('codeBlock').textContent   = genCode;
    document.getElementById('codeLangBadge').textContent = 'output.' + lang.toLowerCase();
    document.getElementById('typeWrap').classList.add('show');

    // Scroll to bottom smoothly
    setTimeout(() => {
      const m = document.querySelector('main');
      m.scrollTo({ top: m.scrollHeight, behavior: 'smooth' });
    }, 80);

    toast('Code ready! 🎉', 'ok', '✅');

  } catch (e) {
    document.getElementById('skelLines').classList.remove('show');
    document.getElementById('codeCard').classList.remove('show');
    document.getElementById('codeBlock').style.display = '';
    toast(e.message, 'err', '❌');
  } finally {
    btn.disabled = false;
    document.getElementById('spinner').classList.remove('on');
    document.getElementById('genTxt').textContent = 'Generate ✦';
    document.getElementById('progWrap').classList.remove('on');
  }
}

// ── Send to Pico ──────────────────────────────────────────────
async function sendToPico() {
  if (!genCode) return;
  if (!cfg.ip)  { toast('Set Pico W IP in Settings', 'err', '📡'); openSheet(); return; }

  const btn = document.getElementById('typeBtn');
  btn.disabled = true;
  document.getElementById('typeTxt').textContent = 'Sending...';
  toast('Switch to your editor — typing in 1.5s!', 'info', '⏳');

  try {
    const r = await fetch('http://' + cfg.ip + ':5000/type', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: genCode, delay: cfg.delay })
    });
    if (!r.ok) throw new Error('Pico error ' + r.status);

    document.getElementById('typeTxt').textContent = 'Typing...';

    const tp       = document.getElementById('typingProgress');
    const bar      = document.getElementById('tpBar');
    const approxMs = genCode.length * cfg.delay;

    tp.classList.add('show');
    bar.style.transition = `width ${approxMs / 1000}s linear`;
    setTimeout(() => bar.style.width = '100%', 80);

    setTimeout(() => {
      tp.classList.remove('show');
      bar.style.width = '0'; bar.style.transition = 'none';
      document.getElementById('typeTxt').textContent = 'Done ✓';
      toast('Typed on your PC!', 'ok', '⌨️');
      setTimeout(() => {
        btn.disabled = false;
        document.getElementById('typeTxt').textContent = 'Type it on PC';
      }, 2000);
    }, approxMs + 1800);

  } catch (e) {
    toast(e.message + ' — check WiFi', 'err', '❌');
    btn.disabled = false;
    document.getElementById('typeTxt').textContent = 'Type it on PC';
  }
}

// ── Copy & Clear ──────────────────────────────────────────────
function copyCode() {
  navigator.clipboard.writeText(genCode).then(() => {
    toast('Copied to clipboard!', 'ok', '📋');
    const btn  = event.target;
    const orig = btn.textContent;
    btn.textContent = '✓ Copied';
    setTimeout(() => btn.textContent = orig, 2000);
  });
}

function clearAll() {
  genCode = '';
  const card = document.getElementById('codeCard');
  const wrap = document.getElementById('typeWrap');
  card.style.transition = 'opacity .28s, transform .28s';
  card.style.opacity    = '0';
  card.style.transform  = 'scale(.97)';
  wrap.style.transition = 'opacity .28s';
  wrap.style.opacity    = '0';
  setTimeout(() => {
    card.classList.remove('show'); wrap.classList.remove('show');
    card.style.cssText = ''; wrap.style.cssText = '';
    document.getElementById('promptInput').value      = '';
    document.getElementById('charCount').textContent  = '0 chars';
    document.getElementById('charCount').classList.remove('active');
  }, 300);
}

// ── Start ─────────────────────────────────────────────────────
boot();