#!/usr/bin/env python3
"""
cliCHair | About us page generator (v2, 2026-10-14)

One markup, four languages (EN primary, IT, DE, FR).
Outputs:
  dist/about-us.<lang>.html   -> page body_html for Shopify (EN) and translations (IT/DE/FR)
  preview/about-us.<lang>.html -> local preview wrapped in a theme-like shell (for screenshots)

Rules honoured:
  - no em-dashes anywhere, DE with "Sie" and Swiss "ss", FR with non-breaking space before : ; ! ?
  - links prefixed with /it /de /fr; EN unprefixed
  - no forbidden claims (cruelty-free, exclusive, guaranteed, certified...)
  - brand spellings: cliCHair, clichAIr (never uppercased by CSS)
"""
import os, re, html, sys

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# CSS (kept inside the page body; Shopify keeps <style> when saved via API)
# ---------------------------------------------------------------------------
CSS = r"""
.cca{--ink:#111;--ink2:#3d3d3d;--mute:#7d7d7d;--line:#e8e8e6;--panel:#f5f5f2;--dark:#121212;--red:#a02222;--r:24px;--cca-g:max(16px,calc((100vw - 24px - 1360px) / 2));
font-family:inherit;color:var(--ink);line-height:1.6;box-sizing:border-box;width:calc(100vw - 24px);max-width:none;margin:0 0 0 calc(50% - 50vw + 12px);padding:0 var(--cca-g) 64px;-webkit-font-smoothing:antialiased;text-align:left}
@media (min-width:750px){.cca{--cca-g:max(40px,calc((100vw - 24px - 1360px) / 2))}}
.cca-panel-intro{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 48px;margin:0 0 8px}
.cca-panel-intro .cca-p{max-width:none}
.cca-p.cca-wide{max-width:80ch}
.cca-2col .cca-roles{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:0}
.cca a{text-decoration:none}
.cca-mt26{margin-top:26px}.cca-mb26{margin-bottom:26px}.cca-mb28{margin-bottom:28px}
.cca *{box-sizing:border-box}
.cca :where(h2,h3,h4,p,ul,li){margin:0;padding:0}
.cca :where(ul){list-style:none}
.cca :where(a){color:inherit;text-decoration:none}
.cca a:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:6px}
.cca svg{display:block}

/* sections */
.cca-s{padding:72px 0;border-top:1px solid var(--line)}
.cca-s.cca-s0{border-top:0;padding-top:28px}
.cca-s.cca-s-last{padding-bottom:16px}
.cca-eye{display:flex;align-items:center;gap:10px;font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 22px}
.cca-eye::before{content:'';flex:none;width:7px;height:7px;border-radius:50%;background:var(--red)}
.cca-eye b{font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.cca-t{font-size:clamp(1.8rem,3.4vw,2.6rem);font-weight:800;letter-spacing:-.025em;line-height:1.08;text-wrap:balance;max-width:26ch;margin:0 0 22px;text-transform:none;color:var(--ink)}
.cca-t .cca-brand{text-transform:none}
.cca-lead{font-size:clamp(1.05rem,1.5vw,1.22rem);line-height:1.55;color:var(--ink2);max-width:60ch;margin:0 0 18px}
.cca-p{font-size:16.5px;line-height:1.65;color:var(--ink2);max-width:62ch;margin:0 0 18px}
.cca-p:last-child{margin-bottom:0}
.cca-2col{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:40px 64px;align-items:start}
.cca-2col .cca-t{margin-bottom:0}
.cca-sticky{position:sticky;top:96px}

/* buttons and links */
.cca-btns{display:flex;flex-wrap:wrap;align-items:center;gap:12px 14px;margin:0}
.cca-btn{display:inline-flex;align-items:center;gap:10px;height:50px;padding:0 24px;border-radius:999px;font-size:14px;font-weight:700;letter-spacing:.01em;border:1px solid var(--ink);color:var(--ink);background:#fff;transition:background .18s ease,color .18s ease,transform .18s ease}
.cca-btn:hover{background:var(--panel);transform:translateY(-1px)}
.cca-btn-dark{background:var(--ink);color:#fff}
.cca-btn-dark:hover{background:#000;color:#fff}
.cca-btn-light{background:#fff;color:var(--ink);border-color:#fff}
.cca-btn-light:hover{background:#e9e9e6}
.cca-btn-ghost{background:transparent;color:#fff;border-color:rgba(255,255,255,.45)}
.cca-btn-ghost:hover{background:rgba(255,255,255,.1);border-color:#fff}
.cca-link{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:700;color:var(--ink);padding:4px 0;border-bottom:1.5px solid var(--ink);transition:gap .18s ease,border-color .18s ease}
.cca-link:hover{gap:12px;border-color:var(--red)}
.cca-link svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.cca-link.cca-link-w{color:#fff;border-color:#fff}
.cca-link.cca-link-w:hover{border-color:#bbb}

/* hero */
.cca-hero{padding:28px 0 56px}
.cca-kicker{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 26px}
.cca-h1{font-size:clamp(3rem,8.2vw,6.4rem);font-weight:800;letter-spacing:-.04em;line-height:1;margin:0 0 34px;text-transform:none;color:var(--ink)}
.cca-h1 span{display:block}
.cca-h1 .cca-outl{color:transparent;-webkit-text-stroke:2.5px var(--ink);text-stroke:2.5px var(--ink)}
.cca-hero .cca-lead{font-size:clamp(1.1rem,1.8vw,1.35rem);max-width:52ch;margin-bottom:32px}
.cca-facts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:18px;overflow:hidden;margin:52px 0 0}
.cca-facts li{background:#fff;padding:18px 20px 20px}
.cca-facts b{display:block;font-size:1.2rem;font-weight:800;letter-spacing:-.02em;line-height:1.2;margin:0 0 4px;font-variant-numeric:tabular-nums}
.cca-facts span{display:block;font-size:13px;color:var(--mute);line-height:1.4}

/* pillars */
.cca-pillars{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:36px 0 0}
.cca-pillar{border:1px solid var(--line);border-radius:var(--r);padding:30px 28px 30px;background:#fff;display:flex;flex-direction:column;gap:14px;transition:transform .2s ease,box-shadow .2s ease}
.cca-pillar:hover{transform:translateY(-2px);box-shadow:0 14px 34px -22px rgba(0,0,0,.35)}
.cca-pillar h3{font-size:1.75rem;font-weight:800;letter-spacing:-.03em;line-height:1;text-transform:none;color:var(--ink)}
.cca-pillar .cca-sub{font-size:15.5px;font-weight:600;color:var(--ink);line-height:1.45}
.cca-pillar ul{display:flex;flex-direction:column;gap:10px;margin:4px 0 6px}
.cca-pillar li{position:relative;padding-left:24px;font-size:14.5px;line-height:1.55;color:var(--ink2)}
.cca-pillar li::before{content:'';position:absolute;left:0;top:9px;width:12px;height:7px;border-left:2px solid var(--ink);border-bottom:2px solid var(--ink);transform:rotate(-45deg)}
.cca-pillar .cca-link{margin-top:auto;align-self:flex-start}
.cca-pillar-dark{background:var(--dark);color:#fff;border-color:var(--dark)}
.cca-pillar-dark h3,.cca-pillar-dark .cca-sub{color:#fff}
.cca-pillar-dark li{color:#c9c9c9}
.cca-pillar-dark li::before{border-color:#fff}
.cca-pillar-dark .cca-link{color:#fff;border-color:#fff}
.cca-pillar-dark .cca-link:hover{border-color:#9a9a9a}
.cca-pillar-i{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;background:var(--panel)}
.cca-pillar-dark .cca-pillar-i{background:rgba(255,255,255,.1)}
.cca-pillar-i svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}

/* method */
.cca-steps{position:relative;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin:40px 0 0;align-items:start}
.cca-steps::before{content:'';position:absolute;left:28px;right:28px;top:27px;height:1px;background:var(--line)}
.cca-step{position:relative;background:#fff;border:1px solid var(--line);border-radius:20px;padding:0 24px 26px}
.cca-step-n{position:relative;display:grid;place-items:center;width:54px;height:54px;border-radius:50%;background:#fff;border:1px solid var(--ink);font-weight:800;font-size:15px;letter-spacing:-.02em;margin:0 0 18px;transform:translateY(-1px);font-variant-numeric:tabular-nums}
.cca-step h3{font-size:1.05rem;font-weight:700;line-height:1.3;margin:0 0 10px;text-transform:none;color:var(--ink)}
.cca-step p{font-size:14.5px;line-height:1.55;color:var(--ink2)}
.cca-step-dark{background:var(--dark);border-color:var(--dark);color:#fff}
.cca-step-dark h3{color:#fff}
.cca-step-dark .cca-step-n{background:#fff;color:var(--ink);border-color:#fff}
.cca-step-dark p{color:#c9c9c9}
.cca-step-loop{display:inline-flex;align-items:center;gap:8px;margin-top:16px;font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#9a9a9a}
.cca-step-loop svg{width:14px;height:14px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.cca-quote{font-size:clamp(1.3rem,2.6vw,1.85rem);font-weight:700;letter-spacing:-.015em;line-height:1.3;max-width:34ch;margin:48px 0 28px}
.cca-quote span{color:var(--mute);font-weight:600}

/* timeline */
.cca-tl{position:relative;margin:30px 0 0;padding-left:28px}
.cca-tl::before{content:'';position:absolute;left:7px;top:10px;bottom:10px;width:1px;background:var(--line)}
.cca-tl li{position:relative;padding:0 0 30px}
.cca-tl li:last-child{padding-bottom:0}
.cca-tl li::before{content:'';position:absolute;left:-28px;top:9px;width:15px;height:15px;border-radius:50%;background:#fff;border:1.5px solid var(--ink)}
.cca-tl li:last-child::before{background:var(--ink)}
.cca-tl-k{display:block;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin:0 0 6px;font-variant-numeric:tabular-nums}
.cca-tl h3{font-size:1.15rem;font-weight:700;letter-spacing:-.01em;margin:0 0 8px;text-transform:none;color:var(--ink)}
.cca-tl p{font-size:15.5px;line-height:1.6;color:var(--ink2);max-width:56ch}

/* dark panel */
.cca-panel{background:var(--dark);color:#fff;border-radius:var(--r);padding:56px 48px 48px}
.cca-panel .cca-eye{color:#9a9a9a}
.cca-panel .cca-eye b{color:#fff}
.cca-panel .cca-t{color:#fff}
.cca-panel .cca-p{color:#d4d4d4}
.cca-hub{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1.3fr) auto minmax(0,1fr);align-items:center;gap:14px;margin:36px 0 44px}
.cca-hub-box{border:1px solid rgba(255,255,255,.22);border-radius:16px;padding:18px 18px 20px;min-height:118px}
.cca-hub-box h4{font-size:11.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#9a9a9a;margin:0 0 8px}
.cca-hub-box p{font-size:14px;line-height:1.5;color:#e2e2e2}
.cca-hub-core{background:#fff;color:var(--ink);border-color:#fff;text-align:center}
.cca-hub-core h4{color:var(--mute)}
.cca-hub-core .cca-hub-name{color:var(--ink)}
.cca-hub-core .cca-hub-name{font-size:1.5rem;font-weight:800;letter-spacing:-.03em;line-height:1;margin:0 0 10px;text-transform:none}
.cca-hub-core p{color:var(--ink2);font-size:13.5px}
.cca-hub-arrow{width:44px;height:1px;background:rgba(255,255,255,.4);position:relative}
.cca-hub-arrow::after,.cca-hub-arrow::before{content:'';position:absolute;top:-4px;width:8px;height:8px;border-top:1px solid rgba(255,255,255,.7);border-right:1px solid rgba(255,255,255,.7)}
.cca-hub-arrow::after{right:0;transform:rotate(45deg)}
.cca-hub-arrow::before{left:0;transform:rotate(-135deg)}
.cca-aud{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.14);border-radius:18px;overflow:hidden}
.cca-aud li{background:var(--dark);padding:26px 24px 26px;display:flex;flex-direction:column;gap:10px;transition:background .18s ease}
.cca-aud li:hover{background:#1c1c1c}
.cca-aud h3{font-size:1.02rem;font-weight:700;letter-spacing:-.005em;text-transform:none;color:#fff}
.cca-aud p{font-size:14px;line-height:1.55;color:#bdbdbd;flex:1}
.cca-aud .cca-link{align-self:flex-start;font-size:13px}

/* brands strip */
.cca-brands{display:flex;flex-wrap:wrap;align-items:center;gap:10px 12px;margin:28px 0 30px;padding:20px 0 0;border-top:1px solid var(--line)}
.cca-brands span{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mute);margin-right:6px}
.cca-chip{display:inline-flex;align-items:center;height:38px;padding:0 16px;border-radius:999px;border:1px solid var(--line);font-size:13.5px;font-weight:700;background:#fff;transition:border-color .18s ease,background .18s ease}
.cca-chip:hover{border-color:var(--ink)}
.cca-chip-more{background:var(--panel);border-color:var(--panel)}

/* engine */
.cca-eng{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px;margin:34px 0 0}
.cca-eng-col{border:1px solid var(--line);border-radius:20px;padding:26px 26px 28px;background:#fff}
.cca-eng-col h3{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--mute);margin:0 0 16px;line-height:1.4}
.cca-eng-col li{position:relative;padding:12px 0 12px 30px;border-top:1px solid var(--line);font-size:15px;line-height:1.5;color:var(--ink2)}
.cca-eng-col li:last-child{padding-bottom:0}
.cca-eng-col li::before{content:'';position:absolute;left:2px;top:19px;width:12px;height:12px;border-radius:50%;border:1.5px solid var(--ink)}
.cca-valid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:24px 48px;align-items:start;margin:18px 0 0;background:var(--panel);border-radius:20px;padding:32px 30px 34px}
.cca-valid h3{font-size:1.4rem;font-weight:800;letter-spacing:-.02em;line-height:1.15;text-transform:none;color:var(--ink)}
.cca-valid p{font-size:15.5px;line-height:1.6;color:var(--ink2)}
.cca-valid p+p{margin-top:12px}
.cca-badge-note{display:flex;align-items:center;gap:14px;margin:26px 0 0;font-size:14px;color:var(--ink2)}
.cca-badge{flex:none;display:inline-grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--ink);color:#fff;font-weight:800;font-size:12px;letter-spacing:-.02em}

/* tools */
.cca-tools{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:34px 0 0}
.cca-tool{border:1px solid var(--line);border-radius:20px;padding:22px 20px 22px;background:#fff;display:flex;flex-direction:column;gap:12px;transition:transform .2s ease,box-shadow .2s ease}
.cca-tool:hover{transform:translateY(-2px);box-shadow:0 14px 34px -22px rgba(0,0,0,.35)}
.cca-tool-top{display:flex;align-items:center;justify-content:space-between;gap:8px}
.cca-tool-i{width:40px;height:40px;border-radius:12px;background:var(--panel);display:grid;place-items:center}
.cca-tool-i svg{width:20px;height:20px;stroke:var(--ink);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.cca-tag{font-size:10.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;padding:5px 9px;border-radius:999px;border:1px solid var(--line);color:var(--mute)}
.cca-tag-pro{background:var(--ink);border-color:var(--ink);color:#fff}
.cca-tool h3{font-size:1rem;font-weight:700;line-height:1.3;text-transform:none;color:var(--ink)}
.cca-tool p{font-size:13.8px;line-height:1.55;color:var(--ink2);flex:1}
.cca-tool .cca-link{font-size:13px;align-self:flex-start}

/* eco */
.cca-eco{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:30px 0 24px}
.cca-eco li{border:1px solid var(--line);border-radius:20px;padding:24px 22px 24px;background:#fff}
.cca-eco-i{width:40px;height:40px;border-radius:12px;background:var(--panel);display:grid;place-items:center;margin:0 0 14px}
.cca-eco-i svg{width:20px;height:20px;stroke:var(--ink);fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.cca-eco h3{font-size:1rem;font-weight:700;margin:0 0 8px;text-transform:none;color:var(--ink)}
.cca-eco p{font-size:14.5px;line-height:1.55;color:var(--ink2)}

/* team */
.cca-roles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:30px 0 26px}
.cca-roles li{border-top:2px solid var(--ink);padding:14px 0 0}
.cca-roles b{display:block;font-size:14.5px;font-weight:700;margin:0 0 6px;line-height:1.3}
.cca-roles span{display:block;font-size:13.5px;line-height:1.5;color:var(--mute)}

/* final panel */
.cca-final{background:var(--dark);color:#fff;border-radius:var(--r);padding:52px 48px;display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:28px 48px;align-items:center}
.cca-final .cca-t{color:#fff;margin:0 0 12px}
.cca-final .cca-p{color:#d4d4d4;margin:0}
.cca-final .cca-btns{justify-content:flex-start}
.cca-final-links{margin-top:18px;font-size:14px;color:#bdbdbd}
.cca-final-links a{color:#fff;border-bottom:1px solid rgba(255,255,255,.5)}
.cca-final-links a:hover{border-color:#fff}

/* responsive */
@media (max-width:1000px){
.cca-pillars{grid-template-columns:1fr}
.cca-steps{grid-template-columns:repeat(2,minmax(0,1fr))}
.cca-steps::before{display:none}
.cca-tools{grid-template-columns:repeat(2,minmax(0,1fr))}
.cca-roles{grid-template-columns:repeat(2,minmax(0,1fr))}
.cca-hub{grid-template-columns:1fr;gap:10px}
.cca-hub-arrow{width:1px;height:28px;margin:0 auto}
.cca-hub-arrow::before{left:-4px;top:0;transform:rotate(-45deg)}
.cca-hub-arrow::after{left:-4px;top:auto;bottom:0;transform:rotate(135deg)}
.cca-aud{grid-template-columns:repeat(2,minmax(0,1fr))}
.cca-2col{grid-template-columns:1fr;gap:18px}
.cca-panel-intro{grid-template-columns:1fr}
.cca-sticky{position:static}
.cca-final{grid-template-columns:1fr}
}
@media (max-width:640px){
.cca{padding-bottom:40px}
.cca-s{padding:52px 0}
.cca-hero{padding:16px 0 44px}
.cca-h1{font-size:clamp(2.7rem,15vw,3.6rem)}
.cca-facts{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:40px}
.cca-facts li{padding:14px 14px 16px}
.cca-facts b{font-size:1.05rem}
.cca-steps{grid-template-columns:1fr}
.cca-step{padding:0 20px 22px}
.cca-panel{padding:36px 20px 28px;border-radius:20px}
.cca-aud{grid-template-columns:1fr}
.cca-eng{grid-template-columns:1fr}
.cca-valid{grid-template-columns:1fr;padding:26px 22px 28px}
.cca-tools{grid-template-columns:1fr}
.cca-eco{grid-template-columns:1fr}
.cca-roles{grid-template-columns:1fr}
.cca-final{padding:36px 22px;border-radius:20px}
.cca-btn{height:46px;padding:0 20px;font-size:13.5px}
.cca-pillar{padding:24px 22px 24px}
}
@media (prefers-reduced-motion:reduce){.cca *{transition:none!important}}
"""

# ---------------------------------------------------------------------------
# Inline SVG icons (stroke based, inherit colour)
# ---------------------------------------------------------------------------
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
LOOP = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 0 1 15.5-6.3L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.3L3 16M3 21v-5h5"/></svg>'
ICONS = {
    'brain': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-2 3 3 3 0 0 0 2 3v1a3 3 0 0 0 3 3h1V4ZM15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 2 3 3 3 0 0 1-2 3v1a3 3 0 0 1-3 3h-1V4ZM10 9h4M10 15h4"/></svg>',
    'spark': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/><circle cx="12" cy="12" r="3"/></svg>',
    'scale': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v18M4 21h16M12 6l7 2M12 6 5 8M5 8l-3 7a3.5 3.5 0 0 0 6 0l-3-7ZM19 8l-3 7a3.5 3.5 0 0 0 6 0l-3-7Z"/></svg>',
    'list': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="4" cy="6" r="1"/><circle cx="4" cy="12" r="1"/><circle cx="4" cy="18" r="1"/></svg>',
    'drop': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11Z"/><path d="M9 14a3 3 0 0 0 3 3"/></svg>',
    'chart': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/></svg>',
    'clock': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    'user': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></svg>',
    'card': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/></svg>',
    'repeat': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17 2l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><path d="M7 22l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>',
    'tag': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12l-8 8-9-9V3h8l9 9Z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
    'leaf': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19c0-8 4-13 14-14 0 10-4 14-12 14"/><path d="M5 19c3-4 6-7 10-9"/></svg>',
    'box': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7l9-4 9 4v10l-9 4-9-4V7Z"/><path d="M3 7l9 4 9-4M12 11v10"/></svg>',
    'check': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>',
}

# ---------------------------------------------------------------------------
# Copy. EN is the master; IT/DE/FR are adaptations.
# ---------------------------------------------------------------------------
T = {}

T['en'] = dict(
    lang='en', prefix='',
    kicker='The cliCHair platform',
    h1=('Intelligent.', 'Innovative.', 'Impartial.'),
    hero_lead='cliCHair is the Swiss platform for professional haircare. One engine that knows every formula, rules that are the same for everyone, and answers verified by experts before they reach you.',
    btn_pro='PRO account', btn_shop='Shop', hero_link='What clichAIr does',
    facts=[('Switzerland and Liechtenstein', 'Delivery area'),
           ('Official importer', 'Of the brands we carry'),
           ('24/7', 'clichAIr answers in writing'),
           ('12:00', 'Orders placed by noon ship the same day, Mon to Fri'),
           ('CHF 99', 'Free DHL Express shipping from'),
           ('4 languages', 'EN, IT, DE, FR')],

    s1_eye='Three words', s1_t='Three words, and what they mean in practice',
    s1_lead='We do not ask you to take them on trust. Each one is backed by something you can check on this site today.',
    p1_h='Intelligent', p1_sub='An engine that calculates, not a chat that reassures.',
    p1=['clichAIr reads every INCI list and works out dosages, cost per service and the right routine.',
        'It answers 24 hours a day, on the site and on WhatsApp.',
        'It learns only from corrections verified by our experts, never from the web.'],
    p1_link='How clichAIr works',
    p2_h='Innovative', p2_sub='The Pure Digital model: repetition automated, expertise kept.',
    p2=['Orders, reorders, invoices, tracking and returns live in your account, with no office hours.',
        'Tools built for the salon: quick order, colour calculator, profitability on every product page.',
        'A version number at the bottom of every page, and a public list of what changes with each release.'],
    p2_link='See the updates',
    p3_h='Impartial', p3_sub='The same rules for everyone who uses the platform.',
    p3=['Prices are set by role and shown before you order: no sales reps, no price lists on request, no negotiation person by person.',
        'Advice follows the formula and the protocol, not the margin: fewer wrong purchases, less waste.',
        'Every brand is presented with the same data: INCI, protocol, cost per service. A correction enters the platform because it has been verified, whoever sends it.'],
    p3_link='Our pricing principle',

    s2_eye='The method', s2_t='Knowledge that grows with the people who work',
    steps=[('We know every formula', 'A few complete ranges, studied down to the last INCI, with the protocol and cost per service for every reference.'),
           ('<span class="cca-brand">clichAIr</span> works with you', 'It calculates dosages and costs, builds routines, handles orders and requests 24 hours a day, on the site and on WhatsApp.'),
           ('The salon reports reality', 'When a protocol behaves differently on real hair, the verified professional flags it.'),
           ('Experts validate, everyone benefits', 'Our team checks the correction, and from that moment clichAIr answers better for every salon and every client. When needed, the information also goes back to the manufacturer.')],
    loop='The cycle starts again',
    quote_a='A distributor sells you the product.', quote_b='cliCHair also gives you back what salons have learned using it.',
    s2_cta='Join the PRO community',

    s3_eye='The origin', s3_t='Distribution first. Then the platform.',
    s3_p='cliCHair started where two trades that rarely talk to each other met: a master colorist with years of technical work behind the chair, who knows the real limits of a product because she has used it on her clients’ hair, and a developer convinced that a salon’s decisions could be calculated rather than guessed.',
    tl=[('2018', 'ÜLTIMA hair concept', 'For years we worked as a professional distributor in the classic way: salon visits, samples, printed price lists. That period taught us the trade from the inside, and showed us precisely which parts of the job were real expertise and which were simply repetition.'),
        ('The platform', 'cliCHair', 'We automated the repetition and kept the expertise. The method did not come after the technology: the technology was built to run the method.'),
        ('The engine', 'clichAIr', 'The calculation engine the platform is named after, on every page of the site and on the messaging channels you already use.'),
        ('Today', 'A platform that evolves', 'Every release has a number and a date. What changed, and what it changes for you, is on the Updates page.')],
    s3_link='Read the updates',

    s4_eye='The platform', s4_t='Always open, between the brand and the people who use it',
    s4_p1='cliCHair is the Swiss platform dedicated to professional haircare. We are the official importer of the brands we carry, with fast delivery throughout Switzerland and Liechtenstein.',
    s4_p2='We work as a hub: the brand on one side, the people who use the product on the other, and in between a platform that never closes. No appointment to arrange, no round of phone calls, no waiting for a price list. You order when you need to, with prices already set for your profile and technical calculation available at any time.',
    s4_p3='Every type of access is verified and sees the catalogue that belongs to it. Private clients find the retail selection: the same products a hairdresser recommends and sells in the salon, with the same INCI lists and the same technical advice. Verified professionals also reach the full catalogue, with the technical lines, the colour ranges and the professional formats that stay out of sight for anyone outside the trade.',
    hub=[('The brands', 'Official importer. Technical data straight from the manufacturer.'),
         ('The platform', 'clichAIr, a catalogue for every role, logistics, pricing, always open.'),
         ('The people', 'Salons, private clients, schools, distributors, online shops.')],
    aud=[('Salons and hairdressers', 'The full technical catalogue, professional formats and reserved pricing, with tools that calculate every service.', 'I’m a hairdresser', '/pages/professionals'),
         ('Private clients', 'You are welcome here. With clichAIr as your expert advisor, you find the same products the best salons sell to their clients. Technical lines, intensive treatments and professional formats stay reserved for professionals.', 'I’m a private client', '/collections/all'),
         ('Schools and academies', 'Continuous supply for teaching labs and practical training.', 'Schools and academies', '/pages/professionals'),
         ('Professional distributors', 'Access to the ranges for those who supply salons through their own network.', 'Distributors', '/pages/professionals'),
         ('Online shops', 'Sell the retail selection on your own Shopify store without buying stock: we ship, you earn. Reserved for PRO members.', 'Retailer programme', '/pages/retailers'),
         ('Partners and creators', 'Schools, laboratories, media, creators: projects that share our idea of professional haircare.', 'Collaborate', '/pages/collaborations')],

    s5_eye='The principle', s5_t='Depth, not breadth',
    s5_p1='The difference is not how many products you find. It is how well we know them.',
    s5_p2='We work with a small number of complete professional ranges, technical and colour lines included, studied down to the last INCI. A generalist assortment offers you a few retail references. Here you find the whole range, with the application protocol for every single reference and the cost per service.',
    s5_p3='This is also why the technical lines stay reserved for professionals: it protects your expertise in the salon and keeps professional references out of online price wars.',
    brands_label='The brands on the platform', brands_all='All brands',
    s5_link='Register as a professional',

    s6_eye='The engine', s6_t='clichAIr', s6_lead='It is not a support chat. It is the calculation engine the platform is named after.',
    eng_a_h='If you run a salon',
    eng_a=['Dosages per application and cost per service', 'How many applications you get from one pack, and how profitable a kit is', 'Orders, reorders and requests, 24 hours a day'],
    eng_b_h='If you buy for yourself',
    eng_b=['It reads the INCI lists and checks that the products you combine are compatible', 'It builds the right routine for your hair, so you stop buying by trial and error', 'How long a product lasts and what it costs per use'],
    valid_h='AI does not decide on its own',
    valid_p1='Every formula goes through our team of experts, every protocol through technical verification in the field. Nothing enters the platform without that check.',
    valid_p2='The platform does not learn on its own and does not learn from the web: it grows only on what the team has verified. And when a question goes beyond its limits, clichAIr hands over to our team.',
    badge_note='Click the AIr badge, bottom left: it is on every page of the site. clichAIr also answers on WhatsApp and on the messaging channels you already use.',

    s7_eye='The tools', s7_t='Built into the platform, no extra app',
    s7_lead='Some are reserved for verified professionals, the others are open to everyone.',
    tag_pro='PRO', tag_all='Everyone',
    tools=[('list', 'Quick order', 'The whole catalogue in one list, by brand and line, with the estimated profit next to each product.', True, None, None),
           ('drop', 'Colour calculator', 'The cost of every colour service and the stock you need for the month.', True, None, None),
           ('chart', 'Profitability panel', 'On every product page: cost per service, break-even and profit for the salon.', True, None, None),
           ('clock', 'Cost per use', 'On the same pages, for private clients: how long the product lasts and what it costs per use.', False, None, None),
           ('user', 'Your account', 'Orders, reorders, invoices, tracking and purchase history. Returns requested in self-service within 14 days.', False, None, None),
           ('card', 'Payments', 'Twint, PayPal, cards and Klarna, with the option to pay in 30 days.', False, None, None),
           ('repeat', 'Subscriptions', 'Eligible products every 4, 6 or 8 weeks, with a discount on every delivery. Pause or cancel at any time.', False, None, None),
           ('tag', 'Updates', 'A version number at the bottom of every page. Every release is listed with its date and what it changes.', False, 'See the updates', '/pages/updates')],

    s8_eye='The value', s8_t='The value stays where the work is',
    s8_p1='Platform automation lowers our structural costs, and we do not keep those savings: they become the price you see. No inflated price list with apparent discounts layered on top.',
    s8_p2='Each channel has its own terms, calculated on the role of the buyer and on the real value of the product. Two salons with the same profile see the same price: it does not depend on who calls more often or negotiates harder.',
    s8_p3='And no strings attached: no contracts, no punitive minimum orders. If you already have a supplier you trust, keep them. cliCHair also works well as a complementary channel, for urgent needs and for testing new lines.',
    s8_cta='Request your terms',

    s9_eye='Education', s9_t='A product performs as well as the hand that applies it',
    s9_p1='A technical product on its own is not enough. That is why we run in-person professional courses alongside the platform, built together with the manufacturers.',
    s9_p2='We hold courses and events regularly, and we open dedicated sessions when a group of salons shares the same technical interest. Write to us with the subject that interests you and we will let you know as soon as dates open.',
    s9_link='Write to us about training',

    s10_eye='Ethics', s10_t='The cliCHair ECO protocol',
    eco=[('box', 'Offset shipping', 'The emissions of every shipment are offset through DHL GoGreen and Shopify Planet, at no extra cost to you.'),
         ('leaf', 'Essential packaging', 'Paper and cardboard, recyclable materials, plastic reduced to the essentials.'),
         ('check', 'Fewer wrong purchases', 'clichAIr reads the full INCI list before you buy: less product wasted, less to throw away.')],
    s10_p='Digital efficiency is not only an economic advantage. It also means less waste.',
    s10_link='Sustainability',

    s11_eye='The team', s11_t='People behind the engine',
    roles=[('Strategic direction', 'Builds the partnerships with the brands.'),
           ('Operations', 'Logistics and daily support.'),
           ('Science and trichology', 'Formulas and protocols under review.'),
           ('Master colorist', 'Verifies every protocol in the field.')],
    s11_p1='clichAIr answers first, in writing, at any hour. Our team steps in on business days, in writing, when a question needs a human decision: the person who answers you is the one who actually does that work.',
    s11_p2='Write to us with any request, technical or commercial.',
    s11_cta='Contact us',

    s12_t='Choose your access',
    s12_p='Private clients browse and order without registering. Professionals register once: free, verified in 24 hours, no commitment.',
    s12_links_a='Not convinced yet?', s12_links_b='Read the Professionals page', s12_links_c='or', s12_links_d='what changes with every version',
)

T['it'] = dict(
    lang='it', prefix='/it',
    kicker='La piattaforma cliCHair',
    h1=('Intelligente.', 'Innovativa.', 'Imparziale.'),
    hero_lead='cliCHair è la piattaforma svizzera dell’haircare professionale. Un motore che conosce ogni formula, regole uguali per tutti e risposte verificate da esperti prima di arrivare a te.',
    btn_pro='Account PRO', btn_shop='Shop', hero_link='Cosa fa clichAIr',
    facts=[('Svizzera e Liechtenstein', 'Area di consegna'),
           ('Importatori ufficiali', 'Dei marchi che proponiamo'),
           ('24/7', 'clichAIr risponde per iscritto'),
           ('12:00', 'Ordini entro mezzogiorno spediti in giornata, lun-ven'),
           ('CHF 99', 'Spedizione DHL Express gratuita da'),
           ('4 lingue', 'IT, DE, FR, EN')],

    s1_eye='Tre parole', s1_t='Tre parole, e cosa vogliono dire in pratica',
    s1_lead='Non ti chiediamo di crederci sulla parola. Dietro ognuna c’è qualcosa che puoi verificare su questo sito oggi stesso.',
    p1_h='Intelligente', p1_sub='Un motore che calcola, non una chat che rassicura.',
    p1=['clichAIr legge ogni INCI e calcola dosaggi, costo per servizio e la routine giusta.',
        'Risponde 24 ore su 24, sul sito e su WhatsApp.',
        'Impara solo dalle correzioni verificate dai nostri esperti, mai dal web.'],
    p1_link='Come lavora clichAIr',
    p2_h='Innovativa', p2_sub='Il modello Pure Digital: la ripetizione automatizzata, la competenza conservata.',
    p2=['Ordini, riordini, fatture, tracking e resi vivono nel tuo account, senza orari d’ufficio.',
        'Strumenti pensati per il salone: ordine rapido, calcolatore colore, redditività su ogni scheda prodotto.',
        'Un numero di versione in fondo a ogni pagina e un elenco pubblico di cosa cambia a ogni rilascio.'],
    p2_link='Vedi gli aggiornamenti',
    p3_h='Imparziale', p3_sub='Le stesse regole per chiunque usi la piattaforma.',
    p3=['I prezzi dipendono dal ruolo e li vedi prima di ordinare: niente agenti, niente listini su richiesta, niente trattative persona per persona.',
        'Il consiglio segue la formula e il protocollo, non il margine: meno acquisti sbagliati, meno sprechi.',
        'Ogni marchio è presentato con gli stessi dati: INCI, protocollo, costo per servizio. Una correzione entra in piattaforma perché è stata verificata, chiunque la invii.'],
    p3_link='Il nostro principio sui prezzi',

    s2_eye='Il metodo', s2_t='Una conoscenza che cresce con chi lavora',
    steps=[('Conosciamo ogni formula', 'Poche gamme complete, studiate fino all’ultimo INCI, con protocollo e costo per servizio per ogni referenza.'),
           ('<span class="cca-brand">clichAIr</span> lavora con te', 'Calcola dosaggi e costi, costruisce routine, gestisce ordini e richieste 24 ore su 24, sul sito e su WhatsApp.'),
           ('Il salone riporta la realtà', 'Quando un protocollo si comporta diversamente su un capello reale, il professionista verificato lo segnala.'),
           ('Gli esperti validano, tutti ne beneficiano', 'Il nostro team verifica la correzione e da quel momento clichAIr risponde meglio a ogni salone e a ogni cliente. Quando serve, l’informazione torna anche alla casa madre.')],
    loop='Il ciclo ricomincia',
    quote_a='Un distributore ti vende il prodotto.', quote_b='cliCHair ti restituisce anche quello che i saloni hanno imparato usandolo.',
    s2_cta='Entra nella community PRO',

    s3_eye='L’origine', s3_t='Prima la distribuzione. Poi la piattaforma.',
    s3_p='cliCHair nasce dall’incontro di due mestieri che di solito non si parlano: una master colorist con anni di lavoro tecnico dietro la poltrona, che conosce i limiti reali dei prodotti perché li ha usati sulle teste dei clienti, e uno sviluppatore convinto che le decisioni di un salone potessero essere calcolate invece che intuite.',
    tl=[('2018', 'ÜLTIMA hair concept', 'Per anni lavoriamo come distributore professionale nel modo classico: visite in salone, campionature, listini su carta. Quel periodo ci ha insegnato il mestiere dall’interno, e ci ha mostrato con precisione quali parti del lavoro erano competenza vera e quali erano soltanto ripetizione.'),
        ('La piattaforma', 'cliCHair', 'Abbiamo automatizzato la ripetizione e tenuto la competenza. Il metodo non è arrivato dopo la tecnologia: la tecnologia è nata per far girare il metodo.'),
        ('Il motore', 'clichAIr', 'Il motore di calcolo che dà il nome alla piattaforma, su ogni pagina del sito e sui canali di messaggistica che usi già.'),
        ('Oggi', 'Una piattaforma che evolve', 'Ogni rilascio ha un numero e una data. Cosa è cambiato, e cosa cambia per te, è sulla pagina Aggiornamenti.')],
    s3_link='Leggi gli aggiornamenti',

    s4_eye='La piattaforma', s4_t='Sempre aperta, tra il marchio e chi lo usa',
    s4_p1='cliCHair è la piattaforma svizzera dedicata all’haircare professionale. Siamo importatori ufficiali dei marchi che proponiamo, con spedizione rapida in tutta la Svizzera e nel Liechtenstein.',
    s4_p2='Funzioniamo come hub: il marchio da una parte, chi usa il prodotto dall’altra, e in mezzo una piattaforma che non chiude mai. Nessun appuntamento da fissare, nessun giro di telefonate, nessuna attesa per un listino. Ordini quando ti serve, con i prezzi già corretti per il tuo profilo e il calcolo tecnico disponibile in ogni momento.',
    s4_p3='Ogni tipo di accesso è verificato e vede il catalogo che gli compete. I privati trovano la selezione retail: gli stessi prodotti che un parrucchiere consiglia e rivende in salone, con gli stessi INCI e la stessa consulenza tecnica. I professionisti verificati accedono in più al catalogo completo, con le linee tecniche, il colore e i formati professionali che restano fuori dalla vista di chi non lavora nel settore.',
    hub=[('I marchi', 'Importazione ufficiale. Dati tecnici direttamente dal produttore.'),
         ('La piattaforma', 'clichAIr, un catalogo per ogni ruolo, logistica, prezzi, sempre aperta.'),
         ('Le persone', 'Saloni, privati, scuole, distributori, negozi online.')],
    aud=[('Saloni e parrucchieri', 'Catalogo tecnico completo, formati professionali e prezzi riservati, con strumenti che calcolano ogni servizio.', 'Sono un parrucchiere', '/pages/professionals'),
         ('Privati', 'Sei il benvenuto. Con clichAIr come consigliere esperto trovi gli stessi prodotti che i migliori saloni rivendono ai loro clienti. Linee tecniche, trattamenti intensivi e formati professionali restano riservati ai professionisti.', 'Sono un privato', '/collections/all'),
         ('Scuole e accademie', 'Fornitura continuativa per i laboratori didattici e le esercitazioni.', 'Scuole e accademie', '/pages/professionals'),
         ('Distributori professionali', 'Accesso alle gamme per chi rifornisce saloni sul territorio con una propria rete.', 'Distributori', '/pages/professionals'),
         ('Negozi online', 'Vendi la selezione retail sul tuo negozio Shopify senza acquistare stock: noi spediamo, tu guadagni. Riservato ai membri PRO.', 'Programma rivenditori', '/pages/retailers'),
         ('Partner e creator', 'Scuole, laboratori, media, creator: progetti che condividono la nostra idea di haircare professionale.', 'Collabora', '/pages/collaborations')],

    s5_eye='Il principio', s5_t='Profondità, non ampiezza',
    s5_p1='La differenza non è quanti prodotti trovi. È quanto li conosciamo.',
    s5_p2='Lavoriamo su poche gamme professionali complete, linee tecniche e colore inclusi, studiate fino all’ultimo INCI. Un assortimento generalista ti offre qualche referenza da banco. Qui trovi la gamma intera, con il protocollo di applicazione di ogni singola referenza e il calcolo del costo per servizio.',
    s5_p3='È anche per questo che le linee tecniche restano riservate ai professionisti: protegge la tua competenza in salone e tiene le referenze professionali fuori dalle guerre di prezzo online.',
    brands_label='I marchi in piattaforma', brands_all='Tutti i marchi',
    s5_link='Registrati come professionista',

    s6_eye='Il motore', s6_t='clichAIr', s6_lead='Non è una chat di assistenza. È il motore di calcolo che dà il nome alla piattaforma.',
    eng_a_h='Se hai un salone',
    eng_a=['Dosaggi per applicazione e costo per servizio', 'Quante applicazioni ottieni da una confezione e la redditività di un kit', 'Ordini, riordini e richieste, 24 ore su 24'],
    eng_b_h='Se compri per te',
    eng_b=['Legge gli INCI e verifica che i prodotti che metti insieme siano compatibili', 'Costruisce la routine giusta per il tuo capello, così smetti di comprare per tentativi', 'Quanto dura un prodotto e quanto costa per utilizzo'],
    valid_h='L’AI non decide da sola',
    valid_p1='Ogni formula passa dal nostro team di esperti, ogni protocollo dalla verifica tecnica sul campo. Niente entra in piattaforma senza quel controllo.',
    valid_p2='La piattaforma non impara da sola e non impara dal web: cresce solo su ciò che il team ha verificato. E quando una domanda supera i suoi limiti, clichAIr passa la mano al nostro team.',
    badge_note='Clicca sul badge AIr, in basso a sinistra: è su ogni pagina del sito. clichAIr risponde anche su WhatsApp e sui canali di messaggistica che usi già.',

    s7_eye='Gli strumenti', s7_t='Integrati nella piattaforma, senza app in più',
    s7_lead='Alcuni sono riservati ai professionisti verificati, gli altri sono aperti a tutti.',
    tag_pro='PRO', tag_all='Per tutti',
    tools=[('list', 'Ordine rapido', 'Tutto il catalogo in un’unica lista, per marchio e linea, con il guadagno stimato accanto a ogni prodotto.', True, None, None),
           ('drop', 'Calcolatore colore', 'Il costo di ogni servizio colore e lo stock che ti serve per il mese.', True, None, None),
           ('chart', 'Pannello redditività', 'Su ogni scheda prodotto: costo per servizio, punto di pareggio e guadagno per il salone.', True, None, None),
           ('clock', 'Costo per utilizzo', 'Sulle stesse schede, per i privati: quanto dura il prodotto e quanto costa per utilizzo.', False, None, None),
           ('user', 'Il tuo account', 'Ordini, riordini, fatture, tracking e storico acquisti. Resi richiesti in autonomia entro 14 giorni.', False, None, None),
           ('card', 'Pagamenti', 'Twint, PayPal, carte e Klarna, con la possibilità di pagare a 30 giorni.', False, None, None),
           ('repeat', 'Abbonamenti', 'I prodotti idonei ogni 4, 6 o 8 settimane, con uno sconto su ogni consegna. Metti in pausa o annulla quando vuoi.', False, None, None),
           ('tag', 'Aggiornamenti', 'Un numero di versione in fondo a ogni pagina. Ogni rilascio è elencato con la sua data e cosa cambia.', False, 'Vedi gli aggiornamenti', '/pages/updates')],

    s8_eye='Il valore', s8_t='Il valore resta a chi lavora',
    s8_p1='L’automazione della piattaforma riduce i costi di struttura, e quel risparmio non lo tratteniamo: diventa il prezzo che vedi. Nessun listino gonfiato con sconti apparenti sopra.',
    s8_p2='Ogni canale ha le proprie condizioni, calcolate sul ruolo di chi acquista e sul valore reale del prodotto. Due saloni con lo stesso profilo vedono lo stesso prezzo: non dipende da chi chiama più spesso o tratta più duramente.',
    s8_p3='E nessun vincolo: niente contratti, niente minimi d’ordine punitivi. Se hai già un fornitore di fiducia, tienilo. cliCHair funziona bene anche come canale complementare, per le urgenze e per testare linee nuove.',
    s8_cta='Richiedi le tue condizioni',

    s9_eye='La formazione', s9_t='Il prodotto rende quanto la mano che lo applica',
    s9_p1='Un prodotto tecnico da solo non basta. Per questo affianchiamo alla piattaforma corsi professionali in presenza, costruiti insieme alle case madri.',
    s9_p2='Organizziamo corsi ed eventi con regolarità, e attiviamo sessioni dedicate quando un gruppo di saloni condivide lo stesso interesse tecnico. Scrivici quale tema ti interessa e ti avvisiamo appena le date sono aperte.',
    s9_link='Scrivici per la formazione',

    s10_eye='L’etica', s10_t='Protocollo cliCHair ECO',
    eco=[('box', 'Spedizioni compensate', 'Le emissioni di ogni spedizione sono compensate tramite DHL GoGreen e Shopify Planet, senza costi aggiuntivi per te.'),
         ('leaf', 'Imballaggi essenziali', 'Carta e cartone, materiali riciclabili, plastica ridotta all’essenziale.'),
         ('check', 'Meno acquisti sbagliati', 'clichAIr legge l’INCI completo prima dell’acquisto: meno prodotto sprecato, meno da buttare.')],
    s10_p='L’efficienza digitale non è solo un vantaggio economico. È anche meno sprechi.',
    s10_link='Sostenibilità',

    s11_eye='Il team', s11_t='Le persone dietro il motore',
    roles=[('Direzione strategica', 'Costruisce le partnership con i marchi.'),
           ('Direzione operativa', 'Logistica e supporto quotidiano.'),
           ('Scienza e tricologia', 'Formule e protocolli sotto esame.'),
           ('Master colorist', 'Verifica sul campo ogni protocollo.')],
    s11_p1='clichAIr risponde per primo, per iscritto, a qualsiasi ora. Il nostro team interviene nei giorni lavorativi, per iscritto, quando una domanda richiede una decisione umana: chi ti risponde è la persona che segue davvero quel lavoro.',
    s11_p2='Scrivici per qualsiasi richiesta, tecnica o commerciale.',
    s11_cta='Contattaci',

    s12_t='Scegli il tuo accesso',
    s12_p='I privati navigano e ordinano senza registrarsi. I professionisti si registrano una volta sola: gratis, verifica in 24 ore, nessun vincolo.',
    s12_links_a='Non sei ancora convinto?', s12_links_b='Leggi la pagina Professionisti', s12_links_c='oppure', s12_links_d='cosa cambia a ogni versione',
)

T['de'] = dict(
    lang='de', prefix='/de',
    kicker='Die cliCHair Plattform',
    h1=('Intelligent.', 'Innovativ.', 'Unparteiisch.'),
    hero_lead='cliCHair ist die Schweizer Plattform für professionelle Haarpflege. Ein Motor, der jede Formel kennt, Regeln, die für alle gleich sind, und Antworten, die von Experten geprüft werden, bevor sie Sie erreichen.',
    btn_pro='PRO-Konto', btn_shop='Shop', hero_link='Was clichAIr macht',
    facts=[('Schweiz und Liechtenstein', 'Liefergebiet'),
           ('Offizieller Importeur', 'Der Marken, die wir führen'),
           ('24/7', 'clichAIr antwortet schriftlich'),
           ('12:00', 'Bestellungen bis Mittag gehen am selben Tag raus, Mo bis Fr'),
           ('CHF 99', 'Kostenloser DHL-Express-Versand ab'),
           ('4 Sprachen', 'DE, FR, IT, EN')],

    s1_eye='Drei Worte', s1_t='Drei Worte, und was sie in der Praxis bedeuten',
    s1_lead='Wir bitten Sie nicht, uns einfach zu glauben. Hinter jedem Wort steht etwas, das Sie heute auf dieser Website prüfen können.',
    p1_h='Intelligent', p1_sub='Ein Motor, der rechnet, kein Chat, der beruhigt.',
    p1=['clichAIr liest jede INCI-Liste und berechnet Dosierungen, Kosten pro Dienstleistung und die passende Routine.',
        'Er antwortet rund um die Uhr, auf der Website und über WhatsApp.',
        'Er lernt nur aus Korrekturen, die unsere Experten geprüft haben, nie aus dem Netz.'],
    p1_link='So arbeitet clichAIr',
    p2_h='Innovativ', p2_sub='Das Pure-Digital-Modell: Wiederholung automatisiert, Kompetenz behalten.',
    p2=['Bestellungen, Nachbestellungen, Rechnungen, Sendungsverfolgung und Rücksendungen liegen in Ihrem Konto, ohne Bürozeiten.',
        'Werkzeuge für den Salon: Schnellbestellung, Farbrechner, Rentabilität auf jeder Produktseite.',
        'Eine Versionsnummer am Ende jeder Seite und eine öffentliche Liste, was sich mit jeder Version ändert.'],
    p2_link='Neuigkeiten ansehen',
    p3_h='Unparteiisch', p3_sub='Dieselben Regeln für alle, die die Plattform nutzen.',
    p3=['Die Preise richten sich nach der Rolle und sind vor der Bestellung sichtbar: keine Aussendienstler, keine Preislisten auf Anfrage, kein Verhandeln von Person zu Person.',
        'Die Beratung folgt der Formel und dem Protokoll, nicht der Marge: weniger Fehlkäufe, weniger Verschwendung.',
        'Jede Marke wird mit denselben Daten präsentiert: INCI, Protokoll, Kosten pro Dienstleistung. Eine Korrektur kommt in die Plattform, weil sie geprüft wurde, egal wer sie schickt.'],
    p3_link='Unser Preisprinzip',

    s2_eye='Die Methode', s2_t='Wissen, das mit denen wächst, die damit arbeiten',
    steps=[('Wir kennen jede Formel', 'Wenige vollständige Sortimente, bis zum letzten INCI studiert, mit Protokoll und Kosten pro Dienstleistung für jede Referenz.'),
           ('<span class="cca-brand">clichAIr</span> arbeitet mit Ihnen', 'Er berechnet Dosierungen und Kosten, erstellt Routinen und bearbeitet Bestellungen und Anfragen rund um die Uhr, auf der Website und über WhatsApp.'),
           ('Der Salon meldet die Praxis', 'Verhält sich ein Protokoll an echtem Haar anders, meldet die geprüfte Fachperson dies.'),
           ('Experten prüfen, alle profitieren', 'Unser Team prüft die Korrektur, und ab diesem Moment antwortet clichAIr jedem Salon und jedem Kunden besser. Wenn nötig, geht die Information auch an den Hersteller zurück.')],
    loop='Der Kreislauf beginnt von vorn',
    quote_a='Ein Distributor verkauft Ihnen das Produkt.', quote_b='cliCHair gibt Ihnen auch zurück, was die Salons bei seiner Anwendung gelernt haben.',
    s2_cta='Der PRO-Community beitreten',

    s3_eye='Der Ursprung', s3_t='Zuerst der Vertrieb. Dann die Plattform.',
    s3_p='cliCHair entstand aus der Begegnung zweier Berufe, die sonst selten miteinander sprechen: eine Master Colorist mit Jahren technischer Arbeit hinter dem Stuhl, die die realen Grenzen der Produkte kennt, weil sie sie am Haar ihrer Kundinnen angewendet hat, und ein Entwickler, der davon überzeugt war, dass sich die Entscheidungen eines Salons berechnen statt schätzen lassen.',
    tl=[('2018', 'ÜLTIMA hair concept', 'Jahrelang arbeiten wir als professioneller Distributor auf klassische Weise: Salonbesuche, Muster, Preislisten auf Papier. Diese Zeit hat uns das Handwerk von innen gelehrt und uns genau gezeigt, welche Teile der Arbeit echte Kompetenz waren und welche blosse Wiederholung.'),
        ('Die Plattform', 'cliCHair', 'Wir haben die Wiederholung automatisiert und die Kompetenz behalten. Die Methode kam nicht nach der Technologie: die Technologie entstand, um die Methode zum Laufen zu bringen.'),
        ('Der Motor', 'clichAIr', 'Der Rechenmotor, der der Plattform ihren Namen gibt, auf jeder Seite der Website und über die Messaging-Kanäle, die Sie ohnehin nutzen.'),
        ('Heute', 'Eine Plattform, die sich weiterentwickelt', 'Jede Version hat eine Nummer und ein Datum. Was sich geändert hat, und was das für Sie bedeutet, steht auf der Seite Neuigkeiten.')],
    s3_link='Neuigkeiten lesen',

    s4_eye='Die Plattform', s4_t='Immer offen, zwischen der Marke und denen, die sie nutzen',
    s4_p1='cliCHair ist die Schweizer Plattform für professionelle Haarpflege. Wir sind offizieller Importeur der Marken, die wir führen, mit schnellem Versand in die ganze Schweiz und nach Liechtenstein.',
    s4_p2='Wir funktionieren als Hub: die Marke auf der einen Seite, die Menschen, die das Produkt anwenden, auf der anderen, und dazwischen eine Plattform, die nie schliesst. Kein Termin zu vereinbaren, keine Telefonrunde, kein Warten auf eine Preisliste. Sie bestellen, wenn Sie es brauchen, mit Preisen, die bereits auf Ihr Profil abgestimmt sind, und mit der technischen Berechnung jederzeit verfügbar.',
    s4_p3='Jeder Zugang wird geprüft und sieht den Katalog, der ihm zusteht. Privatkunden finden die Retail-Auswahl: dieselben Produkte, die ein Coiffeur im Salon empfiehlt und verkauft, mit denselben INCI und derselben technischen Beratung. Geprüfte Fachleute erhalten zusätzlich Zugang zum vollständigen Katalog, mit den technischen Linien, der Farbe und den professionellen Formaten, die für Branchenfremde nicht sichtbar sind.',
    hub=[('Die Marken', 'Offizieller Import. Technische Daten direkt vom Hersteller.'),
         ('Die Plattform', 'clichAIr, ein Katalog für jede Rolle, Logistik, Preise, immer offen.'),
         ('Die Menschen', 'Salons, Privatkunden, Schulen, Distributoren, Online-Shops.')],
    aud=[('Salons und Coiffeure', 'Vollständiger Fachkatalog, professionelle Formate und reservierte Preise, mit Werkzeugen, die jede Dienstleistung berechnen.', 'Ich bin Coiffeur', '/pages/professionals'),
         ('Privatkunden', 'Sie sind herzlich willkommen. Mit clichAIr als fachkundigem Berater finden Sie dieselben Produkte, die die besten Salons ihren Kundinnen und Kunden verkaufen. Technische Linien, Intensivbehandlungen und professionelle Formate bleiben Fachleuten vorbehalten.', 'Ich bin Privatkunde', '/collections/all'),
         ('Schulen und Akademien', 'Laufende Versorgung für Lehrlabore und praktische Übungen.', 'Schulen und Akademien', '/pages/professionals'),
         ('Professionelle Distributoren', 'Zugang zu den Sortimenten für alle, die Salons über ihr eigenes Netz beliefern.', 'Distributoren', '/pages/professionals'),
         ('Online-Shops', 'Verkaufen Sie die Retail-Auswahl in Ihrem eigenen Shopify-Shop, ohne Lager zu kaufen: wir versenden, Sie verdienen. Reserviert für PRO-Mitglieder.', 'Händlerprogramm', '/pages/retailers'),
         ('Partner und Creator', 'Schulen, Labore, Medien, Creator: Projekte, die unsere Idee von professioneller Haarpflege teilen.', 'Zusammenarbeiten', '/pages/collaborations')],

    s5_eye='Das Prinzip', s5_t='Tiefe, nicht Breite',
    s5_p1='Der Unterschied liegt nicht darin, wie viele Produkte Sie finden. Sondern darin, wie gut wir sie kennen.',
    s5_p2='Wir arbeiten mit wenigen, dafür vollständigen professionellen Sortimenten, technische Linien und Farbe inbegriffen, bis zum letzten INCI studiert. Ein Generalistensortiment bietet Ihnen einige Verkaufsreferenzen. Hier finden Sie das ganze Sortiment, mit dem Anwendungsprotokoll jeder einzelnen Referenz und der Berechnung der Kosten pro Dienstleistung.',
    s5_p3='Auch deshalb bleiben die technischen Linien den Fachleuten vorbehalten: das schützt Ihre Kompetenz im Salon und hält die professionellen Referenzen aus den Preiskriegen im Netz heraus.',
    brands_label='Die Marken auf der Plattform', brands_all='Alle Marken',
    s5_link='Als Fachperson registrieren',

    s6_eye='Der Motor', s6_t='clichAIr', s6_lead='Kein Support-Chat. Es ist der Rechenmotor, der der Plattform ihren Namen gibt.',
    eng_a_h='Wenn Sie einen Salon führen',
    eng_a=['Dosierungen pro Anwendung und Kosten pro Dienstleistung', 'Wie viele Anwendungen eine Packung ergibt und wie rentabel ein Kit ist', 'Bestellungen, Nachbestellungen und Anfragen, rund um die Uhr'],
    eng_b_h='Wenn Sie für sich selbst kaufen',
    eng_b=['Er liest die INCI und prüft, ob die Produkte, die Sie kombinieren, verträglich sind', 'Er baut die passende Routine für Ihr Haar, damit Sie nicht mehr auf Verdacht kaufen', 'Wie lange ein Produkt reicht und was es pro Anwendung kostet'],
    valid_h='Die AI entscheidet nicht allein',
    valid_p1='Jede Formulierung geht durch unser Expertenteam, jedes Protokoll durch die technische Prüfung in der Praxis. Nichts kommt ohne diese Kontrolle in die Plattform.',
    valid_p2='Die Plattform lernt nicht von selbst und lernt nicht aus dem Netz: sie wächst nur mit dem, was das Team geprüft hat. Und wenn eine Frage seine Grenzen überschreitet, übergibt clichAIr an unser Team.',
    badge_note='Klicken Sie auf das AIr-Badge unten links: es ist auf jeder Seite der Website. clichAIr antwortet auch über WhatsApp und über die Messaging-Kanäle, die Sie ohnehin nutzen.',

    s7_eye='Die Werkzeuge', s7_t='In die Plattform integriert, ohne zusätzliche App',
    s7_lead='Einige sind geprüften Fachleuten vorbehalten, die anderen stehen allen offen.',
    tag_pro='PRO', tag_all='Für alle',
    tools=[('list', 'Schnellbestellung', 'Der ganze Katalog in einer Liste, nach Marke und Linie, mit dem geschätzten Gewinn neben jedem Produkt.', True, None, None),
           ('drop', 'Farbrechner', 'Die Kosten jeder Farbdienstleistung und der Lagerbedarf für den Monat.', True, None, None),
           ('chart', 'Rentabilitätspanel', 'Auf jeder Produktseite: Kosten pro Dienstleistung, Break-even und Gewinn für den Salon.', True, None, None),
           ('clock', 'Kosten pro Anwendung', 'Auf denselben Seiten, für Privatkunden: wie lange das Produkt reicht und was es pro Anwendung kostet.', False, None, None),
           ('user', 'Ihr Konto', 'Bestellungen, Nachbestellungen, Rechnungen, Sendungsverfolgung und Bestellhistorie. Rücksendungen selbst beantragen, innerhalb von 14 Tagen.', False, None, None),
           ('card', 'Zahlungen', 'Twint, PayPal, Karten und Klarna, mit der Möglichkeit, in 30 Tagen zu bezahlen.', False, None, None),
           ('repeat', 'Abonnements', 'Geeignete Produkte alle 4, 6 oder 8 Wochen, mit Rabatt auf jede Lieferung. Jederzeit pausieren oder kündigen.', False, None, None),
           ('tag', 'Neuigkeiten', 'Eine Versionsnummer am Ende jeder Seite. Jede Version ist mit Datum und Änderungen aufgeführt.', False, 'Neuigkeiten ansehen', '/pages/updates')],

    s8_eye='Der Wert', s8_t='Der Wert bleibt dort, wo gearbeitet wird',
    s8_p1='Die Automatisierung der Plattform senkt die Strukturkosten, und diese Ersparnis behalten wir nicht: sie wird zum Preis, den Sie sehen. Keine aufgeblähte Preisliste mit scheinbaren Rabatten darüber.',
    s8_p2='Jeder Kanal hat seine eigenen Konditionen, berechnet auf die Rolle des Käufers und den realen Wert des Produkts. Zwei Salons mit demselben Profil sehen denselben Preis: er hängt nicht davon ab, wer öfter anruft oder härter verhandelt.',
    s8_p3='Und keine Bindung: keine Verträge, keine strafenden Mindestbestellmengen. Wenn Sie bereits einen Lieferanten Ihres Vertrauens haben, behalten Sie ihn. cliCHair funktioniert auch als ergänzender Kanal sehr gut, für dringende Fälle und um neue Linien zu testen.',
    s8_cta='Ihre Konditionen anfragen',

    s9_eye='Die Ausbildung', s9_t='Ein Produkt wirkt so gut wie die Hand, die es anwendet',
    s9_p1='Ein technisches Produkt allein genügt nicht. Deshalb ergänzen wir die Plattform durch professionelle Präsenzkurse, die wir gemeinsam mit den Herstellern aufbauen.',
    s9_p2='Wir organisieren regelmässig Kurse und Veranstaltungen und öffnen zusätzliche Sessionen, wenn eine Gruppe von Salons dasselbe fachliche Interesse teilt. Schreiben Sie uns, welches Thema Sie interessiert, und wir melden uns, sobald Termine offen sind.',
    s9_link='Schreiben Sie uns zur Ausbildung',

    s10_eye='Die Ethik', s10_t='Das cliCHair ECO Protokoll',
    eco=[('box', 'Kompensierter Versand', 'Die Emissionen jeder Sendung werden über DHL GoGreen und Shopify Planet kompensiert, ohne Mehrkosten für Sie.'),
         ('leaf', 'Reduzierte Verpackung', 'Papier und Karton, recycelbare Materialien, Plastik auf das Nötigste reduziert.'),
         ('check', 'Weniger Fehlkäufe', 'clichAIr liest die vollständige INCI-Liste vor dem Kauf: weniger verschwendetes Produkt, weniger Abfall.')],
    s10_p='Digitale Effizienz ist nicht nur ein wirtschaftlicher Vorteil. Sie bedeutet auch weniger Verschwendung.',
    s10_link='Nachhaltigkeit',

    s11_eye='Das Team', s11_t='Die Menschen hinter dem Motor',
    roles=[('Strategische Leitung', 'Baut die Partnerschaften mit den Marken auf.'),
           ('Operative Leitung', 'Logistik und täglicher Support.'),
           ('Wissenschaft und Trichologie', 'Formeln und Protokolle in der Prüfung.'),
           ('Master Colorist', 'Prüft jedes Protokoll in der Praxis.')],
    s11_p1='clichAIr antwortet zuerst, schriftlich, zu jeder Stunde. Unser Team übernimmt an Werktagen, schriftlich, wenn eine Frage eine menschliche Entscheidung braucht: die Person, die Ihnen antwortet, macht diese Arbeit auch wirklich.',
    s11_p2='Schreiben Sie uns bei jedem Anliegen, technisch oder kaufmännisch.',
    s11_cta='Kontaktieren Sie uns',

    s12_t='Wählen Sie Ihren Zugang',
    s12_p='Privatkunden stöbern und bestellen ohne Registrierung. Fachleute registrieren sich einmal: kostenlos, in 24 Stunden geprüft, ohne Verpflichtung.',
    s12_links_a='Noch nicht überzeugt?', s12_links_b='Lesen Sie die Seite Fachleute', s12_links_c='oder', s12_links_d='was sich mit jeder Version ändert',
)

T['fr'] = dict(
    lang='fr', prefix='/fr',
    kicker='La plateforme cliCHair',
    h1=('Intelligente.', 'Innovante.', 'Impartiale.'),
    hero_lead='cliCHair est la plateforme suisse des soins capillaires professionnels. Un moteur qui connaît chaque formule, des règles identiques pour tous et des réponses vérifiées par des experts avant de vous parvenir.',
    btn_pro='Compte PRO', btn_shop='Shop', hero_link='Ce que fait clichAIr',
    facts=[('Suisse et Liechtenstein', 'Zone de livraison'),
           ('Importateur officiel', 'Des marques que nous proposons'),
           ('24/7', 'clichAIr répond par écrit'),
           ('12:00', 'Commandes avant midi expédiées le jour même, lun-ven'),
           ('CHF 99', 'Livraison DHL Express offerte dès'),
           ('4 langues', 'FR, DE, IT, EN')],

    s1_eye='Trois mots', s1_t='Trois mots, et ce qu’ils veulent dire en pratique',
    s1_lead='Nous ne vous demandons pas de nous croire sur parole. Derrière chacun, il y a quelque chose que vous pouvez vérifier sur ce site dès aujourd’hui.',
    p1_h='Intelligente', p1_sub='Un moteur qui calcule, pas un chat qui rassure.',
    p1=['clichAIr lit chaque INCI et calcule les dosages, le coût par service et la bonne routine.',
        'Il répond 24 heures sur 24, sur le site et sur WhatsApp.',
        'Il n’apprend que des corrections vérifiées par nos experts, jamais du web.'],
    p1_link='Comment travaille clichAIr',
    p2_h='Innovante', p2_sub='Le modèle Pure Digital : la répétition automatisée, la compétence conservée.',
    p2=['Commandes, réassorts, factures, suivi et retours vivent dans votre compte, sans horaires de bureau.',
        'Des outils pensés pour le salon : commande rapide, calculateur couleur, rentabilité sur chaque fiche produit.',
        'Un numéro de version en bas de chaque page et une liste publique de ce qui change à chaque sortie.'],
    p2_link='Voir les mises à jour',
    p3_h='Impartiale', p3_sub='Les mêmes règles pour toutes celles et ceux qui utilisent la plateforme.',
    p3=['Les prix dépendent du rôle et sont visibles avant de commander : pas de représentants, pas de tarifs sur demande, pas de négociation au cas par cas.',
        'Le conseil suit la formule et le protocole, pas la marge : moins d’achats inutiles, moins de gaspillage.',
        'Chaque marque est présentée avec les mêmes données : INCI, protocole, coût par service. Une correction entre dans la plateforme parce qu’elle a été vérifiée, quelle que soit la personne qui l’envoie.'],
    p3_link='Notre principe de prix',

    s2_eye='La méthode', s2_t='Un savoir qui grandit avec celles et ceux qui travaillent',
    steps=[('Nous connaissons chaque formule', 'Peu de gammes complètes, étudiées jusqu’au dernier INCI, avec le protocole et le coût par service de chaque référence.'),
           ('<span class="cca-brand">clichAIr</span> travaille avec vous', 'Il calcule dosages et coûts, construit des routines, gère commandes et demandes 24 heures sur 24, sur le site et sur WhatsApp.'),
           ('Le salon rapporte la réalité', 'Quand un protocole se comporte différemment sur un cheveu réel, le professionnel vérifié le signale.'),
           ('Les experts valident, tout le monde en profite', 'Notre équipe vérifie la correction et, dès ce moment, clichAIr répond mieux à chaque salon et à chaque client. Si nécessaire, l’information remonte aussi à la maison mère.')],
    loop='Le cycle recommence',
    quote_a='Un distributeur vous vend le produit.', quote_b='cliCHair vous rend aussi ce que les salons ont appris en l’utilisant.',
    s2_cta='Rejoindre la communauté PRO',

    s3_eye='L’origine', s3_t='D’abord la distribution. Puis la plateforme.',
    s3_p='cliCHair est née de la rencontre de deux métiers qui se parlent rarement : une master colorist avec des années de travail technique derrière le fauteuil, qui connaît les limites réelles des produits parce qu’elle les a utilisés sur les cheveux de ses clientes, et un développeur convaincu que les décisions d’un salon pouvaient être calculées plutôt que devinées.',
    tl=[('2018', 'ÜLTIMA hair concept', 'Pendant des années nous travaillons comme distributeur professionnel à la manière classique : visites en salon, échantillons, tarifs sur papier. Cette période nous a appris le métier de l’intérieur, et nous a montré avec précision quelles parties du travail relevaient de la vraie compétence et lesquelles n’étaient que de la répétition.'),
        ('La plateforme', 'cliCHair', 'Nous avons automatisé la répétition et gardé la compétence. La méthode n’est pas venue après la technologie : la technologie est née pour faire tourner la méthode.'),
        ('Le moteur', 'clichAIr', 'Le moteur de calcul qui donne son nom à la plateforme, sur chaque page du site et sur les canaux de messagerie que vous utilisez déjà.'),
        ('Aujourd’hui', 'Une plateforme qui évolue', 'Chaque sortie a un numéro et une date. Ce qui a changé, et ce que cela change pour vous, est sur la page Mises à jour.')],
    s3_link='Lire les mises à jour',

    s4_eye='La plateforme', s4_t='Toujours ouverte, entre la marque et ceux qui l’utilisent',
    s4_p1='cliCHair est la plateforme suisse dédiée aux soins capillaires professionnels. Nous sommes importateurs officiels des marques que nous proposons, avec une expédition rapide dans toute la Suisse et au Liechtenstein.',
    s4_p2='Nous fonctionnons comme un hub : la marque d’un côté, celles et ceux qui utilisent le produit de l’autre, et au milieu une plateforme qui ne ferme jamais. Aucun rendez-vous à fixer, aucune série d’appels, aucune attente pour un tarif. Vous commandez quand vous en avez besoin, avec des prix déjà ajustés à votre profil et le calcul technique disponible à tout moment.',
    s4_p3='Chaque type d’accès est vérifié et voit le catalogue qui lui revient. Les particuliers trouvent la sélection retail : les mêmes produits qu’un coiffeur conseille et revend en salon, avec les mêmes INCI et le même conseil technique. Les professionnels vérifiés accèdent en plus au catalogue complet, avec les lignes techniques, la couleur et les formats professionnels qui restent hors de vue pour qui ne travaille pas dans le métier.',
    hub=[('Les marques', 'Importation officielle. Données techniques directement du fabricant.'),
         ('La plateforme', 'clichAIr, un catalogue pour chaque rôle, logistique, prix, toujours ouverte.'),
         ('Les personnes', 'Salons, particuliers, écoles, distributeurs, boutiques en ligne.')],
    aud=[('Salons et coiffeurs', 'Catalogue technique complet, formats professionnels et tarifs réservés, avec des outils qui calculent chaque service.', 'Je suis coiffeur', '/pages/professionals'),
         ('Particuliers', 'Vous êtes les bienvenus. Avec clichAIr comme conseiller expert, vous trouvez les mêmes produits que les meilleurs salons proposent à leur clientèle. Les lignes techniques, les soins intensifs et les formats professionnels restent réservés aux professionnels.', 'Je suis un particulier', '/collections/all'),
         ('Écoles et académies', 'Approvisionnement continu pour les laboratoires pédagogiques et les travaux pratiques.', 'Écoles et académies', '/pages/professionals'),
         ('Distributeurs professionnels', 'Accès aux gammes pour celles et ceux qui approvisionnent les salons avec leur propre réseau.', 'Distributeurs', '/pages/professionals'),
         ('Boutiques en ligne', 'Vendez la sélection retail sur votre propre boutique Shopify sans acheter de stock : nous expédions, vous gagnez. Réservé aux membres PRO.', 'Programme revendeurs', '/pages/retailers'),
         ('Partenaires et créateurs', 'Écoles, laboratoires, médias, créateurs : des projets qui partagent notre idée des soins capillaires professionnels.', 'Collaborer', '/pages/collaborations')],

    s5_eye='Le principe', s5_t='La profondeur, pas l’étendue',
    s5_p1='La différence n’est pas le nombre de produits que vous trouvez. C’est à quel point nous les connaissons.',
    s5_p2='Nous travaillons sur peu de gammes professionnelles complètes, lignes techniques et couleur comprises, étudiées jusqu’au dernier INCI. Un assortiment généraliste vous propose quelques références de revente. Ici vous trouvez la gamme entière, avec le protocole d’application de chaque référence et le calcul du coût par service.',
    s5_p3='C’est aussi pour cela que les lignes techniques restent réservées aux professionnels : cela protège votre compétence en salon et tient les références professionnelles à l’écart des guerres de prix en ligne.',
    brands_label='Les marques sur la plateforme', brands_all='Toutes les marques',
    s5_link='Inscrivez-vous comme professionnel',

    s6_eye='Le moteur', s6_t='clichAIr', s6_lead='Ce n’est pas un chat d’assistance. C’est le moteur de calcul qui donne son nom à la plateforme.',
    eng_a_h='Si vous avez un salon',
    eng_a=['Dosages par application et coût par service', 'Combien d’applications vous obtenez d’un conditionnement, et la rentabilité d’un kit', 'Commandes, réassorts et demandes, 24 heures sur 24'],
    eng_b_h='Si vous achetez pour vous',
    eng_b=['Il lit les INCI et vérifie que les produits que vous associez sont compatibles', 'Il construit la routine adaptée à votre cheveu, pour ne plus acheter par tâtonnements', 'Combien de temps dure un produit et ce qu’il coûte par utilisation'],
    valid_h='L’AI ne décide pas seule',
    valid_p1='Chaque formule passe par notre équipe d’experts, chaque protocole par la vérification technique sur le terrain. Rien n’entre dans la plateforme sans ce contrôle.',
    valid_p2='La plateforme n’apprend pas toute seule et n’apprend pas du web : elle grandit uniquement sur ce que l’équipe a vérifié. Et lorsqu’une question dépasse ses limites, clichAIr passe le relais à notre équipe.',
    badge_note='Cliquez sur le badge AIr, en bas à gauche : il est sur chaque page du site. clichAIr répond aussi sur WhatsApp et sur les canaux de messagerie que vous utilisez déjà.',

    s7_eye='Les outils', s7_t='Intégrés à la plateforme, sans application en plus',
    s7_lead='Certains sont réservés aux professionnels vérifiés, les autres sont ouverts à tous.',
    tag_pro='PRO', tag_all='Pour tous',
    tools=[('list', 'Commande rapide', 'Tout le catalogue en une seule liste, par marque et par ligne, avec le gain estimé à côté de chaque produit.', True, None, None),
           ('drop', 'Calculateur couleur', 'Le coût de chaque service couleur et le stock dont vous avez besoin pour le mois.', True, None, None),
           ('chart', 'Panneau de rentabilité', 'Sur chaque fiche produit : coût par service, seuil de rentabilité et gain pour le salon.', True, None, None),
           ('clock', 'Coût par utilisation', 'Sur les mêmes fiches, pour les particuliers : combien de temps dure le produit et ce qu’il coûte par utilisation.', False, None, None),
           ('user', 'Votre compte', 'Commandes, réassorts, factures, suivi et historique d’achats. Retours demandés en libre-service dans les 14 jours.', False, None, None),
           ('card', 'Paiements', 'Twint, PayPal, cartes et Klarna, avec la possibilité de payer à 30 jours.', False, None, None),
           ('repeat', 'Abonnements', 'Les produits éligibles toutes les 4, 6 ou 8 semaines, avec une remise sur chaque livraison. Pause ou annulation à tout moment.', False, None, None),
           ('tag', 'Mises à jour', 'Un numéro de version en bas de chaque page. Chaque sortie est listée avec sa date et ce qu’elle change.', False, 'Voir les mises à jour', '/pages/updates')],

    s8_eye='La valeur', s8_t='La valeur reste là où se fait le travail',
    s8_p1='L’automatisation de la plateforme réduit les coûts de structure, et nous ne gardons pas cette économie : elle devient le prix que vous voyez. Aucun tarif gonflé avec des remises apparentes par-dessus.',
    s8_p2='Chaque canal a ses propres conditions, calculées sur le rôle de celui qui achète et sur la valeur réelle du produit. Deux salons au même profil voient le même prix : il ne dépend pas de qui appelle le plus souvent ou négocie le plus fort.',
    s8_p3='Et aucune contrainte : pas de contrats, pas de minimums de commande punitifs. Si vous avez déjà un fournisseur de confiance, gardez-le. cliCHair fonctionne aussi très bien comme canal complémentaire, pour les urgences et pour tester de nouvelles lignes.',
    s8_cta='Demandez vos conditions',

    s9_eye='La formation', s9_t='Un produit vaut ce que vaut la main qui l’applique',
    s9_p1='Un produit technique seul ne suffit pas. C’est pourquoi nous complétons la plateforme par des cours professionnels en présentiel, construits avec les maisons mères.',
    s9_p2='Nous organisons des cours et des événements régulièrement, et nous ouvrons des sessions dédiées lorsqu’un groupe de salons partage le même intérêt technique. Écrivez-nous le thème qui vous intéresse et nous vous prévenons dès que les dates s’ouvrent.',
    s9_link='Écrivez-nous pour la formation',

    s10_eye='L’éthique', s10_t='Le protocole cliCHair ECO',
    eco=[('box', 'Expéditions compensées', 'Les émissions de chaque expédition sont compensées via DHL GoGreen et Shopify Planet, sans frais supplémentaires pour vous.'),
         ('leaf', 'Emballages essentiels', 'Papier et carton, matériaux recyclables, plastique réduit à l’essentiel.'),
         ('check', 'Moins d’achats inutiles', 'clichAIr lit l’INCI complet avant l’achat : moins de produit gaspillé, moins à jeter.')],
    s10_p='L’efficacité digitale n’est pas seulement un avantage économique. C’est aussi moins de gaspillage.',
    s10_link='Durabilité',

    s11_eye='L’équipe', s11_t='Les personnes derrière le moteur',
    roles=[('Direction stratégique', 'Construit les partenariats avec les marques.'),
           ('Direction opérationnelle', 'Logistique et support quotidien.'),
           ('Science et trichologie', 'Formules et protocoles à l’examen.'),
           ('Master colorist', 'Vérifie chaque protocole sur le terrain.')],
    s11_p1='clichAIr répond en premier, par écrit, à toute heure. Notre équipe intervient les jours ouvrables, par écrit, quand une question demande une décision humaine : la personne qui vous répond est celle qui fait vraiment ce travail.',
    s11_p2='Écrivez-nous pour toute demande, technique ou commerciale.',
    s11_cta='Contactez-nous',

    s12_t='Choisissez votre accès',
    s12_p='Les particuliers naviguent et commandent sans s’inscrire. Les professionnels s’inscrivent une seule fois : gratuit, vérifié en 24 heures, sans engagement.',
    s12_links_a='Pas encore convaincu ?', s12_links_b='Lisez la page Professionnels', s12_links_c='ou', s12_links_d='ce qui change à chaque version',
)

BRANDS = [('NIKA', '/pages/nika-hair-beauty-excellence'),
          ('Code Zero', '/pages/code-zero-hair-interpreters'),
          ('Edelstein', '/pages/edelstein-hair-cosmetics-factory')]


# ---------------------------------------------------------------------------

def important(css):
    """Append !important to every declaration: the theme's .rte / .page-content rules have a higher
    specificity than our classes and would otherwise override margins, list padding, heading colours
    and link colours (verified on the live theme, 14.10.2026)."""
    def fix_block(m):
        out = []
        for d in m.group(1).split(';'):
            d = d.strip()
            if not d:
                continue
            out.append(d if '!important' in d else d + '!important')
        return '{' + ';'.join(out) + '}'
    return re.sub(r'\{([^{}]*)\}', fix_block, css)

def fr_typo(s):
    """French typography: non-breaking space before : ; ! ?"""
    return re.sub(r' ([:;!?])', ' \\1', s)


def esc(s):
    return s  # strings are authored as HTML-safe text (only &, < > would need escaping; none used)


def lnk(t, path):
    if path.startswith('#'):
        return path
    return t['prefix'] + path


def build(lang):
    t = dict(T[lang])
    if lang == 'fr':
        # apply French typography to every string value (deep)
        def fx(v):
            if isinstance(v, str):
                return fr_typo(v)
            if isinstance(v, (list, tuple)):
                return type(v)(fx(x) for x in v)
            return v
        t = {k: fx(v) for k, v in t.items()}

    L = lambda p: lnk(t, p)
    o = []
    w = o.append

    w(f'<!-- cliCHair | ABOUT US page v2 (2026-10-14). Language: {lang.upper()}. One markup for EN/IT/DE/FR; internal links carry the language prefix. Edit via API only, never from the visual editor (it strips the style block). Source and generator: clichair/about-us/build.py in the BOS repository. -->')
    w('<style>' + important(re.sub(r'\n+', '\n', CSS).strip()) + '</style>')
    w('<div class="cca">')

    # ---------------- HERO
    w('<section class="cca-hero">')
    w(f'<p class="cca-kicker">{t["kicker"]}</p>')
    a, b, c = t['h1']
    w(f'<h2 class="cca-h1"><span>{a}</span><span>{b}</span><span class="cca-outl">{c}</span></h2>')
    w(f'<p class="cca-lead">{t["hero_lead"]}</p>')
    w('<p class="cca-btns">'
      f'<a class="cca-btn cca-btn-dark" href="{L("/pages/pro-login")}">{t["btn_pro"]}</a>'
      f'<a class="cca-btn" href="{L("/collections/all")}">{t["btn_shop"]}</a>'
      f'<a class="cca-link" href="#cca-engine">{t["hero_link"]}{ARROW}</a>'
      '</p>')
    w('<ul class="cca-facts">')
    for v, k in t['facts']:
        w(f'<li><b>{v}</b><span>{k}</span></li>')
    w('</ul>')
    w('</section>')

    # ---------------- 01 THREE WORDS
    w('<section class="cca-s cca-s0" id="cca-words">')
    w(f'<p class="cca-eye"><b>01</b> {t["s1_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s1_t"]}</h2>')
    w(f'<p class="cca-lead">{t["s1_lead"]}</p>')
    w('<div class="cca-pillars">')
    for key, icon, dark, href in (('p1', 'brain', False, '#cca-engine'), ('p2', 'spark', False, '/pages/updates'), ('p3', 'scale', True, '#cca-value')):
        cls = 'cca-pillar cca-pillar-dark' if dark else 'cca-pillar'
        w(f'<div class="{cls}">')
        w(f'<div class="cca-pillar-i">{ICONS[icon]}</div>')
        w(f'<h3>{t[key+"_h"]}</h3>')
        w(f'<p class="cca-sub">{t[key+"_sub"]}</p>')
        w('<ul>' + ''.join(f'<li>{x}</li>' for x in t[key]) + '</ul>')
        w(f'<a class="cca-link" href="{L(href)}">{t[key+"_link"]}{ARROW}</a>')
        w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 02 METHOD
    w('<section class="cca-s" id="cca-method">')
    w(f'<p class="cca-eye"><b>02</b> {t["s2_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s2_t"]}</h2>')
    w('<div class="cca-steps">')
    for i, (h, p) in enumerate(t['steps'], 1):
        dark = ' cca-step-dark' if i == 4 else ''
        w(f'<div class="cca-step{dark}"><div class="cca-step-n">0{i}</div><h3>{h}</h3><p>{p}</p>')
        if i == 4:
            w(f'<p class="cca-step-loop">{LOOP}{t["loop"]}</p>')
        w('</div>')
    w('</div>')
    w(f'<p class="cca-quote"><span>{t["quote_a"]}</span> {t["quote_b"]}</p>')
    w(f'<p class="cca-btns"><a class="cca-btn cca-btn-dark" href="{L("/pages/professionals")}">{t["s2_cta"]}</a></p>')
    w('</section>')

    # ---------------- 03 ORIGIN
    w('<section class="cca-s" id="cca-origin">')
    w('<div class="cca-2col">')
    w('<div class="cca-sticky">')
    w(f'<p class="cca-eye"><b>03</b> {t["s3_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s3_t"]}</h2>')
    w('</div>')
    w('<div>')
    w(f'<p class="cca-p">{t["s3_p"]}</p>')
    w('<ul class="cca-tl">')
    for k, h, p in t['tl']:
        w(f'<li><span class="cca-tl-k">{k}</span><h3>{h}</h3><p>{p}</p></li>')
    w('</ul>')
    w(f'<p class="cca-btns cca-mt26"><a class="cca-link" href="{L("/pages/updates")}">{t["s3_link"]}{ARROW}</a></p>')
    w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 04 PLATFORM (dark panel)
    w('<section class="cca-s" id="cca-platform">')
    w('<div class="cca-panel">')
    w(f'<p class="cca-eye"><b>04</b> {t["s4_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s4_t"]}</h2>')
    w(f'<div class="cca-panel-intro"><p class="cca-p">{t["s4_p1"]}</p><p class="cca-p">{t["s4_p2"]}</p></div>')
    h0, h1, h2 = t['hub']
    w('<div class="cca-hub">')
    w(f'<div class="cca-hub-box"><h4>{h0[0]}</h4><p>{h0[1]}</p></div>')
    w('<div class="cca-hub-arrow" aria-hidden="true"></div>')
    w(f'<div class="cca-hub-box cca-hub-core"><h4>{h1[0]}</h4><p class="cca-hub-name">cliCHair</p><p>{h1[1]}</p></div>')
    w('<div class="cca-hub-arrow" aria-hidden="true"></div>')
    w(f'<div class="cca-hub-box"><h4>{h2[0]}</h4><p>{h2[1]}</p></div>')
    w('</div>')
    w(f'<p class="cca-p cca-wide cca-mb28">{t["s4_p3"]}</p>')
    w('<ul class="cca-aud">')
    for h, p, l, href in t['aud']:
        w(f'<li><h3>{h}</h3><p>{p}</p><a class="cca-link cca-link-w" href="{L(href)}">{l}{ARROW}</a></li>')
    w('</ul>')
    w('</div>')
    w('</section>')

    # ---------------- 05 PRINCIPLE
    w('<section class="cca-s" id="cca-principle">')
    w('<div class="cca-2col">')
    w('<div class="cca-sticky">')
    w(f'<p class="cca-eye"><b>05</b> {t["s5_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s5_t"]}</h2>')
    w('</div>')
    w('<div>')
    w(f'<p class="cca-lead">{t["s5_p1"]}</p>')
    w(f'<p class="cca-p">{t["s5_p2"]}</p>')
    w(f'<p class="cca-p">{t["s5_p3"]}</p>')
    w('<div class="cca-brands">')
    w(f'<span>{t["brands_label"]}</span>')
    for n, href in BRANDS:
        w(f'<a class="cca-chip" href="{L(href)}">{n}</a>')
    w(f'<a class="cca-chip cca-chip-more" href="{L("/collections")}">{t["brands_all"]}</a>')
    w('</div>')
    w(f'<p class="cca-btns"><a class="cca-link" href="{L("/pages/pro-login")}">{t["s5_link"]}{ARROW}</a></p>')
    w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 06 ENGINE
    w('<section class="cca-s" id="cca-engine">')
    w(f'<p class="cca-eye"><b>06</b> {t["s6_eye"]}</p>')
    w(f'<h2 class="cca-t"><span class="cca-brand">{t["s6_t"]}</span></h2>')
    w(f'<p class="cca-lead">{t["s6_lead"]}</p>')
    w('<div class="cca-eng">')
    for hk, lk in (('eng_a_h', 'eng_a'), ('eng_b_h', 'eng_b')):
        w(f'<div class="cca-eng-col"><h3>{t[hk]}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in t[lk]) + '</ul></div>')
    w('</div>')
    w(f'<div class="cca-valid"><h3>{t["valid_h"]}</h3><div><p>{t["valid_p1"]}</p><p>{t["valid_p2"]}</p></div></div>')
    w(f'<p class="cca-badge-note"><span class="cca-badge" aria-hidden="true">AIr</span><span>{t["badge_note"]}</span></p>')
    w('</section>')

    # ---------------- 07 TOOLS
    w('<section class="cca-s" id="cca-tools">')
    w(f'<p class="cca-eye"><b>07</b> {t["s7_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s7_t"]}</h2>')
    w(f'<p class="cca-lead">{t["s7_lead"]}</p>')
    w('<div class="cca-tools">')
    for icon, h, p, pro, ltxt, lhref in t['tools']:
        tag = f'<span class="cca-tag cca-tag-pro">{t["tag_pro"]}</span>' if pro else f'<span class="cca-tag">{t["tag_all"]}</span>'
        w(f'<div class="cca-tool"><div class="cca-tool-top"><div class="cca-tool-i">{ICONS[icon]}</div>{tag}</div><h3>{h}</h3><p>{p}</p>')
        if ltxt:
            w(f'<a class="cca-link" href="{L(lhref)}">{ltxt}{ARROW}</a>')
        w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 08 VALUE
    w('<section class="cca-s" id="cca-value">')
    w('<div class="cca-2col">')
    w('<div class="cca-sticky">')
    w(f'<p class="cca-eye"><b>08</b> {t["s8_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s8_t"]}</h2>')
    w('</div>')
    w('<div>')
    w(f'<p class="cca-p">{t["s8_p1"]}</p>')
    w(f'<p class="cca-p">{t["s8_p2"]}</p>')
    w(f'<p class="cca-p cca-mb26">{t["s8_p3"]}</p>')
    w(f'<p class="cca-btns"><a class="cca-btn cca-btn-dark" href="{L("/pages/pro-login")}">{t["s8_cta"]}</a></p>')
    w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 09 EDUCATION
    w('<section class="cca-s" id="cca-education">')
    w('<div class="cca-2col">')
    w('<div class="cca-sticky">')
    w(f'<p class="cca-eye"><b>09</b> {t["s9_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s9_t"]}</h2>')
    w('</div>')
    w('<div>')
    w(f'<p class="cca-p">{t["s9_p1"]}</p>')
    w(f'<p class="cca-p cca-mb26">{t["s9_p2"]}</p>')
    w(f'<p class="cca-btns"><a class="cca-link" href="{L("/pages/contact")}">{t["s9_link"]}{ARROW}</a></p>')
    w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 10 ETHICS
    w('<section class="cca-s" id="cca-ethics">')
    w(f'<p class="cca-eye"><b>10</b> {t["s10_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s10_t"]}</h2>')
    w('<ul class="cca-eco">')
    for icon, h, p in t['eco']:
        w(f'<li><div class="cca-eco-i">{ICONS[icon]}</div><h3>{h}</h3><p>{p}</p></li>')
    w('</ul>')
    w(f'<p class="cca-p cca-mb26">{t["s10_p"]}</p>')
    w(f'<p class="cca-btns"><a class="cca-link" href="{L("/pages/sustainability")}">{t["s10_link"]}{ARROW}</a></p>')
    w('</section>')

    # ---------------- 11 TEAM
    w('<section class="cca-s" id="cca-team">')
    w('<div class="cca-2col">')
    w('<div class="cca-sticky">')
    w(f'<p class="cca-eye"><b>11</b> {t["s11_eye"]}</p>')
    w(f'<h2 class="cca-t">{t["s11_t"]}</h2>')
    w('</div>')
    w('<div>')
    w('<ul class="cca-roles">')
    for b, s in t['roles']:
        w(f'<li><b>{b}</b><span>{s}</span></li>')
    w('</ul>')
    w(f'<p class="cca-p">{t["s11_p1"]}</p>')
    w(f'<p class="cca-p cca-mb26">{t["s11_p2"]}</p>')
    w(f'<p class="cca-btns"><a class="cca-btn cca-btn-dark" href="{L("/pages/contact")}">{t["s11_cta"]}</a></p>')
    w('</div>')
    w('</div>')
    w('</section>')

    # ---------------- 12 FINAL
    w('<section class="cca-s cca-s-last" id="cca-access">')
    w('<div class="cca-final">')
    w('<div>')
    w(f'<h2 class="cca-t">{t["s12_t"]}</h2>')
    w(f'<p class="cca-p">{t["s12_p"]}</p>')
    w(f'<p class="cca-final-links">{t["s12_links_a"]} <a href="{L("/pages/professionals")}">{t["s12_links_b"]}</a> {t["s12_links_c"]} <a href="{L("/pages/updates")}">{t["s12_links_d"]}</a>.</p>')
    w('</div>')
    w('<p class="cca-btns">'
      f'<a class="cca-btn cca-btn-light" href="{L("/pages/pro-login")}">{t["btn_pro"]}</a>'
      f'<a class="cca-btn cca-btn-ghost" href="{L("/collections/all")}">{t["btn_shop"]}</a>'
      '</p>')
    w('</div>')
    w('</section>')

    w('</div>')
    w('<!-- LINK ROUTING: /pages/professionals when the reader still needs convincing; /pages/pro-login for action CTAs (register or log in); /collections/all for private visitors; /pages/updates for the public release list; /pages/retailers and /pages/collaborations for the online-shop programme and partnerships. The "up to +20% margin" claim stays off this page (it belongs on /pages/professionals). -->')
    return '\n'.join(o) + '\n'


SHELL = """<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | cliCHair preview</title>
<style>
html{{font-size:16px}}
body{{margin:0;font-family:Inter,"Inter Display",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;color:#1a1a1a;background:#fff;font-size:14px;line-height:1.5}}
.shell-h{{display:flex;align-items:center;justify-content:space-between;height:64px;padding:0 40px;border-bottom:1px solid #eee;font-weight:800;letter-spacing:-.03em}}
.shell-h span{{font-size:12px;font-weight:500;color:#888;letter-spacing:0}}
.shell-w{{max-width:752px;margin:0 auto;padding:48px 40px 24px}}
/* theme rules that clashed with the page (copied from base.css / page-content block) */
body{{--color:#1a1a1a}}
h1,h2,h3,h4{{color:var(--color);font-family:inherit}}
h2{{font-size:32px;line-height:1.1}} h3{{font-size:24px;line-height:1}} h4{{font-size:20px}}
.rte :is(h1,h2,h3,h4,h5,h6){{margin-block:clamp(1.5rem,1em * 3.3,2.5rem) .25em}}
.rte ul,.rte ol{{margin-block-start:0;padding-inline-start:1.5em}}
.rte :is(ul,ol):not(:is(ul,ol) :is(ul,ol)){{margin-block-end:1em}}
a{{color:currentcolor;text-decoration-color:transparent}}
.page-content a{{color:currentcolor}}
p:not(.h1) a:where(:not(.button)){{text-decoration-color:currentcolor}}
:is(h1,h2,h3,h4,h5,h6,p) > a:hover{{color:rgb(26 26 26 / .7)}}
.shell-t{{text-align:right;font-size:1.25rem;text-transform:uppercase;font-weight:900;margin:0 0 24px}}
.shell-d{{height:1px;background:#1a1a1a;margin:0 0 25px}}
.shell-f{{border-top:1px solid #eee;padding:28px 40px;color:#888;font-size:12px;display:flex;justify-content:space-between}}
@media (max-width:640px){{.shell-h,.shell-f{{padding-left:16px;padding-right:16px}}.shell-w{{padding:28px 16px 16px}}}}
</style></head><body>
<div class="shell-h">cliCHair <span>preview shell (not the real theme)</span></div>
<div class="shell-w"><h1 class="shell-t">{title}</h1><div class="shell-d"></div>
<div class="page-content rte"><rte-formatter>
{body}
</rte-formatter></div>
</div>
<div class="shell-f"><span>cliCHair is a Brand of ÜLTIMA hair concept Sàrl</span><span>v3 r4.3.0.05</span></div>
</body></html>"""

TITLES = {'en': 'About us', 'it': 'Chi siamo', 'de': 'Über uns', 'fr': 'À propos'}


def checks(lang, body):
    bad = []
    if '—' in body or '–' in body:
        bad.append('em/en dash found')
    low = body.lower()
    for word in ('cruelty', 'exclusive', 'guaranteed', 'infallible', 'certified', 'esclusiv', 'garantit', 'garanti ', 'exklusiv', 'exclusif'):
        if word in low:
            bad.append('forbidden word: ' + word)
    if lang == 'de' and 'ß' in body:
        bad.append('ß found (use ss)')
    if lang != 'en':
        # every internal link must carry the prefix
        for m in re.finditer(r'href="(/[^"]*)"', body):
            if not m.group(1).startswith(T[lang]['prefix'] + '/'):
                bad.append('unprefixed link ' + m.group(1))
    else:
        for m in re.finditer(r'href="(/(it|de|fr)/[^"]*)"', body):
            bad.append('prefixed link in EN ' + m.group(1))
    if 'CLICHAIR' in body or 'CLICHAIR' in body.upper() and 'cliCHair' not in body:
        bad.append('brand spelling')
    # brand spellings must only appear in canonical form
    visible = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    for m in re.finditer(r'\bclich?air\b', visible, flags=re.I):
        if m.group(0) not in ('cliCHair', 'clichAIr'):
            bad.append('non-canonical brand spelling: ' + m.group(0))
    return bad


def main():
    os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
    os.makedirs(os.path.join(HERE, 'preview'), exist_ok=True)
    ok = True
    for lang in ('en', 'it', 'de', 'fr'):
        body = build(lang)
        problems = checks(lang, body)
        if problems:
            ok = False
            print(lang, 'PROBLEMS:', problems)
        with open(os.path.join(HERE, 'dist', f'about-us.{lang}.html'), 'w', encoding='utf-8') as f:
            f.write(body)
        with open(os.path.join(HERE, 'preview', f'about-us.{lang}.html'), 'w', encoding='utf-8') as f:
            f.write(SHELL.format(lang=lang, title=TITLES[lang], body=body))
        print(f'{lang}: {len(body):,} chars, {body.count("<section"):d} sections, {body.count("<a "):d} links')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
