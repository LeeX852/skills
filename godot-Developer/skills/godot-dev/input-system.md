# Input System Skill

## Description
Expert skill for Godot's input system including actions, gamepad, and touch input

## Triggers
- Input handling
- Keyboard input
- Mouse input
- Gamepad support
- Touch input
- Input mapping

## Input Actions

### Setup in Project Settings
```
Project Settings → Input Map
- Add action: "jump"
- Add key: Space
- Add gamepad button: A
```

### Using Input Actions
```gdscript
extends Node

func _input(event):
    # Check action pressed
    if event.is_action_pressed("jump"):
        jump()
    
    # Check action released
    if event.is_action_released("jump"):
        stop_jump()

func _process(delta):
    # Continuous input check
    if Input.is_action_pressed("move_right"):
        move_right()
    
    # Just pressed (one frame)
    if Input.is_action_just_pressed("attack"):
        attack()
    
    # Just released
    if Input.is_action_just_released("attack"):
        end_attack()

    # Get axis (-1 to 1)
    var move_x = Input.get_axis("move_left", "move_right")
    var move_y = Input.get_axis("move_up", "move_down")
    
    # Get vector (normalized)
    var direction = Input.get_vector("move_left", "move_right", "move_up", "move_down")
```

## Keyboard Input

```gdscript
extends Node

func _input(event):
    if event is InputEventKey:
        if event.pressed:
            match event.keycode:
                KEY_SPACE:
                    jump()
                KEY_ESCAPE:
                    pause()
                KEY_F1:
                    toggle_debug()
        
        # Check modifiers
        if event.ctrl_pressed and event.keycode == KEY_S:
            save_game()
```

## Mouse Input

```gdscript
extends Node

func _input(event):
    # Mouse button
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            shoot()
        
        if event.button_index == MOUSE_BUTTON_RIGHT:
            if event.pressed:
                start_aim()
            else:
                end_aim()
        
        # Mouse wheel
        if event.button_index == MOUSE_BUTTON_WHEEL_UP:
            zoom_in()
        if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
            zoom_out()
    
    # Mouse motion
    if event is InputEventMouseMotion:
        # Relative movement
        var delta = event.relative
        rotate_camera(delta)
        
        # Global position
        var pos = event.position
        update_cursor(pos)
```

## Gamepad Input

```gdscript
extends Node

func _input(event):
    if event is InputEventJoypadButton:
        if event.pressed:
            match event.button_index:
                JOY_BUTTON_A:
                    jump()
                JOY_BUTTON_B:
                    cancel()
                JOY_BUTTON_START:
                    pause()
    
    if event is InputEventJoypadMotion:
        # Left stick
        if event.axis == JOY_AXIS_LEFT_X:
            var stick_x = event.axis_value
            move_horizontal(stick_x)
        
        if event.axis == JOY_AXIS_LEFT_Y:
            var stick_y = event.axis_value
            move_vertical(stick_y)
        
        # Triggers
        if event.axis == JOY_AXIS_TRIGGER_RIGHT:
            var trigger = event.axis_value
            if trigger > 0.5:
                shoot()

func get_stick_vector() -> Vector2:
    return Vector2(
        Input.get_joy_axis(0, JOY_AXIS_LEFT_X),
        Input.get_joy_axis(0, JOY_AXIS_LEFT_Y)
    )
```

## Touch Input

```gdscript
extends Node

func _input(event):
    if event is InputEventScreenTouch:
        if event.pressed:
            on_touch_down(event.position, event.index)
        else:
            on_touch_up(event.position, event.index)
    
    if event is InputEventScreenDrag:
        on_touch_move(event.position, event.index)

func on_touch_down(pos: Vector2, index: int):
    print("Touch down at: ", pos, " index: ", index)

func on_touch_up(pos: Vector2, index: int):
    print("Touch up at: ", pos, " index: ", index)

func on_touch_move(pos: Vector2, index: int):
    print("Touch move at: ", pos, " index: ", index)
```

## Virtual Joystick (Touch)

```gdscript
extends TouchScreenButton

signal joystick_input(direction: Vector2)

var touch_index = -1
var deadzone = 0.15

func _input(event):
    if event is InputEventScreenTouch:
        if event.pressed and is_point_inside(event.position):
            touch_index = event.index
        elif not event.pressed and event.index == touch_index:
            touch_index = -1
            joystick_input.emit(Vector2.ZERO)
    
    if event is InputEventScreenDrag and event.index == touch_index:
        var center = global_position + texture_normal.get_size() / 2
        var direction = (event.position - center).normalized()
        var distance = event.position.distance_to(center)
        
        if distance > deadzone * texture_normal.get_size().x:
            joystick_input.emit(direction)
        else:
            joystick_input.emit(Vector2.ZERO)

func is_point_inside(point: Vector2) -> bool:
    var rect = Rect2(global_position, texture_normal.get_size())
    return rect.has_point(point)
```

## Input Mapping Best Practices

### Standard FPS Controls
```
move_forward: W, Up, Left Stick Up
move_back: S, Down, Left Stick Down
move_left: A, Left, Left Stick Left
move_right: D, Right, Left Stick Right
jump: Space, A Button
crouch: Left Ctrl, B Button
sprint: Left Shift, Left Stick Press
interact: E, X Button
attack: Left Mouse, Right Trigger
```

### Standard Platformer Controls
```
move_left: A, Left, Left Stick Left
move_right: D, Right, Left Stick Right
jump: Space, A Button
attack: Z, X Button
dash: Shift, B Button
```

## Mouse Modes

```gdscript
extends Node

func _ready():
    # Visible and free
    Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
    
    # Captured (for FPS)
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
    
    # Hidden
    Input.set_mouse_mode(Input.MOUSE_MODE_HIDDEN)
    
    # Confined to window
    Input.set_mouse_mode(Input.MOUSE_MODE_CONFINED)

func _input(event):
    if event.is_action_pressed("ui_cancel"):
        Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
```

## Best Practices

1. **Use Input Actions**: Not raw keycodes
2. **Support multiple devices**: Keyboard + Gamepad
3. **Deadzones**: For analog sticks
4. **Remappable inputs**: Let players customize
5. **Touch gestures**: Implement for mobile
6. **Input buffering**: For responsive controls
