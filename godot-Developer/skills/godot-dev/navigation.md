# Navigation System Skill

## Description
Expert skill for Godot's navigation system including pathfinding and navigation meshes

## Triggers
- Pathfinding
- Navigation mesh
- AI movement
- NavAgent
- NavRegion

## NavigationServer3D

### Basic Pathfinding
```gdscript
extends Node3D

var path: PackedVector3Array = []
var path_index = 0

@onready var agent = $NavigationAgent3D

func _ready():
    # Set target position
    agent.target_position = Vector3(10, 0, 10)

func _physics_process(delta):
    if agent.is_navigation_finished():
        return
    
    var next_pos = agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    
    velocity = direction * speed
    move_and_slide()
```

## NavigationAgent3D

### Setup
```gdscript
extends CharacterBody3D

@onready var nav_agent = $NavigationAgent3D

@export var speed = 5.0
@export var target: Node3D

func _ready():
    # Agent properties
    nav_agent.path_desired_distance = 0.5
    nav_agent.target_desired_distance = 1.0
    nav_agent.radius = 0.5
    nav_agent.height = 1.8
    
    # Set navigation map
    nav_agent.set_navigation_map(get_world_3d().navigation_map)

func _physics_process(delta):
    if target:
        nav_agent.target_position = target.global_position
    
    if nav_agent.is_navigation_finished():
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    direction.y = 0  # Keep on ground
    
    velocity = direction * speed
    
    # Face movement direction
    if velocity.length() > 0:
        look_at(global_position + velocity)
    
    move_and_slide()
```

## NavigationRegion3D

### Setup in Editor
1. Add NavigationRegion3D node
2. Create NavigationMesh resource
3. Bake navigation mesh

### Runtime Baking
```gdscript
extends Node3D

@onready var nav_region = $NavigationRegion3D

func _ready():
    # Bake navigation mesh
    NavigationServer3D.region_bake_navigation_mesh(
        nav_region.navigation_mesh,
        get_world_3d()
    )
```

## NavigationAgent2D

### 2D Pathfinding
```gdscript
extends CharacterBody2D

@onready var nav_agent = $NavigationAgent2D

@export var speed = 200.0
@export var target_position: Vector2

func _ready():
    nav_agent.target_position = target_position

func _physics_process(delta):
    if nav_agent.is_navigation_finished():
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    
    velocity = direction * speed
    move_and_slide()
```

## AI Patrol System

```gdscript
extends CharacterBody3D

@export var patrol_points: Array[Vector3] = []
@export var speed = 3.0
@export var wait_time = 2.0

@onready var nav_agent = $NavigationAgent3D
@onready var wait_timer = $Timer

var current_point_index = 0
var is_waiting = false

func _ready():
    wait_timer.wait_time = wait_time
    wait_timer.one_shot = true
    wait_timer.timeout.connect(_on_wait_finished)
    
    if patrol_points.size() > 0:
        nav_agent.target_position = patrol_points[0]

func _physics_process(delta):
    if is_waiting:
        return
    
    if nav_agent.is_navigation_finished():
        start_waiting()
        return
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    direction.y = 0
    
    velocity = direction * speed
    move_and_slide()

func start_waiting():
    is_waiting = true
    wait_timer.start()

func _on_wait_finished():
    is_waiting = false
    current_point_index = (current_point_index + 1) % patrol_points.size()
    nav_agent.target_position = patrol_points[current_point_index]
```

## Obstacle Avoidance

```gdscript
extends CharacterBody3D

@onready var nav_agent = $NavigationAgent3D

func _ready():
    # Enable avoidance
    nav_agent.avoidance_enabled = true
    nav_agent.neighbor_distance = 10.0
    nav_agent.max_neighbors = 10
    nav_agent.time_horizon = 2.0
    nav_agent.avoidance_layers = 1
    nav_agent.avoidance_mask = 1

func _physics_process(delta):
    nav_agent.target_position = target.global_position
    
    var next_pos = nav_agent.get_next_path_position()
    var direction = (next_pos - global_position).normalized()
    
    velocity = direction * speed
    move_and_slide()
```

## Dynamic Navigation

### Adding Obstacles at Runtime
```gdscript
extends Node3D

@onready var nav_region = $NavigationRegion3D

func add_obstacle(position: Vector3, size: Vector3):
    var obstacle = NavigationObstacle3D.new()
    obstacle.position = position
    obstacle.radius = size.x / 2
    obstacle.height = size.y
    add_child(obstacle)
    
    # Rebake navigation
    nav_region.bake_navigation_mesh()
```

## Best Practices

1. **Use NavigationAgent**: Handles pathfinding automatically
2. **Bake nav mesh**: For static environments
3. **Dynamic obstacles**: Use NavigationObstacle3D
4. **Agent radius**: Set correctly for obstacle avoidance
5. **Path smoothing**: Interpolate between path points
6. **Multiple layers**: For different movement types (ground, water, air)
