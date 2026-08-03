document.documentElement.classList.add('js');
(() => {
  const form = document.querySelector('#directory-controls');
  if (!form) return;
  const grid = document.querySelector('#directory-grid');
  const cards = [...grid.querySelectorAll('.directory-card')];
  const params = new URLSearchParams(location.search);
  const fields = ['q','role','geo','reach','access','format','delivery','private','research','status','sort'];
  const title = value => value.replace(/\b\w/g, c => c.toUpperCase());
  const addOptions = (name, attr) => {
    const select = form.elements[name];
    const values = new Set();
    cards.forEach(card => card.dataset[attr].split('|').filter(Boolean).forEach(v => values.add(v)));
    [...values].sort().forEach(v => select.add(new Option(title(v), v)));
  };
  addOptions('role','role'); addOptions('geo','geo'); addOptions('access','access'); addOptions('format','format');
  fields.forEach(name => { if (params.has(name) && form.elements[name]) form.elements[name].value = params.get(name); });
  const selected = new Set((params.get('compare') || '').split(',').filter(Boolean).slice(0,3));
  cards.forEach(card => { const box=card.querySelector('input[type=checkbox]'); box.checked=selected.has(box.value); });
  const updateCompare = () => {
    cards.forEach(card => { const box=card.querySelector('input[type=checkbox]'); if (box.checked) selected.add(box.value); else selected.delete(box.value); });
    while (selected.size > 3) { const last=[...selected].pop(); selected.delete(last); cards.find(c=>c.querySelector('input').value===last).querySelector('input').checked=false; }
    document.querySelector('#compare-count').textContent=selected.size;
    document.querySelector('#compare-button').disabled=selected.size<2;
  };
  const apply = () => {
    const data = new FormData(form), q=(data.get('q')||'').toLowerCase().trim();
    const matches = card => !q || card.dataset.search.includes(q);
    let visible=cards.filter(card => matches(card) && ['role','geo','reach','access','format','delivery','private','research','status'].every(name => !data.get(name) || card.dataset[name].split('|').includes(data.get(name))));
    visible.sort((a,b) => data.get('sort')==='review' ? b.dataset.review.localeCompare(a.dataset.review) : data.get('sort')==='geography' ? a.dataset.geo.localeCompare(b.dataset.geo) : a.dataset.name.localeCompare(b.dataset.name));
    cards.forEach(card => card.hidden=!visible.includes(card)); visible.forEach(card => grid.append(card));
    document.querySelector('#result-count').textContent=visible.length;
    const url=new URL(location.href); fields.forEach(name => { const value=data.get(name); if(value && !(name==='sort'&&value==='name')) url.searchParams.set(name,value); else url.searchParams.delete(name); });
    if(selected.size) url.searchParams.set('compare',[...selected].join(',')); else url.searchParams.delete('compare'); history.replaceState({},'',url);
  };
  form.addEventListener('input', apply); form.addEventListener('reset', () => setTimeout(apply));
  cards.forEach(card => card.querySelector('input').addEventListener('change', e => { if(e.target.checked && selected.size>=3){e.target.checked=false; return;} updateCompare(); apply(); }));
  document.querySelector('#compare-button').addEventListener('click', () => {
    const chosen=cards.filter(c=>selected.has(c.querySelector('input').value));
    const rows=[['Description','p'],['Geography','[data-geo]'],['Access','[data-access]'],['Formats','[data-format]'],['Delivery','[data-delivery]'],['Verification','[data-status]'],['Reviewed','[data-review]']];
    document.querySelector('#compare-head').innerHTML='<tr><th>Attribute</th>'+chosen.map(c=>`<th>${c.dataset.name}</th>`).join('')+'</tr>';
    document.querySelector('#compare-body').innerHTML=rows.map(([label,key])=>'<tr><th>'+label+'</th>'+chosen.map(c=>`<td>${key==='p'?c.querySelector('p').textContent:c.dataset[key.slice(6,-1)]}</td>`).join('')+'</tr>').join('');
    document.querySelector('#compare-dialog').showModal();
  });
  updateCompare(); apply();
})();
(() => {
  const release = document.querySelector('[data-release-date]');
  if (!release) return;
  try {
    const previous = localStorage.getItem('eci-last-visit');
    if (previous && previous < release.dataset.releaseDate) document.querySelector('#since-last-visit').hidden = false;
    localStorage.setItem('eci-last-visit', new Date().toISOString().slice(0,10));
  } catch (_) {}
})();
