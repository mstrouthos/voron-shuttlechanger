"""v34 draft: the v33 concept (CxChanger coupling, dock and swing arm on a CNC Tap V2) with the stock CW2 / BMG gears.
Frame: X right, Y back, Z up, filament at x=0,y=0. The drive shaft keeps its stock stack, except that the front bearing
moves from in front of the hobbed gear to behind it, so nothing on the head sits in front of the filament."""
import numpy as np, manifold3d as mf, pickle
from geo import *
def ok(m,name):
    assert m.status()==mf.Error.NoError and m.volume()>0,name; return m
def rotY(m,c,ang): return m.translate([-c[0],0,-c[1]]).rotate([0,-np.degrees(ang),0]).translate([c[0],0,c[1]])
def cy(c,r,y0,y1,n=64): return cyl('y',c,r,y0,y1,n)
def cx_(y,z,r,x0,x1,n=48): return cyl('x',(y,z),r,x0,x1,n)
def cz(x,y,r,z0,z1,n=48): return cyl('z',(x,y),r,z0,z1,n)
def tear(axis,c,r,a0,a1,up,n=48):
    """hole along `axis` with a 45 deg roof towards `up` (unit vector, one of the other two axes)"""
    ax='xyz'.index(axis); o=[i for i in range(3) if i!=ax]; pts=[]
    for a in (a0,a1):
        for t in np.linspace(0,2*np.pi,n,endpoint=False):
            p=[0,0,0]; p[ax]=a; p[o[0]]=c[0]+r*np.cos(t); p[o[1]]=c[1]+r*np.sin(t); pts.append(p)
        p=[0,0,0]; p[ax]=a; p[o[0]]=c[0]+1.4142*r*up[o[0]]; p[o[1]]=c[1]+1.4142*r*up[o[1]]; pts.append(p)
    return mf.Manifold.hull_points(pts)
def above(nrm,d,big=400):
    """half-space {p : nrm.p >= d}"""
    n=np.array(nrm,float); L=np.linalg.norm(n); return mf.Manifold.cube([2*big]*3,True).trim_by_plane(list(n/L),d/L)
UPF=(0,-1,0)                                        # print-up for parts printed back face down
# ---------------- layout ----------------
ZG=81.25
GD=(-4.3,ZG); GI=(4.17,ZG)                           # BMG drive gear (fixed) and idler (on the arm); hob at y=0
MOT=(-4.3,96.25)                                    # LDO-36STH20, 10T pinion on the 50T gear, 15 mm centres
PIV=np.array([14.0,101.0])                           # swing-arm pivot pin
YF=10.25; YR=7.25; YT=22.5; YM=22.5                 # plate front, raised front, Tap face, motor face
ZRAISE=88.2; ZTOP=133.0; YSP=15.6; ZSPL=67.5   # the plate is two prints: a front slab above ZSPL (y < YSP) on the main body
Y_DG=(-3.5,10.5); Y_B1=(10.8,13.3); Y_50=(15.8,19.8); Y_B2=(20.0,YM); Y_SH=(YM-27.4,YM)   # stack along the 5 mm shaft (27.4 long)
TOPB=(0.0,101.0); LOWB=[(-16.5,46.5),(16.5,46.5)]
CEN=(0.0,(TOPB[1]+2*46.5)/3)
MAG_T=[(0.0,107.5),(0.0,113.7)]; MAG_L=[(-12.6,52.0),(12.6,52.0)]
TAP_TOP=[(-15.7,62.4),(15.05,62.4)]; TAP_LOW=[(-17.9,11.9),(17.45,11.9)]
EAR=21.92; A_E=np.radians(41.0)
MS=[(MOT[0]-EAR*np.cos(A_E),MOT[1]-EAR*np.sin(A_E)),(MOT[0]+EAR*np.cos(A_E),MOT[1]+EAR*np.sin(A_E))]
ZS=123.0; YS=4.6                                    # spring / adjuster axis (along X)
ARM_SEAT=12.5
SCR=(22.4,-1.0)
ZPIN=60.0; XPIN=SCR[0]-1.5-2.5-0.3
SHIFT=-3.5; DODGE=14.0; SAFE=30.0; PITCH=54.0
YTF=-9.5                                            # tool front face
HOOK=[(-11.5,50.0),(11.5,50.0)]
PHI_MAX=(abs(SHIFT)-0.3)/(PIV[1]-ZPIN)
EB_X0=-33.25; EB_Z0=78.0; EB_Y=YM+31.1            # SB2209 USB behind the motor
EB_H=[(EB_X0+27.2,EB_Z0+12.01),(EB_X0+15.18,EB_Z0+24.79)]
EB_S=[(-21.0,11.4),(-5.0,11.4)]
J=[(-20.0,108.0),(20.0,108.0)]                     # extra screws joining the front slab to the body
ZSTEM=118.5; WB=19.2                                # tool top; half-width of the tool base
DUCT=[(-26.3,17.05),(26.3,17.05)]
ZNOZ=-8.0; WX=(SHIFT/2-8.0,SHIFT/2+8.0)               # nozzle tip height; x range of the wiper (centred between the two parked/unparked positions)
ARM_LOW=[(24.9,63.0),(19.9,63.0),(19.9,66.5),(1.5,78.0),(1.5,84.5),(9.5,91.0)]
def build():
    P={}
    # ---------- back plate (modelled whole, then split into the body and the front slab) ----------
    pl=union(box(-23.5,23.5,14.0,YT,8.5,41.5), box(-25,25,YF,YT,41.5,ZTOP),
             box(-25,6.0,YR,YF,95.0,ZTOP), box(-25,0.7,YR,YF,ZRAISE,95.1), box(-11.0,-3.0,-1.0,YR,ZS-4,ZS+4))
    pl-=box(-3.0,6.1,YR-0.1,YF,ZS-3.5,ZS+3.6)
    for x,z in TAP_TOP: pl-=cy((x,z),1.7,YF-1,YT+1)+cy((x,z),3.1,YF-1,15.25)
    for x,z in TAP_LOW: pl-=cy((x,z),1.7,13,YT+1)+cy((x,z),3.1,13,17.5)+box(x-3.1,x+3.1,13,17.5,8.4,z)   # head recess open to the bottom edge
    # drive shaft: collar recess, front bearing on a shoulder, hub tunnel (front slab); 50T cavity over a rear-bearing web (body)
    pl-=box(GD[0]-5.3,1.1,YF-1,10.75,GD[1]-5.3,GD[1]+5.3)+cy(GD,4.05,YF-1,13.4)+cy(GD,3.4,13,14.5)+cy(GD,5.4,14.4,YSP+0.1)+cy(GD,13.3,YSP-0.01,Y_B2[0])+cy(GD,4.05,Y_B2[0]-0.1,YM+1)
    pl-=cy(MOT,8.3,YSP-0.01,YM+1)                                   # the motor's boss centres it in this hole
    for m in MS: pl-=cy(m,1.7,YF-1,YM+1)+cy(m,3.1,YF-1,13.4)
    for j in J: pl-=cy(j,1.7,YR-1,YSP+0.1)+cy(j,3.1,YR-1,13.4)+cy(j,2.35,YSP-0.01,YSP+5.5)
    pl-=prism_xz([(1.0,61.5),(26.0,61.5),(26.0,93.5),(1.0,93.5)],YF-0.1,12.25)
    pl-=cy(tuple(PIV),1.5,YF-1,19.5)
    def groove(b,yf):
        d=np.array(CEN)-np.array(b); a=np.degrees(np.arctan2(d[1],d[0])); g=None
        g=box(-2.5,2.5,yf-0.1,yf+1.0,-2.95,2.95)+box(-1.9,1.9,yf-0.1,yf+2.0,-1.45,1.45)      # one slot for both pins, deeper between them for the ball
        return g.rotate([0,-a,0]).translate([b[0],0,b[1]])
    pl-=groove(TOPB,YR)
    for b in LOWB: pl-=groove(b,YF)
    pl-=cy(MAG_T[0],3.05,YR-0.1,YR+2.2)+cy(MAG_T[1],3.05,YR-0.1,YR+2.2)+box(-3.05,3.05,YR-0.1,YR+2.2,MAG_T[0][1],MAG_T[1][1])   # one pocket for the two top magnets
    for m in MAG_L: pl-=cy(m,3.05,YF-0.1,YF+4.85)
    pl-=tear('x',(YS,ZS),1.7,-12,-2,UPF)+box(-7.3,-4.7,YS-2.85,YS+2.85,ZS-2.8,ZS+4.1)
    for sx in (-1,1):
        x0,x1=sorted((sx*22.2,sx*25.1)); pl-=box(x0,x1,YF-0.1,YT+0.1,41.0,55.7)       # the duct legs run up here
        x0,x1=sorted((sx*22.0,sx*29.5)); pl+=box(x0,x1,13.2,YT,55.7,61.4)             # ears over the legs, down to the bed
    for x,y in DUCT: pl-=tear('z',(x,y),1.7,55,62,UPF)
    for x,y in EB_S: pl-=tear('z',(x,y),2.35,ZTOP-5.5,ZTOP+1,UPF)
    ok(pl,'plate')
    front=box(-40,40,-5,YSP,ZSPL,ZTOP+1)
    P['slab']=ok(pl^front,'slab'); P['plate']=ok(pl-front,'plate')
    # ---------- SB2209 bracket: prints on its left side. The board stands on two loose spacers. ----------
    yb=YM+20.5
    eb=box(-24.5,-1.5,7.5,yb+4.0,ZTOP,ZTOP+3.5)+box(-24.5,-1.5,yb,yb+4.0,84.0,ZTOP+3.5)
    for x,z in EB_H: eb-=tear('y',(x,z),2.35,yb-1,yb+5,(1,0,0))
    for x,y in EB_S: eb-=tear('z',(x,y),1.7,ZTOP-1,ZTOP+5,(1,0,0))
    P['ebbmount']=ok(eb,'ebbmount')
    P['spacer']=ok(cy(EB_H[0],3.2,yb+4.05,EB_Y-0.05)-cy(EB_H[0],1.7,yb+3,EB_Y+1),'spacer')
    # ---------- swing arm ----------
    web=ARM_LOW+[(9.5,ZS+4.5),(24.9,ZS+4.5)]
    arm=prism_xz(web,YTF,9.75)+prism_xz(ARM_LOW+[(24.9,91.0)],9.7,11.75)
    arm-=box(0,19.85,-4.0,7.0,62,91.15)                              # the idler runs between the two webs
    arm-=cy(GI,1.5,-8.5,12)
    arm-=tear('y',tuple(PIV),1.65,YTF-1,12,(-1,0,0))
    arm-=cx_(YS,ZS,3.3,9,ARM_SEAT)+box(ARM_SEAT-0.1,26,YS-1.8,YS+1.8,ZS-2.5,ZS+2.5)
    arm-=cz(SCR[0],SCR[1],1.25,62,71)
    P['arm']=ok(arm,'arm')
    # ---------- tool body: prints upright on the base ----------
    up=box(-4.3,4.3,-10.1,6.5,75.0,ZSTEM)^above((0,-1,1),ZG+9.5)^above((-1,0,1),ZG+3.15)     # upper guide, 45 deg undersides
    beam=(box(-8.0,8.0,-15.5,-10.0,56.0,ZSTEM)+box(-4.2,4.2,-10.05,-9.4,56.0,ZG-10))^above((0,1,1),46.6)                          # front beam, chamfered foot above the dock tongue
    t=union(box(-WB,WB,YTF,9.5,40.6,54.5), box(-4.2,4.2,YTF,9.5,54.5,ZG-10), up, beam)
    t-=cz(0,0,1.05,40,ZG-9.9)+cz(0,0,1.05,ZG+5,ZSTEM-7.9)+cz(0,0,2.15,ZSTEM-8.0,ZSTEM+1)
    for sx in (-1,1):
        t-=cz(sx*5.72,-5.72,1.45,40,43)+cz(sx*5.72,-5.72,2.3,42.8,140)                       # front screws drop in from the top
        t-=cz(sx*5.72,5.72,1.45,40,43)+cz(sx*5.72,5.72,2.3,42.8,55.5)+box(sx*5.72-2.3,sx*5.72+2.3,5.72,10,42.8,55.5)+cz(sx*5.72,5.72,1.4,55,140)   # rear screws go in from the back; key hole above
    for b in LOWB: t-=cy(b,1.5,5.0,10)
    t-=cy(TOPB,1.5,2.0,7)
    for m in MAG_L: t-=cy(m,3.05,4.2,10)+box(m[0]-3.05,m[0]+3.05,4.2,10,m[1],55)            # dropped in from the top
    t-=cy(MAG_T[0],3.05,3.85,7)+box(-3.05,3.05,3.85,7,MAG_T[0][1],ZSTEM+1)                  # both top magnets drop into one slot from the top
    for h in HOOK: t-=cy(h,1.25,YTF-1,-2.5)
    t-=cy((0,50.0),1.25,YTF-1,-4.25)
    P['tool']=ok(t,'tool')
    # ---------- dock with the nozzle wiper built in: one part, printed on its back (the rail face) ----------
    # dock frame = head frame with the head at the dock, before the shift. The parked tool sits at x = SHIFT.
    XL=-24.3+SHIFT; XR=24.2; zt=ZNOZ+0.2-2.0; zf=zt-4.5            # left wall leaves room for the shroud to shift; floor under the nozzle
    d=union(box(XL,XR,-34,-29.5,43,70),                              # plate on the back face of the rail
            box(XL,-19.9,-34,-10.0,43,55.5), box(19.9,XR,-34,-10.0,43,55.5), box(XL,XR,-14.0,-10.0,43,55.5),   # beams and the tongue with the keyholes
            box(14.5,XR,-34,-14.0,55.5,70.0),                         # block for the opener pin, down to the plate
            box(XL,-24.3,-34,-10.0,zf,43.1), box(20.5,XR,-34,-10.0,zf,43.1),      # side walls beside the fan shroud
            box(XL,XR,-34,6.0,zf,zt+0.3))                             # floor that carries the silicone strip
    ab=box(-19.95,19.95,-34,-13.9,43,55.5); arch=(ab^above((-1,1,0),-14.0))+(ab^above((1,1,0),-14.0))    # 45 deg vault under the tongue, so it prints without a bridge
    d+=arch
    for hx,hz in HOOK:
        d-=cy((hx,hz),3.25,-15,-9)+box(hx+SHIFT-0.2,hx,-15,-9,hz-1.75,hz+1.75)+cy((hx+SHIFT-0.2,hz),1.75,-15,-9)      # keyhole
        d-=box(hx+SHIFT-3.5,hx+3.25,-34.1,-14.0,hz-3.25,hz+3.25)                                                # room for the screw head in front of the tongue
    d-=cy((SHIFT,50.0),3.05,-12.65,-9)
    d-=cy((XPIN,ZPIN),2.5,-24.0,-13)
    d-=cx_(-19.0,ZPIN,1.25,XPIN,25)
    for x in (-12.0,4.0): d-=cy((x,60.0),2.75,-35,-29)
    d-=box(WX[0],WX[1],-5.2,5.2,zt,zt+1)
    P['dock']=ok(d,'dock')
    return P
def hardware():
    H={}
    H['gd']=cy(GD,4.0,Y_DG[0],6.0)+cy(GD,4.75,6.0,Y_DG[1]); H['gi']=cy(GI,4.02,-3.5,6.5)
    H['g50']=cy(GD,13.0,*Y_50)+cy(GD,5.0,14.6,Y_50[0])
    H['shaft']=cy(GD,2.5,Y_SH[0],YM-0.05)
    H['brg']=(cy(GD,4.0,*Y_B1)-cy(GD,2.5,Y_B1[0]-1,Y_B1[1]+1))+(cy(GD,4.0,Y_B2[0],YM-0.02)-cy(GD,2.5,Y_B2[0]-1,YM+1))
    ear=mf.Manifold.hull_points([(m[0]+3.5*np.cos(a),y,m[1]+3.5*np.sin(a)) for m in MS for a in np.linspace(0,6.28,24) for y in (YM,YM+3)])
    H['motor']=cy(MOT,18.0,YM,YM+20)+ear+cy(MOT,8.0,YM-2.4,YM)+cy(MOT,3.0,YM-6,YM)
    H['pivot']=cy(tuple(PIV),1.5,-4.5,19.5)
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
    sc=None
    for m in MS:
        s=cy(m,1.5,13.4,YM+3.0)+cy(m,2.75,10.4,13.4); sc=s if sc is None else sc+s
    for j in J: sc+=cy(j,1.5,13.4,YSP+5.0)+cy(j,2.75,10.4,13.4)
    H['mscrews']=sc
    H['adj']=cx_(YS,ZS,1.5,-12.5,17.5)+cx_(YS,ZS,2.75,-15.5,-12.5)+cx_(YS,ZS,3.1,-7.2,-4.8,6)+cx_(YS,ZS,3.1,3.0,5.4,6)
    H['spring']=cx_(YS,ZS,3.0,5.4,ARM_SEAT)-cx_(YS,ZS,2.2,5,ARM_SEAT+1)
    H['ebb']=box(EB_X0,EB_X0+66.5,EB_Y,EB_Y+1.6,EB_Z0,EB_Z0+39.5)
    env=box(EB_X0+0.5,EB_X0+66.0,EB_Y+1.6,EB_Y+8.1,EB_Z0+0.5,EB_Z0+39.0)+box(EB_X0+0.5,EB_X0+66.0,EB_Y-6.35,EB_Y,EB_Z0+0.5,EB_Z0+39.0)
    for x,z in EB_H: env-=cy((x,z),3.7,EB_Y-7,EB_Y+9)
    H['ebbenv']=env
    sc=None
    for x,z in EB_H:
        q=cy((x,z),1.5,YM+20.5,EB_Y+1.6)+cy((x,z),2.75,EB_Y+1.6,EB_Y+4.6); sc=q if sc is None else sc+q
    for x,y in EB_S: sc+=cz(x,y,1.5,ZTOP-3.5,ZTOP+3.5)+cz(x,y,2.75,ZTOP+3.5,ZTOP+6.5)
    H['ebbscrews']=sc
    q=None
    for x,y in EB_S:
        s=cz(x,y,2.3,ZTOP-5,ZTOP)-cz(x,y,1.5,ZTOP-6,ZTOP+1); q=s if q is None else q+s
    for j in J: q+=cy(j,2.3,YSP,YSP+5)-cy(j,1.5,YSP-1,YSP+6)
    for x,z in EB_H: q+=cy((x,z),2.3,YM+20.5,YM+24.5)-cy((x,z),1.5,YM+20,YM+25)
    H['spacer2']=cy(EB_H[1],3.2,YM+24.55,EB_Y-0.05)-cy(EB_H[1],1.7,YM+23,EB_Y+1)
    H['ebbins']=q
    # arm group
    H['giax']=cy(GI,1.5,-8.5,11.3)
    H['ascrew']=cz(SCR[0],SCR[1],1.5,51,71)+cz(SCR[0],SCR[1],2.75,48,51)
    # tool group
    b=None
    for c in LOWB+[TOPB]:
        yb=10.03 if c!=TOPB else 7.03
        s=cy(c,1.5,yb-4.5,yb)+mf.Manifold.sphere(1.5,32).translate([c[0],yb,c[1]]); b=s if b is None else b+s
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
    H['dpin']=cy((XPIN,ZPIN),2.5,-24.0,5.25)+mf.Manifold.sphere(2.5,32).translate([XPIN,5.25,ZPIN])
    H['dmag']=cy((SHIFT,50.0),3.0,-12.65,-10.0)
    H['m5']=cy((-12.0,60.0),2.5,-39.5,-29.5)+cy((-12.0,60.0),4.25,-29.5,-24.5)+cy((4.0,60.0),2.5,-39.5,-29.5)+cy((4.0,60.0),4.25,-29.5,-24.5)
    H['tnut']=box(-17,-7,-39.4,-36.2,55.5,64.5)+box(-1,9,-39.4,-36.2,55.5,64.5)
    zt=ZNOZ+0.2-2.0
    H['pad']=box(WX[0],WX[1],-5.0,5.0,zt,zt+2.0)
    H['dset']=cx_(-19.0,ZPIN,1.5,XPIN+2.5,24.2)
    for k,v in H.items(): ok(v,k)
    return H
ARMG=['arm','gi','giax','ascrew']; TOOLG=['tool','balls','mags_t','hooks','steel','m25','ptfe','fil']; DOCKG=['dock','dpin','dmag','m5','tnut','dset','pad']
if __name__=='__main__':
    P=build(); H=hardware()
    for k,v in P.items(): print(k,'vol %.0f mm3'%v.volume(),'bbox',np.round(v.bounding_box(),1).tolist())
    LS=ZS-PIV[1]; LP=PIV[1]-ZPIN; LG=PIV[1]-GI[1]
    print('levers: spring %.1f pin %.1f idler %.1f; phi_max %.2f deg; idler opens %.2f mm'%(LS,LP,LG,np.degrees(PHI_MAX),PHI_MAX*LG))
    F0=40*LG/LS; print('40 N grip: spring %.1f N -> %.1f N open; push on pin %.1f -> %.1f N'%(F0,F0+6.25*LS*PHI_MAX,F0*LS/LP,(F0+6.25*LS*PHI_MAX)*LS/LP))
