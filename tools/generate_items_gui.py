from pathlib import Path
import random, struct, zlib, json

OUT=Path("build/pack")
ITEM=OUT/"assets/minecraft/textures/item"
GUI=OUT/"assets/minecraft/textures/gui"
ITEM.mkdir(parents=True,exist_ok=True); GUI.mkdir(parents=True,exist_ok=True)

PAL={
"stone":(72,78,86),"metal":(155,164,168),"iron":(170,176,180),"gold":(224,180,55),
"diamond":(65,215,205),"emerald":(65,195,110),"lapis":(55,95,195),"redstone":(215,55,50),
"copper":(184,105,66),"amethyst":(165,105,210),"quartz":(220,216,204),"wood":(130,86,50),
"food":(190,105,65),"green":(65,150,75),"blue":(65,130,200),"purple":(140,80,185),
"white":(225,225,220),"dark":(35,39,46),"obsidian":(38,31,58),"paper":(205,198,170),
"leather":(145,88,55),"ender":(65,210,190)
}
COLORS={"white":(225,225,220),"light_gray":(165,165,160),"gray":(88,90,92),"black":(30,32,35),
"red":(190,55,52),"orange":(225,110,45),"yellow":(225,190,55),"lime":(115,190,55),
"green":(60,145,72),"cyan":(55,175,175),"light_blue":(75,155,215),"blue":(55,85,180),
"purple":(130,70,175),"magenta":(195,75,150),"pink":(225,135,160),"brown":(125,78,48)}

def png(path,w,h,base,accent=None,seed=0,alpha=255):
    r=random.Random(seed); px=[]
    for y in range(h):
        row=[]
        for x in range(w):
            q=r.randint(-9,9); row.append((max(0,min(255,base[0]+q)),max(0,min(255,base[1]+q)),max(0,min(255,base[2]+q)),alpha))
        px.append(row)
    if accent:
        for _ in range(max(2,(w*h)//18)):
            x=r.randrange(w); y=r.randrange(h)
            px[y][x]=(*accent,255)
            if x+1<w: px[y][x+1]=(*accent,255)
    raw=b"".join(b"\0"+bytes(sum((list(v) for v in row),[])) for row in px)
    def ch(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+ch(b"IHDR",struct.pack(">IIBBBBB",w,h,8,6,0,0,0))+ch(b"IDAT",zlib.compress(raw,9))+ch(b"IEND",b"")
    path.write_bytes(data)

# Safe, non-weapon item families: materials, food, utilities, navigation and armor.
ITEMS={
"coal":("dark",None),"charcoal":("dark",None),"raw_iron":("iron",None),"iron_ingot":("iron",None),
"raw_copper":("copper",None),"copper_ingot":("copper",None),"raw_gold":("gold",None),"gold_ingot":("gold",None),
"diamond":("diamond",None),"emerald":("emerald",None),"lapis_lazuli":("lapis",None),"redstone":("redstone",None),
"quartz":("quartz",None),"amethyst_shard":("amethyst",None),"netherite_scrap":("obsidian","redstone"),
"nether_star":("white","ender"),"ender_pearl":("ender","purple"),"echo_shard":("sculk","ender"),
"flint":("stone","dark"),"clay_ball":("paper","stone"),"brick":("redstone","paper"),
"wheat":("gold","green"),"wheat_seeds":("green","gold"),"beetroot_seeds":("green","redstone"),
"pumpkin_seeds":("gold","green"),"melon_seeds":("green","redstone"),"torchflower_seeds":("green","gold"),
"bread":("food","paper"),"apple":("redstone","green"),"golden_apple":("gold","redstone"),
"carrot":("orange","green"),"golden_carrot":("gold","green"),"potato":("paper","green"),
"beetroot":("redstone","green"),"melon_slice":("green","redstone"),"sweet_berries":("redstone","green"),
"glow_berries":("gold","green"),"cocoa_beans":("brown","gold"),
"stick":("wood","paper"),"paper":("paper","blue"),"book":("paper","leather"),"writable_book":("paper","leather"),
"map":("paper","blue"),"compass":("iron","redstone"),"clock":("gold","dark"),
"bucket":("iron","blue"),"water_bucket":("iron","blue"),"lava_bucket":("iron","redstone"),
"milk_bucket":("iron","white"),"powder_snow_bucket":("iron","white"),"shears":("iron","dark"),
"flint_and_steel":("iron","redstone"),"name_tag":("paper","redstone"),"lead":("leather","gold"),
"slime_ball":("green","white"),"magma_cream":("redstone","gold"),"blaze_powder":("gold","redstone"),
"ender_eye":("ender","gold"),"bone":("white","dark"),"bone_meal":("white","green"),
"string":("paper","white"),"feather":("white","paper"),"leather":("leather","paper"),
"rabbit_hide":("leather","white"),"ink_sac":("dark","blue"),"glow_ink_sac":("dark","gold"),
"experience_bottle":("green","glass"),"glass_bottle":("glass","white"),
"armor_trim_smithing_template":("paper","gold"),"netherite_upgrade_smithing_template":("paper","redstone"),
"diamond_horse_armor":("diamond","metal"),"golden_horse_armor":("gold","metal"),"iron_horse_armor":("iron","metal"),
"leather_horse_armor":("leather","paper"),"wolf_armor":("diamond","leather"),
"elytra":("obsidian","diamond"),"shield":("wood","iron")
}
PAL["sculk"]=(35,105,108); PAL["glass"]=(115,185,200); PAL["brown"]=(125,78,48)

for i,(name,(a,b)) in enumerate(ITEMS.items()):
    png(ITEM/f"{name}.png",16,16,PAL[a],PAL[b] if b else None,1000+i)

# UI texture family: dark obsidian panels, cyan accents, subtle pixel borders.
for i,name in enumerate(["widgets","inventory","container","recipe_book","crafting_table","furnace","smithing","creative_inventory_tab","slot","background"]):
    base=PAL["dark"]; acc=PAL["diamond"] if i%2==0 else PAL["amethyst"]
    png(GUI/f"{name}.png",32,32,base,acc,5000+i)

meta={"min_format":[75,0],"max_format":[75,0],
      "description":{"text":"OBSIDIAN // Performance 16x v0.5 — Items + GUI","color":"a8fff5"}}
(OUT/"pack.mcmeta").write_text(json.dumps(meta,indent=2))
print(f"Generated {len(ITEMS)} item textures and GUI textures.")
