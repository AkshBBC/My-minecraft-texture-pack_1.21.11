from pathlib import Path
import random, struct, zlib, json, math

OUT=Path("build/pack")
PART=OUT/"assets/minecraft/textures/particle"
ENV=OUT/"assets/minecraft/textures/environment"
PART.mkdir(parents=True,exist_ok=True); ENV.mkdir(parents=True,exist_ok=True)

def png(path,w,h,pixel_fn):
    path.parent.mkdir(parents=True, exist_ok=True)
    px=[]
    for y in range(h):
        row=[]
        for x in range(w):
            row.append(pixel_fn(x,y,w,h))
        px.append(row)
    raw=b"".join(b"\0"+bytes(sum((list(v) for v in row),[])) for row in px)
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+ch(b"IDAT",zlib.compress(raw,9))+ch(b"IEND",b"")
    path.write_bytes(data)

def circle_particle(base,accent,seed):
    r=random.Random(seed)
    def f(x,y,w,h):
        dx=x-(w-1)/2; dy=y-(h-1)/2
        d=(dx*dx+dy*dy)**0.5
        if d>min(w,h)*0.43: return (0,0,0,0)
        a=max(35,int(245-(d/(min(w,h)*0.43))*170))
        if r.random()<0.12: a//=2
        t=max(0,min(1,d/(min(w,h)*0.43)))
        c=tuple(int(base[i]*(1-t)+accent[i]*t) for i in range(3))
        return (*c,a)
    return f

PARTICLES={
"flame":((255,110,35),(255,220,70)),
"soul_fire_flame":((35,175,205),(120,245,235)),
"lava":((230,70,25),(255,205,55)),
"smoke":((70,75,82),(150,155,165)),
"campfire_cosy_smoke":((82,80,78),(185,170,150)),
"campfire_signal_smoke":((90,92,100),(190,195,205)),
"cloud":((190,198,210),(235,240,245)),
"bubble":((65,180,210),(190,245,255)),
"crit":((220,220,220),(245,80,70)),
"enchanted_hit":((125,70,210),(80,225,215)),
"electric_spark":((90,225,235),(235,255,255)),
"sculk_soul":((35,115,125),(90,235,220)),
"note":((120,90,220),(230,100,210)),
"heart":((220,45,65),(255,125,145)),
"damage_indicator":((235,65,55),(255,180,80)),
"glow":((235,190,70),(255,245,170)),
"ash":((100,94,90),(185,175,165)),
"white_ash":((170,175,180),(235,240,245)),
"wax_on":((220,170,55),(255,230,110)),
"wax_off":((110,115,120),(205,210,215))
}
for i,(name,(a,b)) in enumerate(PARTICLES.items()):
    png(PART/f"{name}.png",16,16,circle_particle(a,b,100+i))

# A few tiny deterministic environmental particles with crisp silhouettes.
for name,base,acc in [
    ("rain", (65,115,170),(150,220,255)),
    ("snowflake", (185,200,215),(255,255,255)),
]:
    def make(base=base,acc=acc,name=name):
        def f(x,y,w,h):
            if name=="rain":
                on=(x==7 and 1<=y<=14) or (x==6 and y>=9)
            else:
                on=(x==7 and 3<=y<=12) or (y==7 and 3<=x<=12) or (x==5 and y==5) or (x==9 and y==9)
            return (*((acc) if on else base), 210 if on else 0)
        return f
    png(PART/f"{name}.png",16,16,make())

# 1.21.11 celestial/weather paths.
# The 1.21.11 client uses the celestials atlas for the sun and eight moon phases.
def sun(x,y,w,h):
    d=((x-(w-1)/2)**2+(y-(h-1)/2)**2)**0.5
    if d>15.5: return (0,0,0,0)
    if d>12: return (235,185,70,170)
    t=d/12
    return (int(225-80*t),int(250-40*t),int(245-20*t),255)
png(ENV/"celestial/sun.png",32,32,sun)

phases=["full_moon","waning_gibbous","third_quarter","waning_crescent",
        "new_moon","waxing_crescent","first_quarter","waxing_gibbous"]
for pi,name in enumerate(phases):
    def moon(x,y,w,h,pi=pi):
        cx=15.5; cy=15.5
        d=((x-cx)**2+(y-cy)**2)**0.5
        if d>14.5: return (0,0,0,0)
        # Stylized phase mask with cool cyan-white lunar surface.
        nx=(x-15.5)/14.5
        shift=[-1.0,-0.55,-0.05,0.45,1.0,0.45,-0.05,-0.55][pi]
        lit=nx>=shift
        if pi==0: lit=True
        if pi==4: lit=False
        if not lit: return (0,0,0,0)
        edge=205+int(40*(1-d/14.5))
        return (185,215,220,edge)
    png(ENV/f"celestial/moon/{name}.png",32,32,moon)

# Repeating cloud mask.
png(ENV/"clouds.png",256,256,lambda x,y,w,h:
    (205,215,220,115) if ((x//16 + y//12) % 5 in (0,1) and (x*7+y*3)%11<8) else (0,0,0,0))

# Vanilla weather sheets are 64x256 in 1.21.x.
png(ENV/"rain.png",64,256,lambda x,y,w,h:
    (75,145,205,145) if ((x + (y*3)%64) % 17 in (0,1)) else (0,0,0,0))
png(ENV/"snow.png",64,256,lambda x,y,w,h:
    (220,230,235,175) if ((x*3+y) % 23 in (0,1)) else (0,0,0,0))

# Tiled End backdrop.
def endsky(x,y,w,h):
    if (x*17+y*31)%127==0: return (110,245,225,230)
    if (x*29+y*13)%173==0: return (210,100,225,210)
    return (13,7,25,255)
png(ENV/"end_sky.png",128,128,endsky)

# End flash used by the celestial/environment rendering.
png(ENV/"end_flash.png",64,64,lambda x,y,w,h:
    (220,245,240,210) if ((x-31.5)**2+(y-31.5)**2)<500 else (0,0,0,0))

meta={"min_format":[75,0],"max_format":[75,0],
      "description":{"text":"OBSIDIAN // Performance 16x v0.6 — Particles + Environment","color":"a8fff5"}}
(OUT/"pack.mcmeta").write_text(json.dumps(meta,indent=2))
print(f"Generated {len(PARTICLES)+2} particle textures and v0.6 celestial/weather assets.")
