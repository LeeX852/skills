---
name: state-machine
description: Implement state machine patterns in Godot for game logic, AI behavior, and player states. Use this skill when creating player state machines (idle/run/jump/attack), enemy AI behaviors (patrol/chase/attack), game state management (menu/playing/paused), or any system that needs clean state transitions.
metadata:
  author: godot-dev
  version: "1.0"
---

# State Machine Pattern

## Base State Machine

```gdscript
class_name StateMachine
extends Node

signal state_changed(old_state: String, new_state: String)

@export var initial_state: State

var current_state: State
var states: Dictionary = {}

func _ready():
    for child in get_children():
        if child is State:
            states[child.name.to_lower()] = child
            child.state_machine = self
            child.player = owner

    if initial_state:
        current_state = initial_state
        current_state.enter()

func _process(delta):
    if current_state:
        current_state.process(delta)

func _physics_process(delta):
    if current_state:
        current_state.physics_process(delta)

func transition_to(new_state_name: String):
    var new_state = states.get(new_state_name.to_lower())
    if not new_state:
        push_error("State not found: " + new_state_name)
        return

    if current_state:
        current_state.exit()

    var old_state_name = current_state.name if current_state else ""
    current_state = new_state
    current_state.enter()
    state_changed.emit(old_state_name, new_state_name)
```

## Base State Class

```gdscript
class_name State
extends Node

var state_machine: StateMachine
var player: CharacterBody3D

func enter():
    pass

func exit():
    pass

func process(delta: float):
    pass

func physics_process(delta: float):
    pass
```

## Player State Machine

### Idle State

```gdscript
extends State

func enter():
    player.velocity = Vector3.ZERO
    player.animation_player.play("idle")

func physics_process(delta: float):
    var input_dir = Input.get_vector("left", "right", "forward", "back")

    if input_dir.length() > 0:
        state_machine.transition_to("Run")
        return

    if Input.is_action_just_pressed("jump"):
        state_machine.transition_to("Jump")
        return

    if Input.is_action_just_pressed("attack"):
        state_machine.transition_to("Attack")
        return

    if not player.is_on_floor():
        state_machine.transition_to("Fall")
```

### Run State

```gdscript
extends State

@export var speed = 5.0

func enter():
    player.animation_player.play("run")

func physics_process(delta: float):
    var input_dir = Input.get_vector("left", "right", "forward", "back")
    var direction = (player.transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction:
        player.velocity.x = direction.x * speed
        player.velocity.z = direction.z * speed
        player.look_at(player.global_position + direction)
    else:
        state_machine.transition_to("Idle")
        return

    if Input.is_action_just_pressed("jump"):
        state_machine.transition_to("Jump")
        return

    if Input.is_action_just_pressed("attack"):
        state_machine.transition_to("Attack")
        return

    player.move_and_slide()
```

### Jump State

```gdscript
extends State

@export var jump_force = 4.5

func enter():
    player.velocity.y = jump_force
    player.animation_player.play("jump")

func physics_process(delta: float):
    player.velocity.y -= ProjectSettings.get_setting("physics/3d/default_gravity") * delta

    var input_dir = Input.get_vector("left", "right", "forward", "back")
    var direction = (player.transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
    player.velocity.x = direction.x * speed * 0.8
    player.velocity.z = direction.z * speed * 0.8

    player.move_and_slide()

    if player.is_on_floor():
        state_machine.transition_to("Idle")
```

### Attack State

```gdscript
extends State

@export var attack_duration = 0.5

var attack_timer = 0.0

func enter():
    attack_timer = attack_duration
    player.velocity = Vector3.ZERO
    player.animation_player.play("attack")
    player.attack_area.monitoring = true

func exit():
    player.attack_area.monitoring = false

func physics_process(delta: float):
    attack_timer -= delta
    if attack_timer <= 0:
        state_machine.transition_to("Idle")
```

## AI State Machine

### Enemy Patrol State

```gdscript
extends State

@export var patrol_speed = 3.0
@export var patrol_points: Array[Vector3] = []

var current_point = 0

func enter():
    player.animation_player.play("walk")
    if patrol_points.size() > 0:
        player.nav_agent.target_position = patrol_points[current_point]

func physics_process(delta: float):
    if player.nav_agent.is_navigation_finished():
        current_point = (current_point + 1) % patrol_points.size()
        player.nav_agent.target_position = patrol_points[current_point]
        return

    var next_pos = player.nav_agent.get_next_path_position()
    var direction = (next_pos - player.global_position).normalized()

    player.velocity = direction * patrol_speed
    player.move_and_slide()

    if player.can_see_player():
        state_machine.transition_to("Chase")
```

### Enemy Chase State

```gdscript
extends State

@export var chase_speed = 5.0

func enter():
    player.animation_player.play("run")

func physics_process(delta: float):
    if not player.can_see_player():
        state_machine.transition_to("Patrol")
        return

    var target_pos = player.player.global_position
    player.nav_agent.target_position = target_pos

    var next_pos = player.nav_agent.get_next_path_position()
    var direction = (next_pos - player.global_position).normalized()

    player.velocity = direction * chase_speed
    player.move_and_slide()

    if player.global_position.distance_to(target_pos) < 2.0:
        state_machine.transition_to("Attack")
```

## Game State Machine

```gdscript
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state = GameState.MENU

func change_state(new_state: GameState):
    match current_state:
        GameState.PLAYING:
            get_tree().paused = false
        GameState.PAUSED:
            get_tree().paused = false

    current_state = new_state

    match new_state:
        GameState.MENU:
            show_menu()
        GameState.PLAYING:
            start_game()
        GameState.PAUSED:
            pause_game()
        GameState.GAME_OVER:
            show_game_over()

func pause_game():
    get_tree().paused = true
    $PauseMenu.show()
```

## Best Practices

1. **Single responsibility**: Each state handles one behavior
2. **Clean transitions**: Exit/enter logic in proper places
3. **Signal communication**: Decouple state from external systems
4. **Animation integration**: States control animations
5. **Reusability**: Make states generic where possible
6. **Debug visualization**: Show current state in editor
