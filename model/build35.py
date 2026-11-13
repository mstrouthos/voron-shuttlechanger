"""v35 draft: CxChanger mechanism on a CNC Tap V2 with HGX gears, reshaped to print without supports.
Frame: X right, Y back, Z up, filament at x=0,y=0. Gear positions are CxChanger's (CAD 6.11)."""
import numpy as np, manifold3d as mf, pickle
from geo import *
from build34 import ok,rotY,cy,cx_,cz,tear,above,UPF
# ---------------- layout ----------------
G1=(-9.39,74.0); G2=(9.39,74.0); RG=9.75           # HGX gears, 37T m0.5, hob at y=0, teeth y 1.75..7.75
DG=(-10.26,87.7)                                    # 17/44 dual gear on MR63 bearings
MOT=(0.19,96.25)                                    # LDO-36STH20 with 10T pinion
PIV=np.array([14.54,92.0])
YF=10.25; YR=7.25; YT=22.5; YM=17.75; YSP=YM        # slab front, coupling-plate front, Tap face, motor face = slab back
YP2=7.95; YCF=-7.75                                 # front face of the cover and the arm                                            # coupling-plate front behind the fixed gear
ZSPL=65.6; ZRAISE=84.2; ZP2=108.3; ZS=111.5; YS=4.6; ZTOP=121.5
TOPB=(0.0,92.0); LOWB=[(-16.5,46.5),(16.5,46.5)]
CEN=(0.0,(TOPB[1]+2*46.5)/3)
MAG_T=[(0.0,98.2),(0.0,104.4)]; MAG_L=[(-12.6,52.0),(12.6,52.0)]
TAP_TOP=[(-15.7,62.4),(15.05,62.4)]; TAP_LOW=[(-17.9,11.9),(17.45,11.9)]
EAR=21.92; u=np.array([np.cos(np.radians(158)),np.sin(np.radians(158))])   # ears turned so the upper screw clears the spring boss
MS=[(MOT[0]+EAR*u[0],MOT[1]+EAR*u[1]),(MOT[0]-EAR*u[0],MOT[1]-EAR*u[1])]
PA=(-22.65,69.5); PB=(-22.65,98.5); XLT=-26.5; ZLT=107.0   # cover screws; the plate has a tab on the left for them  # cover posts A, B and a third screw for the coupling plate
J=[(-20.5,109.0),(20.5,112.0),(20.5,69.8)]   # slab -> body, self-tapping
BOSS=(-17.0,-5.0)
ARM_SEAT=13.5; SCR=(22.4,-1.0)
ZPIN=60.0; XPIN=SCR[0]-1.5-2.5-0.3
SHIFT=-3.0; DODGE=14.0; SAFE=30.0; PITCH=54.0
YTF=-9.5; HOOK=[(-11.5,50.0),(11.5,50.0)]; WB=19.2; ZSTEM=107.9
PHI_MAX=(abs(SHIFT)-0.3)/(PIV[1]-ZPIN)
EB_HOLE=[(3.0,90.73),(14.98,103.5)]                 # SB2209 screws (y,z) in the side of the gear housing and of the slab, 12 x 12.8 apart as on the board
DUCT=[(-26.3,17.05),(26.3,17.05)]
ZNOZ=-8.0; WX=(SHIFT/2-8.0,SHIFT/2+8.0)
ARM_LOW=[(24.9,63.0),(19.9,63.0),(19.9,66.5),(5.0,70.0),(5.0,78.0),(10.5,84.2)]
def groove(b,yf):
    d=np.array(CEN)-np.array(b); a=np.degrees(np.arctan2(d[1],d[0]))
    g=box(-2.5,2.5,yf-0.1,yf+1.0,-2.95,2.95)+box(-1.9,1.9,yf-0.1,yf+2.0,-1.45,1.45)
    return g.rotate([0,-a,0]).translate([b[0],0,b[1]])
def build():
    P={}
    armpk=prism_xz([(3.0,61.5),(31.0,61.5),(31.0,86.0),(3.0,86.0)],YF-0.1,12.25)
    # ---------- back plate body: Tap face, lower coupling, duct ears, and a frame behind the slab around the motor ----------
    b=union(box(-23.5,23.5,14.0,YT,8.5,41.5), box(-25,25,YF,YT,41.5,ZSPL), box(-25,25,YSP,YT,ZSPL-0.1,ZTOP), box(XLT,-24.9,YSP,YT,ZSPL-0.1,ZLT))
    ear=mf.Manifold.hull_points([(m[0]+4.3*np.cos(a),y,m[1]+4.3*np.sin(a)) for m in MS for a in np.linspace(0,6.28,32) for y in (YSP-1,YT+1)])
    b-=cy(MOT,18.6,YSP-1,YT+1)+ear+box(MS[1][0],25.1,YSP-1,YT+1,MS[1][1]-4.3,MS[1][1]+4.3)                                  # the motor passes through and bolts to the slab
    for x,z in TAP_TOP: b-=cy((x,z),1.7,YF-1,YT+1)+cy((x,z),3.1,YF-1,15.25)+box(x-3.1,x+3.1,YF-1,15.25,z,ZSPL+1)
    for x,z in TAP_LOW: b-=cy((x,z),1.7,13,YT+1)+cy((x,z),3.1,13,17.5)+box(x-3.1,x+3.1,13,17.5,8.4,z)
    b-=armpk
    for lb in LOWB: b-=groove(lb,YF)
    for m in MAG_L: b-=cy(m,3.05,YF-0.1,YF+4.85)
    for sx in (-1,1):
        x0,x1=sorted((sx*22.2,sx*25.1)); b-=box(x0,x1,YF-0.1,YT+0.1,41.0,55.7)
        x0,x1=sorted((sx*22.0,sx*29.5)); b+=box(x0,x1,13.2,YT,55.7,61.4)
    for x,y in DUCT: b-=tear('z',(x,y),1.7,55,62,UPF)
    for j in J+[PA]: b-=cy(j,1.25,YSP-1,YT+1)
    b^=above((-1,0,-1),-(25+ZTOP-8.0))
    P['plate']=ok(b,'plate')
    # ---------- front slab: gears, motor, pivot, spring adjuster ----------
    s=box(-25,25,YF,YSP,ZSPL,ZTOP)+box(XLT,-24.9,YF,YSP,ZSPL,ZLT)+box(BOSS[0],BOSS[1],-1.0,YF+0.1,ZS-4,ZS+4)
    s-=cy(DG,12.3,YF-1,15.3)+cy(DG,3.05,15,YSP+1)                    # dual-gear pocket, open to the front; rear bearing in its floor
    s-=cy(MOT,3.6,YF-1,15.4)+cy(MOT,8.3,15.3,YSP+1)+mf.Manifold.cylinder(4.75,8.3,3.55,64).rotate([90,0,0]).translate([MOT[0],15.35,MOT[1]])   # boss hole, then a 45 deg cone down to the pinion hole                  # pinion, and the motor boss that centres the motor
    s-=cy(MS[0],1.7,YF-1,YSP+1)+cy(MS[0],3.1,YF-1,13.45)+cy(MS[1],1.7,YF-1,YSP+1)+cy(MS[1],3.1,YF-1,15.25)
    for j in J: s-=cy(j,1.7,YF-1,YSP+1)+cy(j,3.1,YF-1,15.25 if j[1]<86 and j[0]>3 else 13.4)
    s-=cy(PA,1.7,YF-1,YSP+1)
    s-=cy(PB,2.35,YF-0.1,YF+5.5)
    s-=armpk
    s-=cy(G1,1.5,YF-1,11.4)
    s-=cy(tuple(PIV),1.5,YF-1,16.25)
    s-=tear('x',(YS,ZS),1.7,BOSS[0]-1,BOSS[1]+1,UPF)+box(-9.3,-6.7,YS-2.85,YS+2.85,ZS-2.8,ZS+4.1)
    s-=cx_(EB_HOLE[1][0],EB_HOLE[1][1],1.25,XLT-0.1,-22.9)            # self-tapping, for the SB2209
    s^=above((-1,0,-1),-(25+ZTOP-8.0))                               # faceted top right corner
    P['slab']=ok(s,'slab')
    # ---------- coupling plate: covers the dual gear, carries the top groove and magnets, holds the back of the fixed gear's axle ----------
    c=prism_xz([(XLT,65.9),(-0.5,65.9),(-0.5,ZRAISE),(XLT,ZRAISE)],YP2,YF)+prism_xz([(XLT,ZRAISE-0.05),(6.5,ZRAISE-0.05),(6.5,ZP2),(-4.5,ZP2),(-4.5,ZLT),(XLT,ZLT)],YR,YF)
    c-=cy(DG,5.4,YR-1,YF+1)+cy(G1,1.5,YR-1,YF+1)
    c-=groove(TOPB,YR)
    c-=cy(MAG_T[0],3.05,YR-0.1,YR+2.2)+cy(MAG_T[1],3.05,YR-0.1,YR+2.2)+box(-3.05,3.05,YR-0.1,YR+2.2,MAG_T[0][1],MAG_T[1][1])
    for p in (PA,PB): c-=cy(p,1.7,YR-1,YF+1)
    P['cplate']=ok(c,'cplate')
    # ---------- left gear housing: a thick faceted front with a side wall back to the coupling plate (as CxChanger's cover) ----------
    out=np.array([(XLT,69.0),(XLT+3,65.9),(-4.8,65.9),(-4.8,93.0),(-9.0,102.2),(XLT+3,102.2),(XLT,99.0)])
    def slab_(o,y0,y1): return prism_xz([tuple(p) for p in o],y0,y1)
    cen=out.mean(0); ins=cen+(out-cen)*np.array([1-2.5/10.2,1-2.5/18.2])            # front face pulled in 2.5 mm all round
    cv=mf.Manifold.batch_hull([slab_(out,YCF+2.5,YCF+2.6),slab_(ins,YCF,YCF+0.05)])+slab_(out,YCF+2.55,1.75)
    cv+=(slab_(out,1.0,YP2)^box(XLT-1,-19.8,0,YP2+1,60,ZRAISE+0.3))+(slab_(out,1.0,YR)^box(XLT-1,-19.8,0,YR+1,ZRAISE,110))   # side wall back to the coupling plate
    cv-=cy(G1,RG+0.5,-1.5,9)+cy(G1,1.5,-3.25,0)
    cv-=cy(DG,3.05,-0.85,2)+cy(DG,5.4,1.0,9)
    for p,yb_ in ((PA,YP2),(PB,YR)): cv-=cy(p,1.7,YCF-1,yb_+1)+mf.Manifold.cylinder(1.6,3.2,1.6,48).rotate([-90,0,0]).translate([p[0],YCF-0.05,p[1]])   # countersunk
    cv-=cx_(EB_HOLE[0][0],EB_HOLE[0][1],1.25,XLT-0.1,-20.5)
    P['cover']=ok(cv,'cover')
    # ---------- swing arm: thick, with the gear between two webs and a 7 mm spine ----------
    XA=27.0
    low=[(XA,63.0),(19.9,63.0),(19.9,66.5),(5.0,70.0),(5.0,78.0),(10.5,84.2)]
    web=low+[(10.5,ZS+4.5),(XA,ZS+4.5)]
    arm=prism_xz(web,YCF,9.75)+prism_xz(low+[(XA,84.0)],9.7,11.75)
    arm^=above((-1,-1,0),-(XA-YCF-2.5))   # chamfers: front edge of the spine, top corner
    arm^=above((0,1,-1),YCF-(ZS+4.5)+3.0)                                               # top front edge
    arm-=cy(G2,RG+0.5,-1.6,8.45)+box(4,19.85,-1.6,8.45,62,84.25)
    arm-=cy(G2,1.5,-4.25,12)
    arm-=tear('y',tuple(PIV),1.65,YCF-1,12,(-1,0,0))
    arm-=cx_(YS,ZS,3.3,10,ARM_SEAT)+box(ARM_SEAT-0.1,XA+1,YS-1.8,YS+1.8,ZS-2.5,ZS+2.5)
    arm-=cz(SCR[0],SCR[1],1.25,62,71)
    P['arm']=ok(arm,'arm')
    P['spacer']=ok(cx_(EB_HOLE[0][0],EB_HOLE[0][1],3.2,XLT-6.65,XLT-0.05)-cx_(EB_HOLE[0][0],EB_HOLE[0][1],1.7,XLT-8,XLT+1),'spacer')   # the board stands on two of these
    # ---------- tool body: prints upright on the base ----------
    up=box(-4.3,4.3,-10.1,6.5,70.0,ZSTEM)^above((0,-1,1),G1[1]+11.75)                          # upper guide with a 45 deg underside over the gears
    beam=(box(-8.0,8.0,-15.5,-10.0,56.0,ZSTEM)+box(-4.2,4.2,-10.05,-9.4,56.0,G1[1]-10.5))^above((0,1,1),46.6)
    t=union(box(-WB,WB,YTF,9.5,40.6,54.5), box(-4.2,4.2,YTF,9.5,54.5,G1[1]-10.5), up, beam)
    t-=cz(0,0,1.05,40,G1[1]-10.4)+cz(0,0,1.05,G1[1]+9,ZSTEM-7.9)+cz(0,0,2.15,ZSTEM-8.0,ZSTEM+1)
    for sx in (-1,1):
        t-=cz(sx*5.72,-5.72,1.45,40,43)+cz(sx*5.72,-5.72,2.3,42.8,140)
        t-=cz(sx*5.72,5.72,1.45,40,43)+cz(sx*5.72,5.72,2.3,42.8,55.5)+box(sx*5.72-2.3,sx*5.72+2.3,5.72,10,42.8,55.5)+cz(sx*5.72,5.72,1.4,55,140)
    for lb in LOWB: t-=cy(lb,1.5,5.0,10)
    t-=cy(TOPB,1.5,2.0,7)
    for m in MAG_L: t-=cy(m,3.05,4.2,10)+box(m[0]-3.05,m[0]+3.05,4.2,10,m[1],55)
    t-=cy(MAG_T[0],3.05,3.85,7)+box(-3.05,3.05,3.85,7,MAG_T[0][1],ZSTEM+1)
    for h in HOOK: t-=cy(h,1.25,YTF-1,-2.5)
    t-=cy((0,50.0),1.25,YTF-1,-4.25)
    P['tool']=ok(t,'tool')
    # ---------- dock with the nozzle wiper built in: one part, printed on its back (the rail face) ----------
    XL=-24.3+SHIFT; XR=24.2; zt=ZNOZ+0.2-2.0; zf=zt-4.5
    d=union(box(XL,XR,-34,-29.5,43,70), box(XL,-19.9,-34,-10.0,43,55.5), box(19.9,XR,-34,-10.0,43,55.5), box(XL,XR,-14.0,-10.0,43,55.5),
            box(14.5,XR,-34,-14.0,55.5,70.0), box(XL,-24.3,-34,-10.0,zf,43.1), box(20.5,XR,-34,-10.0,zf,43.1), box(XL,XR,-34,6.0,zf,zt+0.3))
    ab=box(-19.95,19.95,-34,-13.9,43,55.5); d+=(ab^above((-1,1,0),-14.0))+(ab^above((1,1,0),-14.0))
    for hx,hz in HOOK:
        d-=cy((hx,hz),3.25,-15,-9)+box(hx+SHIFT-0.2,hx,-15,-9,hz-1.75,hz+1.75)+cy((hx+SHIFT-0.2,hz),1.75,-15,-9)
        d-=box(hx+SHIFT-3.5,hx+3.25,-34.1,-14.0,hz-3.25,hz+3.25)
    d-=cy((SHIFT,50.0),3.05,-12.65,-9)
    d-=cy((XPIN,ZPIN),2.5,-24.0,-13)
    d-=cx_(-19.0,ZPIN,1.25,XPIN,25)
    for x in (-12.0,4.0): d-=cy((x,60.0),2.75,-35,-29)
    d-=box(WX[0],WX[1],-5.2,5.2,zt,zt+1)
    P['dock']=ok(d,'dock')
    return P
def hardware():
    H={}
    H['g1']=cy(G1,RG,1.75,7.75)+cy(G1,8.85,-1.25,1.75); H['g2']=cy(G2,RG,1.75,7.75)+cy(G2,8.85,-1.25,1.75)
    H['dg']=cy(DG,4.75,2.75,11.75)+cy(DG,11.62,11.75,15.2)+cy(DG,1.5,-0.75,17.7)
    H['brg']=(cy(DG,3.0,-0.75,1.75)-cy(DG,1.5,-1,2))+(cy(DG,3.0,15.3,YM)-cy(DG,1.5,15,YM+1))
    ear=mf.Manifold.hull_points([(m[0]+3.5*np.cos(a),y,m[1]+3.5*np.sin(a)) for m in MS for a in np.linspace(0,6.28,24) for y in (YM,YM+3)])
    H['motor']=cy(MOT,18.0,YM,YM+20)+ear+cy(MOT,8.0,YM-2.4,YM)+cy(MOT,3.0,YM-6,YM)
    H['axles']=cy(G1,1.5,-3.25,11.4)
    H['pivot']=cy(tuple(PIV),1.5,-7.75,16.25)
    H['mags_h']=cy(MAG_T[0],3.0,YR-0.45,YR+2.2)+cy(MAG_T[1],3.0,YR-0.45,YR+2.2)+cy(MAG_L[0],3.0,YF-0.45,YF+4.85)+cy(MAG_L[1],3.0,YF-0.45,YF+4.85)
    def pins(b,yf):
        d=np.array(CEN)-np.array(b); a=np.degrees(np.arctan2(d[1],d[0])); g=None
        for s in (-2.2,2.2):
            p=cx_(yf+0.25,s,0.75,-2.5,2.5,24).rotate([0,-a,0]).translate([b[0],0,b[1]]); g=p if g is None else g+p
        return g
    H['gpins']=pins(TOPB,YR)+pins(LOWB[0],YF)+pins(LOWB[1],YF)
    sc=None
    for x,z in TAP_TOP:
        s=cy((x,z),1.5,15.25,31.25)+cy((x,z),2.75,12.25,15.25); sc=s if sc is None else sc+s
    for x,z in TAP_LOW: sc+=cy((x,z),1.5,17.5,25.5)+cy((x,z),2.75,14.5,17.5)
    H['tapscrews']=sc
    sc=cy(MS[0],1.5,13.45,YM+3)+cy(MS[0],2.75,10.45,13.45)+cy(MS[1],1.5,15.25,YM+3)+cy(MS[1],2.75,12.25,15.25)
    for j in J:
        f=15.25 if j[1]<86 and j[0]>3 else 13.4; sc+=cy(j,1.5,f,YT+0.4)+cy(j,2.75,f-3,f)
    H['mscrews']=sc
    H['cscrews']=cy(PA,1.5,YCF,YCF+30)+cy(PB,1.5,YCF,YCF+22)
    q=None
    H['inserts']=cy(PB,2.3,YF,YF+5)-cy(PB,1.5,YF-1,YF+6)
    H['adj']=cx_(YS,ZS,1.5,BOSS[0]-1.5,18.5)+cx_(YS,ZS,2.75,BOSS[0]-4.5,BOSS[0]-1.5)+cx_(YS,ZS,3.1,-9.2,-6.8,6)+cx_(YS,ZS,3.1,2.65,5.05,6)
    H['spring']=cx_(YS,ZS,3.0,5.05,ARM_SEAT)-cx_(YS,ZS,2.2,5,ARM_SEAT+1)
    # arm group
    H['g2ax']=cy(G2,1.5,-4.25,11.75)
    H['ascrew']=cz(SCR[0],SCR[1],1.5,51,71)+cz(SCR[0],SCR[1],2.75,48,51)
    # tool group
    b=None
    for c in LOWB+[TOPB]:
        yb_=10.03 if c!=TOPB else 7.03
        s=cy(c,1.5,yb_-4.5,yb_)+mf.Manifold.sphere(1.5,32).translate([c[0],yb_,c[1]]); b=s if b is None else b+s
    H['balls']=b
    H['mags_t']=cy(MAG_T[0],3.0,3.85,6.5)+cy(MAG_T[1],3.0,3.85,6.5)+cy(MAG_L[0],3.0,4.2,9.5)+cy(MAG_L[1],3.0,4.2,9.5)
    hk=None
    for h in HOOK:
        s=cy(h,1.5,YTF-5.0,-2.5)+cy(h,2.75,YTF-8.0,YTF-5.0); hk=s if hk is None else hk+s
    H['hooks']=hk; H['steel']=cy((0,50.0),1.5,YTF,YTF+5)
    m=None
    for sx in (-1,1):
        for sy in (-1,1):
            s=cz(sx*5.72,sy*5.72,1.25,32.8,42.8)+cz(sx*5.72,sy*5.72,2.25,42.8,45.3); m=s if m is None else m+s
    H['m25']=m
    H['ptfe']=cz(0,0,2.0,ZSTEM-7.9,230)-cz(0,0,1.0,ZSTEM-8,231); H['fil']=cz(0,0,0.875,4,230,24)
    # dock group
    zt=ZNOZ+0.2-2.0
    H['dpin']=cy((XPIN,ZPIN),2.5,-24.0,5.25)+mf.Manifold.sphere(2.5,32).translate([XPIN,5.25,ZPIN])
    H['dmag']=cy((SHIFT,50.0),3.0,-12.65,-10.0)
    H['m5']=cy((-12.0,60.0),2.5,-39.5,-29.5)+cy((-12.0,60.0),4.25,-29.5,-24.5)+cy((4.0,60.0),2.5,-39.5,-29.5)+cy((4.0,60.0),4.25,-29.5,-24.5)
    H['tnut']=box(-17,-7,-39.4,-36.2,55.5,64.5)+box(-1,9,-39.4,-36.2,55.5,64.5)
    H['pad']=box(WX[0],WX[1],-5.0,5.0,zt,zt+2.0)
    H['dset']=cx_(-19.0,ZPIN,1.5,XPIN+2.5,24.2)
    for k,v in H.items(): ok(v,k)
    return H
ARMG=['arm','g2','g2ax','ascrew']; TOOLG=['tool','balls','mags_t','hooks','steel','m25','ptfe','fil']; DOCKG=['dock','dpin','dmag','m5','tnut','dset','pad']
LS=ZS-PIV[1]; LP=PIV[1]-ZPIN; LG=PIV[1]-G2[1]
if __name__=='__main__':
    P=build(); H=hardware()
    for k,v in P.items(): print(k,'vol %.0f mm3'%v.volume(),'bodies',len(v.decompose()),'bbox',np.round(v.bounding_box(),1).tolist())
    print('levers: spring %.1f pin %.1f idler %.1f; phi_max %.2f deg; idler opens %.2f mm'%(LS,LP,LG,np.degrees(PHI_MAX),PHI_MAX*LG))
    F0=40*LG/LS; print('40 N grip: spring %.1f N -> %.1f N open; push on pin %.1f -> %.1f N'%(F0,F0+6.25*LS*PHI_MAX,F0*LS/LP,(F0+6.25*LS*PHI_MAX)*LS/LP))
