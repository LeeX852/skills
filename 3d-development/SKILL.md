---
name: 3d-development
description: Develop 3D games in Godot including meshes, lighting, cameras, environments, and 3D model importing. Use this skill when building 3D scenes, setting up lighting rigs, configuring cameras, importing glTF/FBX models, implementing 3D character controllers, or working with the 3D rendering pipeline.
metadata:
  author: godot-dev
  version: "1.0"
---

# 3D Development

## Node3D Basics

### Transform and Position

```gdscript
extends Node3D

func _ready():
    position = Vector3(1, 2, 3)
    rotation = Vector3(0, PI/2, 0)
    scale = Vector3(2, 2, 2)
    look_at(Vector3(10, 0, 10))
    global_position = Vector3(0, 5, 0)
```

## MeshInstance3D

### Basic Mesh Setup

```gdscript
extends MeshInstance3D

func _ready():
    var mesh = BoxMesh.new()
    mesh.size = Vector3(1, 1, 1)
    self.mesh = mesh

    var material = StandardMaterial3D.new()
    material.albedo_color = Color.RED
    material.metallic = 0.5
    material.roughness = 0.3
    set_surface_override_material(0, material)
```

## Camera3D

### Basic Camera

```gdscript
extends Camera3D

@export var target: Node3D
@export var distance = 10.0
@export var height = 5.0
@export var smooth_speed = 5.0

func _ready():
    current = true
    fov = 75.0
    near = 0.1
    far = 1000.0

func _physics_process(delta):
    if target:
        var target_pos = target.global_position
        global_position = global_position.lerp(
            target_pos + Vector3(0, height, distance),
            smooth_speed * delta
        )
        look_at(target_pos)
```

### Third Person Camera

```gdscript
extends Node3D

@export var target: Node3D
@export var mouse_sensitivity = 0.003
@export var distance = 5.0
@export var min_pitch = -30.0
@export var max_pitch = 60.0

var yaw = 0.0
var pitch = 0.0

@onready var camera = $Camera3D

func _ready():
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event):
    if event is InputEventMouseMotion:
        yaw -= event.relative.x * mouse_sensitivity
        pitch -= event.relative.y * mouse_sensitivity
        pitch = clamp(pitch, deg_to_rad(min_pitch), deg_to_rad(max_pitch))

func _physics_process(delta):
    if target:
        global_position = target.global_position
        rotation = Vector3.ZERO
        rotate_y(yaw)
        rotate_x(pitch)
        camera.position = Vector3(0, 0, distance)
        camera.look_at(global_position)
```

## 3D Lighting

### Directional Light (Sun)

```gdscript
extends DirectionalLight3D

func _ready():
    light_color = Color(1, 0.95, 0.8)
    light_energy = 1.2
    shadow_enabled = true
    rotation_degrees = Vector3(-45, 30, 0)
```

### Point Light

```gdscript
extends OmniLight3D

func _ready():
    light_color = Color(1, 0.8, 0.6)
    light_energy = 2.0
    omni_range = 10.0
    shadow_enabled = true
```

### Spot Light

```gdscript
extends SpotLight3D

func _ready():
    light_color = Color(1, 1, 1)
    light_energy = 3.0
    spot_range = 15.0
    spot_angle = 30.0
    shadow_enabled = true
```

## Environment Setup

### WorldEnvironment

```gdscript
extends WorldEnvironment

func _ready():
    var env = Environment.new()
    env.background_mode = Environment.BG_SKY
    env.sky = Sky.new()
    env.ambient_light_source = Environment.AMBIENT_SOURCE_SKY
    env.ambient_light_energy = 0.5
    env.tonemap_mode = Environment.TONE_MAP_ACES
    env.glow_enabled = true
    env.glow_intensity = 0.8
    env.ssr_enabled = true
    env.ssao_enabled = true
    environment = env
```

## 3D Movement

### Character Movement (FPS)

```gdscript
extends CharacterBody3D

@export var speed = 5.0
@export var jump_velocity = 4.5
@export var mouse_sensitivity = 0.002

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready():
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        $Camera3D.rotate_x(-event.relative.y * mouse_sensitivity)
        $Camera3D.rotation.x = clamp($Camera3D.rotation.x, -1.2, 1.2)

func _physics_process(delta):
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity

    var input_dir = Input.get_vector("left", "right", "forward", "back")
    var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        velocity.z = move_toward(velocity.z, 0, speed)

    move_and_slide()
```

## Importing 3D Models

### Supported Formats

- **glTF 2.0** (.glb, .gltf) - Recommended
- **FBX** (.fbx)
- **OBJ** (.obj)
- **Collada** (.dae)

### Import and Access

```gdscript
var model = preload("res://models/character.glb").instantiate()
add_child(model)

var mesh_instance = model.get_node("MeshInstance3D")
```

## Raycasting 3D

```gdscript
extends Node3D

@onready var ray_cast = $RayCast3D

func _physics_process(delta):
    if ray_cast.is_colliding():
        var collider = ray_cast.get_collider()
        var point = ray_cast.get_collision_point()
        var normal = ray_cast.get_collision_normal()
        if collider.has_method("interact"):
            collider.interact()
```

## Best Practices

1. **Use glTF format** for 3D models
2. **Optimize meshes**: Reduce polygon count
3. **LOD (Level of Detail)**: Use for distant objects
4. **Occlusion culling**: Hide objects behind walls
5. **Lightmaps**: Bake lighting for static scenes
6. **Navigation**: Use NavigationRegion3D for pathfinding
