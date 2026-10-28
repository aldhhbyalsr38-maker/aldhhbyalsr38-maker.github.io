
(function(){
var P=window.PAGE,OZ=31.1035,$=function(i){return document.getElementById(i)};
function nf(v,d){try{return new Intl.NumberFormat(P.loc,{minimumFractionDigits:d,maximumFractionDigits:d}).format(v)}catch(e){return v.toFixed(d)}}
function dd(v){return v>=1000?0:v>=100?2:v>=1?3:v>=0.01?4:6}
function j(u){return fetch(u).then(function(r){if(!r.ok)throw 0;return r.json()})}
function hist(){return j(P.base+'/data/history.json').catch(function(){return []})}
function live(H){
  try{var c=JSON.parse(localStorage.getItem('lv')||'null');if(c&&Date.now()-c.t<300000)return Promise.resolve(c)}catch(e){}
  return Promise.all([j('https://api.gold-api.com/price/XAU'),j('https://api.gold-api.com/price/XAG').catch(function(){return null}),j('https://open.er-api.com/v6/latest/USD')])
  .then(function(a){var d={t:Date.now(),xau:a[0].price,xag:a[1]?a[1].price:null,r:a[2].rates};try{localStorage.setItem('lv',JSON.stringify(d))}catch(e){}return d})
  .catch(function(){var l=H[H.length-1];if(l)return {t:Date.parse(l.t||l.d),xau:l.xau,xag:l.xag,r:l.r,stale:1};throw 0})
}
function chart(el,pts,d){
  if(!el)return;if(pts.length<2){el.textContent=P.wait;return}
  var W=640,Hh=190,p=8,mn=Math.min.apply(null,pts),mx=Math.max.apply(null,pts),rg=(mx-mn)||1;
  var path=pts.map(function(v,i){return (i?'L':'M')+(p+i*(W-2*p)/(pts.length-1)).toFixed(1)+' '+(Hh-p-(v-mn)/rg*(Hh-2*p)).toFixed(1)}).join('');
  el.innerHTML='<svg viewBox="0 0 '+W+' '+Hh+'" width="100%" role="img"><path d="'+path+'" fill="none" stroke="var(--g)" stroke-width="2.5" stroke-linejoin="round"/></svg><div class="mm"><span>'+nf(mn,d)+'</span><span>'+nf(mx,d)+'</span></div>';
}
function change(el,pts){
  if(!el||pts.length<2)return;var c=(pts[pts.length-1]/pts[0]-1)*100;
  el.innerHTML=P.chg+': <b class="'+(c>=0?'up':'dn')+'">'+(c>=0?'+':'')+nf(c,2)+'%</b>';
}
function series(H,fn){var o=[];H.slice(-30).forEach(function(e){try{var v=fn(e);if(isFinite(v)&&v>0)o.push(v)}catch(x){}});return o}
function pg(d,k,cur){return d.xau/OZ*k/24*d.r[cur]}
function stamp(d){var u=$('upd');if(u)u.textContent=new Date(d.t).toLocaleString(P.loc,{dateStyle:'medium',timeStyle:'short'})}
function gold(H,d){
  document.querySelectorAll('[data-k]').forEach(function(e){e.textContent=nf(pg(d,+e.dataset.k,P.cur),P.dec)});
  if($('oz'))$('oz').textContent=nf(d.xau,2);
  if($('usd'))$('usd').textContent=nf(d.r[P.cur],dd(d.r[P.cur]));
  var tb=$('wt');if(tb){var ws=[1,5,8,10,20,50,100],h='';ws.forEach(function(w){h+='<tr><td>'+w+'</td>';P.cols.forEach(function(k){h+='<td><b>'+nf(w*pg(d,k,P.cur),P.dec)+'</b></td>'});h+='</tr>'});tb.innerHTML=h}
  var pts=series(H,function(e){return pg(e,P.hk,P.cur)});pts.push(pg(d,P.hk,P.cur));
  chart($('chart'),pts,P.dec);change($('chg'),pts);
  var g=$('gr'),kk=$('kk'),mk=$('mk'),tx=$('tx'),rs=$('res');
  function f(){var w=parseFloat(g.value)||0,m=parseFloat(mk.value)||0,x=parseFloat(tx.value)||0;rs.textContent=nf(w*pg(d,+kk.value,P.cur)*(1+m/100)*(1+x/100),P.dec)+' '+P.cur}
  [g,kk,mk,tx].forEach(function(e){e.oninput=f;e.onchange=f});f();
}
function rate(H,d){
  var r=d.r[P.to]/d.r[P.from];
  $('rate').textContent='1 '+P.from+' = '+nf(r,dd(r))+' '+P.to;
  var a=$('amt'),o=$('out');function f(){o.textContent=nf((parseFloat(a.value)||0)*r,dd(r)>3?4:2)+' '+P.to}a.oninput=f;f();
  var tb=$('ct'),h='';[1,5,10,50,100,500,1000].forEach(function(v){h+='<tr><td>'+nf(v,0)+' '+P.from+'</td><td><b>'+nf(v*r,dd(r)>3?4:2)+'</b> '+P.to+'</td><td>'+nf(v/r,dd(1/r)>3?4:2)+' '+P.from+'</td></tr>'});tb.innerHTML=h;
  var pts=series(H,function(e){return e.r[P.to]/e.r[P.from]});pts.push(r);chart($('chart'),pts,dd(r));change($('chg'),pts);
}
function zakat(H,d){
  var c=$('zc'),ids=['zg','zs','zm','zd'];
  function f(){var cur=c.value,rt=d.r[cur],g=pg(d,24,cur)*(parseFloat($('zg').value)||0),
    s=d.xag?d.xag/OZ*rt*(parseFloat($('zs').value)||0):0,w=g+s+(parseFloat($('zm').value)||0)-(parseFloat($('zd').value)||0),
    ns=d.xag?595*d.xag/OZ*rt:85*pg(d,24,cur),k=dec(cur);
    $('zn').textContent=nf(ns,k);$('zw').textContent=nf(w,k);
    $('zr').textContent=w>=ns?(nf(w*0.025,k)+' '+cur):P.notdue;}
  function dec(cur){return P.decs&&P.decs[cur]!=null?P.decs[cur]:2}
  ids.concat(['zc']).forEach(function(i){$(i).oninput=f;$(i).onchange=f});f();
}
function share(){var b=$('share');if(!b)return;b.onclick=function(){var u=location.href,tt=document.title;
  if(navigator.share){navigator.share({title:tt,url:u}).catch(function(){})}else{window.open('https://wa.me/?text='+encodeURIComponent(tt+' '+u),'_blank')}}}
share();
if('serviceWorker' in navigator){navigator.serviceWorker.register(P.base+'/sw.js').catch(function(){})}
if(P.type==='home'){live([]).then(function(d){if($('oz'))$('oz').textContent=nf(d.xau,2)}).catch(function(){});return}
hist().then(function(H){return live(H).then(function(d){
  stamp(d);if(d.stale&&$('upd'))$('upd').textContent+=' *';
  if(P.type==='gold')gold(H,d);else if(P.type==='rate')rate(H,d);else if(P.type==='zakat')zakat(H,d);
})}).catch(function(){if($('upd'))$('upd').textContent=P.err});
})();
