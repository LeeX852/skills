---
name: 2d-development
description: Develop 2D games in Godot including sprites, tilemaps, cameras, lighting, and parallax backgrounds. Use this skill when building 2D platformers, top-down games, implementing tilemap-based levels, 2D camera systems, day/night cycles, or any 2D-specific game feature.
metadata:
  author: godot-dev
  version: "1.0"
---

# 2D Development

## Sprite2D

### Basic Sprite

```gdscript
extends Sprite2D

func _ready():
    texture = preload("res://assets/player.png")
    flip_h = true
    flip_v = true
    modulate = Color(1, 0, 0, 1)  # Red tint
    modulate.a = 0.5  # Semi-transparent
```

### AnimatedSprite2D

```gdscript
extends CharacterBody2D

@onready var sprite = $AnimatedSprite2D

func _physics_process(delta):
    if velocity.length() > 0:
        sprite.play("run")
        sprite.flip_h = velocity.x < 0
    else:
        sprite.play("idle")
```

## TileMap

### Setup

```gdscript
extends TileMap

func _ready():
    var cell_pos = local_to_map(Vector2(100, 100))
    set_cell(0, cell_pos, 0, Vector2i(0, 0))
    var tile_data = get_cell_tile_data(0, cell_pos)
    erase_cell(0, cell_pos)
```

### TileMap Layers

```gdscript
func setup_tilemap():
    # Layer 0: Ground
    # Layer 1: Walls
    # Layer 2: Decoration
    set_cell(0, Vector2i(5, 3), source_id, atlas_coords)
    set_cell(1, Vector2i(5, 3), source_id, atlas_coords)
```

### Custom Data from Tiles

```gdscript
func check_tile_property(cell_pos: Vector2i):
    var tile_data = get_cell_tile_data(0, cell_pos)
    if tile_data:
        var is_dangerous = tile_data.get_custom_data("dangerous")
        if is_dangerous:
            take_damage()
```

## Camera2D

### Basic Camera

```gdscript
extends Camera2D

@export var target: Node2D
@export var smoothing: float = 5.0

func _ready():
    position_smoothing_enabled = true
    position_smoothing_speed = smoothing
    limit_left = 0
    limit_top = 0
    limit_right = 1000
    limit_bottom = 600

func _physics_process(delta):
    if target:
        global_position = target.global_position
```

### Camera Shake

```gdscript
extends Camera2D

var shake_intensity = 0.0
var shake_decay = 5.0

func shake(intensity: float, duration: float):
    shake_intensity = intensity
    var tween = create_tween()
    tween.tween_property(self, "shake_intensity", 0.0, duration)

func _process(delta):
    if shake_intensity > 0:
        offset = Vector2(
            randf_range(-1, 1) * shake_intensity,
            randf_range(-1, 1) * shake_intensity
        )
    else:
        offset = Vector2.ZERO
```

## 2D Lighting

### Point Light

```gdscript
extends PointLight2D

func _ready():
    color = Color(1, 0.8, 0.6)
    energy = 1.5
    texture_scale = 2.0
    shadow_enabled = true
```

### Day/Night Cycle

```gdscript
extends CanvasModulate

var time_of_day = 0.0
@export var day_duration = 120.0

func _process(delta):
    time_of_day += delta / day_duration
    time_of_day = fmod(time_of_day, 1.0)
    var brightness = sin(time_of_day * PI) * 0.5 + 0.5
    color = Color(brightness, brightness, brightness * 0.8)
```

## Parallax Background

```gdscript
extends ParallaxBackground

@export var scroll_speed: float = 100.0

func _process(delta):
    scroll_offset.x += scroll_speed * delta
```

## 2D Movement Patterns

### Top-Down Movement

```gdscript
extends CharacterBody2D

@export var speed = 200.0

func _physics_process(delta):
    var input = Input.get_vector("left", "right", "up", "down")
    velocity = input * speed
    move_and_slide()
```

### Platformer Movement

```gdscript
extends CharacterBody2D

@export var speed = 300.0
@export var jump_force = -500.0
@export var gravity = 1000.0

func _physics_process(delta):
    velocity.y += gravity * delta
    var direction = Input.get_axis("left", "right")
    velocity.x = direction * speed
    if is_on_floor() and Input.is_action_just_pressed("jump"):
        velocity.y = jump_force
    move_and_slide()
```

### Grid-Based Movement

```gdscript
extends CharacterBody2D

@export var tile_size = 32
@export var move_speed = 4.0

var target_position = Vector2.ZERO
var is_moving = false

func _ready():
    target_position = position

func _process(delta):
    if not is_moving:
        var input = Input.get_vector("left", "right", "up", "down")
        if input.length() > 0:
            target_position = position + input * tile_size
            is_moving = true
    if is_moving:
        position = position.lerp(target_position, move_speed * delta)
        if position.distance_to(target_position) < 1:
            position = target_position
            is_moving = false
```

## Best Practices

1. **Use CharacterBody2D** for player/enemies with physics
2. **Use TileMap** for level design
3. **Use Camera2D** for viewport control
4. **Layer organization**: Background, main, foreground, UI
5. **Pixel art**: Set texture filtering to Nearest
6. **Collision layers**: Organize by object type
