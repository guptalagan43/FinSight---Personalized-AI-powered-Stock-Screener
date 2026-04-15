/**
 * FinSight – AI Chatbot v3.0
 * Rich, personalized chatbot with Gemini AI, voice input, copy response,
 * streaming animation, suggestions, history, and markdown rendering.
 */

/* ── State ──────────────────────────────────────────────── */
let chatMessages = [];
let chatSuggestionsLoaded = false;
let chatHistoryLoaded = false;
let chatPanelOpen = false;
let isRecording = false;
let recognition = null;

/* ── Toggle Panel ───────────────────────────────────────── */
function toggleChatbot() {
    const panel = document.getElementById('chatbot-panel');
    if (!panel) return;

    chatPanelOpen = !chatPanelOpen;
    panel.classList.toggle('open', chatPanelOpen);

    // Hide FAB when panel is open
    const fab = document.querySelector('.chatbot-fab');
    if (fab) fab.style.opacity = chatPanelOpen ? '0' : '1';
    if (fab) fab.style.pointerEvents = chatPanelOpen ? 'none' : 'auto';

    if (chatPanelOpen && !chatSuggestionsLoaded) {
        loadChatSuggestions();
        chatSuggestionsLoaded = true;
    }
    if (chatPanelOpen && !chatHistoryLoaded) {
        loadChatHistory();
        chatHistoryLoaded = true;
    }

    // Focus input
    if (chatPanelOpen) {
        setTimeout(() => {
            const input = document.getElementById('chat-input');
            if (input) input.focus();
        }, 300);
    }
}

/* ── Get Instrument ID from URL ─────────────────────────── */
function getChatInstrumentId() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    return id ? parseInt(id) : null;
}

/* ── Load Suggestions ───────────────────────────────────── */
async function loadChatSuggestions() {
    if (!Auth.isLoggedIn()) return;
    const container = document.getElementById('chat-suggestions');
    if (!container) return;

    try {
        const instrumentId = getChatInstrumentId();
        const url = instrumentId
            ? `/chat/suggestions?instrumentId=${instrumentId}`
            : '/chat/suggestions';
        const data = await api.get(url);
        const suggestions = data.suggestions || [];

        if (suggestions.length > 0) {
            container.innerHTML = suggestions.map(s =>
                `<button class="chat-suggestion-chip" onclick="useSuggestion(this)">${escapeHtml(s)}</button>`
            ).join('');
            container.style.display = 'flex';
        }
    } catch (err) {
        console.log('Could not load suggestions:', err);
    }
}

/* ── Load Chat History ──────────────────────────────────── */
async function loadChatHistory() {
    if (!Auth.isLoggedIn()) return;
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;

    try {
        const instrumentId = getChatInstrumentId();
        const url = instrumentId
            ? `/chat/history?instrumentId=${instrumentId}&limit=10`
            : '/chat/history?limit=10';
        const data = await api.get(url);
        const history = data.history || [];

        if (history.length > 0) {
            const welcomeMsg = messagesEl.querySelector('.chat-message.ai');
            const historyHtml = history.reverse().map(h => `
                <div class="chat-message user">${escapeHtml(h.user_message)}</div>
                <div class="chat-message ai">${formatChatMarkdown(h.ai_response_summary)}</div>
            `).join('');

            if (welcomeMsg) {
                welcomeMsg.insertAdjacentHTML('afterend', historyHtml);
            }
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }
    } catch (err) {
        console.log('Could not load history:', err);
    }
}

/* ── Use Suggestion Chip ────────────────────────────────── */
function useSuggestion(btn) {
    const input = document.getElementById('chat-input');
    if (input) {
        input.value = btn.textContent;
        sendChat();
    }
}

/* ── Send Chat Message ──────────────────────────────────── */
async function sendChat() {
    const input = document.getElementById('chat-input');
    const messagesEl = document.getElementById('chat-messages');
    if (!input || !messagesEl) return;

    const text = input.value.trim();
    if (!text) return;
    input.value = '';

    // Check auth
    if (!Auth.isLoggedIn()) {
        addChatMessage('ai', '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="width: 1em; height: 1em; vertical-align: middle;"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg> Please **log in** to use the AI assistant. Your responses will be personalized to your profile, portfolio, and investment goals.');
        return;
    }

    const instrumentId = getChatInstrumentId();

    // Add user message
    addChatMessage('user', text);

    // Hide suggestions after first message
    const sugContainer = document.getElementById('chat-suggestions');
    if (sugContainer) sugContainer.style.display = 'none';

    // Show typing indicator
    const typingId = 'typing-' + Date.now();
    messagesEl.insertAdjacentHTML('beforeend', `
        <div class="chat-message ai typing-msg" id="${typingId}">
            <div class="typing-indicator">
                <span></span><span></span><span></span>
            </div>
        </div>
    `);
    messagesEl.scrollTop = messagesEl.scrollHeight;

    try {
        const data = await api.post('/chat', { instrumentId, userMessage: text });
        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.classList.remove('typing-msg');
            // Streaming-feel animation: reveal word by word
            animateResponseReveal(typingEl, data.response);
        }

        // Show follow-up suggestions
        loadFollowUpSuggestions();
    } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) {
            typingEl.classList.remove('typing-msg');
            typingEl.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle;"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> Sorry, I couldn\'t process your message. Please try again.';
        }
    }
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

/* ── Streaming-Feel Reveal Animation ────────────────────── */
function animateResponseReveal(element, rawText) {
    const formattedHtml = formatChatMarkdown(rawText);
    const copyBtnHtml = `<button class="chat-copy-btn" onclick="copyChatResponse(this)" title="Copy response">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
    </button>`;

    // Set content immediately but start with opacity animation
    element.innerHTML = `<div class="chat-response-body reveal-anim">${formattedHtml}</div>${copyBtnHtml}`;
    element.classList.add('has-copy');

    const body = element.querySelector('.chat-response-body');
    if (body) {
        body.style.opacity = '0';
        body.style.transform = 'translateY(8px)';
        requestAnimationFrame(() => {
            body.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            body.style.opacity = '1';
            body.style.transform = 'translateY(0)';
        });
    }

    const messagesEl = document.getElementById('chat-messages');
    if (messagesEl) messagesEl.scrollTop = messagesEl.scrollHeight;
}

/* ── Copy Response ──────────────────────────────────────── */
function copyChatResponse(btn) {
    const msgEl = btn.closest('.chat-message');
    const body = msgEl.querySelector('.chat-response-body');
    const text = body ? body.innerText : msgEl.innerText;
    navigator.clipboard.writeText(text).then(() => {
        btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        btn.classList.add('copied');
        setTimeout(() => {
            btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>`;
            btn.classList.remove('copied');
        }, 2000);
    });
}

/* ── Clear Chat ─────────────────────────────────────────── */
function clearChat() {
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;
    messagesEl.innerHTML = `
        <div class="chat-message ai">Hi! I'm your <strong>FinSight AI assistant</strong> powered by Gemini. I can analyze stocks, review your portfolio, explain financial concepts, and give personalized advice. Ask me anything! 🚀</div>
    `;
    chatSuggestionsLoaded = false;
    loadChatSuggestions();
}

/* ── Voice Input (Web Speech API) ───────────────────────── */
function toggleVoiceInput() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        showToast('Voice input not supported in this browser', 'error');
        return;
    }

    const voiceBtn = document.getElementById('chat-voice-btn');

    if (isRecording) {
        if (recognition) recognition.stop();
        isRecording = false;
        if (voiceBtn) voiceBtn.classList.remove('recording');
        return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        isRecording = true;
        if (voiceBtn) voiceBtn.classList.add('recording');
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = transcript;
            sendChat();
        }
    };

    recognition.onerror = () => {
        isRecording = false;
        if (voiceBtn) voiceBtn.classList.remove('recording');
    };

    recognition.onend = () => {
        isRecording = false;
        if (voiceBtn) voiceBtn.classList.remove('recording');
    };

    recognition.start();
}

/* ── Add Message to Chat ────────────────────────────────── */
function addChatMessage(type, content) {
    const messagesEl = document.getElementById('chat-messages');
    if (!messagesEl) return;

    const rendered = type === 'user' ? escapeHtml(content) : formatChatMarkdown(content);
    messagesEl.insertAdjacentHTML('beforeend',
        `<div class="chat-message ${type}">${rendered}</div>`
    );
    messagesEl.scrollTop = messagesEl.scrollHeight;
}

/* ── Load Follow-up Suggestions ─────────────────────────── */
async function loadFollowUpSuggestions() {
    if (!Auth.isLoggedIn()) return;
    const container = document.getElementById('chat-suggestions');
    if (!container) return;

    try {
        const instrumentId = getChatInstrumentId();
        const url = instrumentId
            ? `/chat/suggestions?instrumentId=${instrumentId}`
            : '/chat/suggestions';
        const data = await api.get(url);
        const suggestions = data.suggestions || [];

        if (suggestions.length > 0) {
            container.innerHTML = suggestions.slice(0, 4).map(s =>
                `<button class="chat-suggestion-chip" onclick="useSuggestion(this)">${escapeHtml(s)}</button>`
            ).join('');
            container.style.display = 'flex';
        }
    } catch (err) {
        // Silent fail
    }
}

/* ── HTML Escape ────────────────────────────────────────── */
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

/* ── Rich Markdown Formatter ────────────────────────────── */
function formatChatMarkdown(text) {
    if (!text) return '';

    let html = text;

    // Tables: detect markdown tables and convert
    html = html.replace(/^(\|.+\|)\n(\|[-| :]+\|)\n((?:\|.+\|\n?)+)/gm, (match, header, sep, body) => {
        const headerCells = header.split('|').filter(c => c.trim());
        const bodyRows = body.trim().split('\n');

        let table = '<table class="chat-table"><thead><tr>';
        headerCells.forEach(c => { table += `<th>${c.trim()}</th>`; });
        table += '</tr></thead><tbody>';

        bodyRows.forEach(row => {
            const cells = row.split('|').filter(c => c.trim());
            table += '<tr>';
            cells.forEach(c => {
                let content = c.trim();
                // Color P&L values
                if (content.match(/[+-]\d.*%/) || content.match(/🟢|🔴/)) {
                    const isPositive = content.includes('+') || content.includes('🟢');
                    table += `<td class="${isPositive ? 'text-positive' : 'text-negative'}">${content}</td>`;
                } else {
                    table += `<td>${content}</td>`;
                }
            });
            table += '</tr>';
        });
        table += '</tbody></table>';
        return table;
    });

    // Score bars
    html = html.replace(/\[([█░]+)\]/g, '<span class="score-bar">[$1]</span>');

    // Bold with **
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    // Italic with *
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

    // Bullet points
    html = html.replace(/^[•·]\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/^[-]\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');

    // Headings (not used in chat but just in case)
    html = html.replace(/^### (.+)$/gm, '<h4 class="chat-heading">$1</h4>');
    html = html.replace(/^## (.+)$/gm, '<h3 class="chat-heading">$1</h3>');

    // Line breaks
    html = html.replace(/\n\n/g, '<br><br>');
    html = html.replace(/\n/g, '<br>');

    // ── Emoji to SVG icon conversion ──
    const emojiSVGs = {
        '📈': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
        '📉': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg>',
        '📊': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        '🔍': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        '✅': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polyline points="20 6 9 17 4 12"/></svg>',
        '🏆': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2z"/></svg>',
        '💡': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0 0 18 8 6 6 0 0 0 6 8c0 1.5.82 2.8 2.5 3.5.76.76 1.23 1.52 1.41 2.5"/></svg>',
        '💰': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        '🛡️': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        '🚀': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="M12 15l-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>',
        '🎯': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        '⭐': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'
    };
    for (const [emoji, svg] of Object.entries(emojiSVGs)) {
        html = html.replaceAll(emoji, svg);
    }

    // Color-coded indicators
    html = html.replace(/🟢/g, '<span class="emoji-green"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg></span>');
    html = html.replace(/🔴/g, '<span class="emoji-red"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><polyline points="22 17 13.5 8.5 8.5 13.5 2 7"/><polyline points="16 17 22 17 22 11"/></svg></span>');

    // Warning icon
    const warnSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
    html = html.replaceAll('⚠️', warnSVG);
    html = html.replaceAll('⚠', warnSVG);

    // Disclaimer styling
    html = html.replace(/\*Disclaimer:(.+?)\*/g, '<div class="chat-disclaimer">' + warnSVG + ' <em>Disclaimer:$1</em></div>');

    return html;
}
