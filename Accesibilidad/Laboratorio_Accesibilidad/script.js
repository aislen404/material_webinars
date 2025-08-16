// Helpers
const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];

// Theme toggle
$('#themeToggle')?.addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  document.documentElement.setAttribute('data-theme', cur === 'dark' ? 'light' : 'dark');
});

// Tabs accesibles
$$('.tab').forEach((tab) => {
  tab.addEventListener('click', () => activateTab(tab));
  tab.addEventListener('keydown', (e) => {
    const tabs = $$('.tab');
    let i = tabs.indexOf(document.activeElement);
    if(e.key === 'ArrowRight') { i = (i+1) % tabs.length; tabs[i].focus(); }
    if(e.key === 'ArrowLeft')  { i = (i-1+tabs.length) % tabs.length; tabs[i].focus(); }
    if(e.key === 'Home')       { tabs[0].focus(); }
    if(e.key === 'End')        { tabs[tabs.length-1].focus(); }
    if(e.key === 'Enter' || e.key === ' ') { activateTab(document.activeElement); e.preventDefault(); }
  });
});
function activateTab(tab){
  $$('.tab').forEach(t=>{ t.classList.remove('active'); t.setAttribute('aria-selected','false'); t.setAttribute('tabindex','-1'); });
  $$('.pane').forEach(p=>p.classList.remove('active'));
  tab.classList.add('active'); tab.setAttribute('aria-selected','true'); tab.setAttribute('tabindex','0');
  $('#'+tab.getAttribute('aria-controls')).classList.add('active');
}

// Preview & simulator
function updatePreview(){
  const html = $('#htmlInput')?.value || '';
  const css  = $('#cssInput')?.value || '';
  const doc = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${html}</body></html>`;
  const frame = $('#preview')?.contentWindow?.document;
  if(frame){ frame.open(); frame.write(doc); frame.close(); }
  applySimulator();
  renderFocusMap(html);
}
$('#htmlInput')?.addEventListener('input', updatePreview);
$('#cssInput')?.addEventListener('input', updatePreview);

function applySimulator(){
  const sim = $('#simulator')?.value;
  const el = $('#preview');
  if(!el) return;
  el.style.filter = 'none';
  if(sim === 'blur') el.style.filter = 'blur(2px)';
  if(sim === 'highcontrast') el.style.filter = 'contrast(1.6)';
  if(sim === 'protanopia') el.style.filter = 'grayscale(.25) saturate(.7) hue-rotate(-20deg)';
  if(sim === 'deuteranopia') el.style.filter = 'grayscale(.2) saturate(.75) hue-rotate(15deg)';
  if(sim === 'tritanopia') el.style.filter = 'grayscale(.2) saturate(.8) hue-rotate(125deg)';
}
$('#simulator')?.addEventListener('change', applySimulator);

// Contrast calculator
function hexToRgb(hex){ hex=(hex||'').replace('#','').trim(); if(!hex) return null; if(hex.length===3) hex=hex.split('').map(x=>x+x).join(''); const n=parseInt(hex,16); if(Number.isNaN(n)) return null; return {r:(n>>16)&255, g:(n>>8)&255, b:n&255}; }
function luminance({r,g,b}){ const a=[r,g,b].map(v=>{ v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); }); return 0.2126*a[0] + 0.7152*a[1] + 0.0722*a[2]; }
function contrastRatio(c1,c2){ const A=hexToRgb(c1), B=hexToRgb(c2); if(!A||!B) return null; const L1=luminance(A), L2=luminance(B); const bright=Math.max(L1,L2), dark=Math.min(L1,L2); return (bright+0.05)/(dark+0.05); }

$('#btnContrast')?.addEventListener('click', ()=>{
  const t = $('#colorText').value || '#111111';
  const b = $('#colorBg').value || '#ffffff';
  const ratio = contrastRatio(t,b);
  const res = $('#contrastResult');
  if(!ratio){ res.textContent = 'Colores no válidos.'; return; }
  const r = ratio.toFixed(2);
  let status = '❌ Fail';
  if(ratio >= 7) status = '✅ AAA';
  else if(ratio >= 4.5) status = '✅ AA (texto normal)';
  else if(ratio >= 3) status = '⚠️ AA (solo texto grande)';
  res.textContent = `Ratio ≈ ${r} — ${status}`;
});

// Analyze HTML/CSS
function analyze(html, css){
  const out = [];
  const parser = new DOMParser();
  const doc = parser.parseFromString(html, 'text/html');

  // 0) lang en <html>
  const htmlEl = doc.querySelector('html');
  if(htmlEl){
    const lang = htmlEl.getAttribute('lang');
    if(!lang || !/^[a-z]{2}(-[A-Za-z0-9]+)?$/.test(lang)) out.push({cat:'Estructura', level:'warn', msg:'Falta o no válido el atributo lang en <html> (ej. lang="es").'});
  }

  // 1) Estructura
  const h1s = doc.querySelectorAll('h1');
  if(h1s.length === 0) out.push({cat:'Estructura', level:'warn', msg:'No hay <h1> en la página.'});
  if(h1s.length > 1) out.push({cat:'Estructura', level:'warn', msg:'Hay múltiples <h1>. Debería haber uno principal.'});
  const headingsEls = [...doc.querySelectorAll('h1,h2,h3,h4,h5,h6')];
  const headings = headingsEls.map(h=>parseInt(h.tagName[1]));
  let prev = 0;
  headings.forEach((lvl, i)=>{
    if(i>0 && (lvl - prev) > 1) out.push({cat:'Estructura', level:'warn', msg:`Salto de jerarquía: h${prev} → h${lvl}.`});
    prev = lvl;
  });
  // Encabezados huérfanos: p.ej. h3 sin que haya aparecido ningún h2 antes
  const seen = {};
  headings.forEach((lvl) => {
    if(lvl===1) seen[1]=true;
    if(lvl===2) seen[2]=true;
    if(lvl===3 && !seen[2]) out.push({cat:'Estructura', level:'warn', msg:'Existe un h3 antes de que aparezca un h2.'});
    if(lvl===4 && !seen[3]) out.push({cat:'Estructura', level:'warn', msg:'Existe un h4 antes de que aparezca un h3.'});
  });
  if(!doc.querySelector('main')) out.push({cat:'Estructura', level:'warn', msg:'Falta landmark <main>.'});

  // 2) IDs duplicados
  const ids = {};
  doc.querySelectorAll('[id]').forEach(el=>{
    const id = el.id;
    ids[id] = (ids[id]||0)+1;
  });
  Object.entries(ids).forEach(([id,count])=>{
    if(count>1) out.push({cat:'Estructura', level:'warn', msg:`ID duplicado: "${id}" (${count} veces).`});
  });

  // 3) Navegación/teclado
  doc.querySelectorAll('[tabindex]').forEach(n=>{
    const val = parseInt(n.getAttribute('tabindex'));
    if(val > 0) out.push({cat:'Navegación', level:'warn', msg:'Evita tabindex > 0. Puede romper el orden natural.'});
    if(val === -1){
      const role = (n.getAttribute('role')||'').toLowerCase();
      const tag = n.tagName.toLowerCase();
      if(role==='button' || role==='link' || tag==='button' || tag==='a'){
        out.push({cat:'Navegación', level:'warn', msg:'Elemento interactivo con tabindex="-1": no será accesible con Tab.'});
      }
    }
  });

  // 4) Enlaces
  const linkMap = {}; // texto -> set de hrefs
  doc.querySelectorAll('a').forEach(a=>{
    const text = (a.textContent||'').trim();
    const t = text.toLowerCase();
    const href = a.getAttribute('href') || '';
    if(!href) out.push({cat:'Enlaces', level:'warn', msg:'Enlace sin href.'});
    const generic = ['haz clic','click aquí','click aqui','aquí','aqui','leer más','leer mas','más','mas'];
    if(generic.includes(t)) out.push({cat:'Enlaces', level:'warn', msg:'Enlace con texto genérico. Usa texto descriptivo.'});
    if(text.length === 0 && !a.getAttribute('aria-label')) out.push({cat:'Enlaces', level:'bad', msg:'Enlace sin texto visible ni aria-label.'});
    if(a.getAttribute('role') === 'button') out.push({cat:'Enlaces', level:'warn', msg:'<a role="button"> detectado. Considera <button> o gestiona teclado.'});
    if(text && text.length >= 4){
      const key = t.replace(/\s+/g,' ');
      (linkMap[key] = linkMap[key] || new Set()).add(href);
    }
  });
  Object.entries(linkMap).forEach(([text,setHrefs])=>{
    if(setHrefs.size > 1) out.push({cat:'Enlaces', level:'warn', msg:`Texto de enlace repetido ("${text}") apunta a destinos diferentes.`});
  });

  // 5) Imágenes
  doc.querySelectorAll('img').forEach(img=>{
    const hasAlt = img.hasAttribute('alt');
    const alt = img.getAttribute('alt') || '';
    const decorative = img.getAttribute('role')==='presentation' || img.getAttribute('aria-hidden')==='true';
    if(!hasAlt && !decorative) out.push({cat:'Imágenes', level:'bad', msg:'Imagen sin alt.'});
    if(hasAlt && alt.trim()==='') out.push({cat:'Imágenes', level:'warn', msg:'alt vacío: verifica si es decorativa.'});
  });

  // 6) Formularios y labels
  const inputs = doc.querySelectorAll('input, textarea, select');
  inputs.forEach(el=>{
    const id=el.getAttribute('id');
    let labeled=false;
    if(id && doc.querySelector(`label[for="${id}"]`)) labeled=true;
    if(el.closest('label')) labeled=true;
    const hasAria = el.hasAttribute('aria-label') || el.hasAttribute('aria-labelledby');
    if(!labeled && !hasAria) out.push({cat:'Formularios', level:'bad', msg:'Campo sin etiqueta (label/for o aria-*).'});
    if(el.hasAttribute('required') && !el.hasAttribute('aria-required')) out.push({cat:'Formularios', level:'warn', msg:'Campo requerido sin aria-required="true".'});
    if(el.getAttribute('aria-required')==='true' && !el.hasAttribute('required')) out.push({cat:'Formularios', level:'warn', msg:'aria-required="true" sin atributo required.'});
  });
  // Labels con for inválido o texto vacío
  doc.querySelectorAll('label').forEach(lab=>{
    const f = lab.getAttribute('for');
    const txt = (lab.textContent||'').trim();
    if(f && !doc.getElementById(f)) out.push({cat:'Formularios', level:'warn', msg:`label[for="${f}"] apunta a un id inexistente.`});
    if(!txt) out.push({cat:'Formularios', level:'warn', msg:'Etiqueta <label> vacía.'});
  });

  // 7) Iframes
  doc.querySelectorAll('iframe').forEach(f=>{ if(!f.getAttribute('title')) out.push({cat:'Estructura', level:'bad', msg:'<iframe> sin title.'}); });

  // 8) Vídeo
  doc.querySelectorAll('video').forEach(v=>{
    const tracks = v.querySelectorAll('track[kind="subtitles"], track[kind="captions"]');
    if(tracks.length === 0) out.push({cat:'Multimedia', level:'bad', msg:'Vídeo sin subtítulos (track).'});
    if(v.hasAttribute('autoplay') && !v.hasAttribute('muted') && !v.hasAttribute('controls'))
      out.push({cat:'Multimedia', level:'warn', msg:'Autoplay sin controles ni mute: intrusivo.'});
  });

  // 9) ARIA redundante / roles inválidos
  const validRoles = new Set(['button','link','heading','navigation','main','banner','contentinfo','complementary','region','dialog','checkbox','radio','textbox','search','list','listitem','listbox','option','tab','tablist','tabpanel','toolbar','menubar','menu','menuitem','grid','row','cell','gridcell','table','rowgroup','rowheader','columnheader','slider','switch','progressbar','status','alert','alertdialog','tooltip','note','presentation','img']);
  doc.querySelectorAll('[role]').forEach(el=>{
    const role = (el.getAttribute('role')||'').toLowerCase();
    if(!validRoles.has(role)) out.push({cat:'ARIA', level:'warn', msg:`Rol ARIA no reconocido o poco común: "${role}". Verifica documentación WAI-ARIA.`});
    const tag = el.tagName.toLowerCase();
    const implicit = {button:'button', a:'link', h1:'heading', h2:'heading', h3:'heading', h4:'heading', h5:'heading', h6:'heading', nav:'navigation', main:'main', header:'banner', footer:'contentinfo'}[tag];
    if(implicit && implicit===role) out.push({cat:'ARIA', level:'warn', msg:`Rol ARIA redundante en <${tag}> (implícito: ${role}).`});
  });

  // 10) Estilos inline simple
  doc.querySelectorAll('[style]').forEach(el=>{
    const s = (el.getAttribute('style')||'').toLowerCase();
    if(s.includes('outline:none')) out.push({cat:'Estilo', level:'warn', msg:'Se elimina el foco (outline:none). Añade foco visible.'});
    const mColor = s.match(/color\s*:\s*#([0-9a-f]{3,6})/i);
    const mBg    = s.match(/background(?:-color)?\s*:\s*#([0-9a-f]{3,6})/i);
    if(mColor && mBg){
      const ratio = contrastRatio('#'+mColor[1], '#'+mBg[1]);
      if(ratio && ratio<4.5) out.push({cat:'Contraste', level:'bad', msg:`Contraste bajo inline (≈ ${ratio.toFixed(2)}). AA mínimo 4.5:1.`});
    }
    const f = s.match(/font-size\s*:\s*(\d{1,2})px/);
    if(f && parseInt(f[1],10) < 12) out.push({cat:'Estilo', level:'warn', msg:`Fuente muy pequeña (${f[1]}px).`});
  });

  // 11) CSS global
  if(css){
    if(/outline\s*:\s*none/i.test(css)) out.push({cat:'Estilo', level:'warn', msg:'CSS elimina outline globalmente.'});
    const smallFonts = css.match(/font-size\s*:\s*(\d{1,2})px/gi) || [];
    smallFonts.forEach(m => { const n = parseInt((m.match(/\d+/)||['0'])[0],10); if(n < 12) out.push({cat:'Estilo', level:'warn', msg:`Fuente pequeña detectada en CSS (${n}px).`}); });
  }

  if(out.length===0) out.push({cat:'OK', level:'good', msg:'Sin problemas evidentes en chequeos básicos.'});
  return out;
}

function renderIssues(list){
  const box = $('#issues'); if(!box) return;
  box.innerHTML = '';
  list.forEach(it=>{
    const d = document.createElement('div');
    d.className = `issue ${it.level}`;
    d.innerHTML = `<strong>[${it.cat}]</strong> ${it.msg}`;
    box.appendChild(d);
  });
}

// Focus map (estimated order)
function renderFocusMap(html){
  const list = $('#focusList'); if(!list) return;
  list.innerHTML = '';
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const focusable = [...doc.querySelectorAll('a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])')];
  if(focusable.length === 0){ list.innerHTML = '<li class="muted">No se detectaron elementos enfocables.</li>'; return; }
  const items = focusable.map((el,idx)=>{
    const tag = el.tagName.toLowerCase();
    const id = el.id ? `#${el.id}` : '';
    const name = (el.getAttribute('name')||'').trim();
    const text = (el.textContent||'').trim().replace(/\s+/g,' ').slice(0,60);
    const ti = el.hasAttribute('tabindex') ? ` tabindex=${el.getAttribute('tabindex')}` : '';
    return `${idx+1}. <${tag}${id}${name?` name=${name}`:''}${ti}> ${text}`;
  });
  items.forEach(s=>{ const li=document.createElement('li'); li.textContent = s; list.appendChild(li); });
}

// Prompt generation
function buildPrompt(){
  const html = $('#htmlInput')?.value || '';
  const css  = $('#cssInput')?.value || '';
  const header = `Actúa como auditor experto en accesibilidad (WCAG 2.2 AA).
Analiza el siguiente HTML/CSS y devuelve:
1) Hallazgos organizados por principio POUR y criterio WCAG.
2) Impacto en usuarios (quién y cómo).
3) Correcciones con fragmentos de código.
4) Prioridad (Alta/Media/Baja) y esfuerzo.
5) Pruebas manuales y automáticas recomendadas.`;
  const prompt = `${header}

HTML:
\`\`\`html
${html}
\`\`\`

CSS:
\`\`\`css
${css}
\`\`\``;
  const pb = $('#promptBox'); if(pb) pb.textContent = prompt;
}

// Export report
function escapeHtml(s){ return (s||'').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }
function exportReportHTML(issues){
  const html = $('#htmlInput')?.value || '';
  const css  = $('#cssInput')?.value || '';
  const rows = issues.map(i=>`<tr><td>${i.cat}</td><td>${i.level}</td><td>${i.msg}</td></tr>`).join('');
  const doc = `<!doctype html><meta charset="utf-8"><title>Informe de Accesibilidad</title>
  <style>body{font-family:system-ui;padding:16px} table{border-collapse:collapse;width:100%} td,th{border:1px solid #ddd;padding:8px} th{background:#f1f1f5}</style>
  <h1>Informe de Accesibilidad</h1>
  <h3>Hallazgos</h3>
  <table><tr><th>Categoría</th><th>Nivel</th><th>Descripción</th></tr>${rows}</table>
  <h3>Código analizado</h3>
  <h4>HTML</h4><pre>${escapeHtml(html)}</pre>
  <h4>CSS</h4><pre>${escapeHtml(css)}</pre>`;
  const blob = new Blob([doc], {type:'text/html'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'informe_accesibilidad.html'; a.click();
}
function exportReportJSON(issues){
  const html = $('#htmlInput')?.value || '';
  const css  = $('#cssInput')?.value || '';
  const focusDoc = new DOMParser().parseFromString(html, 'text/html');
  const focusable = [...focusDoc.querySelectorAll('a[href], button, input, textarea, select, [tabindex]:not([tabindex="-1"])')].map(el=>{
    return {
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      name: el.getAttribute('name') || null,
      text: (el.textContent||'').trim().replace(/\s+/g,' '),
      tabindex: el.getAttribute('tabindex') || null
    };
  });
  const data = { issues, code: { html, css }, focus_order: focusable };
  const blob = new Blob([JSON.stringify(data, null, 2)], {type:'application/json'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'informe_accesibilidad.json'; a.click();
}

// Compare view
function loadCompare(){
  const l = $('#selLeft')?.value;
  const r = $('#selRight')?.value;
  if($('#frameLeft')) $('#frameLeft').src = l || '';
  if($('#frameRight')) $('#frameRight').src = r || '';
}

// Load examples into editor
const exampleSnippets = {
  malo: `
<header><h1>Mi sitio</h1><h3>Subtítulo</h3></header>
<img src="foto.jpg">
<a>aquí</a>
<div onclick="alert('hola')">Abrir</div>
<form>
  <input type="text" placeholder="Nombre">
  <button></button>
</form>
  `,
  bueno: `
<header><h1>Mi sitio</h1></header>
<main id="contenido">
  <nav aria-label="Principal"><ul><li><a href="#contenido">Ir al contenido</a></li></ul></nav>
  <figure>
    <img src="foto.jpg" alt="Persona usando una web con alto contraste">
    <figcaption>Ejemplo con texto alternativo.</figcaption>
  </figure>
  <button type="button" class="btn">Abrir</button>
  <form aria-describedby="help">
    <p id="help">Campos con * son obligatorios.</p>
    <label for="nombre">Nombre *</label>
    <input id="nombre" required>
    <button type="submit">Enviar</button>
  </form>
</main>
  `,
  form: `
<form>
  <div><input placeholder="Email"></div>
  <div><input type="password"></div>
  <button>OK</button>
</form>
  `,
  menu: `
<nav>
  <div>Inicio</div><div>Servicios</div><div>Contacto</div>
</nav>
  `
};

// Bindings
$('#btnAnalyze')?.addEventListener('click', ()=>{
  const issues = analyze($('#htmlInput')?.value || '', $('#cssInput')?.value || '');
  renderIssues(issues);
  updatePreview();
});
$('#btnExport')?.addEventListener('click', ()=>{
  const issues = analyze($('#htmlInput')?.value || '', $('#cssInput')?.value || '');
  exportReportHTML(issues);
});
$('#btnExportJSON')?.addEventListener('click', ()=>{
  const issues = analyze($('#htmlInput')?.value || '', $('#cssInput')?.value || '');
  exportReportJSON(issues);
});
$('#btnReset')?.addEventListener('click', ()=>{
  if($('#htmlInput')) $('#htmlInput').value = '';
  if($('#cssInput'))  $('#cssInput').value = '';
  if($('#issues'))    $('#issues').innerHTML = '';
  if($('#promptBox')) $('#promptBox').textContent = '';
  $('#focusList').innerHTML = '';
  updatePreview();
});
$('#btnGenPrompt')?.addEventListener('click', buildPrompt);
$('#btnCopyPrompt')?.addEventListener('click', async ()=>{
  try{ await navigator.clipboard.writeText($('#promptBox')?.textContent || ''); alert('Prompt copiado'); }
  catch(e){ alert('No se pudo copiar. Selecciona manualmente.'); }
});
$('#btnDownloadPrompt')?.addEventListener('click', ()=>{
  const blob = new Blob([($('#promptBox')?.textContent || '')], {type:'text/plain'});
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'prompt_wcag22.txt'; a.click();
});
$('#btnLoadCompare')?.addEventListener('click', loadCompare);
$$('#pane-examples .btn').forEach(b=> b.addEventListener('click', ()=>{
  const key = b.getAttribute('data-load');
  if(exampleSnippets[key] && $('#htmlInput')){
    $('#htmlInput').value = exampleSnippets[key].trim();
    updatePreview();
    activateTab($('#tab-basic'));
  }
}));

// Initialize
updatePreview();
loadCompare();
