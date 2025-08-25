
# BlockWorld3D (Python • Pygame + OpenGL)

A minimal block-based 3D sandbox written in **Python** using **Pygame** + **PyOpenGL**,
with a stub **RL interface** for future learning/interaction. This adapts your original
Python code into a small, modular engine with shaders and a world of blocks.
The character is named **Rashal**. You can **move**, **look around**, **place** and **remove** blocks.

> Note: Your original tree mentioned `main.java` and build files (`build.gradle`/`pom.xml`).
> Since your codebase is Python, this project provides a Python structure with `main.py`,
> while still matching the spirit of the requested layout (src/*, shaders, assets/*).

## Features
- Basic 3D world of cubes (flat terrain)
- First-person controller (WASD + mouse look), jump, gravity
- Place block (Right Click), remove block (Left Click)
- Simple per-face coloring & basic lighting in GLSL for nicer visuals
- Character named **Rashal** (see `entities/player.py`)
- RL interface stub in `src/ai/rl_interface.py` (socket-based JSON messages)
- Clean modular structure

## Controls
- **W A S D**: Move
- **SPACE**: Jump
- **Mouse Move**: Look around
- **Left Click**: Remove targeted block
- **Right Click**: Place block on the targeted face
- **ESC**: Release mouse / Quit when window closes

## Setup
```bash
# 1) Create venv (Windows PowerShell example)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install deps
python -m pip install pygame PyOpenGL PyOpenGL_accelerate numpy

# 3) Run
python src/main.py
```

If the window is black or shaders fail, ensure your GPU/driver supports OpenGL 3.3+.
Pygame will try to create a 3.3 context via `engine/window.py`.

## RL Interface (stub)
See `src/ai/rl_interface.py`. It exposes a simple socket server the agent can connect to:
- **OBSERVE** → returns camera/position/velocity and a sparse voxel snapshot around the player
- **ACT** (with movement flags) → applies actions next frame
This keeps the training loop decoupled from the rendering/game loop.

## Project Layout
```
BlockWorld3D/
├─ src/
│  ├─ engine/          # OpenGL, window, input, shader helpers
│  ├─ world/           # blocks, world storage, raycast & terrain
│  ├─ entities/        # player (Rashal), camera
│  ├─ ai/              # RL connection / interface (stub)
│  └─ main.py
├─ shaders/
│  ├─ vertex.glsl
│  └─ fragment.glsl
├─ assets/
│  └─ textures/        # (optional future use)
└─ README.md
```

## Notes
- Performance is fine for small worlds. For large worlds, add chunk meshing & frustum culling.
- Textures are optional—current shader uses per-face coloring + lighting for clarity.
- To extend graphics, drop PNGs in `assets/textures/` and modify the shader/engine to use a texture atlas.
