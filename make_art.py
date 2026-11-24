from pathlib import Path
import random, math
p=Path(__file__).parent/'assets'
p.mkdir(exist_ok=True)
W,H=1600,1000

def svg(content):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice"><defs><linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff" stop-opacity=".24"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient></defs>{content}</svg>'''
def save(name,content): (p/name).write_text(svg(content),encoding='utf-8')
def path_hills(y,amp,seed,lowcolor,opacity=1):
 r=random.Random(seed); pts=[]
 for x in range(-80,1770,100):
  yy=y +r.uniform(-amp,amp) + 23*math.sin(x/300+seed)
  pts.append((x,yy))
 d='M '+' '.join(('%.1f %.1f'%(x,yy) if i==0 else 'L %.1f %.1f'%(x,yy)) for i,(x,yy) in enumerate(pts))+' L 1750 1030 L -80 1030 Z'
 return f'<path d="{d}" fill="{lowcolor}" opacity="{opacity}"/>'
def mountain_polys(y,amp,seed,color,opacity=1,noise=False):
 r=random.Random(seed); coords=[]
 for i in range(23):
  x=-150+i*86
  yy=y +r.uniform(-amp,amp)+amp*.4*math.sin(i*.64+seed)
  coords.append((x,yy))
 points=' '.join(f'{x:.0f},{y:.0f}' for x,y in coords)+ ' 1750,1030 -150,1030'
 result=f'<polygon points="{points}" fill="{color}" opacity="{opacity}"/>'
 if noise:
  for i in range(24):
   x=r.randint(50,1550); yy=r.randint(y+50,min(y+200,920))
   result+=f'<path d="M{x},{yy} l{r.randint(12,50)},{-r.randint(2,18)}" stroke="#d5f2eb" stroke-opacity=".12" stroke-width="2"/>'
 return result

def pine(x,y,h,fill,w=None,alpha=1):
 if w is None:w=h*.3
 trunk=f'<rect x="{x-h*.02:.1f}" y="{y-h*.05:.1f}" width="{h*.04:.1f}" height="{h*.1:.1f}" fill="{fill}"/>'
 result=trunk
 # layered boughs taper upwards
 for tier in range(5):
  top=y-h+ tier*h*.17; bottom=top+h*.35
  scale=(tier+1)/5
  width=w*(.42+scale*.65)
  points=f'{x:.1f},{top:.1f} {x-width:.1f},{bottom:.1f} {x+width:.1f},{bottom:.1f}'
  result+=f'<polygon points="{points}" fill="{fill}"/>'
 return f'<g opacity="{alpha}">{result}</g>'

def tree_line(seed, ylo, yhi, heightlo, heighthi, fill, n, opacity=1, edges=False):
 r=random.Random(seed); a=f'<g opacity="{opacity}">'
 if edges:
  # trees frame scene; center deliberately sparser for reading
  xs=[r.uniform(-40,500) for _ in range(n//2)]+[r.uniform(1100,1650) for _ in range(n-n//2)]
 else: xs=[r.uniform(-50,1650) for _ in range(n)]
 for x in sorted(xs):
  y=r.uniform(ylo,yhi); h=r.uniform(heightlo,heighthi)
  a+=pine(x,y,h,fill)
 a+='</g>'; return a

def branch_from_top(seed,color,side='left'):
 r=random.Random(seed)
 if side=='left':
  base='M -70 65 Q 175 75 395 -20'; leaves=''
  for _ in range(38):
   x=r.uniform(-20,340); y=40-x*.16+r.uniform(-30,40)
   leaves+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.randint(14,32)}" ry="{r.randint(3,11)}" fill="{color}" transform="rotate({r.randint(-65,55)} {x:.0f} {y:.0f})"/>'
 else:
  base='M 1680 75 Q 1430 76 1190 -25'; leaves=''
  for _ in range(38):
   x=r.uniform(1250,1660); y=15+(x-1250)*.08+r.uniform(-28,48)
   leaves+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.randint(14,32)}" ry="{r.randint(3,11)}" fill="{color}" transform="rotate({r.randint(-65,55)} {x:.0f} {y:.0f})"/>'
 return f'<path d="{base}" fill="none" stroke="{color}" stroke-width="22" stroke-linecap="round"/>'+leaves

# Scene dawn. The images are transparent independent depth layers.
save('dawn-back.svg', mountain_polys(525,84,4,'#a89d9f')+mountain_polys(615,58,7,'#87969a',.96))
save('dawn-middle.svg', mountain_polys(665,89,13,'#53777a',noise=True)+tree_line(21,750,820,80,195,'#365d59',58,.8))
save('dawn-trees.svg', path_hills(811,29,15,'#204a49') + tree_line(23,840,1000,160,390,'#133b3b',49,.98,True))
save('dawn-front.svg', path_hills(949,30,36,'#0c302f') + tree_line(39,980,1080,120,300,'#0a302f',28,.9,True) +branch_from_top(5,'#133b38','left')+branch_from_top(6,'#123936','right'))
# Forest set. distant luminous layered forest, trunks and leaves.
def broadleaf(x,y,h,fill,r):
 trunk=f'<path d="M{x-9:.0f} {y+30:.0f} Q{x-16:.0f} {y-h*.4:.0f} {x:.0f} {y-h*.8:.0f} Q{x+9:.0f} {y-h*.25:.0f} {x+8:.0f} {y+30:.0f}Z" fill="{fill}"/>'
 crown=''
 for _ in range(8):
  xx=x+r.uniform(-h*.4,h*.4); yy=y-h*r.uniform(.65,1.1)
  crown+=f'<ellipse cx="{xx:.0f}" cy="{yy:.0f}" rx="{r.uniform(h*.2,h*.32):.0f}" ry="{r.uniform(h*.18,h*.31):.0f}" fill="{fill}"/>'
 return trunk+crown

def broad_forest(seed, rowY, hmin,hmax,fill,n,opacity=1,edges=False):
 r=random.Random(seed);a=f'<g opacity="{opacity}">'
 xs=[r.uniform(0,450) for _ in range(n//2)] + [r.uniform(1150,1600) for _ in range(n-n//2)] if edges else [i*1600/(n-1)+r.uniform(-30,30) for i in range(n)]
 for x in xs:
  a+=broadleaf(x,rowY+r.uniform(-35,35),r.uniform(hmin,hmax),fill,r)
 return a+'</g>'
save('forest-back.svg', broad_forest(11,840,260,440,'#315e53',20,.72) + path_hills(854,24,9,'#204f46',.55))
save('forest-middle.svg', broad_forest(22,900,320,540,'#174d45',17,.92,True) + path_hills(891,34,24,'#17473f',.95))
save('forest-near.svg', broad_forest(26,990,440,760,'#0c3837',18,1,True) +path_hills(957,24,33,'#0b3535'))
# Fern fronds
r=random.Random(99); fern=''
for i in range(48):
 x=r.uniform(-50,1650)
 if 530<x<1080 and i%3!=0:continue
 by=r.uniform(990,1070); h=r.uniform(85,225)
 fern+=f'<path d="M {x:.0f} {by:.0f} q {-h*.22:.0f} {-h*.45:.0f} {h*.05:.0f} {-h:.0f}" stroke="#0a2d2e" stroke-width="5" fill="none"/>'
 for j in range(7):
  yy=by-h*(j+1)/8
  xx=x-h*.12*math.sin((j+1)/8*math.pi)
  span=h*.07*(1-j/8)
  fern+=f'<path d="M {xx:.0f} {yy:.0f} l {-span*2:.0f} {-span*.7:.0f} l {span*1.3:.0f} {span*1.6:.0f} Z M {xx:.0f} {yy:.0f} l {span*2:.0f} {-span*.7:.0f} l {-span*1.3:.0f} {span*1.6:.0f} Z" fill="#0a2d2e"/>'
save('forest-front.svg',path_hills(973,23,34,'#062829')+fern+branch_from_top(52,'#0b302d','left')+branch_from_top(67,'#092e2b','right'))
# Night ridge.
save('night-back.svg',mountain_polys(570,102,42,'#53677f')+mountain_polys(680,69,43,'#40566c'))
save('night-middle.svg',mountain_polys(738,84,44,'#283f56')+tree_line(45,845,985,90,190,'#1c344b',52,.8))
save('night-near.svg',path_hills(888,45,47,'#132f42')+tree_line(51,940,1040,190,365,'#0e2638',33,.86,True))
save('night-front.svg',path_hills(960,28,54,'#071e30')+tree_line(59,1010,1100,130,270,'#071d2c',26,.8,True))
print('Generated assets:',len(list(p.glob('*.svg'))))
