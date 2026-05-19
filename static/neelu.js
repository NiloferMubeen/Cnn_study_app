/* neelu.js — GUVI CNN Study
   - Injects GUVI logo into every page nav
   - Injects a persistent full nav bar on module pages so learners can jump between topics
   - Forces white background on all pages
   - Mounts Neelu chatbot (server-side Groq, no browser key)
   Place in: static/neelu.js
*/
(function () {
  'use strict';

  /* ── NAV ITEMS ───────────────────────────────────────── */
  const NAV_ITEMS = [
    { href:'/convolution',       icon:'⊕', label:'Convolution'     },
    { href:'/pooling',           icon:'⬇', label:'Pooling'         },
    { href:'/activation',        icon:'⚡', label:'Activation'      },
    { href:'/training',          icon:'🎯', label:'Training'        },
    { href:'/architectures',     icon:'🏛', label:'Architectures'   },
    { href:'/codeLab',           icon:'💻', label:'Code Lab'        },
    { href:'/data-augmentation', icon:'🔀', label:'Augmentation'    },
    { href:'/quiz',              icon:'🧠', label:'Quiz', pill:true  },
  ];

  /* ── STYLES ──────────────────────────────────────────── */
  function injectStyles() {
    if (document.getElementById('neelu-global-styles')) return;
    const s = document.createElement('style');
    s.id = 'neelu-global-styles';
    s.textContent = `
/* ── Force white background ── */
html, body { background: #ffffff !important; }

/* ── Global persistent top nav (module pages) ── */
#guvi-global-nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 9990;
  height: 56px;
  background: rgba(255,255,255,0.97);
  backdrop-filter: blur(14px) saturate(1.5);
  border-bottom: 1.5px solid #f0f0f0;
  display: flex; align-items: center;
  padding: 0 20px; gap: 6px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.06);
  overflow-x: auto;
}
#guvi-global-nav::-webkit-scrollbar { height: 0; }

.ggnav-logo {
  display: flex; align-items: center; gap: 7px;
  text-decoration: none; flex-shrink: 0; margin-right: 8px;
}
.ggnav-divider {
  width: 1px; height: 28px; background: #e5e7eb; flex-shrink: 0; margin: 0 4px;
}
.ggnav-links {
  display: flex; align-items: center; gap: 2px; flex: 1; overflow-x: auto;
}
.ggnav-links::-webkit-scrollbar { height: 0; }
.ggnav-link {
  display: flex; align-items: center; gap: 5px;
  text-decoration: none;
  font-size: .74rem; font-weight: 600;
  color: #52525b;
  padding: 5px 10px; border-radius: 8px;
  transition: all .18s; white-space: nowrap;
  font-family: 'Plus Jakarta Sans', 'Nunito Sans', sans-serif;
}
.ggnav-link:hover { color: #7D2AE8; background: #f3eeff; }
.ggnav-link.active {
  color: #7D2AE8; background: #f3eeff;
  font-weight: 700;
}
.ggnav-pill {
  background: #6366f1 !important; color: #fff !important;
  border-radius: 20px !important; padding: 5px 13px !important;
  font-weight: 700 !important;
  box-shadow: 0 2px 8px rgba(99,102,241,.3);
}
.ggnav-pill:hover { background: #4338ca !important; color: #fff !important; }

/* Push page content down so it's not hidden behind the fixed nav */
body.has-guvi-nav { padding-top: 56px !important; }
body.has-guvi-nav nav,
body.has-guvi-nav .nav { top: 56px !important; }

/* ── Neelu chatbot ── */
#neelu-fab{position:fixed;bottom:24px;right:24px;z-index:9998;width:54px;height:54px;border-radius:50%;border:none;cursor:pointer;background:linear-gradient(135deg,#FF6634,#ff9a6c);box-shadow:0 6px 24px rgba(255,102,52,.5);display:flex;align-items:center;justify-content:center;font-size:1.4rem;transition:all .2s;}
#neelu-fab:hover{transform:scale(1.1);box-shadow:0 8px 30px rgba(255,102,52,.65);}
#neelu-fab .n-badge{position:absolute;top:-2px;right:-2px;width:13px;height:13px;background:#10b981;border-radius:50%;border:2.5px solid #fff;}
#neelu-panel{position:fixed;bottom:88px;right:24px;z-index:9997;width:336px;height:500px;background:#fff;border-radius:22px;border:1.5px solid #f0f0f0;box-shadow:0 24px 70px rgba(0,0,0,.15);display:none;flex-direction:column;overflow:hidden;font-family:'Plus Jakarta Sans','Nunito Sans',sans-serif;}
#neelu-panel.open{display:flex;animation:nslide .22s ease;}
@keyframes nslide{from{opacity:0;transform:translateY(14px) scale(.96)}to{opacity:1;transform:none}}
#neelu-head{background:linear-gradient(135deg,#FF6634,#ff8c42);padding:12px 15px;display:flex;align-items:center;gap:9px;flex-shrink:0;}
#neelu-av{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.22);display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex-shrink:0;}
.n-hinfo{flex:1;}
.n-hname{color:#fff;font-weight:700;font-size:.88rem;}
.n-hsub{color:rgba(255,255,255,.8);font-size:.62rem;font-family:'DM Mono',monospace;letter-spacing:.04em;}
.n-hbtn{background:rgba(255,255,255,.2);border:none;color:#fff;width:27px;height:27px;border-radius:7px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.78rem;transition:background .15s;flex-shrink:0;}
.n-hbtn:hover{background:rgba(255,255,255,.36);}
#neelu-msgs{flex:1;overflow-y:auto;padding:11px;display:flex;flex-direction:column;gap:8px;background:#f9f9f9;}
#neelu-msgs::-webkit-scrollbar{width:3px;}
#neelu-msgs::-webkit-scrollbar-thumb{background:#e0e0e0;border-radius:2px;}
.n-msg{display:flex;gap:6px;}
.n-msg.user{flex-direction:row-reverse;}
.n-bubble{max-width:85%;padding:8px 12px;border-radius:13px;font-size:.81rem;line-height:1.58;}
.n-msg.bot .n-bubble{background:#fff;border:1px solid #eee;color:#1f2937;border-radius:4px 13px 13px 13px;}
.n-msg.user .n-bubble{background:linear-gradient(135deg,#FF6634,#ff8c42);color:#fff;border-radius:13px 4px 13px 13px;}
.n-time{font-size:.56rem;color:#bbb;margin-top:3px;font-family:'DM Mono',monospace;align-self:flex-end;}
.n-typing{display:flex;gap:4px;align-items:center;padding:9px 13px;}
.n-typing span{width:7px;height:7px;border-radius:50%;background:#FF6634;animation:nbounce .8s infinite;}
.n-typing span:nth-child(2){animation-delay:.16s;}.n-typing span:nth-child(3){animation-delay:.32s;}
@keyframes nbounce{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}
#neelu-quick{padding:0 11px 8px;display:flex;gap:5px;flex-wrap:wrap;flex-shrink:0;background:#f9f9f9;}
.n-qbtn{font-size:.63rem;padding:4px 9px;border-radius:20px;border:1px solid rgba(255,102,52,.4);background:#fff;color:#FF6634;cursor:pointer;transition:all .15s;font-family:'DM Mono',monospace;white-space:nowrap;}
.n-qbtn:hover{background:#FF6634;color:#fff;}
#neelu-foot{display:flex;gap:6px;padding:9px 11px;border-top:1px solid #f0f0f0;background:#fff;flex-shrink:0;}
#neelu-inp{flex:1;border:1.5px solid #e5e7eb;border-radius:9px;padding:7px 10px;font-size:.81rem;outline:none;resize:none;font-family:'Plus Jakarta Sans','Nunito Sans',sans-serif;line-height:1.4;max-height:76px;overflow-y:auto;transition:border-color .2s;}
#neelu-inp:focus{border-color:#FF6634;}
#neelu-send{width:34px;height:34px;border-radius:9px;border:none;background:#FF6634;color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:all .2s;font-size:.82rem;align-self:flex-end;}
#neelu-send:hover{background:#e55a2b;}
#neelu-send:disabled{background:#e0e0e0;cursor:not-allowed;}
`;
    document.head.appendChild(s);
  }

  /* ── GLOBAL NAV INJECTION ────────────────────────────── */
  function injectGlobalNav() {
    // Don't add on home page — it has its own full nav
    if (location.pathname === '/' || location.pathname === '') return;
    if (document.getElementById('guvi-global-nav')) return;

    const nav = document.createElement('div');
    nav.id = 'guvi-global-nav';

    // Logo
    const logo = document.createElement('a');
    logo.href = '/'; logo.className = 'ggnav-logo'; logo.title = 'Home';
    logo.innerHTML = `
      <img src="/static/guvi.png" alt="GUVI" style="height:32px;width:auto;display:block;object-fit:contain;">`;
    nav.appendChild(logo);

    const divider = document.createElement('div');
    divider.className = 'ggnav-divider';
    nav.appendChild(divider);

    const links = document.createElement('div');
    links.className = 'ggnav-links';

    const currentPath = location.pathname.replace(/\/$/, '');

    NAV_ITEMS.forEach(item => {
      const a = document.createElement('a');
      a.href = item.href;
      a.className = 'ggnav-link' +
        (currentPath === item.href ? ' active' : '') +
        (item.pill ? ' ggnav-pill' : '');
      a.innerHTML = `<span>${item.icon}</span><span>${item.label}</span>`;
      links.appendChild(a);
    });

    nav.appendChild(links);
    document.body.prepend(nav);
    document.body.classList.add('has-guvi-nav');
  }

  /* ── LEGACY NAV LOGO (index page has its own nav) ─────── */
  function injectLogoIntoExistingNav() {
    // Only for index page which has .nav-logo already — skip, already has GUVI logo
  }

  /* ── CHAT ─────────────────────────────────────────────── */
  let chatHistory = [];

  async function serverChat(userMsg) {
    chatHistory.push({ role: 'user', content: userMsg });
    try {
      const resp = await fetch('/api/neelu-chat', {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({
          message:   userMsg,
          history:   chatHistory.slice(-12),
          page_path: location.pathname,
        }),
      });
      const data  = await resp.json();
      const reply = data.reply || '❌ Empty response.';
      chatHistory.push({ role: 'assistant', content: reply });
      return reply;
    } catch (err) {
      const msg = '❌ Network error — check your connection.';
      chatHistory.push({ role: 'assistant', content: msg });
      return msg;
    }
  }

  /* ── BUILD CHATBOT UI ─────────────────────────────────── */
  function buildChatUI() {
    const fab = document.createElement('button');
    fab.id = 'neelu-fab'; fab.title = 'Chat with Neelu';
    fab.innerHTML = '🤖<div class="n-badge"></div>';
    document.body.appendChild(fab);

    const panel = document.createElement('div'); panel.id = 'neelu-panel';
    panel.innerHTML = `
      <div id="neelu-head">
        <div id="neelu-av">🤖</div>
        <div class="n-hinfo">
          <div class="n-hname">Neelu</div>
          <div class="n-hsub">GUVI · CNN Study Guide</div>
        </div>
        <div style="display:flex;gap:5px;">
          <button class="n-hbtn" id="n-clear" title="Clear chat">🗑</button>
          <button class="n-hbtn" id="n-close" title="Close">✕</button>
        </div>
      </div>
      <div id="neelu-msgs"></div>
      <div id="neelu-quick">
        <button class="n-qbtn" data-q="How do I use the interactive demo on this page?">Demo help</button>
        <button class="n-qbtn" data-q="What should I study next after this module?">What's next?</button>
        <button class="n-qbtn" data-q="Explain the main concept on this page simply">Explain this</button>
        <button class="n-qbtn" data-q="What is a CNN?">What is CNN?</button>
      </div>
      <div id="neelu-foot">
        <textarea id="neelu-inp" rows="1" placeholder="Ask Neelu anything…"></textarea>
        <button id="neelu-send">➤</button>
      </div>`;
    document.body.appendChild(panel);

    const msgs    = document.getElementById('neelu-msgs');
    const inp     = document.getElementById('neelu-inp');
    const sendBtn = document.getElementById('neelu-send');

    const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    const fmt = s => s
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g,     '<em>$1</em>')
      .replace(/`([^`]+)`/g,     '<code style="background:#f3f4f6;padding:1px 5px;border-radius:3px;font-family:monospace;font-size:.85em">$1</code>')
      .replace(/\n/g, '<br>');
    const ts  = () => new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' });
    const scrollB = () => { msgs.scrollTop = msgs.scrollHeight; };

    function addUser(t) {
      const d = document.createElement('div'); d.className = 'n-msg user';
      d.innerHTML = `<div><div class="n-bubble">${esc(t)}</div><div class="n-time">${ts()}</div></div>`;
      msgs.appendChild(d); scrollB();
    }
    function addBot(t) {
      const d = document.createElement('div'); d.className = 'n-msg bot';
      d.innerHTML = `<div style="font-size:1.1rem;flex-shrink:0;">🤖</div><div><div class="n-bubble">${fmt(t)}</div><div class="n-time">${ts()}</div></div>`;
      msgs.appendChild(d); scrollB();
    }
    function addTyping() {
      const d = document.createElement('div'); d.className = 'n-msg bot';
      d.innerHTML = `<div style="font-size:1.1rem;flex-shrink:0;">🤖</div><div class="n-typing"><span></span><span></span><span></span></div>`;
      msgs.appendChild(d); scrollB(); return d;
    }

    const PAGE_LABELS = {
      '/':               'the GUVI CNN Study home',
      '/convolution':    'the Convolution module',
      '/pooling':        'the Pooling module',
      '/activation':     'the Activation Functions module',
      '/training':       'the Training CNNs module',
      '/architectures':  'the Architectures module',
      '/codeLab':        'the Code Lab',
      '/data-augmentation': 'the Data Augmentation module',
      '/quiz':           'the Quiz page',
    };

    function welcome() {
      const page = PAGE_LABELS[location.pathname] || 'this page';
      addBot(`Hi GUVIan! 👋 I'm **Neelu**, your GUVI CNN study guide. I see you're on ${page}.\n\nAsk me anything — concepts, how to use the demo, where to go next. I'm here to help! 🚀`);
    }

    async function send(msg) {
      if (!msg.trim()) return;
      inp.value = ''; inp.style.height = 'auto';
      addUser(msg); sendBtn.disabled = true;
      const typing = addTyping();
      const reply  = await serverChat(msg);
      typing.remove(); sendBtn.disabled = false;
      addBot(reply);
    }

    fab.addEventListener('click', () => {
      panel.classList.toggle('open');
      if (panel.classList.contains('open') && !msgs.children.length) welcome();
    });
    document.getElementById('n-close').addEventListener('click', () => panel.classList.remove('open'));
    document.getElementById('n-clear').addEventListener('click', () => { chatHistory = []; msgs.innerHTML = ''; welcome(); });
    document.querySelectorAll('.n-qbtn').forEach(b => b.addEventListener('click', () => send(b.dataset.q)));
    sendBtn.addEventListener('click', () => send(inp.value));
    inp.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(inp.value); } });
    inp.addEventListener('input', () => { inp.style.height = 'auto'; inp.style.height = Math.min(inp.scrollHeight, 80) + 'px'; });
  }

  /* ── INIT ─────────────────────────────────────────────── */
  function init() {
    injectStyles();
    injectGlobalNav();
    buildChatUI();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();