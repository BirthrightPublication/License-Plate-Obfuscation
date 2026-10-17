import {states,sources,validate,legalRecord,availability,parseProject} from './domain.js';
const $=id=>document.getElementById(id), key='birthright.plate.project.v1';
for(const state of states) $('state').add(new Option(state,state)); $('state').value='California';
function link(container,url,title){const a=document.createElement('a');a.href=url;a.textContent=title;a.target='_blank';a.rel='noopener noreferrer';container.append(a);}
function render(){const state=$('state').value;$('plateState').textContent=state;$('plateText').textContent=$('text').value;$('validation').textContent=validate(state,$('text').value).message;$('legal').textContent=legalRecord(state).explanation;$('catalog').replaceChildren();$('law').replaceChildren();$('lookup').textContent='';const s=sources[state];if(s){link($('catalog'),s.catalog,'Open issuing authority catalog ↗');link($('law'),s.law,s.title+' ↗');const p=document.createElement('p');p.textContent=s.rule+' Source currency unverified.';$('law').append(p);}else{$('catalog').textContent='Catalog source not curated for this state.';$('law').textContent='No curated legal source available.';}}
$('state').onchange=render;$('text').oninput=()=>{$('text').value=$('text').value.toUpperCase();render();};
$('orbit').oninput=()=>{$('plate').style.transform=`rotateX(12deg) rotateY(${$('orbit').value}deg)`;};$('reset').onclick=()=>{$('orbit').value=-12;$('orbit').oninput();};
$('availability').onclick=()=>{$('lookup').textContent=availability().message;};
function project(){return parseProject({schemaVersion:1,name:$('name').value,state:$('state').value,text:$('text').value});}
function apply(p){$('name').value=p.name;$('state').value=p.state;$('text').value=p.text;render();}
function attempt(fn){try{fn();}catch(e){$('storage').textContent='Operation failed: '+e.message;}}
$('save').onclick=()=>attempt(()=>{localStorage.setItem(key,JSON.stringify(project()));$('storage').textContent='Project saved on this device.';});
$('load').onclick=()=>attempt(()=>{const raw=localStorage.getItem(key);if(!raw)throw Error('No saved project');apply(parseProject(JSON.parse(raw)));$('storage').textContent='Saved project loaded.';});
$('export').onclick=()=>attempt(()=>{const url=URL.createObjectURL(new Blob([JSON.stringify(project(),null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='plate-project.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
$('import').onchange=async()=>{try{const f=$('import').files[0];if(!f)return;if(f.size>10000)throw Error('Backup exceeds 10 KB');apply(parseProject(JSON.parse(await f.text())));$('storage').textContent='Imported preview. Save to retain it.';}catch(e){$('storage').textContent='Import failed: '+e.message;}};
$('notes').oninput=()=>attempt(()=>localStorage.setItem('birthright.plate.notes.v1',$('notes').value));attempt(()=>{$('notes').value=localStorage.getItem('birthright.plate.notes.v1')||'';});render();
