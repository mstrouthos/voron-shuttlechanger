"""collision checks for v33: static, arm sweep, tool-change sweep with neighbours"""
import numpy as np, manifold3d as mf, pickle, trimesh, itertools, sys
import build36 as B
from geo import to_mf
P=B.build(); H=B.hardware(); A={**P,**H}
old=pickle.load(open("old_parts.pkl","rb"))
def oldm(k):
    g,v,t,c,m=old[k]; tm=trimesh.Trimesh(v,t,process=True); m=to_mf(tm); return m if m.status()==mf.Error.NoError and m.volume()>0 else None
for k in ('tap','duct','fans','dscrew','ins_duct','tz_he','tz_bl','tz_sh','tz_fan','fscrew_tz','dr_he','dr_bl','dr_sh','dr_fan'):
    m=oldm(k)
    if m is None: print('old mesh not solid, skipped:',k)
    else: A[k]=m
HOT=[k for k in ('tz_he','tz_bl','tz_sh','tz_fan','fscrew_tz','dr_sh','dr_he','dr_bl','dr_fan') if k in A]
ARMG=B.ARMG; TOOLG=B.TOOLG+HOT; DOCKG=B.DOCKG
HEADG=[k for k in A if k not in ARMG+TOOLG+DOCKG and not k.startswith('dr_')]
def vol(a,b): return (a^b).volume()
# pairs that are meant to touch or sit inside one another
OKP={frozenset(p) for p in [('plate','slab'),('slab','cplate'),('slab','cover'),('cplate','cover'),('slab','gpins'),('cplate','gpins'),('cplate','mags_h'),('slab','mags_h'),('slab','axles'),('cplate','axles'),('cover','axles'),('g1','axles'), ('slab','brg'),('cover','brg'),('dg','brg'),('slab','pivot'),('arm','pivot'),('slab','inserts'),('inserts','cscrews'),('slab','cscrews'),('cplate','cscrews'),('cover','cscrews'),('plate','cscrews'), ('slab','mscrews'),('plate','mscrews'),('motor','mscrews'),('slab','adj'),('arm','adj'),('arm','spring'),('adj','spring'),('g1','g2'),('g1','dg'),('dg','motor'),('g1','fil'),('g2','fil'),('arm','g2ax'),('g2','g2ax'), ('slab','ebbins'),('slab','ebbscrews'),('slab','motor'),('cplate','dg'), ('plate','gpins'),('plate','mags_h'),('plate','axles'),('plate','pivot'),('plate','inserts'),('plate','adj'),('cover','axles'),
     ('g1','axles'),('dg','brg'),('arm','g2ax'),('g2','g2ax'),('arm','ascrew'),('arm','pivot'),('tool','balls'),('tool','mags_t'),('tool','hooks'),('tool','steel'),
     ('tool','m25'),('tool','ptfe'),('tool','fil'),('ptfe','fil'),('dock','dpin'),('dock','dmag'),('dock','m5'),('dock','dset'),('g1','g2'),('g1','dg'),('dg','motor'),
     ('balls','gpins'),('g1','fil'),('g2','fil'),('m25','tz_he'),('m25','tz_sh'),('m25','dr_sh'),('m25','dr_he'),('fil','tz_he'),('fil','tz_bl'),('fil','dr_he'),('tz_he','tz_sh'),('tz_sh','tz_fan'),
     ('fscrew_tz','tz_sh'),('fscrew_tz','tz_fan'),('tz_he','tz_bl'),('inserts','cscrews'),('plate','tapscrews'),('tap','tapscrews'),('motor','mscrews'),('plug','brg'),('adj','spring'),('dpin','dset'),
     ('cover','brg'),('cover','cscrews'),('plate','cscrews'),('plate','mscrews'),('arm','spring'),('arm','adj'),('tnut','m5'),('cover','ebbscrews'),('slab','ebbscrews'),('spacer','ebbscrews'),('spacer2','ebbscrews'),('ebb','ebbscrews'),('ebbenv','ebbscrews'),('ebb','ebbenv'),('spacer','ebbenv'),('spacer2','ebbenv'),('dock','pad'),('pad','tz_bl'),('pad','dr_bl'),('spacer','ebbscrews'),('spacer2','ebbscrews'),('ebbmount','ebbins'),('ebbmount','ebbscrews'),('spacer','ebbenv'),('spacer2','ebbenv'),('slab','brg'),('slab','shaft'),('slab','mags_h'),('slab','gpins'),('slab','pivot'),('slab','adj'),('slab','mscrews'),('slab','ebbscrews'),('slab','ebbins'),('plate','slab'),('arm','pivot'),('plate','ebbins'),('gd','shaft'),('g50','shaft'),('brg','shaft'),('plate','brg'),('gd','gi'),('gd','fil'),('gi','fil'),('arm','giax'),('gi','giax'),('g50','motor'),('plate','shaft'),('plug','shaft'),('ebb','ebbenv'),('ebb','ebbscrews'),('ebbenv','ebbscrews'),('ebbmount','ebbscrews'),('plate','ebbscrews'),('ebb','ebbmount'),('ebbins','ebbscrews'),('plate','ebbins'),('duct','ins_duct'),('duct','dscrew'),('ins_duct','dscrew'),('plate','dscrew'),('duct','fans')]}
def rep(tag,ga,gb,Ta=None,Tb=None,thr=0.3):
    bad=[]
    for a in ga:
        ma=A[a] if Ta is None else Ta(A[a])
        for b in gb:
            if a==b or frozenset((a,b)) in OKP: continue
            mb=A[b] if Tb is None else Tb(A[b]); v=vol(ma,mb)
            if v>thr: bad.append((a,b,round(v,1)))
    if bad: print(tag,bad)
    return bad
print('== static, tool on head, arm closed')
allg=[k for k in HEADG+ARMG+TOOLG if not k.startswith('dr_')]
n=0
for a,b in itertools.combinations(allg,2):
    if frozenset((a,b)) in OKP: continue
    v=vol(A[a],A[b])
    if v>0.3: print('  ',a,b,round(v,1)); n+=1
print('  overlaps:',n)
print('== arm sweep')
for ph in np.linspace(0,B.PHI_MAX*1.15,6):
    T=lambda m: B.rotY(m,B.PIV,ph)
    rep('  phi %.1f deg'%np.degrees(ph),ARMG,HEADG+TOOLG,Ta=T)
def phi_at(hx,hy):
    """arm angle forced by the dock pin with the head at (hx,hy) from the dock"""
    ys=B.SCR[1]+hy                         # contact screw y in the dock frame
    if ys>5.25+2.5: return 0.0
    r=2.5 if ys<=5.25 else np.sqrt(max(0,2.5**2-(ys-5.25)**2))
    need=(B.SCR[0]+hx)-(B.XPIN-r-1.5)      # mirrored: how far the screw must sit left of where the closed arm puts it
    return max(0.0,need/(B.PIV[1]-B.ZPIN))
print('== tool change sweep (release then pickup), neighbours at +-%g'%B.PITCH)
path=[]
def seg(p0,p1,n,att):
    for t in np.linspace(0,1,n): path.append((p0[0]+(p1[0]-p0[0])*t,p0[1]+(p1[1]-p0[1])*t,att))
S,D,F=B.SHIFT,B.DODGE,B.SAFE
seg((0,F),(0,0),13,True); seg((0,0),(S,0),7,True); seg((S,0),(S,F),13,False); seg((S,F),(0,F),4,False)   # stay shifted until clear: the duct would catch a Dragon block otherwise
worst=0
for hx,hy,att in path:
    ph=phi_at(hx,hy); worst=max(worst,ph)
    Th=lambda m: m.translate([hx,hy,0]); Ta=lambda m: B.rotY(m,B.PIV,ph).translate([hx,hy,0])
    Tt=Th if att else (lambda m: m.translate([S,0,0]))
    tag='  head (%.1f,%.1f) %s phi %.1f'%(hx,hy,'tool on' if att else 'tool parked',np.degrees(ph))
    rep(tag+' head-dock',HEADG,DOCKG,Ta=Th); rep(tag+' arm-dock',ARMG,[k for k in DOCKG if k!='dpin'],Ta=Ta); rep(tag+' tool-dock',TOOLG,DOCKG,Ta=Tt)
    if not att: rep(tag+' head-tool',HEADG,TOOLG,Ta=Th,Tb=Tt); rep(tag+' arm-tool',ARMG,TOOLG,Ta=Ta,Tb=Tt)
    for s in (-1,1):
        Tn=lambda m: m.translate([s*B.PITCH+S,0,0]); Tnd=lambda m: m.translate([s*B.PITCH,0,0])
        rep(tag+' head-neigh%+d'%s,HEADG,TOOLG,Ta=Th,Tb=Tn); rep(tag+' arm-neigh%+d'%s,ARMG,TOOLG+DOCKG,Ta=Ta,Tb=Tn)
        rep(tag+' head-neighdock%+d'%s,HEADG,DOCKG,Ta=Th,Tb=Tnd)
        if att: rep(tag+' tool-neigh%+d'%s,TOOLG,TOOLG,Ta=Th,Tb=Tn); rep(tag+' tool-neighdock%+d'%s,TOOLG,DOCKG,Ta=Th,Tb=Tnd)
print('max arm angle from the pin: %.2f deg -> %.2f mm at the idler'%(np.degrees(worst),worst*(B.PIV[1]-B.G2[1])))
print('parked neighbours: tool-tool',round(vol(A['tool'],A['tool'].translate([B.PITCH,0,0])),2),'dock-dock',round(vol(A['dock'],A['dock'].translate([B.PITCH,0,0])),2))
