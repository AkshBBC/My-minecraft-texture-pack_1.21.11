from pathlib import Path
import random,struct,zlib,math,json
R=Path("build/pack"); B=R/"assets/minecraft/textures/block"; B.mkdir(parents=True,exist_ok=True)
def png(n,c,kind="noise",a=None,s=0):
 r=random.Random(s); p=[]
 for y in range(16):
  row=[]
  for x in range(16):
   q=r.randint(-12,12)
   if kind=="wood": q+=int(math.sin(x/2+y/3)*7)
   row.append((*[max(0,min(255,v+q)) for v in c],255))
  p.append(row)
 if kind=="brick":
  for y in range(16):
   for x in range(16):
    if y%4==0 or (x-(0 if y//4%2==0 else 2))%8==0:p[y][x]=(*[max(0,v-35) for v in c],255)
 if kind=="wood" and a:
  for _ in range(5):
   x=r.randrange(16)
   for y in range(16):p[y][x]=(*a,255)
 if kind=="leaf":
  for y in range(16):
   for x in range(16):
    if r.random()<.12:p[y][x]=(0,0,0,0)
 if kind=="glass":
  for y in range(16):
   for x in range(16):p[y][x]=(*c,150 if (x+y)%3 else 90)
  for i in range(16):p[i][i]=(*a,210);p[i][15-i]=(*a,110)
 raw=b"".join(b"\0"+bytes(sum((list(z) for z in row),[])) for row in p)
 def ch(t,d):return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
 (B/f"{n}.png").write_bytes(b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",16,16,8,6,0,0,0))+ch(b"IDAT",zlib.compress(raw,9))+ch(b"IEND",b""))
S=[("stone",(104,104,104),"noise"),("granite",(140,110,95),"noise"),("diorite",(175,175,170),"noise"),("andesite",(125,128,126),"noise"),("deepslate",(55,58,60),"noise"),("tuff",(105,103,96),"noise"),("calcite",(205,204,195),"noise"),("basalt",(75,76,74),"noise"),("blackstone",(45,43,43),"noise"),("netherrack",(100,43,42),"noise"),("end_stone",(215,210,155),"noise"),("sandstone",(194,174,115),"noise"),("red_sandstone",(160,75,48),"noise"),("mud",(75,61,48),"noise"),("packed_mud",(110,84,64),"noise"),("obsidian",(30,25,48),"noise"),("crying_obsidian",(38,25,52),"noise"),("prismarine",(80,145,135),"noise"),("dark_prismarine",(45,100,98),"noise"),("purpur_block",(170,120,175),"noise"),("quartz_block",(225,220,210),"noise"),("glowstone",(215,165,75),"noise"),("sea_lantern",(170,225,215),"noise"),("snow_block",(235,240,245),"noise"),("clay",(155,160,160),"noise"),("stone_bricks",(115,115,115),"brick"),("mossy_stone_bricks",(95,120,90),"brick"),("bricks",(145,70,55),"brick"),("nether_bricks",(65,35,40),"brick"),("red_nether_bricks",(90,35,35),"brick"),("end_stone_bricks",(185,180,135),"brick"),("mud_bricks",(95,72,60),"brick")]
for i,x in enumerate(S):png(*x,s=i)
W={"oak":((150,105,55),(105,70,35)),"spruce":((95,65,40),(65,42,28)),"birch":((205,190,145),(120,105,75)),"jungle":((155,105,55),(95,60,35)),"acacia":((165,80,50),(105,50,35)),"dark_oak":((75,50,35),(45,30,22)),"mangrove":((105,45,40),(65,28,28)),"cherry":((205,125,145),(150,75,105)),"bamboo":((165,180,75),(100,125,45))}
for i,(n,(c,a)) in enumerate(W.items()):png(n+"_planks",c,"wood",a,100+i);png(n+"_log",c,"wood",a,120+i);png(n+"_leaves",(55,120,65),"leaf",(35,90,45),140+i)
C={"white":(225,225,220),"light_gray":(155,155,150),"gray":(80,82,82),"black":(30,30,32),"red":(165,55,50),"orange":(220,105,45),"yellow":(220,185,55),"lime":(110,185,55),"green":(60,135,70),"cyan":(50,165,165),"light_blue":(70,150,210),"blue":(55,80,170),"purple":(125,65,165),"magenta":(190,70,145),"pink":(225,135,155),"brown":(120,75,48)}
for i,(n,c) in enumerate(C.items()):png(n+"_concrete",c,s=300+i);png(n+"_terracotta",tuple(int(v*.8) for v in c),s=330+i)
(R/"pack.mcmeta").write_text(json.dumps({"min_format":[75,0],"max_format":[75,0],"description":{"text":"OBSIDIAN // Performance 16x v0.3 — Block Overhaul","color":"a8fff5"}},indent=2))
