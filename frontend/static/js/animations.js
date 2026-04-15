/**
 * FinSight – Hidden Finance Pattern Background
 * Financial patterns (candlesticks, charts, grids) are invisible until
 * the cursor moves near them, revealing them with a spotlight effect.
 */

(function () {
    'use strict';

    const SPOT = {
        radius: 300,
        softEdge: 100,      // gradient fade at edge
        patternAlpha: 1.0,  // max alpha of revealed patterns (increased for full vividness)
    };

    let mouseX = -9999, mouseY = -9999;
    let smoothX = -9999, smoothY = -9999;

    function initFinanceBackground() {
        // ── Main visible canvas ──
        const canvas = document.createElement('canvas');
        canvas.id = 'finance-bg';
        canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none;';
        document.body.prepend(canvas);
        const ctx = canvas.getContext('2d');

        // ── Offscreen canvas for patterns ──
        const offscreen = document.createElement('canvas');
        const offCtx = offscreen.getContext('2d');

        let W, H, dpr;

        function resize() {
            dpr = Math.min(window.devicePixelRatio, 2);
            W = window.innerWidth;
            H = window.innerHeight;
            canvas.width = offscreen.width = W * dpr;
            canvas.height = offscreen.height = H * dpr;
            canvas.style.width = W + 'px';
            canvas.style.height = H + 'px';
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            offCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
            drawPatterns();
        }

        window.addEventListener('mousemove', e => {
            mouseX = e.clientX;
            mouseY = e.clientY;
        }, { passive: true });

        // ── Draw all the finance patterns onto offscreen canvas ──
        function drawPatterns() {
            offCtx.clearRect(0, 0, W, H);

            const cols = Math.ceil(W / 180) + 1;
            const rows = Math.ceil(H / 160) + 1;

            for (let row = 0; row < rows; row++) {
                for (let col = 0; col < cols; col++) {
                    const cx = col * 180 + 30 + (row % 2) * 90;
                    const cy = row * 160 + 40;
                    const patternType = (row * cols + col) % 7;

                    offCtx.save();
                    offCtx.translate(cx, cy);

                    switch (patternType) {
                        case 0: drawCandlesticks(offCtx); break;
                        case 1: drawLineChart(offCtx); break;
                        case 2: drawBarChart(offCtx); break;
                        case 3: drawGridPattern(offCtx); break;
                        case 4: drawPieChart(offCtx); break;
                        case 5: drawTrendArrow(offCtx); break;
                        case 6: drawAreaChart(offCtx); break;
                    }

                    offCtx.restore();
                }
            }
        }

        
        // ── Pattern drawing functions ──

        function drawCandlesticks(c) {
            const candles = 8;
            const w = 12, gap = 6;
            for (let i = 0; i < candles; i++) {
                const x = i * (w + gap);
                const bodyH = 15 + Math.abs(Math.sin(i * 1.8)) * 30;
                const wickH = bodyH * 0.6;
                const top = 80 - bodyH - Math.sin(i * 0.9) * 20;

                c.strokeStyle = 'rgba(59, 130, 246, 0.3)';
                c.fillStyle = 'rgba(59, 130, 246, 0.05)';
                c.lineWidth = 1.2;

                // Wick
                c.beginPath();
                c.moveTo(x + w / 2, top - wickH);
                c.lineTo(x + w / 2, top + bodyH + wickH);
                c.stroke();

                // Body
                c.fillRect(x, top, w, bodyH);
                c.strokeRect(x, top, w, bodyH);
            }
        }

        function drawLineChart(c) {
            c.strokeStyle = 'rgba(59, 130, 246, 0.4)';
            c.lineWidth = 1.5;
            c.beginPath();
            const pts = [60, 45, 55, 30, 40, 20, 35, 15, 25, 38, 22, 30, 18];
            for (let i = 0; i < pts.length; i++) {
                const x = i * 14;
                const y = pts[i] + 10;
                i === 0 ? c.moveTo(x, y) : c.lineTo(x, y);
            }
            c.stroke();

            // Fill area under
            c.lineTo((pts.length - 1) * 14, 90);
            c.lineTo(0, 90);
            c.closePath();
            c.fillStyle = 'rgba(59, 130, 246, 0.05)';
            c.fill();
        }

        function drawBarChart(c) {
            const bars = [50, 70, 35, 85, 60, 45, 75, 55];
            const bw = 12, gap = 6;
            for (let i = 0; i < bars.length; i++) {
                const h = bars[i];
                const x = i * (bw + gap);
                c.fillStyle = 'rgba(59, 130, 246, 0.08)';
                c.fillRect(x, 90 - h, bw, h);

                c.strokeStyle = 'rgba(59, 130, 246, 0.3)';
                c.lineWidth = 0.8;
                c.strokeRect(x, 90 - h, bw, h);
            }
        }

        function drawGridPattern(c) {
            c.strokeStyle = 'rgba(59, 130, 246, 0.15)';
            c.lineWidth = 0.6;
            for (let i = 0; i <= 8; i++) {
                c.beginPath(); c.moveTo(0, i * 12); c.lineTo(140, i * 12); c.stroke();
                c.beginPath(); c.moveTo(i * 17.5, 0); c.lineTo(i * 17.5, 96); c.stroke();
            }

            c.strokeStyle = 'rgba(59, 130, 246, 0.4)';
            c.lineWidth = 1.2;
            c.setLineDash([4, 3]);
            c.beginPath();
            for (let i = 0; i < 10; i++) {
                const x = i * 15;
                const y = 50 + Math.sin(i * 0.8 + 1) * 25;
                i === 0 ? c.moveTo(x, y) : c.lineTo(x, y);
            }
            c.stroke();
            c.setLineDash([]);
        }

        function drawPieChart(c) {
            const slices = [0.35, 0.25, 0.22, 0.18];
            const alphas = [0.15, 0.1, 0.05, 0.02];
            let angle = -Math.PI / 2;
            const r = 38;

            for (let i = 0; i < slices.length; i++) {
                const sliceAngle = slices[i] * Math.PI * 2;
                c.beginPath();
                c.moveTo(0, 0);
                c.arc(0, 0, r, angle, angle + sliceAngle);
                c.closePath();
                c.fillStyle = `rgba(59, 130, 246, ${alphas[i]})`;
                c.fill();
                c.strokeStyle = 'rgba(59, 130, 246, 0.3)';
                c.lineWidth = 1;
                c.stroke();
                angle += sliceAngle;
            }
        }

        function drawTrendArrow(c) {
            c.strokeStyle = 'rgba(59, 130, 246, 0.3)';
            c.lineWidth = 1.5;
            c.beginPath();
            c.moveTo(0, 80);
            c.quadraticCurveTo(60, 50, 120, 15);
            c.stroke();

            c.fillStyle = 'rgba(59, 130, 246, 0.4)';
            c.beginPath();
            c.moveTo(120, 15);
            c.lineTo(112, 22);
            c.lineTo(115, 28);
            c.closePath();
            c.fill();
        }

        function drawAreaChart(c) {
            c.fillStyle = 'rgba(59, 130, 246, 0.05)';
            c.strokeStyle = 'rgba(59, 130, 246, 0.3)';
            c.lineWidth = 1.2;

            const pts = [70, 55, 65, 40, 50, 30, 45, 25, 35, 42, 28, 38];
            c.beginPath();
            c.moveTo(0, 90);
            for (let i = 0; i < pts.length; i++) {
                c.lineTo(i * 13, pts[i]);
            }
            c.lineTo((pts.length - 1) * 13, 90);
            c.closePath();
            c.fill();
            
            c.beginPath();
            for (let i = 0; i < pts.length; i++) {
                i === 0 ? c.moveTo(i * 13, pts[i]) : c.lineTo(i * 13, pts[i]);
            }
            c.stroke();
        }

        // ── Render loop: spotlight reveal ──
        function draw() {
            // Smooth cursor follow
            smoothX += (mouseX - smoothX) * 0.12;
            smoothY += (mouseY - smoothY) * 0.12;

            ctx.clearRect(0, 0, W, H);

            // Only draw a circular revealed region around the cursor
            if (smoothX > -500 && smoothY > -500) {
                ctx.save();

                // Create circular clipping with soft edge via radial gradient mask
                const r = SPOT.radius;

                // Draw the offscreen patterns masked by a radial gradient
                // We use globalCompositeOperation for soft-edge reveal
                ctx.globalAlpha = SPOT.patternAlpha;
                ctx.drawImage(offscreen, 0, 0, offscreen.width, offscreen.height, 0, 0, W, H);
                ctx.globalAlpha = 1;

                // Now erase everything OUTSIDE the spotlight
                ctx.globalCompositeOperation = 'destination-in';
                const grad = ctx.createRadialGradient(
                    smoothX, smoothY, r - SPOT.softEdge,
                    smoothX, smoothY, r
                );
                grad.addColorStop(0, 'rgba(255,255,255,1)');
                grad.addColorStop(1, 'rgba(255,255,255,0)');
                ctx.fillStyle = grad;
                ctx.fillRect(0, 0, W, H);

                // Erase the hero heading so graphics don't show behind "Invest Smarter. Grow Faster."
                const heroTitle = document.querySelector('.hero-title');
                if (heroTitle) {
                    const rect = heroTitle.getBoundingClientRect();
                    ctx.globalCompositeOperation = 'destination-out';
                    
                    const cx = rect.left + rect.width / 2;
                    const cy = rect.top + rect.height / 2;
                    
                    // Create an erasing gradient around the text
                    const textGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, rect.width * 0.55);
                    textGrad.addColorStop(0, 'rgba(0,0,0,1)');
                    textGrad.addColorStop(0.7, 'rgba(0,0,0,0.8)');
                    textGrad.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle = textGrad;
                    ctx.fillRect(cx - rect.width, cy - rect.height, rect.width * 2, rect.height * 2);
                }

                // Decrease opacity behind the hero description
                const heroDesc = document.querySelector('.hero-desc');
                if (heroDesc) {
                    const rect = heroDesc.getBoundingClientRect();
                    
                    const cx = rect.left + rect.width / 2;
                    const cy = rect.top + rect.height / 2;
                    
                    // Create a semi-transparent erasing gradient around the text
                    const descGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, rect.width * 0.6);
                    descGrad.addColorStop(0, 'rgba(0,0,0,0.85)');
                    descGrad.addColorStop(0.5, 'rgba(0,0,0,0.6)');
                    descGrad.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle = descGrad;
                    ctx.fillRect(cx - rect.width, cy - rect.height, rect.width * 2, rect.height * 2);
                }

                ctx.globalCompositeOperation = 'source-over';
                ctx.restore();
            }

            requestAnimationFrame(draw);
        }

        resize();
        window.addEventListener('resize', resize);
        draw();
    }

    /* ═══════════════════════════════════════════════════
       SCROLL ANIMATIONS
       ═══════════════════════════════════════════════════ */
    function initScrollAnimations() {
        if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
            gsap.registerPlugin(ScrollTrigger);
            gsap.to('.hero-content', {
                scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: 1 },
                y: -80, opacity: 0, scale: 0.96,
            });
            gsap.utils.toArray('.float-shape').forEach((s, i) => {
                gsap.to(s, {
                    scrollTrigger: { trigger: '.cta-section', start: 'top bottom', end: 'bottom top', scrub: 1 },
                    y: (i + 1) * -50, rotation: (i + 1) * 20,
                });
            });
        }

        const style = document.createElement('style');
        style.textContent = `
            .reveal { opacity: 0; transform: translateY(40px); transition: opacity 0.7s ease, transform 0.7s ease; }
            .reveal.visible { opacity: 1; transform: translateY(0); }
            .reveal-delay-1 { transition-delay: 0.07s; }
            .reveal-delay-2 { transition-delay: 0.14s; }
            .reveal-delay-3 { transition-delay: 0.21s; }
            .reveal-delay-4 { transition-delay: 0.28s; }
            .reveal-delay-5 { transition-delay: 0.35s; }
        `;
        document.head.appendChild(style);

        document.querySelectorAll('.feature-card, .feature-item, .step-card, .stat-item, .reveal-section, .market-card').forEach((el) => {
            el.classList.add('reveal');
            const siblings = el.parentElement ? Array.from(el.parentElement.children).filter(c => c.classList.contains('reveal')) : [];
            const idx = siblings.indexOf(el);
            if (idx > 0 && idx <= 5) el.classList.add('reveal-delay-' + idx);
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } });
        }, { threshold: 0.08, rootMargin: '0px 0px -30px 0px' });
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    const target = parseInt(el.dataset.value) || 0;
                    const suffix = el.dataset.suffix || '';
                    let current = 0;
                    const step = target / 60;
                    const timer = setInterval(() => { current += step; if (current >= target) { current = target; clearInterval(timer); } el.textContent = Math.floor(current).toLocaleString() + suffix; }, 25);
                    counterObserver.unobserve(el);
                }
            });
        }, { threshold: 0.3 });
        document.querySelectorAll('.stat-value[data-value]').forEach(el => counterObserver.observe(el));
    }

    /* ═══════════════════════════════════════════════════
       MINI CHART
       ═══════════════════════════════════════════════════ */
    function initMiniChart() {
        const canvases = document.querySelectorAll('.mini-chart');
        if (canvases.length === 0) return;
        const charts = Array.from(canvases).map((c, index) => {
            const ctx = c.getContext('2d');
            const changeEl = c.parentElement.parentElement.querySelector('.market-change');
            const isUp = changeEl ? changeEl.classList.contains('up') : true;
            const color = isUp ? '#00f0ff' : '#ff2d78';
            const rgbaColor = isUp ? 'rgba(0,240,255,' : 'rgba(255,45,120,';
            const resize = () => { c.width = c.parentElement.clientWidth; c.height = c.parentElement.clientHeight; };
            resize(); window.addEventListener('resize', resize);
            const pts = []; let v = 50 + (index * 10);
            for (let i = 0; i < 40; i++) { v += (Math.random() - (isUp ? 0.45 : 0.55)) * 6; v = Math.max(10, Math.min(90, v)); pts.push(v); }
            return { c, ctx, pts, off: Math.random() * 10, color, rgbaColor, speed: 0.05 + Math.random() * 0.03 };
        });
        (function draw() {
            charts.forEach(chart => {
                const { c, ctx, pts, color, rgbaColor } = chart;
                const w = c.width, h = c.height;
                ctx.clearRect(0, 0, w, h);
                const g = ctx.createLinearGradient(0, 0, 0, h);
                g.addColorStop(0, rgbaColor + '0.15)'); g.addColorStop(1, rgbaColor + '0)');
                ctx.beginPath(); ctx.moveTo(0, h);
                for (let i = 0; i < pts.length; i++) { const x = (i / (pts.length - 1)) * w; const y = h - (pts[(i + Math.floor(chart.off)) % pts.length] / 100) * h; ctx.lineTo(x, y); }
                ctx.lineTo(w, h); ctx.closePath(); ctx.fillStyle = g; ctx.fill();
                ctx.beginPath();
                for (let i = 0; i < pts.length; i++) { const x = (i / (pts.length - 1)) * w; const y = h - (pts[(i + Math.floor(chart.off)) % pts.length] / 100) * h; i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y); }
                ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.shadowColor = rgbaColor + '0.5)'; ctx.shadowBlur = 8; ctx.stroke(); ctx.shadowBlur = 0;
                chart.off += chart.speed;
            });
            requestAnimationFrame(draw);
        })();
    }

    /* ═══════════════════════════════════════════════════
       BOOT
       ═══════════════════════════════════════════════════ */
    function boot() {
        initFinanceBackground();
        initScrollAnimations();
        initMiniChart();
    }

    window.initAnimations = boot;
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', boot);
    } else {
        boot();
    }
})();
