from pathlib import Path
import random, struct, zlib, json, math

OUT=Path("build/pack")
PART=OUT/"assets/minecraft/textures/particle"
ENV=OUT/"assets/minecraft/textures/environment"
PART.mkdir(parents=True,exist_ok=True); ENV.mkdir(parents=True,exist_ok=True)

def png(path,w,h,pixel_fn):
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

# OBSIDIAN sky: subtle midnight gradient with cyan horizon and a compact star field.
def sky(x,y,w,h):
    t=y/(h-1)
    top=(12,10,20); bottom=(48,72,92)
    c=tuple(int(top[i]*(1-t)+bottom[i]*t) for i in range(3))
    stars={(7,5),(20,9),(34,6),(49,14),(58,8),(12,22),(42,25),(53,29)}
    if (x,y) in stars: return (175,240,235,235)
    return (*c,255)
png(ENV/"overworld_sky.png",64,64,sky)

# Sun: compact cyan-white OBSIDIAN core with a warm rim.
def sun(x,y,w,h):
    d=((x-(w-1)/2)**2+(y-(h-1)/2)**2)**0.5
    if d>24: return (0,0,0,0)
    if d>20: return (235,185,70,170)
    t=d/20
    return (int(225-80*t),int(250-40*t),int(245-20*t),255)
png(ENV/"sun.png",64,64,sun)

# Eight moon phases in one 256x32 strip.
def moon(x,y,w,h):
    phase=(x//32)%8
    cx=(phase*32)+15.5; cy=15.5
    d=((x-cx)**2+(y-cy)**2)**0.5
    if d>14.5: return (0,0,0,0)
    # phase shading shifts from left to right across the strip.
    local=x-phase*32
    shadow=(phase/7)*30
    edge=200+int(35*(1-d/14.5))
    return (175+int(shadow),220+int(shadow/2),225,edge)
png(ENV/"moon_phases.png",256,32,moon)

# Rain/snow overlays use simple high-contrast silhouettes.
png(ENV/"rain.png",64,64,lambda x,y,w,h: (75,145,205,130) if ((x+y*2)%17 in (0,1)) else (0,0,0,0))
png(ENV/"snow.png",64,64,lambda x,y,w,h: (220,230,235,170) if ((x*3+y)%19 in (0,1)) else (0,0,0,0))

# End sky: deep obsidian field with cyan/magenta star accents.
def endsky(x,y,w,h):
    t=(x+y)/(w+h)
    base=(13,7,25)
    if (x*17+y*31)%127==0: return (110,245,225,230)
    if (x*29+y*13)%173==0: return (210,100,225,210)
    return (*base,255)
png(ENV/"end_sky.png",128,128,endsky)

meta={"min_format":[75,0],"max_format":[75,0],
      "description":{"text":"OBSIDIAN // Performance 16x v0.6 — Particles + Environment","color":"a8fff5"}}
(OUT/"pack.mcmeta").write_text(json.dumps(meta,indent=2))
print(f"Generated {len(PARTICLES)+2} particle textures and environment sky/weather assets.")
