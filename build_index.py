#!/usr/bin/env python3
"""Fabrique index.html (version GitHub) à partir de analyse3-java.html, avec la page d'entrée prénom/nom.
Réglages du formulaire Google dans gate-config.json : {"url": "...formResponse", "prenom": "entry.123", "nom": "entry.456"}"""
import json, os
here=os.path.dirname(os.path.abspath(__file__))
s=open(os.path.join(here,'analyse3-java.html'),encoding='utf-8').read()
cfg={"url":"","prenom":"","nom":""}
cp=os.path.join(here,'gate-config.json')
if os.path.exists(cp): cfg.update(json.load(open(cp,encoding='utf-8')))
gate_css='''<style>
.gate{position:fixed;inset:0;z-index:100;background:var(--bg);display:grid;place-items:center;padding:16px;overflow:auto}
.gate form{width:100%;max-width:26rem;border:1.5px solid var(--ink);background:var(--surface);display:grid}
.gate header{padding:.8rem 1rem;border-bottom:1.5px solid var(--ink);font-family:var(--mono)}
.gate header span{display:block;font-size:.72rem;color:var(--muted)}
.gate header b{font-size:1.05rem}
.gate .in{padding:1rem;display:grid;gap:.8rem}
.gate label{display:grid;gap:.3rem;font-family:var(--mono);font-size:.78rem;font-weight:600}
.gate input{font:inherit;font-size:1rem;padding:.55rem .65rem;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.gate input:focus-visible{outline:2px solid var(--ink);outline-offset:1px}
.gate button{font-family:var(--mono);font-size:.85rem;font-weight:700;padding:.6rem .9rem;border:1px solid var(--ink);background:var(--ink);color:var(--bg);cursor:pointer;justify-self:start}
.gate button:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.gate .note{font-size:.82rem;color:var(--muted)}
.gate .err{font-size:.85rem;color:var(--ko);min-height:1.2em}
html.gated,html.gated body{overflow:hidden}
</style>'''
gate_html='''<div class="gate" id="gate" role="dialog" aria-modal="true" aria-labelledby="gateT">
  <form id="gateForm" novalidate>
    <header><span>«class»</span><b id="gateT">Connexion</b></header>
    <div class="in">
      <label for="gPrenom">String prenom<input id="gPrenom" name="prenom" autocomplete="given-name" required></label>
      <label for="gNom">String nom<input id="gNom" name="nom" autocomplete="family-name" required></label>
      <p class="err" id="gateErr" role="alert"></p>
      <button type="submit">entrer()</button>
      <p class="note">Ton prénom, ton nom et la date de ta visite sont envoyés à l'auteur de la fiche, qui peut voir la liste des connexions. Ils sont aussi gardés dans ce navigateur pour ne pas te les redemander.</p>
    </div>
  </form>
</div>'''
gate_js='''<script>
(function(){
  var FORM=%s;
  var gate=document.getElementById('gate'), form=document.getElementById('gateForm'), err=document.getElementById('gateErr');
  var who=null; try{ who=JSON.parse(localStorage.getItem('a3who')||'null'); }catch(e){}
  function log(w){
    try{ if(sessionStorage.getItem('a3logged')) return; sessionStorage.setItem('a3logged','1'); }catch(e){}
    if(!FORM.url) return;
    var d=new URLSearchParams(); d.append(FORM.prenom,w.prenom); d.append(FORM.nom,w.nom);
    try{ fetch(FORM.url,{method:'POST',mode:'no-cors',body:d}).catch(function(){}); }catch(e){}
  }
  function open(w){ gate.hidden=true; document.documentElement.classList.remove('gated'); log(w); }
  if(who && who.prenom && who.nom){ open(who); return; }
  document.documentElement.classList.add('gated');
  document.getElementById('gPrenom').focus();
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var p=document.getElementById('gPrenom').value.trim(), n=document.getElementById('gNom').value.trim();
    if(p.length<2 || n.length<2){ err.textContent='Écris ton prénom et ton nom pour entrer.'; return; }
    var w={prenom:p,nom:n}; try{ localStorage.setItem('a3who',JSON.stringify(w)); }catch(e2){}
    open(w);
  });
})();
</script>''' % json.dumps(cfg)
head='<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
i=s.index('<nav class="pk"')
doc=head+s[:i]+gate_css+'\n</head>\n<body style="margin:0">\n'+gate_html+'\n'+s[i:]+'\n'+gate_js+'\n</body>\n</html>\n'
open(os.path.join(here,'index.html'),'w',encoding='utf-8').write(doc)
print('index.html écrit ; journal des connexions', 'ACTIF' if cfg['url'] else 'INACTIF (gate-config.json absent)')
