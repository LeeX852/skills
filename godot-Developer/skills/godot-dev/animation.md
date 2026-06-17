# Animation System Skill

## Description
Expert skill for Godot's animation system including AnimationPlayer, AnimationTree, and Tween

## Triggers
- Animation creation
- AnimationPlayer
- AnimationTree
- Tween animations
- Sprite animation
- Skeletal animation

## AnimationPlayer

### Basic Setup
```gdscript
extends Node2D

@onready var animation_player = $AnimationPlayer

func _ready():
    # Play animation
    animation_player.play("walk")
    
    # Play with custom speed
    animation_player.play("run", -1, 2.0)  # name, blend, speed

func _process(delta):
    # Check if animation is playing
    if animation_player.is_playing():
        print(animation_player.current_animation)
```

### Animation Callbacks
```gdscript
func _ready():
    animation_player.animation_finished.connect(_on_animation_finished)
    animation_player.animation_started.connect(_on_animation_started)

func _on_animation_finished(anim_name: String):
    if anim_name == "attack":
        state = IDLE

func _on_animation_started(anim_name: String):
    print("Started: ", anim_name)
```

## Tween Animations

### Basic Tween
```gdscript
extends Node2D

func _ready():
    # Create tween
    var tween = create_tween()
    
    # Animate property
    tween.tween_property(self, "position", Vector2(100, 0), 1.0)
    
    # Chain animations
    tween.tween_property(self, "modulate:a", 0.0, 0.5)
    tween.tween_callback(queue_free)
```

### Tween Options
```gdscript
func animate_with_options():
    var tween = create_tween()
    
    # Set ease and transition
    tween.set_ease(Tween.EASE_IN_OUT)
    tween.set_trans(Tween.TRANS_CUBIC)
    
    # Parallel animations
    tween.tween_property($Sprite, "position", Vector2(100, 0), 1.0)
    tween.parallel().tween_property($Sprite, "modulate", Color.RED, 1.0)
    
    # Looped tween
    tween.set_loops(3)
    
    # Interval
    tween.tween_interval(0.5)
```

### Common Tween Patterns
```gdscript
# Fade in
func fade_in(node: CanvasItem, duration: float = 0.5):
    node.modulate.a = 0.0
    var tween = create_tween()
    tween.tween_property(node, "modulate:a", 1.0, duration)

# Fade out
func fade_out(node: CanvasItem, duration: float = 0.5):
    var tween = create_tween()
    tween.tween_property(node, "modulate:a", 0.0, duration)

# Scale bounce
func bounce_scale(node: Node2D):
    var tween = create_tween()
    tween.tween_property(node, "scale", Vector2(1.2, 1.2), 0.1)
    tween.tween_property(node, "scale", Vector2(1.0, 1.0), 0.1)

# Move to position
func move_to(target: Node2D, destination: Vector2, duration: float):
    var tween = create_tween()
    tween.tween_property(target, "position", destination, duration)
```

## AnimatedSprite2D

```gdscript
extends CharacterBody2D

@onready var animated_sprite = $AnimatedSprite2D

func _physics_process(delta):
    if velocity.length() > 0:
        animated_sprite.play("walk")
        animated_sprite.flip_h = velocity.x < 0
    else:
        animated_sprite.play("idle")
```

## AnimationTree

### State Machine
```gdscript
extends CharacterBody3D

@onready var animation_tree = $AnimationTree

enum State { IDLE, WALK, RUN, JUMP }
var current_state = State.IDLE

func _ready():
    animation_tree.active = true

func _physics_process(delta):
    # Update animation parameters
    animation_tree.set("parameters/Idle/blend_position", velocity.length())
    animation_tree.set("parameters/Walk/blend_position", velocity.length())
    
    # Transition between states
    if is_on_floor():
        if velocity.length() > 0:
            current_state = State.WALK
        else:
            current_state = State.IDLE
    else:
        current_state = State.JUMP
```

## Best Practices

1. **Use AnimationPlayer for complex sequences**: Key multiple properties
2. **Use Tween for simple one-shot animations**: Position, scale, fade
3. **Use AnimatedSprite2D for frame-based sprites**: Character animations
4. **Use AnimationTree for blending**: Character movement states
5. **Named animations**: Use descriptive names ("attack", "walk", "idle")
6. **Animation callbacks**: Use signals for game logic tied to animations
