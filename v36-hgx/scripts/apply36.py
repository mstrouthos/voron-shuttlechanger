"""Build the v33 draft viewer page from the v32 page shell."""
import pickle,re,json,base64,numpy as np,trimesh
import build36 as B
from geo import to_tm,box
P=B.build(); H=B.hardware(); N={k:to_tm(v) for k,v in {**P,**H}.items()}
old=pickle.load(open('../old_parts.pkl','rb'))
b64=lambda a: base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
def rec(pid,tm,grp,col,metal=False,op=1):
    t=trimesh.graph.smooth_shade(trimesh.Trimesh(tm.vertices,tm.faces,process=False),angle=np.radians(30))
    return dict(id=pid,grp=grp,col=col,op=op,metal=metal,v=b64(np.asarray(t.vertices,np.float32)),n=b64(np.asarray(t.vertex_normals,np.float32)),i=b64(np.asarray(t.faces,np.uint32)))
ST='#c4c9cf'; parts=[]
def add(pid,grp,col,metal=False): parts.append(rec(pid,N[pid],grp,col,metal))
add('plate','head','#3f6fb5'); add('slab','head','#5b8fd6'); add('cplate','head','#e0a030'); add('cover','head','#58a36c'); parts.append(rec('spacer',N['spacer'],'head','#7a8794')); add('spacer2','head','#7a8794'); add('ebb','head','#1f7a3d'); parts.append(rec('ebbenv',N['ebbenv'],'head','#9aa3ad',False,0.25)); add('ebbscrews','head',ST,True)
for k,c in (('g1','#c9a227'),('dg','#b98b1e'),('brg','#9aa3ad'),('motor','#2b2f35'),('axles',ST),('pivot',ST),('mags_h','#8b8f96'),('gpins',ST),('tapscrews',ST),('mscrews',ST),('cscrews',ST),('inserts','#c8a24a'),('adj',ST),('spring','#7f9bb8')): add(k,'head',c,True)
g,v,t,c,m=old['tap']; parts.append(rec('tap',trimesh.Trimesh(v,t,process=False),'head','#8d949c',True))
for k in ('duct','fans','dscrew','ins_duct'):
    g,v,t,c,m=old[k]; parts.append(rec(k,trimesh.Trimesh(v,t,process=False),'head',c,bool(m)))
add('arm','arm','#d9622b'); add('g2','arm','#c9a227',True); add('g2ax','arm',ST,True); add('ascrew','arm',ST,True)
add('tool','tool','#8a6ff0')
for k,c in (('balls',ST),('mags_t','#8b8f96'),('hooks','#3a3d42'),('steel','#3a3d42'),('m25',ST)): add(k,'tool',c,True)
add('ptfe','tool','#e8e8e2'); add('fil','tool','#e24a8d')
for k in old:
    if k.startswith(('tz_','dr_','fscrew_')):
        g,v,t,c,m=old[k]; parts.append(rec(k,trimesh.Trimesh(v,t,process=False),'tz' if 'tz' in k else 'dr',c,bool(m)))
add('dock','dock','#3aa6a0'); parts.append(rec('pad',N['pad'],'dock','#b3261e'))
for k,c in (('dpin',ST),('dmag','#8b8f96'),('m5',ST),('tnut','#aeb5bd'),('dset',ST)): add(k,'dock',c,True)
parts.append(rec('rail',to_tm(box(-100,100,-54,-34,50,70)),'rail','#b9bec4',True))
LS=B.LS; LP=B.LP; LG=B.LG
Cc=dict(PIV=[float(B.PIV[0]),float(B.PIV[1])],SHIFT=B.SHIFT,DODGE=B.DODGE,SAFE=B.SAFE,PITCH=B.PITCH,XPIN=B.XPIN,SX=B.SCR[0],SY=B.SCR[1],YTIP=5.25,SGN=-1,LS=LS,LP=LP,LG=LG,PHI=float(B.PHI_MAX),K=6.25,F0=round(40*LG/LS,1))
bom=[
 ['Printed – head',1,0,'01 Back plate body','bolts to the Tap face; lower coupling grooves, duct ears, and a frame around the motor',['plate']],
 ['Printed – head',1,0,'02 Back plate front slab','carries the motor, the dual-gear pocket, the pivot and the spring adjuster',['slab']],
 ['Printed – head',1,0,'03 Coupling plate','covers the dual gear; top coupling groove and magnets; holds the back of the fixed gear axle',['cplate']],
 ['Printed – head',1,0,'04 Gear housing','thick front with a side wall around the fixed gear; front support for its axle and the dual gear',['cover']],
 ['Printed – head',1,0,'05 Swing arm','carries the idler gear between two webs; the dock pin pushes the screw at its foot',['arm']],
 ['Printed – head',2,0,'06 SB2209 spacer','between the board and the right side of the head',['spacer','spacer2']],
 ['Printed – head',1,0,'09 Duct and fan mount (from v32, unchanged)','hangs under two ears on the back plate',['duct']],
 ['Printed – per tool',0,1,'10 Tool body','front beam links the lower and upper filament guides; three ball pins and magnets locate it',['tool']],
 ['Printed – per tool',0,1,'4010 fan shroud (TZ-V6 or Dragon HF)','unchanged from v32',['tz_sh','dr_sh']],
 ['Printed – per tool',0,1,'13 Dock with wiper','one part: hook slots, opener pin, side walls and a floor with the silicone strip under the nozzle',['dock']],
 ['Extruder',1,0,'HGX gear set (2 hobbed 37T gears)','one fixed, one on the swing arm; each axle held at both ends',['g1','g2']],
 ['Extruder',1,0,'17/44 dual gear (module 0.5)','between the motor pinion and the fixed gear, as CxChanger',['dg']],
 ['Extruder',2,0,'MR63 bearing 3 × 6 × 2.5','dual gear',['brg']],
 ['Extruder',1,0,'LDO-36STH20 motor with 10T pinion','the CW2 motor; sits above the Tap',['motor']],
 ['Extruder',1,0,'BMG / CW2 idler spring','stock spring; pushes the top of the swing arm',['spring']],
 ['Extruder',1,0,'M3×35 SHCS + 2 M3 nuts','spring adjuster: captive nut in the slab, nyloc as the collar',['adj']],
 ['Extruder',2,0,'Dowel pin Ø3 × 16','gear axles',['axles','g2ax']],
 ['Extruder',1,0,'Dowel pin Ø3 × 24','swing-arm pivot',['pivot']],
 ['Extruder',1,0,'M3×20 SHCS','contact screw at the foot of the swing arm',['ascrew']],
 ['Coupling',6,0,'Dowel pin Ø1.5 × 5','three V grooves',['gpins']],
 ['Coupling',0,3,'Round-head pin Ø3 × 6','the three balls on the tool',['balls']],
 ['Coupling',6,6,'Magnet Ø6 × 2.65','head: 2 top + 2×2 below; tool the same',['mags_h','mags_t']],
 ['Electronics',1,0,'EBB SB2209 USB main board','on the right side, upright, long edge front to back as on a CW2; the grey boxes are the space its connectors take',['ebb','ebbenv']],
 ['Electronics',1,0,'Part cooling fans','as v32',['fans']],
 ['Fasteners',2,0,'M3×16 SHCS','plate → Tap, top holes',['tapscrews']],
 ['Fasteners',2,0,'M3×8 SHCS','plate → Tap, bottom holes',['tapscrews']],
 ['Fasteners',5,0,'M3×8 / M3×6 / M3×10 SHCS','motor (2) and slab → body (3, self-tapping)',['mscrews']],
 ['Fasteners',2,0,'M3×30 and M3×20 countersunk + 1 heat-set insert','gear housing → coupling plate → slab (the long one goes on into the body)',['cscrews','inserts']],
 ['Fasteners',2,0,'M3×12 SHCS','board → gear housing and slab, through the spacers, self-tapping',['ebbscrews']],
 ['Fasteners',2,0,'M3×10 SHCS','plate ears → inserts in the duct legs',['dscrew','ins_duct']],
 ['Fasteners',0,4,'M2.5×12 SHCS','tool body → hotend, through the shroud',['m25']],
 ['Fasteners',0,2,'M3×12 SHCS, grade 12.9','hook screws on the tool',['hooks']],
 ['Fasteners',0,1,'M3×5 set screw, steel','in the tool front, facing the dock magnet',['steel']],
 ['Dock',0,1,'Silicone strip 10 × 2 × 16 mm, self-adhesive, heat-resistant','the nozzle slides 3 mm across it at every tool change and rests on it when parked',['pad']],
 ['Dock',0,1,'Pin Ø5 × 30, one end rounded','opens the swing arm',['dpin']],
 ['Dock',0,1,'Magnet Ø6 × 2.65','holds the parked tool',['dmag']],
 ['Dock',0,2,'M5×10 SHCS + T-nut','dock → rail',['m5','tnut']],
 ['Dock',0,1,'M3×6 set screw','locks the pin',['dset']],
]
D=dict(parts=parts,c=Cc,bom=bom)
s=open('shell_old.html').read()
a=s.index('<script type="module">'); head=s[:a]
def sub(x,y):
    global head
    assert x in head,x[:50]; head=head.replace(x,y)
sub('<title>Hotend Changer v32.4</title>','<title>Hotend Changer v36 draft</title>')
sub('Hotend changer · v32.4','Hotend changer · v36 draft (HGX gears, arm on the left)')
sub('aria-label="Idler opening">','aria-label="Swing arm opening">')
sub('<button data-v="open">Opener</button><button data-v="tens">Pull rod</button><button data-v="trip">Dock shaft</button>','<button data-v="gears">Gears</button><button data-v="back">Back</button><button data-v="pin">Opener pin</button>')
sub('aria-label="3D model of the head, tool and dock"','aria-label="3D model of the head, tools and docks"')
js=r'''<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
const $=id=>document.getElementById(id);
const D=JSON.parse($('data').textContent), C=D.c;
const canvas=$('c'), R=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true}); R.setPixelRatio(Math.min(devicePixelRatio,2)); R.outputColorSpace=THREE.SRGBColorSpace; R.localClippingEnabled=true;
const scene=new THREE.Scene(); scene.environment=new THREE.PMREMGenerator(R).fromScene(new RoomEnvironment(),0.04).texture;
const L=new THREE.DirectionalLight(0xffffff,1); L.position.set(100,-200,300); scene.add(L);
const cam=new THREE.PerspectiveCamera(30,1,1,5000); cam.up.set(0,0,1); const ctl=new OrbitControls(cam,canvas); ctl.enableDamping=true;
const f=s=>{const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u.buffer;};
const G={}; ['head','arm','tool','tz','dr','dock','rail'].forEach(k=>G[k]=new THREE.Group());
const headG=new THREE.Group(); scene.add(headG,G.tool,G.dock,G.rail); headG.add(G.head);
const piv=new THREE.Group(); piv.position.set(C.PIV[0],0,C.PIV[1]); G.arm.position.set(-C.PIV[0],0,-C.PIV[1]); piv.add(G.arm); headG.add(piv);
G.tool.add(G.tz,G.dr); G.dr.visible=false;
const clip=new THREE.Plane(new THREE.Vector3(1,0,0),0), planes=[];
const meshes={}, mats=[];
function mat(col,op,metal){const m=new THREE.MeshStandardMaterial({color:col,roughness:metal?.32:.55,metalness:metal?.85:.05,transparent:op<1,opacity:op,depthWrite:op>=1,side:THREE.DoubleSide,clippingPlanes:planes,clipShadows:true});m.userData.op=op;mats.push(m);return m;}
for(const p of D.parts){const g=new THREE.BufferGeometry(); g.setAttribute('position',new THREE.BufferAttribute(new Float32Array(f(p.v)),3)); g.setAttribute('normal',new THREE.BufferAttribute(new Float32Array(f(p.n)),3)); g.setIndex(new THREE.BufferAttribute(new Uint32Array(f(p.i)),1));
 const m=new THREE.Mesh(g,mat(p.col,p.op,p.metal)); G[p.grp].add(m); meshes[p.id]=m;}
// neighbours: a dock and a parked tool on each side (same materials, so toggles and see-through apply to them too)
for(const s of [-1,1]){const d=G.dock.clone(); d.position.x=s*C.PITCH; scene.add(d); const t=G.tool.clone(); t.position.x=s*C.PITCH+C.SHIFT; scene.add(t);}
// swing arm: phi (rad) opens the idler. The dock pin pushes the screw at the arm's foot as the head shifts.
function pinPhi(hx,hy){const ys=C.SY+hy; if(ys>C.YTIP+2.5) return 0; const r=ys<=C.YTIP?2.5:Math.sqrt(Math.max(0,6.25-(ys-C.YTIP)**2));
 return Math.max(0,((C.SX+hx)-(C.XPIN-r-1.5))/C.LP);}
function setArm(phi){piv.rotation.y=phi; const Fs=C.F0+C.K*C.LS*phi; return {Fs,push:Fs*C.LS/C.LP,grip:C.F0*C.LS/C.LG,open:phi*C.LG};}
// BOM
let NT=4; const rows=[]; let iso=null;
function setIso(r){iso=(iso===r)?null:r; refresh();}
function refresh(){rows.forEach(x=>x.tr.classList.toggle('iso',x===iso));
 const keep=new Set(iso?iso.ids:[]);
 for(const [id,m] of Object.entries(meshes)){const M=m.material; if(iso&&!keep.has(id)){M.transparent=true;M.opacity=.06;M.depthWrite=false;} else {M.opacity=xray&&XR.includes(id)?.15:M.userData.op;M.transparent=M.opacity<1;M.depthWrite=M.opacity>=1;}}}
function buildBom(){const box=$('bom'); box.innerHTML=''; rows.length=0; const secs={};
 for(const [sec,qh,qt,item,note,ids] of D.bom){if(!secs[sec]){const d=document.createElement('details'); d.innerHTML=`<summary>${sec}<small></small></summary><table></table>`; box.appendChild(d); secs[sec]={d,t:d.querySelector('table'),n:0};}
  const q=qh+qt*NT; secs[sec].n+=q; const tr=document.createElement('tr'); tr.className=ids.length?'r':'r none';
  const col=ids.length&&meshes[ids[0]]?'#'+meshes[ids[0]].material.color.getHexString():'transparent';
  tr.innerHTML=`<td class="c">${ids.length?'<input type="checkbox" checked aria-label="show">':''}</td><td class="q">${q}</td><td class="n"><span class="sw" style="background:${col}"></span>${item}<span class="nt">${note}${qt&&qh?` · ${qh} head + ${qt}/tool`:qt?` · ${qt} per tool`:''}</span></td>`;
  const r={tr,ids}; rows.push(r); secs[sec].t.appendChild(tr);
  const cb=tr.querySelector('input'); if(cb) cb.onchange=()=>ids.forEach(i=>meshes[i]&&(meshes[i].visible=cb.checked));
  if(ids.length) tr.querySelector('.n').onclick=()=>setIso(r);}
 for(const s of Object.values(secs)) s.d.querySelector('small').textContent=s.n+' pcs';}
$('nt').oninput=e=>{NT=Math.max(1,Math.min(12,+e.target.value||1)); const open=[...document.querySelectorAll('#bom details')].map(d=>d.open); buildBom(); document.querySelectorAll('#bom details').forEach((d,i)=>d.open=open[i]);};
$('ex').onclick=()=>{const ds=[...document.querySelectorAll('#bom details')],o=!ds.every(d=>d.open);ds.forEach(d=>d.open=o);$('ex').textContent=o?'Collapse all':'Expand all';};
$('rs').onclick=()=>{iso=null;rows.forEach(r=>{r.tr.classList.remove('iso');const cb=r.tr.querySelector('input');if(cb)cb.checked=true;});Object.values(meshes).forEach(m=>m.visible=true);refresh();};
// timeline: release, then pickup. Dock frame: the head is at (0,0) when the hook screws sit in the large holes.
const cl=x=>Math.max(0,Math.min(1,x)), ss=t=>{t=cl(t);return t*t*(3-2*t);};
const K=[0,.16,.28,.42,.5,.62,.74,.86,1]; const seg=(s,i)=>ss((s-K[i])/(K[i+1]-K[i])), mix=(a,b,t)=>a+(b-a)*t;
const S=C.SHIFT, Dg=C.DODGE, F=C.SAFE;
function apply(s){
 let hx=0,hy=F,att=true,txt='';
 if(s<K[1]){hy=mix(F,0,seg(s,0));txt='1 release: head moves in; the hook screws pass through the large holes of the dock';}
 else if(s<K[2]){hy=0;hx=mix(0,S,seg(s,1));txt='2 shift 3 mm right: the hooks slide into the slots and the dock pin pushes the swing arm open';}
 else if(s<K[3]){hx=S;hy=mix(0,Dg,seg(s,2));att=false;txt='3 head backs out 14 mm: magnets let go, the gears slide off the filament, then the arm closes';}
 else if(s<K[4]){hy=mix(Dg,F,cl(seg(s,3)*1.5));hx=mix(S,0,cl(seg(s,3)*3-2));att=false;txt='4 head leaves, still shifted, and only moves back sideways once it is clear';}
 else if(s<K[5]){hy=mix(F,Dg,cl(seg(s,4)*1.5-0.5));hx=mix(0,S,cl(seg(s,4)*3));att=false;txt='5 pickup: head comes back, already shifted 3 mm right';}
 else if(s<K[6]){hx=S;hy=mix(Dg,0,seg(s,5));att=false;txt='6 head moves in: the round pin tip opens the arm, the gears slide over the filament, magnets grab';}
 else if(s<K[7]){hy=0;hx=mix(S,0,seg(s,6));txt='7 shift 3 mm left: the arm closes on the filament, the hooks reach the large holes';}
 else {hy=mix(0,F,seg(s,7));txt='8 head leaves with the tool';}
 headG.position.set(hx,hy,0); G.tool.position.set(att?hx:S,att?hy:0,0);
 const phi=pinPhi(hx,hy); status(txt,phi,att); $('ph').value=phi/C.PHI;}
function status(txt,phi,att){const r=setArm(phi);
 $('st').textContent=`${txt}\nidler open ${r.open.toFixed(2)} mm   spring ${r.Fs.toFixed(0)} N   push on pin ${phi>0?r.push.toFixed(0):'0'} N\ngrip set to ${r.grip.toFixed(0)} N   tool ${att?'on head':'in dock'}`;}
let playing=false,t=0; const stop=()=>{playing=false;$('play').classList.remove('on');};
$('play').onclick=()=>{playing=!playing; $('play').classList.toggle('on',playing);};
$('s').oninput=e=>{stop();apply(+e.target.value);};
$('ph').oninput=e=>{stop();status('swing arm only (as if pushed by hand)',C.PHI*(+e.target.value),true);};
let xray=false; const XR=['plate','slab','cplate','cover','motor','tap','duct','ebbenv'];
$('xr').onclick=()=>{xray=$('xr').classList.toggle('on'); refresh();};
// section cut
let cax='0',cs=1; const N={x:[1,0,0],y:[0,1,0],z:[0,0,1]};
function cut(){planes.length=0; if(cax!=='0'){clip.normal.set(...N[cax]).multiplyScalar(-cs); clip.constant=cs*(+$('cp').value); planes.push(clip);} mats.forEach(m=>m.needsUpdate=true);}
document.querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{cax=b.dataset.c;document.querySelectorAll('[data-c]').forEach(x=>x.classList.toggle('on',x===b));
 const r={x:[-70,70,0],y:[-60,45,2],z:[-20,140,74],'0':[-70,140,0]}[cax]; $('cp').min=r[0];$('cp').max=r[1];$('cp').value=r[2];cut();});
$('cp').oninput=cut; $('cf').onclick=()=>{cs=-cs;cut();};
const hs=k=>{G.tz.visible=k==='z';G.dr.visible=k==='d';$('hz').classList.toggle('on',k==='z');$('hd').classList.toggle('on',k==='d');};
$('hz').onclick=()=>hs('z'); $('hd').onclick=()=>hs('d');
const V={fr:[[230,-300,210],[0,0,60]],fl:[[-250,-290,190],[0,0,60]],side:[[-340,10,75],[0,5,62]],gears:[[20,-230,120],[0,0,84]],back:[[150,300,180],[0,10,65]],pin:[[-150,-150,95],[-14,-6,66]],dock:[[-90,-230,170],[0,-20,55]]};
function view(k){cam.position.set(...V[k][0]); ctl.target.set(...V[k][1]); ctl.update();}
document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>view(b.dataset.v)); view('fr');
function rs(){const r=canvas.parentElement.getBoundingClientRect(); R.setSize(r.width,r.height,false); cam.aspect=r.width/Math.max(1,r.height); cam.updateProjectionMatrix();}
addEventListener('resize',rs); rs(); buildBom(); apply(0);
window.MM=meshes; window.VIEW=view; window.APPLY=apply; window.CAM=cam; window.CTL=ctl;
let last=performance.now();
(function loop(now){const dt=(now-last)/1000; last=now; if(playing){t=(t+dt/20)%1; $('s').value=t; apply(t);} ctl.update(); R.render(scene,cam); requestAnimationFrame(loop);})(last);
</script>
</body></html>'''
out=(head+js).replace('@@DATA@@',json.dumps(D,separators=(',',':')))
open('v36/index.html','w').write(out); print('wrote',len(out),'parts',len(parts))
