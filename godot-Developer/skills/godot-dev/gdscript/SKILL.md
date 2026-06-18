---
name: gdscript
description: Write, debug, and optimize GDScript code for Godot Engine 4.x. Use this skill when creating scripts, fixing GDScript errors, connecting signals, configuring export variables, setting up node references, or implementing character movement and game logic in GDScript.
metadata:
  author: godot-dev
  version: "1.0"
---

# GDScript Development

## Script Structure

```gdscript
extends Node2D  # or Node3D, CharacterBody2D, etc.

# Export variables for editor inspection
@export var speed: float = 200.0
@export var health: int = 100

# Node references
@onready var sprite = $Sprite2D
@onready var animation_player = $AnimationPlayer

# Signals
signal health_changed(new_health)
signal died()

# Private variables
var _velocity: Vector2 = Vector2.ZERO
var _is_alive: bool = true

func _ready():
    # Initialize when node enters scene tree
    pass

func _process(delta: float):
    # Called every frame
    pass

func _physics_process(delta: float):
    # Called every physics frame (fixed timestep)
    pass
```

## Common Node Types

- **Node2D/Node3D**: Base spatial nodes
- **CharacterBody2D/3D**: Player/enemy movement with physics
- **RigidBody2D/3D**: Physics-driven objects
- **StaticBody2D/3D**: Static collision objects
- **Area2D/3D**: Trigger zones
- **Sprite2D/Sprite3D**: Visual sprites
- **AnimationPlayer**: Animation playback
- **Timer**: Delayed execution
- **Camera2D/Camera3D**: Viewport control

## Signal Pattern

```gdscript
# Define signal
signal player_hit(damage: int)

# Connect in code
enemy.player_hit.connect(_on_player_hit)

# Connect in editor (via @export)
func _on_player_hit(damage: int):
    health -= damage
    health_changed.emit(health)
```

## Movement Patterns

### 2D Character Movement

```gdscript
extends CharacterBody2D

@export var speed: float = 200.0
@export var jump_velocity: float = -400.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
    if not is_on_floor():
        velocity.y += gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    var direction = Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

    move_and_slide()
```

### 3D Character Movement

```gdscript
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_velocity: float = 4.5

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta):
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    var input_dir = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        velocity.z = move_toward(velocity.z, 0, speed)

    move_and_slide()
```

## Best Practices

1. Use `@onready` for node references (resolved when scene enters tree)
2. Use `@export` for editor-configurable values
3. Prefer `move_and_slide()` for character physics
4. Use signals for decoupled communication
5. Type variables when possible for better performance
6. Use `_physics_process()` for physics calculations
7. Use `_process()` for visual/gameplay updates

## Debug Tips

- Use `print()` or `prints()` for console output
- Use `breakpoint` keyword or `push_warning()` for debugging
- Enable "Visible Collision Shapes" in Debug menu
- Use the Debugger panel for breakpoints and profiling
