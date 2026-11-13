"""v33 draft: CxChanger mechanism on a CNC Tap V2. Frame: X right, Y back, Z up, filament at x=0,y=0.
Hardware positions are CxChanger's (CAD 6.11) shifted by (-19.76, +17.75, +50.8)."""
import numpy as np, manifold3d as mf, pickle
from geo import *
def ok(m,name):
    assert m.status()==mf.Error.NoError and m.volume()>0,name; return m
def rotY(m,c,ang): return m.translate([-c[0],0,-c[1]]).rotate([0,-np.degrees(ang),0]).translate([c[0],0,c[1]])
def cy(c,r,y0,y1,n=64): return cyl('y',c,r,y0,y1,n)
def cx_(y,z,r,x0,x1,n=48): return cyl('x',(y,z),r,x0,x1,n)
def cz(x,y,r,z0,z1,n=48): return cyl('z',(x,y),r,z0,z1,n)
# ---------------- layout ----------------
G1=(-9.39,74.0); G2=(9.39,74.0); RG=9.75           # HGX gears, 37T m0.5, hob at y=0, teeth y 1.75..7.75
DG=(-10.26,87.7)                                    # 17/44 dual gear on MR63 bearings
MOT=(0.19,96.25)                                    # LDO-36STH20 with 10T pinion, face at y=YM
PIV=np.array([14.54,87.3])                          # swing-arm pivot pin
YF=10.25; YR=7.25; YT=22.5; YM=17.75                # plate front, raised front (above the gears), Tap face, motor face
ZRAISE=84.2
TOPB=(0.0,87.3); LOWB=[(-15.6,44.0),(15.6,44.0)]    # coupling balls (x,z)
CEN=(0.0,(TOPB[1]+2*44.0)/3)
MAG_T=(0.0,93.5); MAG_L=[(-12.0,50.5),(12.0,50.5)]
TAP_TOP=[(-15.7,62.4),(15.05,62.4)]; TAP_LOW=[(-17.9,11.9),(17.45,11.9)]
EAR=21.92; u=np.array([-8.55,10.45])/13.5           # motor ears lie across the motor->dual-gear line
MS=[(MOT[0]+EAR*u[0],MOT[1]+EAR*u[1]),(MOT[0]-EAR*u[0],MOT[1]-EAR*u[1])]
PA=(-22.7,68.0); PB=(-22.0,98.5)                    # cover posts
ZS=106.0; YS=4.6                                    # spring / adjuster axis (along X)
ARM_SEAT=13.5
SCR=(22.4,-1.0)                                     # contact screw on the arm (x,y), vertical
ZPIN=60.0; XPIN=SCR[0]-1.5-2.5-0.3                  # dock pin axis (dock frame, before the shift)
SHIFT=-3.0; DODGE=14.0; SAFE=30.0; PITCH=50.0
HOOK=[(-11.5,50.0),(11.5,50.0)]
PHI_MAX=(abs(SHIFT)-0.3)/(PIV[1]-ZPIN)
# EBB SB2209 USB main board (BigTreeTech CAD): 39.5 x 66.5, two Ø3.7 mounting holes. Landscape behind the motor, parts side to the back.
EB_X0=-33.25; EB_Z0=78.0; EB_Y=47.85                 # board left edge (x), bottom (z), PCB face towards the motor (y)
EB_H=[(EB_X0+27.2,EB_Z0+12.01),(EB_X0+15.18,EB_Z0+24.79)]   # (x,z)
EB_S=[(-21.0,13.5),(-5.0,13.5)]                      # bracket screws into the top edge of the plate (x,y)
DUCT=[(-26.3,17.05),(26.3,17.05)]                    # the v32 duct legs end here with their inserts at z 55.6
def build():
    P={}
    # ---------- back plate ----------
    pl=union(box(-23.5,23.5,14.0,YT,8.5,41.5), box(-25,25,YF,YT,41.5,75.5), box(-25,25,YF,YM,75.5,116.5),
             box(-25,6.0,YR,YF,ZRAISE,116.5), box(-8.0,-3.0,-1.0,YR,102.0,110.0))
    pl-=box(-3.0,6.1,YR-0.1,YF,102.5,109.6)                       # room for the spring collar nut
    for x,z in TAP_TOP: pl-=cy((x,z),1.7,YF-1,YT+1)+cy((x,z),3.1,YF-1,15.25)
    for x,z in TAP_LOW: pl-=cy((x,z),1.7,13,YT+1)+cy((x,z),3.1,13,17.5)
    pl-=cy(DG,12.3,11.5,YM+1)+cy(DG,5.3,YR-1,11.6)                 # dual-gear cavity, open to the motor side
    pl-=cy(MOT,3.6,11.5,YM+1)+cy(MOT,8.3,15.2,YM+1)                # pinion and motor boss
    pl-=cy(MS[0],1.7,YR-1,YM+1)+cy(MS[0],3.1,YR-1,13.75)
    pl-=cy(MS[1],1.7,YF-1,YM+1)+cy(MS[1],3.1,YF-1,15.25)
    armpk=prism_xz([(3.0,61.5),(26.0,61.5),(26.0,85.0),(3.0,85.0)],YF-0.1,12.25)   # the arm's back web runs in this pocket
    pl-=armpk
    pl-=cy(G1,1.5,YF-1,13.0)                                        # gear axle, press
    pl-=cy(tuple(PIV),1.5,YF-1,16.75)                               # pivot pin, press
    for c,yf in ((PA,YF),(PB,YR)): pl-=cy(c,2.35,yf-0.1,yf+5.5)     # heat-set inserts for the cover
    # coupling: pin pairs form the V grooves; a relief hole lets the ball sit between them
    def groove(b,yf):
        d=np.array(CEN)-np.array(b); a=np.degrees(np.arctan2(d[1],d[0])); g=None
        for s in (-2.2,2.2):
            ch=box(-2.5,2.5,yf-0.1,yf+1.0,s-0.75,s+0.75).rotate([0,-a,0]).translate([b[0],0,b[1]]); g=ch if g is None else g+ch
        return g+cy(b,1.7,yf-0.1,yf+2.0)
    pl-=groove(TOPB,YR)
    for b in LOWB: pl-=groove(b,YF)
    pl-=cy(MAG_T,3.05,YR-0.1,YR+2.2)
    for m in MAG_L: pl-=cy(m,3.05,YF-0.1,YF+4.85)
    # adjuster: M3 through the boss into a captive nut
    pl-=cx_(YS,ZS,1.7,-9,-2)+box(-6.3,-3.7,YS-2.85,YS+2.85,ZS-2.8,110.1)
    for sx in (-1,1):                                               # the duct legs run up the sides; ears above them take the two screws
        x0,x1=sorted((sx*22.2,sx*25.1)); pl-=box(x0,x1,12.5,21.5,41.0,55.7)
        x0,x1=sorted((sx*22.0,sx*29.5)); pl+=box(x0,x1,13.2,20.9,55.7,61.4)
    for x,y in DUCT: pl-=cz(x,y,1.7,55,62)
    for x,y in EB_S: pl-=cz(x,y,2.35,111.0,117)
    P['plate']=ok(pl,'plate')
    # ---------- bracket for the EBB SB2209 USB: over the motor and down behind it ----------
    eb=box(-24.5,-1.5,9.5,40.75,116.5,120.0)+box(-24.5,-1.5,38.25,40.75,84.0,120.0)
    for x,z in EB_H: eb+=cy((x,z),3.2,40.7,EB_Y)
    for x,z in EB_H: eb-=cy((x,z),1.25,39.5,EB_Y+1)
    for x,y in EB_S: eb-=cz(x,y,1.7,116,121)
    eb-=box(MS[0][0]-4.5,MS[0][0]+4.5,YM-0.5,YM+3.6,116.4,117.6)             # the motor's upper ear just reaches the arm
    P['ebbmount']=ok(eb,'ebbmount')
    # ---------- bearing plug (holds the dual gear's rear bearing, clamped by the motor face) ----------
    plug=cy(DG,12.1,15.3,YM)-cy(DG,3.05,15,YM+1)-cy(MOT,8.5,15,YM+1)
    P['plug']=ok(plug,'plug')
    # ---------- left front cover ----------
    out=[(-25,64.4),(-19.0,64.4),(-19.0,66.2),(-4.8,66.2),(-4.8,95.0),(-14.0,95.0),(-14.0,102.2),(-25,102.2)]
    cv=prism_xz(out,-4.75,1.75)+cy(PA,3.6,1.75,YF)+cy(PB,3.6,1.75,YR)
    cv-=cy(G1,RG+0.5,-1.5,2)+cy(G1,1.5,-3.25,0)                    # gear pocket and axle
    cv-=cy(DG,3.05,-0.85,2)+cy(DG,5.3,1.0,2)                        # front bearing of the dual gear
    for c,yb in ((PA,YF),(PB,YR)): cv-=cy(c,1.7,-5,yb+1)+cy(c,3.1,-5,-1.75)
    P['cover']=ok(cv,'cover')
    # ---------- swing arm ----------
    web=[(24.9,63.0),(19.9,63.0),(5.0,70.0),(5.0,78.0),(10.5,84.2),(10.5,110.5),(24.9,110.5)]
    arm=prism_xz(web,-6.0,9.75)+prism_xz([(24.9,63.0),(19.9,63.0),(5.0,70.0),(5.0,78.0),(10.5,84.0),(24.9,84.0)],9.7,11.75)
    arm-=cy(G2,RG+0.5,-1.6,8.45)+box(4,19.9,-1.6,8.45,62,84.2)     # gear slot between the two webs
    arm-=cy(G2,1.5,-4.25,12)                                        # idler axle
    arm-=cy(tuple(PIV),1.65,-7,12)                                  # pivot bore
    arm-=cx_(YS,ZS,3.3,10,ARM_SEAT)+box(ARM_SEAT-0.1,26,YS-1.8,YS+1.8,ZS-2.5,ZS+2.5)   # spring seat and slot for the screw tip
    arm-=cz(SCR[0],SCR[1],1.25,62,71)                               # contact screw, self-tapping
    P['arm']=ok(arm,'arm')
    # ---------- tool body ----------
    t=union(box(-18.5,18.5,-7.75,9.5,40.6,54.5), box(-4.2,4.2,-7.75,9.5,54.5,63.5),
            box(-4.2,4.2,-7.75,-1.75,63.5,85.0), box(-4.0,4.0,-7.75,6.5,85.0,97.5))
    t-=cz(0,0,1.05,40,63.6)+cz(0,0,1.05,84.9,89.6)+cz(0,0,2.15,89.5,98)
    for sx in (-1,1):
        for sy in (-1,1): t-=cz(sx*5.72,sy*5.72,1.45,40,43)+cz(sx*5.72,sy*5.72,2.3,42.8,120)
    for b in LOWB: t-=cy(b,1.5,5.0,10)
    t-=cy(TOPB,1.5,2.0,7)
    for m in MAG_L: t-=cy(m,3.05,4.2,10)
    t-=cy(MAG_T,3.05,3.85,7)
    for h in HOOK: t-=cy(h,1.25,-8,-0.75)
    t-=cy((0,50.0),1.25,-8,-2.5)
    P['tool']=ok(t,'tool')
    # ---------- dock (dock frame = head frame with the head at the dock, before the shift) ----------
    d=union(box(-23.5,23.5,-34,-29.5,43,70), box(-23.5,-19.2,-34,-8.25,43,55.5), box(19.2,23.5,-34,-8.25,43,55.5),
            box(-23.5,23.5,-12.25,-8.25,43,55.5), box(14.5,23.5,-24,-12.25,55.5,64.0), box(19.2,23.5,-29.6,-12.25,55.5,64.0))
    for hx,hz in HOOK: d-=cy((hx,hz),3.25,-13,-8)+box(hx+SHIFT-0.2,hx,-13,-8,hz-1.75,hz+1.75)+cy((hx+SHIFT-0.2,hz),1.75,-13,-8)
    d-=cy((SHIFT,50.0),3.05,-10.9,-8)                               # magnet facing the steel screw in the tool
    d-=cy((XPIN,ZPIN),2.5,-22.25,-12)                               # pin socket
    d-=cx_(-17.0,ZPIN,1.25,XPIN,24)                                 # set screw onto the pin
    for x in (-12.0,4.0): d-=cy((x,60.0),2.75,-35,-29)
    P['dock']=ok(d,'dock')
    return P
def hardware():
    H={}
    H['g1']=cy(G1,RG,1.75,7.75)+cy(G1,8.85,-1.25,1.75); H['g2']=cy(G2,RG,1.75,7.75)+cy(G2,8.85,-1.25,1.75)
    H['dg']=cy(DG,4.75,2.75,11.75)+cy(DG,11.62,11.75,15.2)+cy(DG,1.5,-0.75,17.75)
    H['brg']=cy(DG,3.0,-0.75,1.75)+cy(DG,3.0,15.3,YM)
    ear=mf.Manifold.hull_points([(MS[0][0]+3.5*np.cos(a),y,MS[0][1]+3.5*np.sin(a)) for a in np.linspace(0,6.28,24) for y in (YM,YM+3)]+
                                [(MS[1][0]+3.5*np.cos(a),y,MS[1][1]+3.5*np.sin(a)) for a in np.linspace(0,6.28,24) for y in (YM,YM+3)])
    H['motor']=cy(MOT,18.0,YM,YM+20)+ear+cy(MOT,8.0,YM-2.4,YM)+cy(MOT,3.0,YM-6,YM)
    H['axles']=cy(G1,1.5,-3.25,12.75)
    H['pivot']=cy(tuple(PIV),1.5,-7.25,16.75)
    H['mags_h']=cy(MAG_T,3.0,YR-0.45,YR+2.2)+cy(MAG_L[0],3.0,YF-0.45,YF+4.85)+cy(MAG_L[1],3.0,YF-0.45,YF+4.85)
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
    H['mscrews']=cy(MS[0],1.5,13.75,21.75)+cy(MS[0],2.75,10.75,13.75)+cy(MS[1],1.5,15.25,21.25)+cy(MS[1],2.75,12.25,15.25)
    H['cscrews']=cy(PA,1.5,-1.75,14.25)+cy(PA,2.75,-4.75,-1.75)+cy(PB,1.5,-1.75,10.25)+cy(PB,2.75,-4.75,-1.75)
    H['inserts']=(cy(PA,2.3,YF,YF+5)-cy(PA,1.5,YF-1,YF+6))+(cy(PB,2.3,YR,YR+5)-cy(PB,1.5,YR-1,YR+6))
    H['adj']=cx_(YS,ZS,1.5,-9.5,20.5)+cx_(YS,ZS,2.75,-12.5,-9.5)+cx_(YS,ZS,3.1,-6.2,-3.8,6)+cx_(YS,ZS,3.1,2.65,5.05,6)
    H['spring']=cx_(YS,ZS,3.0,5.05,ARM_SEAT)-cx_(YS,ZS,2.2,5,ARM_SEAT+1)
    H['ebb']=box(EB_X0,EB_X0+66.5,EB_Y,EB_Y+1.6,EB_Z0,EB_Z0+39.5)
    env=box(EB_X0+0.5,EB_X0+66.0,EB_Y+1.6,EB_Y+8.1,EB_Z0+0.5,EB_Z0+39.0)+box(EB_X0+0.5,EB_X0+66.0,EB_Y-6.35,EB_Y,EB_Z0+0.5,EB_Z0+39.0)
    for x,z in EB_H: env-=cy((x,z),3.7,EB_Y-7,EB_Y+9)
    H['ebbenv']=env
    sc=None
    for x,z in EB_H:
        q=cy((x,z),1.5,EB_Y-6.4,EB_Y+1.6)+cy((x,z),2.75,EB_Y+1.6,EB_Y+4.6); sc=q if sc is None else sc+q
    for x,y in EB_S: sc+=cz(x,y,1.5,113.0,120.0)+cz(x,y,2.75,120.0,123.0)
    H['ebbscrews']=sc
    H['ebbins']=(cz(EB_S[0][0],EB_S[0][1],2.3,111.5,116.5)-cz(EB_S[0][0],EB_S[0][1],1.5,111,117))+(cz(EB_S[1][0],EB_S[1][1],2.3,111.5,116.5)-cz(EB_S[1][0],EB_S[1][1],1.5,111,117))
    # arm group
    H['g2ax']=cy(G2,1.5,-4.25,11.75)
    H['ascrew']=cz(SCR[0],SCR[1],1.5,51,71)+cz(SCR[0],SCR[1],2.75,48,51)
    # tool group
    b=None
    for c in LOWB+[TOPB]:
        yb=10.03 if c!=TOPB else 7.03
        s=cy(c,1.5,yb-4.5,yb)+mf.Manifold.sphere(1.5,32).translate([c[0],yb,c[1]]); b=s if b is None else b+s
    H['balls']=b
    H['mags_t']=cy(MAG_T,3.0,3.85,6.5)+cy(MAG_L[0],3.0,4.2,9.5)+cy(MAG_L[1],3.0,4.2,9.5)
    hk=None
    for h in HOOK:
        s=cy(h,1.5,-12.75,-0.75)+cy(h,2.75,-15.75,-12.75); hk=s if hk is None else hk+s
    H['hooks']=hk; H['steel']=cy((0,50.0),1.5,-7.75,-2.75)
    m=None
    for sx in (-1,1):
        for sy in (-1,1):
            s=cz(sx*5.72,sy*5.72,1.25,32.8,42.8)+cz(sx*5.72,sy*5.72,2.25,42.8,45.3); m=s if m is None else m+s
    H['m25']=m
    H['ptfe']=cz(0,0,2.0,89.6,230)-cz(0,0,1.0,89,231); H['fil']=cz(0,0,0.875,4,230,24)
    # dock group
    H['dpin']=cy((XPIN,ZPIN),2.5,-22.25,5.25)+mf.Manifold.sphere(2.5,32).translate([XPIN,5.25,ZPIN])
    H['dmag']=cy((SHIFT,50.0),3.0,-10.9,-8.25)
    H['m5']=cy((-12.0,60.0),2.5,-39.5,-29.5)+cy((-12.0,60.0),4.25,-29.5,-24.5)+cy((4.0,60.0),2.5,-39.5,-29.5)+cy((4.0,60.0),4.25,-29.5,-24.5)
    H['tnut']=box(-17,-7,-39.4,-36.2,55.5,64.5)+box(-1,9,-39.4,-36.2,55.5,64.5)
    H['dset']=cx_(-17.0,ZPIN,1.5,XPIN+2.5,23.5)
    for k,v in H.items(): ok(v,k)
    return H
ARMG=['arm','g2','g2ax','ascrew']; TOOLG=['tool','balls','mags_t','hooks','steel','m25','ptfe','fil']; DOCKG=['dock','dpin','dmag','m5','tnut','dset']
if __name__=='__main__':
    P=build(); H=hardware()
    for k,v in P.items(): print(k,'vol %.0f mm3'%v.volume(),'genus',v.genus(),'bbox',np.round(v.bounding_box(),1).tolist())
    print('phi_max deg',np.degrees(PHI_MAX),'open at gear mm',PHI_MAX*(PIV[1]-G2[1]))
    pickle.dump({k:to_tm(v) for k,v in {**P,**H}.items()},open('parts33.pkl','wb'))
