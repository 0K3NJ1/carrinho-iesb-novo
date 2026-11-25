// Motor de cenas determinístico: desenhar(i, p, k) monta o quadro do bloco i,
// com a transição no ponto p (0..1) e a legenda da frase k. Sem relógio, sem aleatoriedade.
'use strict';

const COR = {
  fundo: '#0B1120', painel: '#111827', painel2: '#1E293B', texto: '#F8FAFC', suave: '#94A3B8',
  destaque: '#38BDF8', proc: '#A78BFA', caminho: '#22C55E', alerta: '#F59E0B', erro: '#EF4444',
  no: '#334155', aresta: '#334155',
};
const ESTADO_COR = {
  normal: COR.no, fronteira: COR.proc, expandido: '#1d6f97', atual: COR.alerta,
  caminho: COR.caminho, descartado: COR.erro, destaque: COR.destaque, origem: COR.destaque, destino: COR.caminho,
};

let TL = null, DADOS = null;
window.iniciar = function (timeline, dados) { TL = timeline; DADOS = dados; return true; };

// ---------- utilidades ----------
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const lerp = (a, b, t) => a + (b - a) * t;
function hex(c) { return [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16)); }
function mistura(a, b, t) {
  if (a === b) return a;
  const x = hex(a), y = hex(b);
  return '#' + x.map((v, i) => Math.round(lerp(v, y[i], t)).toString(16).padStart(2, '0')).join('');
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
// `código` vira <code>; **negrito**; o resto é escapado.
function rico(s) {
  return esc(s).replace(/`([^`]+)`/g, '<code>$1</code>').replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>').replace(/&lt;br&gt;/g, '<br>');
}
function mesmaCena(a, b) { return a && b && a.cena === b.cena; }

// ---------- componentes ----------
function cTitulo(v, ant, p) {
  const y = lerp(40, 0, p), o = p;
  return `<div class="titulo-cena" style="opacity:${o};transform:translateY(${y}px)">
    ${v.rotulo ? `<div class="rotulo">${rico(v.rotulo)}</div>` : ''}
    <h1>${rico(v.titulo)}</h1>
    ${v.subtitulo ? `<div class="subtitulo">${rico(v.subtitulo)}</div>` : ''}
    <div class="linha"></div></div>`;
}

function cTopicos(v, ant, p, caixa) {
  const antMostrar = mesmaCena(v, ant) ? (ant.mostrar ?? ant.itens.length) : 0;
  const mostrar = v.mostrar ?? v.itens.length;
  const lis = v.itens.slice(0, mostrar).map((t, i) => {
    const novo = i >= antMostrar;
    const o = novo ? p : 1, dx = novo ? lerp(-30, 0, p) : 0;
    const ativo = v.ativo === i || (v.ativo == null && i === mostrar - 1 && v.realce !== false);
    return `<li class="${ativo ? 'ativo' : ''}" style="opacity:${o};transform:translateX(${dx}px)">${rico(t)}</li>`;
  }).join('');
  const fs = v.fonte ? `style="font-size:${v.fonte}px"` : '';
  return `<div class="topicos" ${caixa ? '' : ''}><h2>${rico(v.titulo || '')}</h2><ul class="itens" ${fs}>${lis}</ul></div>`;
}

function painel(x, y, w, h, titulo, corpo, extra = '') {
  return `<div class="painel" style="left:${x}px;top:${y}px;width:${w}px;height:${h}px;${extra}">
    <div class="painel-titulo"><span class="bolinhas"><i style="background:#ef4444"></i><i style="background:#f59e0b"></i><i style="background:#22c55e"></i></span>${titulo}</div>${corpo}</div>`;
}

function janelaCodigo(v, total, visiveis) {
  if (v.janela) {
    let ini = v.janela[0];
    if (v.linhas && v.linhas[1] > ini + visiveis - 1) ini = Math.max(1, Math.min(v.linhas[0], v.linhas[1] - visiveis + 1));
    return [ini, ini + visiveis - 1];
  }
  const [a, b] = v.linhas || [1, 1];
  let ini = Math.max(1, Math.round((a + b) / 2 - visiveis / 2));
  ini = Math.min(ini, Math.max(1, total - visiveis + 1));
  if (a < ini) ini = a;
  return [ini, ini + visiveis - 1];
}

function cCodigo(v, ant, p, caixa) {
  const LH = 38, TOPO = 14;
  const cel = v.livre ? { titulo: v.titulo || 'exemplo.py', linhas: v.livre } : DADOS.codigo[String(v.celula)];
  const visiveis = Math.floor((caixa.h - 56 - TOPO - 8) / LH);
  const total = cel.linhas.length;
  const jan = janelaCodigo(v, total, visiveis);
  const temAnt = mesmaCena(v, ant) && ant.tipo === 'codigo';
  const janAnt = temAnt ? janelaCodigo(ant, total, visiveis) : jan;
  const ini = lerp(janAnt[0], jan[0], ease(p));
  const [ha, hb] = v.linhas || [0, -1];
  const [aa, ab] = temAnt && ant.linhas ? ant.linhas : [ha, hb];
  const fa = lerp(aa, ha, ease(p)), fb = lerp(ab, hb, ease(p));
  let linhas = '';
  // parado: só linhas inteiras; rolando: uma linha extra entra pela borda
  const parado = Math.abs(ini - Math.round(ini)) < 1e-6;
  const de = Math.max(1, Math.floor(ini)), ate = Math.min(total, parado ? Math.round(ini) + visiveis - 1 : Math.ceil(ini) + visiveis);
  for (let n = de; n <= ate; n++) {
    const on = n >= ha && n <= hb;
    const y = (n - ini) * LH;
    const o = parado ? 1 : Math.max(0, Math.min(1, 1 - Math.max(-y, y - (visiveis - 1) * LH) / LH));
    linhas += `<div class="cl ${on ? 'on' : ''}" style="position:absolute;top:${y}px;left:0;right:0;opacity:${o}"><span class="ln">${n}</span><span class="tx">${cel.linhas[n - 1] || ' '}</span></div>`;
  }
  const faixa = v.linhas ? `<div class="faixa" style="top:${TOPO + (fa - ini) * LH}px;height:${(fb - fa + 1) * LH}px;opacity:${temAnt ? 1 : p}"></div>` : '';
  let notas = '';
  for (const nt of v.notas || []) {
    const novo = !(temAnt && (ant.notas || []).some(o => o.texto === nt.texto));
    notas += `<div class="nota" style="top:${TOPO + (nt.linha - jan[0]) * LH - 4}px;opacity:${novo ? p : 1}">${rico(nt.texto)}</div>`;
  }
  const titulo = v.livre ? `<b>${esc(cel.titulo)}</b> <span style="opacity:.7">— exemplo (não é do projeto)</span>`
    : `<b>${esc(cel.titulo)}</b> <span style="opacity:.7">· célula de código ${v.rotulo_celula || ''}</span>`;
  const corpo = `<div class="codigo-corpo">${faixa}<div class="codigo-rolo">${linhas}</div>${notas}</div>`;
  return painel(caixa.x, caixa.y, caixa.w, caixa.h, titulo, corpo);
}

function cTabela(v, ant, p, caixa) {
  const antN = mesmaCena(v, ant) ? ant.linhas.length : 0;
  const th = v.colunas.map(c => `<th>${rico(c)}</th>`).join('');
  const trs = v.linhas.map((l, i) => {
    const cls = (v.estilos && v.estilos[i]) || ((v.destaque || []).includes(i) ? 'dest' : '');
    const o = i >= antN ? p : 1;
    return `<tr class="${cls}" style="opacity:${o}">${l.map(c => `<td>${rico(String(c))}</td>`).join('')}</tr>`;
  }).join('');
  const fs = v.fonte ? `style="font-size:${v.fonte}px"` : '';
  const corpo = `<div class="tabela-wrap"><table class="tab" ${fs}><thead><tr>${th}</tr></thead><tbody>${trs}</tbody></table>
    ${v.rodape ? `<div style="font-size:26px;color:#CBD5E1;margin-top:14px;line-height:1.4">${rico(v.rodape)}</div>` : ''}</div>`;
  return painel(caixa.x, caixa.y, caixa.w, caixa.h, `<b>${rico(v.titulo || '')}</b>`, corpo);
}

function cCartoes(v, ant, p, caixa) {
  const antK = mesmaCena(v, ant) ? Object.fromEntries(ant.itens.map(c => [c[0], c[1]])) : {};
  const cs = v.itens.map(([k, val, est]) => {
    const mudou = antK[k] !== val;
    const o = (k in antK) ? 1 : p;
    const brilho = mudou && (k in antK) ? `box-shadow:0 0 0 ${lerp(6, 0, p)}px rgba(245,158,11,.5)` : '';
    return `<div class="cartao ${est || ''}" style="opacity:${o};${brilho}"><div class="k">${esc(k)}</div><div class="v">${rico(String(val))}</div></div>`;
  }).join('');
  return painel(caixa.x, caixa.y, caixa.w, caixa.h, `<b>${rico(v.titulo || 'Variáveis')}</b>`, `<div class="cartoes">${cs}</div>`);
}

function cFormula(v, ant, p) {
  const partes = v.partes.map((pt, i) => {
    const cor = pt.cor ? (COR[pt.cor] || pt.cor) : COR.texto;
    const o = (v.realce == null || v.realce.includes(i)) ? 1 : .28;
    return `<span style="color:${cor};opacity:${o}">${esc(pt.t)}</span>`;
  }).join('');
  const antN = mesmaCena(v, ant) ? (ant.linhas || []).length : 0;
  const linhas = (v.linhas || []).map((l, i) => `<div style="opacity:${i >= antN ? p : 1}">${rico(l)}</div>`).join('');
  // fonte menor para fórmulas longas, sempre numa linha só
  const chars = v.partes.reduce((s, pt) => s + pt.t.length, 0) + v.partes.length;
  const tam = Math.min(92, Math.floor(1700 / (chars * 0.62)));
  return `<div class="formula" style="opacity:${mesmaCena(v, ant) ? 1 : p}">${v.titulo ? `<h2>${rico(v.titulo)}</h2>` : ''}
    <div class="formula-exp" style="font-size:${tam}px;gap:${Math.round(tam * .3)}px;white-space:nowrap">${partes}</div><div class="formula-linhas">${linhas}</div></div>`;
}

function cTransformacao(v, ant, p) {
  const antN = mesmaCena(v, ant) ? (ant.mostrar ?? ant.etapas.length) : 0;
  const n = v.mostrar ?? v.etapas.length;
  const els = v.etapas.slice(0, n).map((e, i) => {
    const o = i >= antN ? p : 1, dy = i >= antN ? lerp(24, 0, p) : 0;
    const st = `style="opacity:${o};transform:translateY(${dy}px)"`;
    if (e.op) return `<div class="op-caixa" ${st}><span>${esc(e.op)}</span><span class="seta">→</span></div>`;
    return `<div class="valor ${i === n - 1 ? 'ult' : ''}" ${st}>${esc(e.valor)}</div>`;
  }).join('');
  return `<div class="transf"><h2>${rico(v.titulo || '')}</h2><div class="transf-linha">${els}</div>
    ${v.nota ? `<div class="transf-nota">${rico(v.nota)}</div>` : ''}</div>`;
}

function cTerminal(v, ant, p, caixa) {
  const antN = mesmaCena(v, ant) ? ant.texto.length : 0;
  const ls = v.texto.map((l, i) => {
    const est = (v.estilos && v.estilos[i]) || ((v.destaque || []).includes(i) ? 'dest' : '');
    return `<div class="tl ${est}" style="opacity:${i >= antN ? p : 1}">${esc(l) || ' '}</div>`;
  }).join('');
  const fs = v.fonte ? `font-size:${v.fonte}px;` : '';
  return painel(caixa.x, caixa.y, caixa.w, caixa.h, `<b>${esc(v.titulo || 'Saída')}</b>`, `<div class="term-corpo" style="${fs}">${ls}</div>`);
}

function cPergunta(v, ant, p) {
  const antN = mesmaCena(v, ant) ? (ant.mostrar ?? ant.resposta.length) : 0;
  const n = v.mostrar ?? v.resposta.length;
  const lis = v.resposta.slice(0, n).map((r, i) => `<li style="opacity:${i >= antN ? p : 1}">${rico(r)}</li>`).join('');
  const o = mesmaCena(v, ant) ? 1 : p;
  return `<div class="pergunta" style="opacity:${o}"><div class="num">${esc(v.numero)}</div><h2>${rico(v.pergunta)}</h2><ul class="resposta">${lis}</ul></div>`;
}

function cImagem(v, ant, p, caixa) {
  return painel(caixa.x, caixa.y, caixa.w, caixa.h, `<b>${rico(v.titulo || '')}</b>`,
    `<div class="imagem"><img src="${v.src}"></div>`, `opacity:${mesmaCena(v, ant) ? 1 : p}`);
}

// ---------- fluxo (caixas e setas) ----------
function cFluxo(v, ant, p, caixa) {
  const W = caixa.w, H = caixa.h;
  const ativosAnt = mesmaCena(v, ant) ? (ant.ativo || []) : [];
  const pos = Object.fromEntries(v.nos.map(n => [n.id, n]));
  let svg = `<svg class="fluxo-svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <defs><marker id="ponta" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="#64748B"/></marker>
    <marker id="pontaA" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M0,0 L12,6 L0,12 z" fill="${COR.alerta}"/></marker></defs>`;
  for (const [a, b, rot, ativa] of v.setas || []) {
    const A = pos[a], B = pos[b];
    const ax = A.x + (A.w || 260) / 2, ay = A.y + (A.h || 90) / 2, bx = B.x + (B.w || 260) / 2, by = B.y + (B.h || 90) / 2;
    // recorta a seta na borda das caixas
    const corte = (cx, cy, w, h, dx, dy) => { const t = Math.min(Math.abs((w / 2) / (dx || 1e-9)), Math.abs((h / 2) / (dy || 1e-9))); return [cx + dx * t, cy + dy * t]; };
    const [x1, y1] = corte(ax, ay, (A.w || 260) + 8, (A.h || 90) + 8, bx - ax, by - ay);
    const [x2, y2] = corte(bx, by, (B.w || 260) + 18, (B.h || 90) + 18, ax - bx, ay - by);
    const cor = ativa ? COR.alerta : '#64748B';
    svg += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${cor}" stroke-width="${ativa ? 5 : 3}" marker-end="url(#${ativa ? 'pontaA' : 'ponta'})"/>`;
    if (rot) {
      const ls = String(rot).split('\n'), mx = (x1 + x2) / 2, my = (y1 + y2) / 2;
      const y0 = Math.abs(y2 - y1) < 20 ? my - 18 - (ls.length - 1) * 26 : my - (ls.length - 1) * 13;
      const dx = Math.abs(y2 - y1) < 20 ? 0 : 16;
      ls.forEach((l, i) => { svg += `<text x="${mx + dx}" y="${y0 + i * 26}" fill="${ativa ? COR.alerta : COR.suave}" font-size="21" text-anchor="${dx ? 'start' : 'middle'}">${esc(l)}</text>`; });
    }
  }
  for (const n of v.nos) {
    const ativo = (v.ativo || []).includes(n.id), antes = ativosAnt.includes(n.id);
    const t = ativo === antes ? (ativo ? 1 : 0) : (ativo ? p : 1 - p);
    const w = n.w || 260, h = n.h || 90;
    const borda = mistura('#334155', n.cor ? (COR[n.cor] || n.cor) : COR.destaque, t);
    const fundo = mistura('#111827', '#14324a', t);
    svg += `<rect x="${n.x}" y="${n.y}" width="${w}" height="${h}" rx="16" fill="${fundo}" stroke="${borda}" stroke-width="${lerp(2, 5, t)}"/>`;
    const linhas = String(n.texto).split('\n');
    linhas.forEach((l, i) => {
      const mono = l.startsWith('`');
      const txt = l.replace(/`/g, '');
      svg += `<text x="${n.x + w / 2}" y="${n.y + h / 2 + (i - (linhas.length - 1) / 2) * 30 + 9}" fill="${i === 0 ? COR.texto : COR.suave}" font-size="${i === 0 ? 26 : 21}" font-weight="${i === 0 ? 600 : 400}" text-anchor="middle" ${mono ? 'font-family="Cascadia Code, Consolas, monospace"' : ''}>${esc(txt)}</text>`;
    });
  }
  svg += '</svg>';
  const titulo = v.titulo ? `<div style="position:absolute;left:0;top:-4px;font-size:34px;font-weight:700">${rico(v.titulo)}</div>` : '';
  const desce = v.titulo ? 'transform:translateY(56px);' : '';   // o título não cobre a primeira linha de caixas
  return `<div style="position:absolute;left:${caixa.x}px;top:${caixa.y}px;width:${W}px;height:${H}px;opacity:${mesmaCena(v, ant) ? 1 : p}">${titulo}<div style="${desce}">${svg}</div></div>`;
}

// ---------- grafo do campus ----------
function posCaminho(caminho, frac) {
  const L = DADOS.layout;
  const pts = caminho.map(n => [L[n].x, L[n].y]);
  const segs = []; let total = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push(d); total += d; }
  let alvo = frac * total;
  for (let i = 0; i < segs.length; i++) {
    if (alvo <= segs[i] || i === segs.length - 1) {
      const t = segs[i] ? Math.min(1, alvo / segs[i]) : 0;
      const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
      return [lerp(x1, x2, t), lerp(y1, y2, t), Math.atan2(y2 - y1, x2 - x1) * 180 / Math.PI];
    }
    alvo -= segs[i];
  }
  return [pts[0][0], pts[0][1], 0];
}

function cGrafo(v, ant, p, caixa) {
  const L = DADOS.layout;
  const temAnt = mesmaCena(v, ant) && ant.tipo === 'grafo';
  const cam0 = temAnt ? ant.camera : v.camera, cam = v.camera || [0, 0, 1600, 900];
  const c0 = cam0 || cam;
  const e = ease(p);
  const [cx, cy, cw, ch] = cam.map((x, i) => lerp(c0[i], x, temAnt ? e : 1));
  const escala = cw / 1600;                      // tamanho visual constante na tela
  const R = (v.raio || 15) * escala * (v.zoomTexto || 1);
  const fs = (v.fonteRotulo || 20) * escala * (v.zoomTexto || 1);
  const vis = n => L[n].x >= cx - 80 * escala && L[n].x <= cx + cw + 80 * escala && L[n].y >= cy - 80 * escala && L[n].y <= cy + ch + 80 * escala;
  const estados = v.estados || {}, estAnt = temAnt ? (ant.estados || {}) : estados;
  const corNo = n => mistura(ESTADO_COR[estAnt[n] || 'normal'], ESTADO_COR[estados[n] || 'normal'], temAnt ? p : 1);
  const caminho = v.caminho || [];
  const naRota = new Set(); for (let i = 1; i < caminho.length; i++) { naRota.add(caminho[i - 1] + '|' + caminho[i]); naRota.add(caminho[i] + '|' + caminho[i - 1]); }
  const destA = new Set((v.arestas || []).map(([a, b]) => a + '|' + b).concat((v.arestas || []).map(([a, b]) => b + '|' + a)));
  const descA = new Set((v.arestasDescartadas || []).flatMap(([a, b]) => [a + '|' + b, b + '|' + a]));
  const W = caixa.w, H = caixa.h;
  let s = `<svg width="${W}" height="${H}" viewBox="${cx} ${cy} ${cw} ${ch}" preserveAspectRatio="xMidYMid meet">`;
  const pesos = v.pesos ? (v.pesosValores || null) : null;
  for (const [a, b, m] of DADOS.ligacoes) {
    if (!vis(a) && !vis(b)) continue;
    const A = L[a], B = L[b];
    const k = a + '|' + b;
    let cor = COR.aresta, w = 4 * escala;
    if (descA.has(k)) { cor = COR.erro; w = 6 * escala; }
    if (destA.has(k)) { cor = COR.proc; w = 6 * escala; }
    if (naRota.has(k)) { cor = COR.caminho; w = 9 * escala; }
    s += `<line x1="${A.x}" y1="${A.y}" x2="${B.x}" y2="${B.y}" stroke="${cor}" stroke-width="${w}" stroke-linecap="round"/>`;
    if (v.pesos && vis(a) && vis(b)) {
      const val = pesos ? (pesos[k] ?? pesos[b + '|' + a]) : m;
      if (val !== undefined) {
        const mx = (A.x + B.x) / 2, my = (A.y + B.y) / 2;
        const txt = String(val).replace('.', ',') + (v.unidadePeso || '');
        const tw = txt.length * fs * .58 + 10 * escala;
        s += `<rect x="${mx - tw / 2}" y="${my - fs * .75}" width="${tw}" height="${fs * 1.3}" rx="${6 * escala}" fill="#0B1120" stroke="${naRota.has(k) ? COR.caminho : '#475569'}" stroke-width="${2 * escala}"/>`;
        s += `<text x="${mx}" y="${my + fs * .32}" fill="${naRota.has(k) ? '#BBF7D0' : '#E2E8F0'}" font-size="${fs * .9}" text-anchor="middle" font-family="Cascadia Code, Consolas, monospace">${esc(txt)}</text>`;
      }
    }
  }
  const rotulos = v.rotulos === 'todos' ? null : new Set(v.rotulos || []);
  for (const n of Object.keys(L)) {
    if (!vis(n)) continue;
    const P = L[n], est = estados[n] || 'normal';
    const r = R * (est === 'atual' ? 1.35 : 1);
    if (est !== 'normal') s += `<circle cx="${P.x}" cy="${P.y}" r="${r * 1.7}" fill="${corNo(n)}" opacity=".22"/>`;
    s += `<circle cx="${P.x}" cy="${P.y}" r="${r}" fill="${corNo(n)}" stroke="#0B1120" stroke-width="${3 * escala}"/>`;
    if (!rotulos || rotulos.has(n)) {
      const forte = est !== 'normal';
      let tx = P.x, ty = P.y - r - 8 * escala, anc = 'middle';
      if (P.lado === 'dir') { tx = P.x + r + 8 * escala; ty = P.y + fs * .35; anc = 'start'; }
      if (P.lado === 'esq') { tx = P.x - r - 8 * escala; ty = P.y + fs * .35; anc = 'end'; }
      s += `<text x="${tx}" y="${ty}" fill="${forte ? '#F8FAFC' : '#94A3B8'}" font-size="${fs}" font-weight="${forte ? 700 : 500}" text-anchor="${anc}" paint-order="stroke" stroke="#0B1120" stroke-width="${5 * escala}">${esc(v.nomesCompletos ? n : P.rotulo)}</text>`;
    }
  }
  // selos de valores (g, h, f) ao lado dos nós
  for (const [n, txt] of Object.entries(v.valores || {})) {
    const P = L[n]; if (!P) continue;
    const novo = !(temAnt && ant.valores && ant.valores[n] === txt);
    const linhas = String(txt).split('\n');
    const tw = Math.max(...linhas.map(l => l.length)) * fs * .56 + 18 * escala, th = linhas.length * fs * 1.15 + 12 * escala;
    const dx = (v.ladoValores && v.ladoValores[n] === 'esq') ? -tw - R - 8 * escala : R + 8 * escala;
    s += `<g opacity="${novo ? p : 1}"><rect x="${P.x + dx}" y="${P.y - th / 2}" width="${tw}" height="${th}" rx="${8 * escala}" fill="#1E293B" stroke="${COR.proc}" stroke-width="${2 * escala}"/>`;
    linhas.forEach((l, i) => { s += `<text x="${P.x + dx + 9 * escala}" y="${P.y - th / 2 + 6 * escala + (i + .85) * fs * 1.15}" fill="#E9D5FF" font-size="${fs * .95}" font-family="Cascadia Code, Consolas, monospace">${esc(l)}</text>`; });
    s += '</g>';
  }
  // carrinho percorrendo o caminho
  if (v.carrinho) {
    const frac = v.carrinho.parado !== undefined ? v.carrinho.parado : ease(p);
    const [x, y, ang] = posCaminho(v.carrinho.caminho, frac);
    const k = 1.5 * escala * (v.zoomTexto || 1);
    s += `<g transform="translate(${x},${y}) rotate(${ang}) scale(${k})">
      <rect x="-26" y="-16" width="52" height="32" rx="9" fill="${COR.alerta}" stroke="#0B1120" stroke-width="3"/>
      <rect x="2" y="-11" width="16" height="22" rx="4" fill="#0B1120" opacity=".55"/>
      <circle cx="-15" cy="-18" r="6" fill="#0B1120"/><circle cx="15" cy="-18" r="6" fill="#0B1120"/>
      <circle cx="-15" cy="18" r="6" fill="#0B1120"/><circle cx="15" cy="18" r="6" fill="#0B1120"/></g>`;
  }
  s += '</svg>';
  let leg = '';
  if (v.legendaCores) {
    const itens = v.legendaCores.map(e => `<span style="display:inline-flex;align-items:center;gap:8px;margin-right:22px"><i style="width:18px;height:18px;border-radius:50%;background:${ESTADO_COR[e[0]]};display:inline-block"></i>${esc(e[1])}</span>`).join('');
    leg = `<div style="position:absolute;left:20px;bottom:14px;font-size:22px;color:#CBD5E1">${itens}</div>`;
  }
  const tit = v.titulo ? `<div style="position:absolute;left:20px;top:14px;font-size:28px;font-weight:700">${rico(v.titulo)}</div>` : '';
  return `<div class="painel" style="left:${caixa.x}px;top:${caixa.y}px;width:${W}px;height:${H}px;background:#0d1526;opacity:${temAnt ? 1 : p}">${s}${tit}${leg}</div>`;
}

// ---------- composição ----------
const COMP = { titulo: cTitulo, topicos: cTopicos, codigo: cCodigo, tabela: cTabela, cartoes: cCartoes, formula: cFormula,
  transformacao: cTransformacao, terminal: cTerminal, pergunta: cPergunta, imagem: cImagem, fluxo: cFluxo, grafo: cGrafo };

function montar(v, ant, p, caixa) {
  if (v.tipo === 'dividido') {
    const r = v.proporcao || .56, gap = 28;
    const w1 = Math.round((caixa.w - gap) * r), w2 = caixa.w - gap - w1;
    const a1 = ant && ant.tipo === 'dividido' ? ant.esquerda : null, a2 = ant && ant.tipo === 'dividido' ? ant.direita : null;
    return montar(v.esquerda, a1, p, { x: caixa.x, y: caixa.y, w: w1, h: caixa.h }) +
      montar(v.direita, a2, p, { x: caixa.x + w1 + gap, y: caixa.y, w: w2, h: caixa.h });
  }
  if (v.tipo === 'vertical') {
    const r = v.proporcao || .5, gap = 24;
    const h1 = Math.round((caixa.h - gap) * r), h2 = caixa.h - gap - h1;
    const a1 = ant && ant.tipo === 'vertical' ? ant.cima : null, a2 = ant && ant.tipo === 'vertical' ? ant.baixo : null;
    return montar(v.cima, a1, p, { x: caixa.x, y: caixa.y, w: caixa.w, h: h1 }) +
      montar(v.baixo, a2, p, { x: caixa.x, y: caixa.y + h1 + gap, w: caixa.w, h: h2 });
  }
  const f = COMP[v.tipo];
  if (!f) return `<div style="color:red">componente desconhecido: ${v.tipo}</div>`;
  const html = f(v, ant && mesmaCena(v, ant) ? ant : null, p, caixa);
  if (['titulo', 'topicos', 'formula', 'transformacao', 'pergunta'].includes(v.tipo)) {
    return `<div style="position:absolute;left:${caixa.x}px;top:${caixa.y}px;width:${caixa.w}px;height:${caixa.h}px">${html}</div>`;
  }
  return html;
}

window.desenhar = function (i, p, k) {
  const b = TL.blocos[i], ant = i > 0 ? TL.blocos[i - 1] : null;
  const caixa = { x: 0, y: 0, w: 1824, h: 806 };
  const ep = Math.max(0, Math.min(1, p));
  const area = document.getElementById('area');
  const mesma = ant && ant.visual.cena === b.visual.cena;
  if (mesma || !ant) {
    area.innerHTML = `<div class="camada">${montar(b.visual, mesma ? ant.visual : null, ep, caixa)}</div>`;
  } else {
    // troca de cena: a anterior some enquanto a nova aparece
    const q = ease(ep);
    area.innerHTML = `<div class="camada" style="opacity:${1 - Math.min(1, q * 1.6)}">${montar(ant.visual, null, 1, caixa)}</div>
      <div class="camada" style="opacity:${Math.max(0, (q - .25) / .75)}">${montar(b.visual, null, 1, caixa)}</div>`;
  }
  document.getElementById('cap-num').textContent = TL.rotulo;
  document.getElementById('cap-titulo').textContent = TL.titulo;
  document.getElementById('cap-progresso').style.width = (100 * (i + 1) / TL.blocos.length) + '%';
  const frase = b.frases[Math.min(k, b.frases.length - 1)];
  document.getElementById('legenda-texto').innerHTML = frase ? rico(frase.legenda) : '';
  return true;
};
