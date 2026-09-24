# Chat-GPT's Texture Pack

**OBSIDIAN // Performance 16x** — a lightweight Minecraft Java Edition 1.21.11 resource pack made by GPT for Aksh.

## v0.4 — Complete Block Overhaul

The build now generates a broad 1.21.11 block-texture set in one automated pass, including:

- stone, deepslate, tuff, sandstone, Nether and End families
- all major wood families, logs, planks and variants
- concrete, terracotta, wool, glass and decorative colour families
- ores with high-visibility accent treatment
- copper/weathering/waxed families
- plants, foliage, coral and nature blocks
- redstone/utility/building blocks
- common top/side/bottom model variants

Textures are 16×16 and generated deterministically by the repository's Python build script. Missing/unsupported vanilla model details can still fall back to Minecraft's default textures.

## Build

GitHub Actions automatically builds the ZIP on pushes to main.

The workflow packages the expanded generator output into the build artifact.

## Goals

- 16× textures for a small resource footprint
- darker, cleaner OBSIDIAN visual style
- high-contrast materials and ores
- consistent pixel-art families
- no shaders or gameplay changes

Minecraft Java Edition 1.21.11 resource-pack format 75.0 is targeted.