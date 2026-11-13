"""Hand load cases for the v35 printed parts. Allowables: 20 MPa along the layers, 8 MPa across, 10 MPa bearing."""
import json, build36 as B
LS,LP,LG=B.LS,B.LP,B.LG
GRIP=40.0; F0=GRIP*LG/LS; F1=F0+6.25*LS*B.PHI_MAX; PUSH=F1*LS/LP; STALL=60.0
C=[]
def case(part,what,sigma,allow,note): C.append(dict(part=part,case=what,stress_MPa=round(sigma,1),allow_MPa=allow,ok=bool(sigma<=allow),note=note))
Z=lambda b,h: b*h*h/6
case('swing arm','dock pin push at the foot, leg 7.1 x 19.5',PUSH*(66.5-B.ZPIN)/Z(19.5,7.1),20,'along layers; %.0f N push'%PUSH)
case('swing arm','same, gantry stall 60 N',STALL*(66.5-B.ZPIN)/Z(19.5,7.1),20,'along layers')
case('swing arm','section at the pivot (16.5 wide, bore removed)',STALL*LP/(Z(17.5,16.5)*0.6),20,'along layers')
case('swing arm','idler axle in two webs, bearing',(GRIP+10)/(2*3*3.3),10,'bearing')
case('front slab','spring boss: nut bears on the 7.7 mm left wall, lever 5.65',F1*5.65/Z(8.0,7.7),8,'across layers; spring %.0f N'%F1)
case('front slab + body','pivot pin, 6 mm in the slab, load about grip + spring',(GRIP+F1)/(3*6.0),10,'bearing')
case('gear housing','fixed gear axle, front end 3.25 mm in the housing, half the pinch load',GRIP/2/(3*3.25),10,'bearing')
case('coupling plate + slab','fixed gear axle, back end 3.4 mm engaged',GRIP/2/(3*3.4),10,'bearing')
case('tool body','bowden drag 10 N at the top, front beam 16 x 5.5, lever 44',10*44/Z(16.0,5.5),8,'across layers (printed upright)')
case('tool body','20 N sideways push on the stem top, beam 5.5 x 16',20*44/Z(5.5,16.0),8,'across layers')
case('dock','opener pin block 9.7 x 14.5 on the back plate, lever 28.5, normal push',PUSH*28.5/Z(14.5,9.7),8,'across layers; the block is also joined to the tongue along its length')
case('dock','same, gantry stall 60 N',STALL*28.5/Z(14.5,9.7),8,'across layers')
case('dock','wiper floor: 5 N from the nozzle, floor 4.5 x 51.5, 16 mm past the side walls',5*16/Z(51.5,4.5),8,'across layers')
case('gear housing + slab','20 N cable tug at the board: two M3 self-tapping screws, 4 mm in plastic',20/2/(3*4.0),10,'bearing on the thread; route the USB cable through a strain relief')
json.dump(dict(grip_N=GRIP,spring_closed_N=round(F0,1),spring_open_N=round(F1,1),pin_push_N=[round(F0*LS/LP,1),round(PUSH,1)],cases=C),open('v36/load_cases.json','w'),indent=1)
for c in C: print('%-22s %-74s %5.1f / %2d %s'%(c['part'],c['case'][:74],c['stress_MPa'],c['allow_MPa'],'ok' if c['ok'] else 'OVER'))
