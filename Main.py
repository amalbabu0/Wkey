<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<title>weys</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --bg: #0a0a0f; --surface: #12121a; --border: #2a2a3d;
  --accent: #7c6cfc; --accent2: #34a853;
  --text: #e8e6f0; --muted: #6b6880;
  --success: #34a853; --error: #ea4335; --code-bg: #0d0d15;
  --cobol: #fbbc04; --jcl: #ea4335;
}
body { font-family: 'Syne', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; }

/* ── Header ── */
header { padding: 1.1rem 1.25rem 0.9rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; gap: 10px; background: var(--surface); }
.logo-dot { width: 10px; height: 10px; border-radius: 50%; background: var(--accent); flex-shrink: 0; }
header h1 { font-size: 17px; font-weight: 800; letter-spacing: -0.02em; }
.provider-badge { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 2px 8px; border-radius: 4px; border: 1px solid var(--border); color: var(--muted); letter-spacing: 0.04em; transition: all 0.3s; }
.provider-badge.gemini  { background: rgba(66,133,244,0.12); border-color: rgba(66,133,244,0.35); color: #4285f4; }
.provider-badge.openai  { background: rgba(16,163,127,0.12); border-color: rgba(16,163,127,0.35); color: #10a37f; }
.provider-badge.claude  { background: rgba(210,130,80,0.12); border-color: rgba(210,130,80,0.35); color: #d28250; }
.provider-badge.groq    { background: rgba(244,67,54,0.12);  border-color: rgba(244,67,54,0.35);  color: #f44336; }
.provider-badge.openrouter { background: rgba(124,108,252,0.12); border-color: rgba(124,108,252,0.35); color: #7c6cfc; }
.status-pill { margin-left: auto; font-size: 11px; font-family: 'JetBrains Mono', monospace; padding: 3px 10px; border-radius: 20px; border: 1px solid var(--border); color: var(--muted); display: flex; align-items: center; gap: 5px; cursor: pointer; white-space: nowrap; }
.status-pill.connected { border-color: var(--success); color: var(--success); }
.status-pill.error { border-color: var(--error); color: var(--error); }
.status-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

main { flex: 1; padding: 1.25rem; display: flex; flex-direction: column; gap: 1rem; }

/* ── Config panel ── */
.config-panel { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1rem; display: none; flex-direction: column; gap: 0.9rem; }
.config-panel.open { display: flex; }
.config-panel label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-family: 'JetBrains Mono', monospace; display: block; margin-bottom: 4px; }
.config-hint { font-size: 11px; color: var(--muted); margin-top: 5px; line-height: 1.5; }
.config-hint a { color: var(--accent); text-decoration: none; }
.config-panel input, .config-panel select {
  width: 100%; background: var(--code-bg); border: 1px solid var(--border);
  border-radius: 8px; padding: 9px 12px; font-family: 'JetBrains Mono', monospace;
  font-size: 13px; color: var(--text); outline: none;
}
.config-panel input:focus, .config-panel select:focus { border-color: var(--accent); }
.config-panel select option { background: #1a1a26; }

.provider-pills { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 2px; }
.ppill { font-family: 'JetBrains Mono', monospace; font-size: 11px; padding: 4px 10px; border-radius: 20px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; transition: all 0.15s; }
.ppill.active { border-color: var(--accent); color: var(--accent); background: rgba(124,108,252,0.1); }

.delay-row { display: flex; align-items: center; gap: 10px; }
.delay-row label { font-size: 12px; color: var(--muted); white-space: nowrap; text-transform: none; letter-spacing: 0; margin-bottom: 0; }
.delay-row input[type=range] { flex: 1; accent-color: var(--accent); }
.delay-val { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--accent); min-width: 36px; text-align: right; }
.save-btn { background: var(--accent); color: #fff; border: none; border-radius: 8px; padding: 10px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 14px; cursor: pointer; }

/* ── Section ── */
.section-label { font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 6px; }

/* ── Language buttons ── */
.lang-grid { display: flex; gap: 8px; flex-wrap: wrap; }
.lang-btn { font-family: 'JetBrains Mono', monospace; font-size: 12px; padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border); background: transparent; color: var(--muted); cursor: pointer; transition: all 0.15s; }
.lang-btn.primary-cobol { border-color: rgba(251,188,4,0.5); color: var(--cobol); background: rgba(251,188,4,0.08); font-size: 13px; padding: 7px 18px; }
.lang-btn.primary-jcl   { border-color: rgba(234,67,53,0.5);  color: var(--jcl);   background: rgba(234,67,53,0.08);  font-size: 13px; padding: 7px 18px; }
.lang-btn.active-cobol { border-color: var(--cobol); color: #0a0a0f; background: var(--cobol); font-weight: 700; }
.lang-btn.active-jcl   { border-color: var(--jcl);   color: #fff;    background: var(--jcl);   font-weight: 700; }
.lang-btn.active-other { border-color: var(--accent); color: var(--accent); background: rgba(124,108,252,0.1); }
.active-lang-info { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); margin-top: 6px; }
.active-lang-info span { color: var(--text); }

/* ── Prompt ── */
.prompt-area { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
.prompt-area:focus-within { border-color: var(--accent); }
textarea { width: 100%; background: transparent; border: none; padding: 1rem; font-family: 'Syne', sans-serif; font-size: 15px; color: var(--text); resize: none; outline: none; min-height: 110px; line-height: 1.5; }
textarea::placeholder { color: var(--muted); }
.prompt-footer { padding: 0.6rem 1rem; border-top: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
.char-count { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); }
.generate-btn { background: var(--accent); color: #fff; border: none; border-radius: 8px; padding: 9px 18px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 14px; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.generate-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.spinner { width: 14px; height: 14px; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; border-radius: 50%; animation: spin 0.7s linear infinite; display: none; }
.spinner.visible { display: inline-block; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Code output ── */
.code-output { background: var(--code-bg); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; display: none; }
.code-output.visible { display: block; }
.code-header { padding: 0.7rem 1rem; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; }
.code-lang-badge { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--accent2); background: rgba(52,168,83,0.1); border: 1px solid rgba(52,168,83,0.2); padding: 2px 8px; border-radius: 4px; }
.code-actions { display: flex; gap: 8px; }
.icon-btn { background: transparent; border: 1px solid var(--border); border-radius: 6px; padding: 5px 10px; font-size: 12px; color: var(--muted); cursor: pointer; font-family: 'Syne', sans-serif; }
pre { padding: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 12.5px; line-height: 1.7; color: #c8c3e8; white-space: pre-wrap; word-break: break-word; max-height: 280px; overflow-y: auto; }

/* ── Type button ── */
.type-btn { width: 100%; background: var(--accent2); color: #fff; border: none; border-radius: 10px; padding: 15px; font-family: 'Syne', sans-serif; font-weight: 800; font-size: 16px; cursor: pointer; display: none; align-items: center; justify-content: center; gap: 8px; }
.type-btn.visible { display: flex; }
.type-btn:disabled { opacity: 0.4; cursor: not-allowed; }

/* ── Log ── */
.log-area { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 0.85rem 1rem; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--muted); display: none; line-height: 1.6; }
.log-area.visible { display: block; }
.log-area .ok   { color: var(--success); }
.log-area .err  { color: var(--error); }
.log-area .info { color: var(--accent); }
</style>
</head>
<body>

<header>
  <div class="logo-dot"></div>
  <h1>weys</h1>
  <span class="provider-badge" id="providerBadge">no provider</span>
  <div class="status-pill" id="statusPill" onclick="toggleConfig()">
    <div class="status-dot"></div>
    <span id="statusText">setup</span>
  </div>
</header>

<main>

  <!-- ── Settings ── -->
  <div class="config-panel open" id="configPanel">

    <div>
      <label>AI Provider</label>
      <div class="provider-pills">
        <button class="ppill" onclick="selectProvider(this,'gemini')">Gemini</button>
        <button class="ppill" onclick="selectProvider(this,'openai')">OpenAI</button>
        <button class="ppill" onclick="selectProvider(this,'claude')">Claude</button>
        <button class="ppill" onclick="selectProvider(this,'groq')">Groq</button>
        <button class="ppill" onclick="selectProvider(this,'openrouter')">OpenRouter</button>
        <button class="ppill" onclick="selectProvider(this,'custom')">Custom</button>
      </div>
    </div>

    <div>
      <label>API Key</label>
      <input type="password" id="apiKey" placeholder="Paste your API key here" oninput="autoDetectProvider(this.value)">
      <p class="config-hint" id="providerHint">Select a provider above or paste your key — it will auto-detect.</p>
    </div>

    <div id="modelRow">
      <label>Model</label>
      <input type="text" id="modelInput" placeholder="e.g. gemini-2.0-flash">
      <p class="config-hint" id="modelHint"></p>
    </div>

    <div id="customUrlRow" style="display:none;">
      <label>Custom API Base URL</label>
      <input type="text" id="customUrl" placeholder="https://your-api.com/v1">
    </div>

    <div>
      <label>Pico W IP Address</label>
      <input type="text" id="picoIp" placeholder="192.168.1.X">
      <p class="config-hint">Shown in serial monitor when Pico W boots</p>
    </div>

    <div class="delay-row">
      <label>Typing delay</label>
      <input type="range" min="10" max="200" value="50" id="delaySlider"
             oninput="document.getElementById('delayVal').textContent=this.value+'ms'">
      <span class="delay-val" id="delayVal">50ms</span>
    </div>

    <button class="save-btn" onclick="saveConfig()">Save & Connect</button>
  </div>

  <!-- ── Language ── -->
  <div>
    <div class="section-label">Language</div>
    <div class="lang-grid">
      <button class="lang-btn primary-cobol active-cobol" onclick="setLang(this,'COBOL','cobol')">COBOL</button>
      <button class="lang-btn primary-jcl"                onclick="setLang(this,'JCL','jcl')">JCL</button>
      <button class="lang-btn" onclick="setLang(this,'Java','other')">Java</button>
      <button class="lang-btn" onclick="setLang(this,'Python','other')">Python</button>
      <button class="lang-btn" onclick="setLang(this,'C++','other')">C++</button>
      <button class="lang-btn" onclick="setLang(this,'JavaScript','other')">JS</button>
      <button class="lang-btn" onclick="setLang(this,'Kotlin','other')">Kotlin</button>
      <button class="lang-btn" onclick="setLang(this,'Go','other')">Go</button>
      <button class="lang-btn" onclick="setLang(this,'TypeScript','other')">TS</button>
      <button class="lang-btn" onclick="setLang(this,'Rust','other')">Rust</button>
    </div>
    <div class="active-lang-info" id="langInfo">Generating: <span>COBOL</span></div>
  </div>

  <!-- ── Prompt ── -->
  <div>
    <div class="section-label">Prompt</div>
    <div class="prompt-area">
      <textarea id="promptInput"
        placeholder="e.g. write a program to add two numbers and display the result..."
        rows="4" oninput="updateCount()"></textarea>
      <div class="prompt-footer">
        <span class="char-count" id="charCount">0 chars</span>
        <button class="generate-btn" id="genBtn" onclick="generate()">
          <div class="spinner" id="spinner"></div>
          <span id="genBtnText">Generate</span>
        </button>
      </div>
    </div>
  </div>

  <!-- ── Code output ── -->
  <div class="code-output" id="codeOutput">
    <div class="code-header">
      <span class="code-lang-badge" id="codeLangBadge">cobol</span>
      <div class="code-actions">
        <button class="icon-btn" onclick="copyCode()">copy</button>
        <button class="icon-btn" onclick="clearAll()">clear</button>
      </div>
    </div>
    <pre id="codeBlock"></pre>
  </div>

  <!-- ── Type button ── -->
  <button class="type-btn" id="typeBtn" onclick="sendToPico()">
    ⌨ Type it on PC
  </button>

  <!-- ── Log ── -->
  <div class="log-area" id="logArea"></div>

</main>

<script>
// ── Provider definitions ────────────────────────────────────
const PROVIDERS = {
  gemini: {
    name: 'Gemini',
    defaultModel: 'gemini-2.0-flash',
    modelHint: 'gemini-2.0-flash · gemini-2.5-flash-preview-05-20 · gemini-1.5-flash',
    keyPrefix: 'AIza',
    getUrl: (model, key) =>
      `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`,
    buildBody: (system, prompt, model) => ({
      system_instruction: { parts: [{ text: system }] },
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.2, maxOutputTokens: 1024 }
    }),
    extractCode: d => d.candidates?.[0]?.content?.parts?.[0]?.text || '',
    freeLink: 'aistudio.google.com'
  },
  openai: {
    name: 'OpenAI',
    defaultModel: 'gpt-4o-mini',
    modelHint: 'gpt-4o-mini · gpt-4o · gpt-4-turbo · gpt-3.5-turbo',
    keyPrefix: 'sk-',
    getUrl: () => 'https://api.openai.com/v1/chat/completions',
    buildBody: (system, prompt, model) => ({
      model,
      max_tokens: 1024,
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: prompt }
      ]
    }),
    getHeaders: key => ({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + key
    }),
    extractCode: d => d.choices?.[0]?.message?.content || '',
    freeLink: null
  },
  claude: {
    name: 'Claude',
    defaultModel: 'claude-sonnet-4-20250514',
    modelHint: 'claude-sonnet-4-20250514 · claude-haiku-4-5-20251001 · claude-opus-4-20250514',
    keyPrefix: 'sk-ant-',
    getUrl: () => 'https://api.anthropic.com/v1/messages',
    buildBody: (system, prompt, model) => ({
      model,
      max_tokens: 1024,
      system,
      messages: [{ role: 'user', content: prompt }]
    }),
    getHeaders: key => ({
      'Content-Type': 'application/json',
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    }),
    extractCode: d => d.content?.[0]?.text || '',
    freeLink: null
  },
  groq: {
    name: 'Groq',
    defaultModel: 'llama-3.3-70b-versatile',
    modelHint: 'llama-3.3-70b-versatile · llama-3.1-8b-instant · mixtral-8x7b-32768',
    keyPrefix: 'gsk_',
    getUrl: () => 'https://api.groq.com/openai/v1/chat/completions',
    buildBody: (system, prompt, model) => ({
      model,
      max_tokens: 1024,
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: prompt }
      ]
    }),
    getHeaders: key => ({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + key
    }),
    extractCode: d => d.choices?.[0]?.message?.content || '',
    freeLink: 'console.groq.com'
  },
  openrouter: {
    name: 'OpenRouter',
    defaultModel: 'meta-llama/llama-3.3-70b-instruct:free',
    modelHint: 'meta-llama/llama-3.3-70b-instruct:free · google/gemma-3-27b-it:free · deepseek/deepseek-r1:free',
    keyPrefix: 'sk-or-',
    getUrl: () => 'https://openrouter.ai/api/v1/chat/completions',
    buildBody: (system, prompt, model) => ({
      model,
      max_tokens: 1024,
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: prompt }
      ]
    }),
    getHeaders: key => ({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + key
    }),
    extractCode: d => d.choices?.[0]?.message?.content || '',
    freeLink: 'openrouter.ai'
  },
  custom: {
    name: 'Custom',
    defaultModel: '',
    modelHint: 'Enter the model name for your custom API',
    keyPrefix: null,
    getUrl: (model, key, baseUrl) => (baseUrl || '').replace(/\/$/, '') + '/chat/completions',
    buildBody: (system, prompt, model) => ({
      model,
      max_tokens: 1024,
      temperature: 0.2,
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: prompt }
      ]
    }),
    getHeaders: key => ({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + key
    }),
    extractCode: d => d.choices?.[0]?.message?.content || '',
    freeLink: null
  }
};

const LANG_HINTS = {
  'COBOL': 'Use standard COBOL format with IDENTIFICATION, ENVIRONMENT, DATA, and PROCEDURE divisions. Column-aware: code in columns 7-72. Use DISPLAY for output.',
  'JCL':   'Use standard IBM JCL syntax with proper // notation. Include JOB, EXEC, and DD statements as needed. Each line starts at column 1 with //.',
  'Java':  'Write complete Java with proper class structure and main method.',
  'Python':'Write clean Python, ready to run.',
  'C++':   'Write complete C++ with proper includes and main function.',
  'JavaScript': 'Write clean JavaScript.',
  'Kotlin':'Write complete Kotlin with main function.',
  'Go':    'Write complete Go with package main and main function.',
  'TypeScript': 'Write complete TypeScript.',
  'Rust':  'Write complete Rust with fn main().'
};

// ── State ───────────────────────────────────────────────────
let selectedLang = 'COBOL';
let selectedLangType = 'cobol';
let selectedProviderKey = 'gemini';
let generatedCode = '';
let config = { provider: 'gemini', apiKey: '', model: '', customUrl: '', ip: '', delay: 50 };

// ── Init ────────────────────────────────────────────────────
function loadConfig() {
  try {
    const saved = localStorage.getItem('codetyper_v3');
    if (!saved) return;
    config = { ...config, ...JSON.parse(saved) };
    document.getElementById('apiKey').value = config.apiKey || '';
    document.getElementById('picoIp').value = config.ip || '';
    document.getElementById('delaySlider').value = config.delay || 50;
    document.getElementById('delayVal').textContent = (config.delay || 50) + 'ms';
    document.getElementById('customUrl').value = config.customUrl || '';
    applyProvider(config.provider || 'gemini');
    document.getElementById('modelInput').value = config.model || PROVIDERS[config.provider || 'gemini'].defaultModel;
    if (config.apiKey && config.ip) {
      document.getElementById('configPanel').classList.remove('open');
      pingPico();
    }
  } catch(e) {}
}

function applyProvider(key) {
  selectedProviderKey = key;
  const p = PROVIDERS[key];
  // Highlight pill
  document.querySelectorAll('.ppill').forEach(b => {
    b.classList.toggle('active', b.textContent.toLowerCase() === p.name.toLowerCase());
  });
  // Badge
  const badge = document.getElementById('providerBadge');
  badge.textContent = p.name;
  badge.className = 'provider-badge ' + key;
  // Model hint
  document.getElementById('modelHint').textContent = p.modelHint;
  if (!document.getElementById('modelInput').value || document.getElementById('modelInput').value === (PROVIDERS[config.provider]?.defaultModel)) {
    document.getElementById('modelInput').value = p.defaultModel;
  }
  // Custom URL row
  document.getElementById('customUrlRow').style.display = key === 'custom' ? 'block' : 'none';
  // Provider hint
  const hint = document.getElementById('providerHint');
  if (p.freeLink) {
    hint.innerHTML = 'Free key at <a href="https://' + p.freeLink + '" target="_blank">' + p.freeLink + '</a> — no credit card needed.';
  } else {
    hint.textContent = p.name + ' API key. Paste it above.';
  }
}

function selectProvider(btn, key) {
  config.provider = key;
  applyProvider(key);
  document.getElementById('modelInput').value = PROVIDERS[key].defaultModel;
}

function autoDetectProvider(key) {
  if (!key) return;
  for (const [id, p] of Object.entries(PROVIDERS)) {
    if (p.keyPrefix && key.startsWith(p.keyPrefix)) {
      applyProvider(id);
      config.provider = id;
      return;
    }
  }
}

function saveConfig() {
  config.provider = selectedProviderKey;
  config.apiKey = document.getElementById('apiKey').value.trim();
  config.model = document.getElementById('modelInput').value.trim() || PROVIDERS[selectedProviderKey].defaultModel;
  config.customUrl = document.getElementById('customUrl').value.trim();
  config.ip = document.getElementById('picoIp').value.trim();
  config.delay = parseInt(document.getElementById('delaySlider').value);
  try { localStorage.setItem('codetyper_v3', JSON.stringify(config)); } catch(e) {}
  document.getElementById('configPanel').classList.remove('open');
  pingPico();
}

function toggleConfig() {
  document.getElementById('configPanel').classList.toggle('open');
}

// ── Language ────────────────────────────────────────────────
function setLang(btn, lang, type) {
  selectedLang = lang;
  selectedLangType = type;
  document.querySelectorAll('.lang-btn').forEach(b =>
    b.classList.remove('active-cobol','active-jcl','active-other'));
  btn.classList.add('active-' + type);
  document.getElementById('langInfo').innerHTML = 'Generating: <span>' + lang + '</span>';
}

function updateCount() {
  document.getElementById('charCount').textContent =
    document.getElementById('promptInput').value.length + ' chars';
}

// ── Status ──────────────────────────────────────────────────
function setStatus(state, text) {
  document.getElementById('statusPill').className = 'status-pill ' + state;
  document.getElementById('statusText').textContent = text;
}

async function pingPico() {
  if (!config.ip) return;
  setStatus('', 'checking...');
  try {
    const r = await fetch('http://' + config.ip + ':5000/ping', { signal: AbortSignal.timeout(3000) });
    setStatus(r.ok ? 'connected' : 'error', r.ok ? 'pico ready' : 'pico error');
  } catch {
    setStatus('error', 'pico offline');
  }
}

function log(msg, type) {
  const el = document.getElementById('logArea');
  el.classList.add('visible');
  el.innerHTML = '<span class="' + (type || '') + '">' + msg + '</span>';
}

// ── Generate ────────────────────────────────────────────────
async function generate() {
  const prompt = document.getElementById('promptInput').value.trim();
  if (!prompt) { log('⚠ Enter a prompt first', 'err'); return; }
  if (!config.apiKey) { log('⚠ Add your API key in settings (tap status pill)', 'err'); return; }

  const btn = document.getElementById('genBtn');
  btn.disabled = true;
  document.getElementById('spinner').classList.add('visible');
  document.getElementById('genBtnText').textContent = 'Generating...';
  log('Calling ' + PROVIDERS[config.provider].name + ' API...', 'info');

  const hint = LANG_HINTS[selectedLang] || '';
  const systemPrompt =
    'You are a ' + selectedLang + ' code generator.\n' +
    'STRICT RULES:\n' +
    '- Output ONLY the raw ' + selectedLang + ' code. Nothing else.\n' +
    '- No explanation. No markdown. No backticks. No code fences.\n' +
    '- Do NOT write any text before or after the code.\n' +
    '- Start directly with the very first line of code.\n' +
    '- Make it complete and ready to use.\n' +
    (hint ? hint : '');

  const p = PROVIDERS[config.provider];
  const model = config.model || p.defaultModel;

  try {
    const url = p.getUrl(model, config.apiKey, config.customUrl);
    const body = p.buildBody(systemPrompt, prompt, model);
    const headers = p.getHeaders
      ? p.getHeaders(config.apiKey)
      : { 'Content-Type': 'application/json' };

    const res = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });

    const data = await res.json();
    if (!res.ok) {
      const errMsg = data.error?.message || data.error?.msg || JSON.stringify(data.error) || 'API error ' + res.status;
      throw new Error(errMsg);
    }

    let code = p.extractCode(data);
    // Strip any accidental markdown fences
    code = code.replace(/^```[\w]*\r?\n?/, '').replace(/\r?\n?```$/, '').trim();
    if (!code) throw new Error('API returned empty code — try rephrasing your prompt');

    generatedCode = code;
    document.getElementById('codeBlock').textContent = generatedCode;
    document.getElementById('codeLangBadge').textContent = selectedLang.toLowerCase();
    document.getElementById('codeOutput').classList.add('visible');
    document.getElementById('typeBtn').classList.add('visible');
    log('✓ Code ready! Click into your editor on PC, then tap "Type it on PC"', 'ok');

  } catch(err) {
    log('✗ ' + err.message, 'err');
  } finally {
    btn.disabled = false;
    document.getElementById('spinner').classList.remove('visible');
    document.getElementById('genBtnText').textContent = 'Generate';
  }
}

// ── Send to Pico ────────────────────────────────────────────
async function sendToPico() {
  if (!generatedCode) return;
  if (!config.ip) { log('⚠ Set Pico W IP in settings', 'err'); return; }

  const btn = document.getElementById('typeBtn');
  btn.disabled = true;
  btn.innerHTML = '⏳ Sending to Pico W...';
  log('Sending — switch to your editor now! (1.5s head start)', 'info');

  try {
    const res = await fetch('http://' + config.ip + ':5000/type', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: generatedCode, delay: config.delay })
    });
    if (res.ok) {
      log('✓ Typing in progress on your PC!', 'ok');
      btn.innerHTML = '✓ Done!';
      setTimeout(() => { btn.disabled = false; btn.innerHTML = '⌨ Type it on PC'; }, 3000);
    } else {
      throw new Error('Pico returned error ' + res.status);
    }
  } catch(err) {
    log('✗ ' + err.message + ' — is Pico online and on same WiFi?', 'err');
    btn.disabled = false;
    btn.innerHTML = '⌨ Type it on PC';
  }
}

function copyCode() {
  navigator.clipboard.writeText(generatedCode).then(() => log('✓ Copied!', 'ok'));
}

function clearAll() {
  generatedCode = '';
  document.getElementById('codeOutput').classList.remove('visible');
  document.getElementById('typeBtn').classList.remove('visible');
  document.getElementById('logArea').classList.remove('visible');
  document.getElementById('promptInput').value = '';
  document.getElementById('charCount').textContent = '0 chars';
}

loadConfig();
</script>
</body>
</html>