<script id="animator-simple-js">
/*
 * animator.js: page behavior for bolu.info/animator.
 * Runs from a Code Snippets entry on the WordPress site; this file is the
 * exact served code, kept here so the repo matches what's live.
 *
 * Standing waving preloader with a 0-to-100 counter (~2.2s), then cuts to
 * the seated typing loop. SIT_VIDEO / SIT_POSTER point at the v8
 * true-seamless-loop build.
 */
(function(){
if(!document.body||!document.body.classList.contains('page-id-9274'))return;
var SIT_VIDEO='https://bolu.info/wp-content/uploads/2026/09/media-generation-bolu-typing-v8-seamless.mp4';
var SIT_POSTER='https://bolu.info/wp-content/uploads/2026/09/media-generation-bolu-typing-poster-v8-seamless.webp';
var STAND_IMG='https://bolu.info/wp-content/uploads/2026/09/media-generation-bolu-standing-likeness-0-2d20b420-c99e-4a87-be96-2aeddbe33523.webp';
var phase='loading';
(function(){var img=document.querySelector('.anim-character img')||document.querySelector('img[src*="media-generation-bolu-character-0-"]');if(img){if(img.getAttribute('src')!==STAND_IMG){img.setAttribute('src',STAND_IMG);}img.setAttribute('alt','3D likeness of Boluwatife Johnson waving while holding a coffee cup');}})();
var clockEl=document.getElementById('animClock');
function pad(n){return(n<10?'0':'')+n;}
function tick(){if(!clockEl)return;var d=new Date(),h=d.getHours(),ap=h>=12?'PM':'AM';h=h%12;if(h===0)h=12;if(clockEl.textContent!==(pad(h)+':'+pad(d.getMinutes())+' '+ap))clockEl.textContent=pad(h)+':'+pad(d.getMinutes())+' '+ap;}
tick();setInterval(tick,1000);
var pre=document.getElementById('animPreloader');
if(!pre)return;
pre.innerHTML='<div class="anim-pre-media anim-pre-stand"><img src="'+STAND_IMG+'" alt="Boluwatife Johnson waving"></div><div class="anim-pre-media anim-pre-sit"><video muted loop playsinline autoplay preload="auto" poster="'+SIT_POSTER+'"><source src="'+SIT_VIDEO+'" type="video/mp4"></video></div><div class="anim-pre-count" id="animPreCount">0</div>';
var video=pre.querySelector('video');
if(video){video.addEventListener('error',function(){var i=document.createElement('img');i.src=SIT_POSTER;i.alt='Boluwatife Johnson sitting at a desk';video.parentNode.replaceChild(i,video);},true);try{var p=video.play();if(p&&p.catch)p.catch(function(){});}catch(e){}}
var countEl=document.getElementById('animPreCount');
var DUR=2200,t0=null,done=false;
function counterDone(){if(done)return;done=true;phase='holding';pre.classList.add('anim-count-done');pre.classList.add('anim-to-sit');}
function frame(ts){if(done)return;if(t0===null)t0=ts;var pr=Math.min(1,(ts-t0)/DUR);var e=1-Math.pow(1-pr,4);if(countEl)countEl.textContent=Math.round(e*100);if(pr<1)requestAnimationFrame(frame);else counterDone();}
if(window.requestAnimationFrame)requestAnimationFrame(frame);else setTimeout(counterDone,DUR);
function advance(){if(phase!=='holding')return;phase='hero';pre.classList.add('anim-pre-exit');var ch=document.querySelector('.anim-character');if(ch)ch.classList.add('hero-char-enter');setTimeout(function(){if(pre.parentNode)pre.parentNode.removeChild(pre);},1000);}

})();
</script>
