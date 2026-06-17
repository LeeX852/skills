# Physics System Skill

## Description
Expert skill for Godot's 2D and 3D physics systems including collision, movement, and physics bodies

## Triggers
- Collision detection
- Physics bodies
- Raycasting
- Character movement
- Rigid bodies
- Area detection
- Physics layers

## Physics Body Types

### CharacterBody2D/3D
For player-controlled characters with manual physics handling.

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0
@export var jump_velocity: float = -500.0

var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta):
    # Gravity
    if not is_on_floor():
        velocity.y += gravity * delta
    
    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_velocity
    
    # Movement
    var direction = Input.get_axis("left", "right")
    velocity.x = direction * speed
    
    move_and_slide()
    
    # Check collisions after movement
    for i in get_slide_collision_count():
        var collision = get_slide_collision(i)
        if collision.get_collider().is_in_group("enemies"):
            take_damage()
```

### RigidBody2D/3D
For physics-driven objects (balls, ragdolls, projectiles).

```gdscript
extends RigidBody2D

@export var launch_force: float = 500.0

func launch(direction: Vector2):
    apply_central_impulse(direction * launch_force)

func _ready():
    # Apply force on spawn
    apply_central_impulse(Vector2(100, -200))
    
    # Set gravity scale
    gravity_scale = 1.5
    
    # Set bounce
    physics_material_override = PhysicsMaterial.new()
    physics_material_override.bounce = 0.8
```

### StaticBody2D/3D
For static environment colliders (walls, floors, platforms).

```gdscript
# Moving platform with AnimatableBody2D
extends AnimatableBody2D

@export var move_distance: Vector2 = Vector2(0, -100)
@export var move_speed: float = 2.0

var start_position: Vector2
var target_position: Vector2

func _ready():
    start_position = global_position
    target_position = start_position + move_distance

func _physics_process(delta):
    global_position = global_position.lerp(
        target_position, 
        move_speed * delta
    )
    
    if global_position.distance_to(target_position) < 1:
        # Swap direction
        var temp = target_position
        target_position = start_position
        start_position = temp
```

### Area2D/3D
For trigger zones (pickups, damage zones, detection areas).

```gdscript
extends Area2D

signal collected()

func _ready():
    body_entered.connect(_on_body_entered)
    area_entered.connect(_on_area_entered)

func _on_body_entered(body: Node2D):
    if body.is_in_group("player"):
        collected.emit()
        queue_free()

func _on_area_entered(area: Area2D):
    if area.is_in_group("damage_zone"):
        take_damage()
```

## Collision Setup

### Collision Layers & Masks
- **Layer**: Which layer this object is ON
- **Mask**: Which layers this object can INTERACT WITH

Example setup:
- Layer 1: Player
- Layer 2: Enemies
- Layer 3: Environment
- Layer 4: Pickups

```gdscript
# Set layers in code
collision_layer = 1  # Player layer
collision_mask = 5   # Interact with layers 1 and 3 (1 + 4 = 5)
```

### CollisionShape2D/3D
Required for physics bodies to have collision detection.

Common shapes:
- **RectangleShape2D**: Boxes, walls
- **CircleShape2D**: Spheres, balls
- **CapsuleShape2D**: Characters
- **PolygonShape2D**: Custom shapes

## Raycasting

### 2D Raycast
```gdscript
extends Node2D

@onready var ray_cast = $RayCast2D

func _physics_process(delta):
    ray_cast.target_position = Vector2(100, 0)
    
    if ray_cast.is_colliding():
        var collider = ray_cast.get_collider()
        var point = ray_cast.get_collision_point()
        var normal = ray_cast.get_collision_normal()
        
        if collider.is_in_group("enemy"):
            attack(collider)
```

### 3D Raycast
```gdscript
extends Node3D

@onready var ray_cast = $RayCast3D

func _physics_process(delta):
    ray_cast.target_position = Vector3(0, 0, -10)
    
    if ray_cast.is_colliding():
        var collider = ray_cast.get_collider()
        var point = ray_cast.get_collision_point()
        
        if collider.has_method("take_damage"):
            collider.take_damage(10)
```

### PhysicsDirectSpaceState (Advanced)
```gdscript
func raycast_from_mouse():
    var space_state = get_world_2d().direct_space_state
    var mouse_pos = get_global_mouse_position()
    
    var query = PhysicsRayQueryParameters2D.create(
        global_position, 
        mouse_pos
    )
    query.collision_mask = 2  # Only enemies
    
    var result = space_state.intersect_ray(query)
    if result:
        print("Hit: ", result.collider.name)
```

## Best Practices

1. **Use appropriate body types**:
   - CharacterBody2D: Player, enemies with manual control
   - RigidBody2D: Physics objects (balls, debris)
   - StaticBody2D: Walls, floors, static obstacles
   - Area2D: Triggers, sensors, pickups

2. **Collision layers**:
   - Keep layers organized (player, enemies, environment, etc.)
   - Use minimal masks for performance

3. **Physics process**:
   - Use `_physics_process()` for all physics calculations
   - Fixed timestep ensures consistent behavior

4. **Performance**:
   - Use simple collision shapes when possible
   - Disable physics for off-screen objects
   - Use `freeze` on RigidBody when not needed
