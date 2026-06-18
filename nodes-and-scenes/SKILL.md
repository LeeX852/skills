---
name: nodes-and-scenes
description: Design and manage Godot's node and scene system. Use this skill when creating scenes, designing node hierarchies, instancing scenes, setting up node communication with signals or groups, configuring autoloads/singletons, or implementing scene transitions.
metadata:
  author: godot-dev
  version: "1.0"
---

# Nodes and Scenes

## Scene Tree Structure

```
Game (Node)
├── World (Node2D/Node3D)
│   ├── Player (CharacterBody2D)
│   │   ├── Sprite2D
│   │   ├── CollisionShape2D
│   │   └── Camera2D
│   ├── Enemies (Node2D)
│   │   ├── Enemy1 (CharacterBody2D)
│   │   └── Enemy2 (CharacterBody2D)
│   └── Environment (Node2D)
│       ├── TileMap
│       └── StaticBody2D
└── UI (CanvasLayer)
    ├── HealthBar (ProgressBar)
    └── ScoreLabel (Label)
```

## Node Types Reference

### 2D Nodes

- **Node2D**: Base 2D transform node
- **Sprite2D**: Display 2D textures
- **AnimatedSprite2D**: Sprite sheet animations
- **TileMap**: Tile-based level design
- **Camera2D**: 2D viewport control
- **ParallaxBackground/ParallaxLayer**: Parallax scrolling

### 3D Nodes

- **Node3D**: Base 3D transform node
- **MeshInstance3D**: Display 3D meshes
- **Camera3D**: 3D viewport control
- **DirectionalLight3D/OmniLight3D/SpotLight3D**: Lighting
- **WorldEnvironment**: Post-processing effects

### Physics Nodes

- **CharacterBody2D/3D**: Player/enemy with manual movement
- **RigidBody2D/3D**: Physics simulation
- **StaticBody2D/3D**: Static colliders
- **AnimatableBody2D/3D**: Moving platforms
- **Area2D/3D**: Detection zones
- **CollisionShape2D/3D**: Collision geometry

### UI Nodes (Control)

- **Control**: Base UI node
- **Label**: Text display
- **Button/LinkButton**: Clickable buttons
- **TextureButton**: Image-based buttons
- **ProgressBar/TextureProgressBar**: Health bars, loading
- **LineEdit/TextEdit**: Text input
- **HBoxContainer/VBoxContainer**: Layout containers
- **GridContainer**: Grid layout
- **MarginContainer**: Spacing
- **Panel/PanelContainer**: Background panels

## Scene Instancing

### In Code

```gdscript
# Load scene
var enemy_scene = preload("res://scenes/enemy.tscn")

# Instance scene
var enemy = enemy_scene.instantiate()
enemy.position = Vector2(100, 100)
add_child(enemy)
```

### In Editor

1. Drag scene file from FileSystem to Scene dock
2. Or use "Instance Child Scene" button

## Node Communication Patterns

### Direct Reference (tight coupling)

```gdscript
@onready var player = $Player

func _process(delta):
    player.health -= 10
```

### Signals (loose coupling - recommended)

```gdscript
# In Player.gd
signal health_changed(new_health)

func take_damage(amount):
    health -= amount
    health_changed.emit(health)

# In Game.gd
func _ready():
    player.health_changed.connect(_on_player_health_changed)

func _on_player_health_changed(new_health):
    update_health_bar(new_health)
```

### Groups

```gdscript
# Add to group
enemy.add_to_group("enemies")

# Get all in group
var enemies = get_tree().get_nodes_in_group("enemies")

# Call method on group
get_tree().call_group("enemies", "take_damage", 10)
```

## Autoload / Singletons

### Setup in Project Settings

1. Project → Project Settings → Autoload
2. Add script with a name (e.g., "GameManager")

### Usage

```gdscript
# Access anywhere
GameManager.score += 10
GameManager.save_game()
```

## Scene Transitions

```gdscript
# Change scene
get_tree().change_scene_to_file("res://scenes/level2.tscn")

# With transition effect
func change_scene_with_fade(scene_path: String):
    $AnimationPlayer.play("fade_out")
    await $AnimationPlayer.animation_finished
    get_tree().change_scene_to_file(scene_path)
    $AnimationPlayer.play("fade_in")
```

## Best Practices

1. Keep scenes small and composable
2. Use signals for cross-scene communication
3. Prefer composition over deep inheritance
4. Use groups for managing collections of similar nodes
5. Autoload for global game state (score, settings)
6. Instance scenes rather than duplicating nodes
