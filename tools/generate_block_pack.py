from pathlib import Path
import random, struct, zlib, math, json, re

OUT = Path("build/pack")
BLOCK = OUT / "assets/minecraft/textures/block"
BLOCK.mkdir(parents=True, exist_ok=True)

# Minecraft Java 1.21.11 block registry coverage. Names are used as texture keys;
# additional common *_top/*_side/*_bottom variants are emitted for model coverage.
BLOCKS = """
acacia_button acacia_door acacia_fence acacia_fence_gate acacia_hanging_sign acacia_leaves acacia_log acacia_planks acacia_pressure_plate acacia_sapling acacia_shelf acacia_sign acacia_slab acacia_stairs acacia_trapdoor acacia_wall_hanging_sign acacia_wall_sign acacia_wood
activator_rail allium amethyst_block amethyst_cluster ancient_debris andesite andesite_slab andesite_stairs andesite_wall anvil attached_melon_stem attached_pumpkin_stem azalea azalea_leaves azure_bluet
bamboo bamboo_block bamboo_button bamboo_door bamboo_fence bamboo_fence_gate bamboo_hanging_sign bamboo_mosaic bamboo_mosaic_slab bamboo_mosaic_stairs bamboo_planks bamboo_pressure_plate bamboo_sapling bamboo_shelf bamboo_sign bamboo_slab bamboo_stairs bamboo_trapdoor bamboo_wall_hanging_sign bamboo_wall_sign
barrel barrier basalt beacon bedrock bee_nest beehive beetroot bell big_dripleaf big_dripleaf_stem birch_button birch_door birch_fence birch_fence_gate birch_hanging_sign birch_leaves birch_log birch_planks birch_pressure_plate birch_sapling birch_shelf birch_sign birch_slab birch_stairs birch_trapdoor birch_wall_hanging_sign birch_wall_sign birch_wood
black_banner black_bed black_candle black_candle_cake black_carpet black_concrete black_concrete_powder black_glazed_terracotta black_shulker_box black_stained_glass black_stained_glass_pane black_terracotta black_wall_banner black_wool blackstone blackstone_slab blackstone_stairs blackstone_wall blast_furnace
blue_banner blue_bed blue_candle blue_candle_cake blue_carpet blue_concrete blue_concrete_powder blue_glazed_terracotta blue_ice blue_orchid blue_shulker_box blue_stained_glass blue_stained_glass_pane blue_terracotta blue_wall_banner blue_wool bone_block bookshelf brain_coral brain_coral_block brain_coral_fan brain_coral_wall_fan brewing_stand brick_slab brick_stairs brick_wall bricks brown_banner brown_bed brown_candle brown_candle_cake brown_carpet brown_concrete brown_concrete_powder brown_glazed_terracotta brown_mushroom brown_mushroom_block brown_shulker_box brown_stained_glass brown_stained_glass_pane brown_terracotta brown_wall_banner brown_wool bubble_column bubble_coral bubble_coral_block bubble_coral_fan bubble_coral_wall_fan budding_amethyst bush
cactus cactus_flower cake calibrated_sculk_sensor campfire candle candle_cake carrots cartography_table carved_pumpkin cauldron cave_air cave_vines cave_vines_plant chain_command_block cherry_button cherry_door cherry_fence cherry_fence_gate cherry_hanging_sign cherry_leaves cherry_log cherry_planks cherry_pressure_plate cherry_sapling cherry_shelf cherry_sign cherry_slab cherry_stairs cherry_trapdoor cherry_wall_hanging_sign cherry_wall_sign cherry_wood chest chipped_anvil chiseled_bookshelf chiseled_copper chiseled_deepslate chiseled_nether_bricks chiseled_polished_blackstone chiseled_quartz_block chiseled_red_sandstone chiseled_resin_bricks chiseled_sandstone chiseled_stone_bricks chiseled_tuff chiseled_tuff_bricks chorus_flower chorus_plant clay closed_eyeblossom coal_block coal_ore coarse_dirt cobbled_deepslate cobbled_deepslate_slab cobbled_deepslate_stairs cobbled_deepslate_wall cobblestone cobblestone_slab cobblestone_stairs cobblestone_wall cobweb cocoa command_block comparator composter conduit copper_bars copper_block copper_bulb copper_chain copper_chest copper_door copper_golem_statue copper_grate copper_lantern copper_ore copper_torch copper_trapdoor copper_wall_torch cornflower crimson_button crimson_door crimson_fence crimson_fence_gate crimson_fungus crimson_hanging_sign crimson_hyphae crimson_nylium crimson_planks crimson_pressure_plate crimson_roots crimson_shelf crimson_sign crimson_slab crimson_stairs crimson_stem crimson_trapdoor crimson_wall_hanging_sign crimson_wall_sign crying_obsidian cut_copper cut_copper_slab cut_copper_stairs cut_red_sandstone cut_red_sandstone_slab cut_sandstone cut_sandstone_slab
cyan_banner cyan_bed cyan_candle cyan_candle_cake cyan_carpet cyan_concrete cyan_concrete_powder cyan_glazed_terracotta cyan_shulker_box cyan_stained_glass cyan_stained_glass_pane cyan_terracotta cyan_wall_banner cyan_wool
damaged_anvil dandelion dark_oak_button dark_oak_door dark_oak_fence dark_oak_fence_gate dark_oak_hanging_sign dark_oak_leaves dark_oak_log dark_oak_planks dark_oak_pressure_plate dark_oak_sapling dark_oak_shelf dark_oak_sign dark_oak_slab dark_oak_stairs dark_oak_trapdoor dark_oak_wall_hanging_sign dark_oak_wall_sign dark_oak_wood dark_prismarine daylight_detector dead_brain_coral dead_brain_coral_block dead_brain_coral_fan dead_brain_coral_wall_fan dead_bubble_coral dead_bubble_coral_block dead_bubble_coral_fan dead_bubble_coral_wall_fan dead_bush dead_fire_coral dead_fire_coral_block dead_fire_coral_fan dead_fire_coral_wall_fan dead_horn_coral dead_horn_coral_block dead_horn_coral_fan dead_horn_coral_wall_fan dead_tube_coral dead_tube_coral_block dead_tube_coral_fan dead_tube_coral_wall_fan decorated_pot deepslate deepslate_brick_slab deepslate_brick_stairs deepslate_brick_wall deepslate_bricks deepslate_coal_ore deepslate_copper_ore deepslate_diamond_ore deepslate_emerald_ore deepslate_gold_ore deepslate_iron_ore deepslate_lapis_ore deepslate_redstone_ore deepslate_tile_slab deepslate_tile_stairs deepslate_tile_wall deepslate_tiles detector_rail diamond_block diamond_ore diorite diorite_slab diorite_stairs diorite_wall dirt dirt_path dispenser dragon_egg dragon_head dragon_wall_head dried_ghast dried_kelp_block dripstone_block dropper emerald_block emerald_ore enchanting_table end_gateway end_portal end_portal_frame end_rod end_stone end_stone_brick_slab end_stone_brick_stairs end_stone_brick_wall end_stone_bricks ender_chest exposed_chiseled_copper exposed_copper exposed_copper_bars exposed_copper_bulb exposed_copper_chain exposed_copper_chest exposed_copper_door exposed_copper_golem_statue exposed_copper_grate exposed_copper_lantern exposed_copper_trapdoor exposed_cut_copper exposed_cut_copper_slab exposed_cut_copper_stairs exposed_lightning_rod
farmland fern fire fire_coral fire_coral_block fire_coral_fan fire_coral_wall_fan firefly_bush fletching_table flower_pot flowering_azalea flowering_azalea_leaves frogspawn frosted_ice furnace gilded_blackstone glass glass_pane glow_lichen glowstone gold_block gold_ore granite granite_slab granite_stairs granite_wall grass_block gravel gray_banner gray_bed gray_candle gray_candle_cake gray_carpet gray_concrete gray_concrete_powder gray_glazed_terracotta gray_shulker_box gray_stained_glass gray_stained_glass_pane gray_terracotta gray_wall_banner gray_wool green_banner green_bed green_candle green_candle_cake green_carpet green_concrete green_concrete_powder green_glazed_terracotta green_shulker_box green_stained_glass green_stained_glass_pane green_terracotta green_wall_banner green_wool grindstone hanging_roots hay_block heavy_core heavy_weighted_pressure_plate honey_block honeycomb_block hopper horn_coral horn_coral_block horn_coral_fan horn_coral_wall_fan ice infested_chiseled_stone_bricks infested_cobblestone infested_cracked_stone_bricks infested_deepslate infested_mossy_stone_bricks infested_stone infested_stone_bricks iron_bars iron_block iron_chain iron_door iron_ore iron_trapdoor jack_o_lantern jigsaw jukebox jungle_button jungle_door jungle_fence jungle_fence_gate jungle_hanging_sign jungle_leaves jungle_log jungle_planks jungle_pressure_plate jungle_sapling jungle_shelf jungle_sign jungle_slab jungle_stairs jungle_trapdoor jungle_wall_hanging_sign jungle_wall_sign jungle_wood
kelp kelp_plant ladder lantern lapis_block lapis_ore large_amethyst_bud large_fern lava lava_cauldron leaf_litter lectern lever light light_blue_banner light_blue_bed light_blue_candle light_blue_candle_cake light_blue_carpet light_blue_concrete light_blue_concrete_powder light_blue_glazed_terracotta light_blue_shulker_box light_blue_stained_glass light_blue_stained_glass_pane light_blue_terracotta light_blue_wall_banner light_blue_wool light_gray_banner light_gray_bed light_gray_candle light_gray_candle_cake light_gray_carpet light_gray_concrete light_gray_concrete_powder light_gray_glazed_terracotta light_gray_shulker_box light_gray_stained_glass light_gray_stained_glass_pane light_gray_terracotta light_gray_wall_banner light_gray_wool light_weighted_pressure_plate lightning_rod lilac lily_of_the_valley lily_pad lime_banner lime_bed lime_candle lime_candle_cake lime_carpet lime_concrete lime_concrete_powder lime_glazed_terracotta lime_shulker_box lime_stained_glass lime_stained_glass_pane lime_terracotta lime_wall_banner lime_wool lodestone loom magenta_banner magenta_bed magenta_candle magenta_candle_cake magenta_carpet magenta_concrete magenta_concrete_powder magenta_glazed_terracotta magenta_shulker_box magenta_stained_glass magenta_stained_glass_pane magenta_terracotta magenta_wall_banner magenta_wool magma_block mangrove_button mangrove_door mangrove_fence mangrove_fence_gate mangrove_hanging_sign mangrove_leaves mangrove_log mangrove_planks mangrove_pressure_plate mangrove_propagule mangrove_roots mangrove_shelf mangrove_sign mangrove_slab mangrove_stairs mangrove_trapdoor mangrove_wall_hanging_sign mangrove_wall_sign mangrove_wood medium_amethyst_bud melon melon_stem moss_block moss_carpet mossy_cobblestone mossy_cobblestone_slab mossy_cobblestone_stairs mossy_cobblestone_wall mossy_stone_brick_slab mossy_stone_brick_stairs mossy_stone_brick_wall mossy_stone_bricks moving_piston mud mud_brick_slab mud_brick_stairs mud_brick_wall mud_bricks muddy_mangrove_roots mushroom_stem mycelium nether_brick_fence nether_brick_slab nether_brick_stairs nether_brick_wall nether_bricks nether_gold_ore nether_portal nether_quartz_ore nether_sprouts nether_wart nether_wart_block netherite_block netherrack note_block oak_button oak_door oak_fence oak_fence_gate oak_hanging_sign oak_leaves oak_log oak_planks oak_pressure_plate oak_sapling oak_shelf oak_sign oak_slab oak_stairs oak_trapdoor oak_wall_hanging_sign oak_wall_sign oak_wood observer obsidian ochre_froglight open_eyeblossom orange_banner orange_bed orange_candle orange_candle_cake orange_carpet orange_concrete orange_concrete_powder orange_glazed_terracotta orange_shulker_box orange_stained_glass orange_stained_glass_pane orange_terracotta orange_tulip orange_wall_banner orange_wool oxeye_daisy oxidized_chiseled_copper oxidized_copper oxidized_copper_bars oxidized_copper_bulb oxidized_copper_chain oxidized_copper_chest oxidized_copper_door oxidized_copper_golem_statue oxidized_copper_grate oxidized_copper_lantern oxidized_copper_trapdoor oxidized_cut_copper oxidized_cut_copper_slab oxidized_cut_copper_stairs oxidized_lightning_rod packed_ice packed_mud pale_hanging_moss pale_moss_block pale_moss_carpet pale_oak_button pale_oak_door pale_oak_fence pale_oak_fence_gate pale_oak_hanging_sign pale_oak_leaves pale_oak_log pale_oak_planks pale_oak_pressure_plate pale_oak_sapling pale_oak_shelf pale_oak_sign pale_oak_slab pale_oak_stairs pale_oak_trapdoor pale_oak_wall_hanging_sign pale_oak_wall_sign pale_oak_wood pearlescent_froglight peony petrified_oak_slab piglin_head piglin_wall_head pink_banner pink_bed pink_candle pink_candle_cake pink_carpet pink_concrete pink_concrete_powder pink_glazed_terracotta pink_petals pink_shulker_box pink_stained_glass pink_stained_glass_pane pink_terracotta pink_tulip pink_wall_banner pink_wool piston piston_head pitcher_crop pitcher_plant player_head player_wall_head podzol pointed_dripstone polished_andesite polished_andesite_slab polished_andesite_stairs polished_basalt polished_blackstone polished_blackstone_brick_slab polished_blackstone_brick_stairs polished_blackstone_brick_wall polished_blackstone_bricks polished_blackstone_button polished_blackstone_pressure_plate polished_blackstone_slab polished_blackstone_stairs polished_blackstone_wall polished_deepslate polished_deepslate_slab polished_deepslate_stairs polished_deepslate_wall polished_diorite polished_diorite_slab polished_diorite_stairs polished_granite polished_granite_slab polished_granite_stairs polished_tuff polished_tuff_slab polished_tuff_stairs polished_tuff_wall poppy potatoes potted_acacia_sapling potted_allium potted_azalea_bush potted_azure_bluet potted_bamboo potted_birch_sapling potted_blue_orchid potted_brown_mushroom potted_cactus potted_cherry_sapling potted_closed_eyeblossom potted_cornflower potted_crimson_fungus potted_crimson_roots potted_dandelion potted_dark_oak_sapling potted_dead_bush potted_fern potted_flowering_azalea_bush potted_jungle_sapling potted_lily_of_the_valley potted_mangrove_propagule potted_oak_sapling potted_open_eyeblossom potted_orange_tulip potted_oxeye_daisy potted_pale_oak_sapling potted_pink_tulip potted_poppy potted_red_mushroom potted_red_tulip potted_spruce_sapling potted_torchflower potted_warped_fungus potted_warped_roots potted_white_tulip potted_wither_rose powder_snow powder_snow_cauldron powered_rail prismarine prismarine_brick_slab prismarine_brick_stairs prismarine_bricks prismarine_slab prismarine_stairs prismarine_wall pumpkin pumpkin_stem purple_banner purple_bed purple_candle purple_candle_cake purple_carpet purple_concrete purple_concrete_powder purple_glazed_terracotta purple_shulker_box purple_stained_glass purple_stained_glass_pane purple_terracotta purple_wall_banner purple_wool purpur_block purpur_pillar purpur_slab purpur_stairs quartz_block quartz_bricks quartz_pillar quartz_slab quartz_stairs rail raw_copper_block raw_gold_block raw_iron_block red_banner red_bed red_candle red_candle_cake red_carpet red_concrete red_concrete_powder red_glazed_terracotta red_mushroom red_mushroom_block red_nether_brick_slab red_nether_brick_stairs red_nether_brick_wall red_nether_bricks red_sand red_sandstone red_sandstone_slab red_sandstone_stairs red_sandstone_wall red_shulker_box red_stained_glass red_stained_glass_pane red_terracotta red_tulip red_wall_banner red_wool redstone_block redstone_lamp redstone_ore redstone_torch redstone_wall_torch redstone_wire reinforced_deepslate repeater repeating_command_block resin_block resin_brick_slab resin_brick_stairs resin_brick_wall resin_bricks resin_clump respawn_anchor rooted_dirt rose_bush sand sandstone sandstone_slab sandstone_stairs sandstone_wall scaffolding sculk sculk_catalyst sculk_sensor sculk_shrieker sculk_vein sea_lantern sea_pickle seagrass short_dry_grass short_grass shroomlight shulker_box skeleton_skull skeleton_wall_skull slime_block small_amethyst_bud small_dripleaf smithing_table smoker smooth_basalt smooth_quartz smooth_quartz_slab smooth_quartz_stairs smooth_red_sandstone smooth_red_sandstone_slab smooth_red_sandstone_stairs smooth_sandstone smooth_sandstone_slab smooth_sandstone_stairs smooth_stone smooth_stone_slab sniffer_egg snow snow_block soul_campfire soul_fire soul_lantern soul_sand soul_soil soul_torch soul_wall_torch spawner sponge spore_blossom spruce_button spruce_door spruce_fence spruce_fence_gate spruce_hanging_sign spruce_leaves spruce_log spruce_planks spruce_pressure_plate spruce_sapling spruce_shelf spruce_sign spruce_slab spruce_stairs spruce_trapdoor spruce_wall_hanging_sign spruce_wall_sign spruce_wood sticky_piston stone stone_brick_slab stone_brick_stairs stone_brick_wall stone_bricks stone_button stone_pressure_plate stone_slab stone_stairs stonecutter stripped_acacia_log stripped_acacia_wood stripped_bamboo_block stripped_birch_log stripped_birch_wood stripped_cherry_log stripped_cherry_wood stripped_crimson_hyphae stripped_crimson_stem stripped_dark_oak_log stripped_dark_oak_wood stripped_jungle_log stripped_jungle_wood stripped_mangrove_log stripped_mangrove_wood stripped_oak_log stripped_oak_wood stripped_pale_oak_log stripped_pale_oak_wood stripped_spruce_log stripped_spruce_wood stripped_warped_hyphae stripped_warped_stem structure_block structure_void sugar_cane sunflower suspicious_gravel suspicious_sand sweet_berry_bush tall_dry_grass tall_grass tall_seagrass target terracotta test_block test_instance_block tinted_glass tnt torch torchflower torchflower_crop trapped_chest trial_spawner tripwire tripwire_hook tube_coral tube_coral_block tube_coral_fan tube_coral_wall_fan tuff tuff_brick_slab tuff_brick_stairs tuff_brick_wall tuff_bricks tuff_slab tuff_stairs tuff_wall turtle_egg twisting_vines twisting_vines_plant vault verdant_froglight vine void_air wall_torch warped_button warped_door warped_fence warped_fence_gate warped_fungus warped_hanging_sign warped_hyphae warped_nylium warped_planks warped_pressure_plate warped_roots warped_shelf warped_sign warped_slab warped_stairs warped_stem warped_trapdoor warped_wall_hanging_sign warped_wall_sign warped_wart_block water water_cauldron waxed_chiseled_copper waxed_copper_bars waxed_copper_block waxed_copper_bulb waxed_copper_chain waxed_copper_chest waxed_copper_door waxed_copper_golem_statue waxed_copper_grate waxed_copper_lantern waxed_copper_trapdoor waxed_cut_copper waxed_cut_copper_slab waxed_cut_copper_stairs waxed_exposed_chiseled_copper waxed_exposed_copper waxed_exposed_copper_bars waxed_exposed_copper_bulb waxed_exposed_copper_chain waxed_exposed_copper_chest waxed_exposed_copper_door waxed_exposed_copper_golem_statue waxed_exposed_copper_grate waxed_exposed_copper_lantern waxed_exposed_copper_trapdoor waxed_exposed_cut_copper waxed_exposed_cut_copper_slab waxed_exposed_cut_copper_stairs waxed_exposed_lightning_rod waxed_lightning_rod waxed_oxidized_chiseled_copper waxed_oxidized_copper waxed_oxidized_copper_bars waxed_oxidized_copper_bulb waxed_oxidized_copper_chain waxed_oxidized_copper_chest waxed_oxidized_copper_door waxed_oxidized_copper_golem_statue waxed_oxidized_copper_grate waxed_oxidized_copper_lantern waxed_oxidized_copper_trapdoor waxed_oxidized_cut_copper waxed_oxidized_cut_copper_slab waxed_oxidized_cut_copper_stairs waxed_oxidized_lightning_rod waxed_weathered_chiseled_copper waxed_weathered_copper waxed_weathered_copper_bars waxed_weathered_copper_bulb waxed_weathered_copper_chain waxed_weathered_copper_chest waxed_weathered_copper_door waxed_weathered_copper_golem_statue waxed_weathered_copper_grate waxed_weathered_copper_lantern waxed_weathered_copper_trapdoor waxed_weathered_cut_copper waxed_weathered_cut_copper_slab waxed_weathered_cut_copper_stairs waxed_weathered_lightning_rod weathered_chiseled_copper weathered_copper weathered_copper_bars weathered_copper_bulb weathered_copper_chain weathered_copper_chest weathered_copper_door weathered_copper_golem_statue weathered_copper_grate weathered_copper_lantern weathered_copper_trapdoor weathered_cut_copper weathered_cut_copper_slab weathered_cut_copper_stairs weathered_lightning_rod weeping_vines weeping_vines_plant wet_sponge wheat white_banner white_bed white_candle white_candle_cake white_carpet white_concrete white_concrete_powder white_glazed_terracotta white_shulker_box white_stained_glass white_stained_glass_pane white_terracotta white_tulip white_wall_banner white_wool wildflowers wither_rose wither_skeleton_skull wither_skeleton_wall_skull yellow_banner yellow_bed yellow_candle yellow_candle_cake yellow_carpet yellow_concrete yellow_concrete_powder yellow_glazed_terracotta yellow_shulker_box yellow_stained_glass yellow_stained_glass_pane yellow_terracotta yellow_wall_banner yellow_wool zombie_head zombie_wall_head
""".split()

# Palette is intentionally OBSIDIAN: deep base, cool shadows, bright material accents.
PALETTE = {
    "stone": (92, 98, 104), "deepslate": (43, 49, 57), "sand": (178, 157, 105),
    "dirt": (92, 68, 48), "wood": (128, 82, 48), "spruce": (74, 55, 42),
    "birch": (190, 172, 128), "jungle": (132, 86, 49), "acacia": (154, 76, 49),
    "dark_oak": (65, 45, 34), "mangrove": (103, 45, 43), "cherry": (190, 105, 130),
    "bamboo": (150, 165, 68), "pale_oak": (168, 158, 133), "crimson": (120, 43, 57),
    "warped": (43, 120, 116), "nether": (104, 43, 43), "end": (196, 187, 133),
    "obsidian": (32, 27, 51), "ice": (126, 180, 220), "glass": (115, 185, 200),
    "plant": (52, 125, 69), "flower": (205, 92, 135), "copper": (178, 104, 66),
    "gold": (220, 174, 54), "iron": (157, 164, 166), "diamond": (67, 210, 202),
    "emerald": (65, 190, 110), "lapis": (52, 93, 190), "redstone": (210, 50, 48),
    "coal": (35, 39, 43), "amethyst": (160, 100, 205), "resin": (190, 125, 55),
    "sculk": (35, 105, 108), "quartz": (216, 211, 198), "white": (218, 220, 216)
}

COLORS = {
    "white": (225,225,220), "light_gray": (155,155,150), "gray": (80,82,82),
    "black": (30,30,32), "red": (165,55,50), "orange": (220,105,45), "yellow": (220,185,55),
    "lime": (110,185,55), "green": (60,135,70), "cyan": (50,165,165), "light_blue": (70,150,210),
    "blue": (55,80,170), "purple": (125,65,165), "magenta": (190,70,145), "pink": (225,135,155),
    "brown": (120,75,48)
}



# Stone family: brighter OBSIDIAN treatment with subtle luminous highlights.
# This is a visual brightness treatment only; it does not make blocks emit light.
STONE_PALETTES = {
    "stone": (112, 118, 126),
    "cobblestone": (101, 108, 116),
    "smooth_stone": (145, 151, 158),
    "granite": (177, 108, 88),
    "polished_granite": (194, 116, 92),
    "diorite": (190, 193, 192),
    "polished_diorite": (211, 213, 210),
    "andesite": (126, 131, 136),
    "polished_andesite": (149, 154, 159),
    "deepslate": (59, 67, 78),
    "cobbled_deepslate": (53, 61, 71),
    "polished_deepslate": (75, 84, 96),
    "tuff": (135, 130, 118),
    "calcite": (216, 213, 203),
    "basalt": (76, 83, 92),
    "smooth_basalt": (91, 98, 107),
    "blackstone": (62, 54, 66),
    "polished_blackstone": (76, 66, 82),
    "stone_bricks": (104, 110, 116),
    "deepslate_bricks": (67, 75, 86),
    "deepslate_tiles": (60, 68, 80),
    "tuff_bricks": (126, 122, 112),
    "polished_tuff": (151, 147, 137),
    "end_stone": (202, 198, 151),
    "end_stone_bricks": (183, 180, 139),
    "prismarine": (86, 155, 145),
    "prismarine_bricks": (78, 145, 137),
    "dark_prismarine": (61, 105, 101),
    "mossy_cobblestone": (89, 112, 91),
    "mossy_stone_bricks": (96, 119, 98),
}

STONE_KEYS = set(STONE_PALETTES)

def png(path, base, accent=None, mode="noise", seed=0):
    r = random.Random(seed)
    px = [[(*base,255) for _ in range(16)] for _ in range(16)]
    for y in range(16):
        for x in range(16):
            q = r.randint(-11,11)
            if mode == "brick":
                q += -7 if (y % 4 == 0 or (x-(2 if (y//4)%2 else 0)) % 8 == 0) else 0
            if mode == "wood":
                q += int(math.sin(x/2.2 + y/4)*7)
            px[y][x] = tuple(max(0,min(255,c+q)) for c in base) + (255,)
    if mode == "ore":
        ac = accent or (255,255,255)
        for _ in range(12):
            x,y=r.randrange(1,15),r.randrange(1,15)
            for dx,dy in ((0,0),(1,0),(0,1)):
                if 0<=x+dx<16 and 0<=y+dy<16:
                    px[y+dy][x+dx]=(*ac,255)
    if mode == "glass":
        for y in range(16):
            for x in range(16):
                px[y][x]=(*base,90 if (x+y)%3 else 135)
        ac=accent or base
        for i in range(16):
            px[i][i]=(*ac,205)
    if mode == "leaf":
        for y in range(16):
            for x in range(16):
                if r.random()<.13: px[y][x]=(0,0,0,0)
    if mode == "plant":
        for y in range(16):
            for x in range(16):
                if not (abs(x-7)<3 or (y>8 and abs(x-8)<5)): px[y][x]=(0,0,0,0)
        ac=accent or base
        for y in range(4,15):
            x=7+(y%3-1)
            px[y][x]=(*ac,255)
    if mode == "stone_glow":
        # Keep the recognizable Minecraft-like pixel texture, but brighten the
        # material and add restrained luminous flecks/edges instead of a flat wash.
        for y in range(16):
            for x in range(16):
                rr,gg,bb,_ = px[y][x]
                lift = 8 + ((x * 7 + y * 11 + seed) % 7)
                px[y][x] = (
                    min(255, rr + lift),
                    min(255, gg + lift),
                    min(255, bb + lift),
                    255
                )
        ac = accent or tuple(min(255, v + 42) for v in base)
        for _ in range(10):
            x,y = r.randrange(1,15),r.randrange(1,15)
            px[y][x] = (*ac,255)
            if r.random() < 0.45 and x < 15:
                px[y][x+1] = (*ac,255)
        # A few restrained highlights give the stone a soft "glow" impression
        # without requiring emissive shaders.
        for x,y in ((2,3),(8,2),(13,6),(5,11),(11,13)):
            if (x + y + seed) % 3:
                rr,gg,bb,_ = px[y][x]
                px[y][x] = (min(255,rr+18),min(255,gg+18),min(255,bb+18),255)
    if accent and mode not in ("ore","glass","plant","stone_glow"):
        for i in range(3):
            x=r.randrange(16); y=r.randrange(16)
            px[y][x]=(*accent,255)
    raw=b"".join(b"\0"+bytes(sum((list(v) for v in row),[])) for row in px)
    def chunk(t,d): return struct.pack(">I",len(d))+t+d+struct.pack(">I",zlib.crc32(t+d)&0xffffffff)
    data=b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",16,16,8,6,0,0,0))+chunk(b"IDAT",zlib.compress(raw,9))+chunk(b"IEND",b"")
    path.write_bytes(data)

def base_for(name):
    n=name
    # Stone-family textures get their own brighter, material-specific palette.
    # This intentionally runs before the generic material matching below.
    if n in STONE_PALETTES:
        return STONE_PALETTES[n]
    if any(k in n for k in ("diamond","lapis","blue_ice")): return PALETTE["diamond"]
    if "emerald" in n: return PALETTE["emerald"]
    if "redstone" in n: return PALETTE["redstone"]
    if "coal" in n: return PALETTE["coal"]
    if "gold" in n: return PALETTE["gold"]
    if "iron" in n: return PALETTE["iron"]
    if "copper" in n: return PALETTE["copper"]
    if "amethyst" in n: return PALETTE["amethyst"]
    if "quartz" in n: return PALETTE["quartz"]
    if "resin" in n: return PALETTE["resin"]
    if "sculk" in n: return PALETTE["sculk"]
    for k in ("pale_oak","dark_oak","mangrove","cherry","bamboo","acacia","jungle","birch","spruce"):
        if k in n: return PALETTE[k]
    if "crimson" in n: return PALETTE["crimson"]
    if "warped" in n: return PALETTE["warped"]
    if any(k in n for k in ("nether","netherrack","magma")): return PALETTE["nether"]
    if any(k in n for k in ("end_", "purpur", "chorus", "dragon")): return PALETTE["end"]
    if any(k in n for k in ("obsidian",)): return PALETTE["obsidian"]
    if any(k in n for k in ("glass","ice","water")): return PALETTE["glass"]
    if any(k in n for k in ("flower","rose","tulip","petal","allium","dandelion","lilac","peony")): return PALETTE["flower"]
    if any(k in n for k in ("leaves","leaf","grass","fern","moss","vine","kelp","coral","bush","sapling","roots","fungus","wart")): return PALETTE["plant"]
    if any(k in n for k in ("wood","log","planks","door","fence","shelf","sign","button","trapdoor")): return PALETTE["wood"]
    if any(k in n for k in ("sand","sandstone","gravel","snow","powder")): return PALETTE["sand"]
    if any(k in n for k in ("dirt","mud","farmland","podzol","mycelium")): return PALETTE["dirt"]
    if any(k in n for k in ("brick","stone","slab","stairs","wall","deepslate","tuff","basalt","blackstone","granite","diorite","andesite","cobble")): return PALETTE["stone"]
    if any(k in n for k in ("concrete","wool","banner","bed","candle","carpet","terracotta","shulker")):
        c=next((v for k,v in COLORS.items() if k in n),PALETTE["stone"]); return c
    return PALETTE["stone"]

def accent_for(name):
    for key, val in (("diamond",PALETTE["diamond"]),("emerald",PALETTE["emerald"]),("gold",PALETTE["gold"]),("iron",PALETTE["iron"]),("copper",PALETTE["copper"]),("lapis",PALETTE["lapis"]),("redstone",PALETTE["redstone"]),("coal",PALETTE["coal"])):
        if key in name: return val
    return None

def style_for(name):
    if name in STONE_KEYS:
        return "stone_glow"
    if any(k in name for k in ("ore","debris")): return "ore"
    if "glass" in name: return "glass"
    if any(k in name for k in ("leaves",)): return "leaf"
    if any(k in name for k in ("sapling","flower","grass","fern","vine","kelp","coral","roots","fungus","mushroom","bush","lily","dripleaf","seagrass","wart","petals","torchflower")): return "plant"
    if any(k in name for k in ("brick","tile","bookshelf")): return "brick"
    if any(k in name for k in ("log","wood","planks","hyphae","stem")): return "wood"
    return "noise"

# Emit every registry key.
for i, name in enumerate(sorted(set(BLOCKS))):
    b=base_for(name); a=accent_for(name)
    png(BLOCK/f"{name}.png", b, a, style_for(name), i+1000)

# Common model texture variants. These make top/side/bottom references resolve
# consistently for logs, grass, stone-like cubes and common utility blocks.
for i, name in enumerate(sorted(set(BLOCKS))):
    b=base_for(name); a=accent_for(name); mode=style_for(name)
    if any(k in name for k in ("log","wood","stem","hyphae","block")):
        png(BLOCK/f"{name}_top.png", tuple(min(255,x+12) for x in b), a, mode, 5000+i)
    if any(k in name for k in ("grass_block","dirt","podzol","mycelium","farmland","path")):
        png(BLOCK/f"{name}_top.png", tuple(min(255,x+18) for x in b), a, mode, 6000+i)
        png(BLOCK/f"{name}_side.png", b, a, mode, 7000+i)
        png(BLOCK/f"{name}_bottom.png", tuple(max(0,x-12) for x in b), a, mode, 8000+i)

# Explicit high-visibility ore variants used by vanilla deepslate models.
for ore, ac in {
    "coal":PALETTE["coal"], "copper":PALETTE["copper"], "diamond":PALETTE["diamond"],
    "emerald":PALETTE["emerald"], "gold":PALETTE["gold"], "iron":PALETTE["iron"],
    "lapis":PALETTE["lapis"], "redstone":PALETTE["redstone"]
}.items():
    for host, hb in (("stone",PALETTE["stone"]),("deepslate",PALETTE["deepslate"])):
        if host=="deepslate" or f"{ore}_ore" in BLOCKS:
            png(BLOCK/f"{host}_{ore}_ore.png", hb, ac, "ore", 9000+len(ore)+(1 if host=="deepslate" else 0))

meta={"min_format":[75,0],"max_format":[75,0],
      "description":{"text":"OBSIDIAN // Performance 16x v0.6 — Brighter Stone Family","color":"a8fff5"}}
(OUT/"pack.mcmeta").write_text(json.dumps(meta,indent=2))
print(f"Generated {len(list(BLOCK.glob('*.png')))} block textures.")
