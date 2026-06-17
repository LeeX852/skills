# UI System Skill

## Description
Expert skill for Godot's Control node system and UI development

## Triggers
- UI design
- Menus
- HUD
- Buttons
- Layouts
- Themes
- Input fields

## Core UI Nodes

### Layout Containers
```gdscript
# HBoxContainer - Horizontal layout
# VBoxContainer - Vertical layout
# GridContainer - Grid layout
# MarginContainer - Adds margins
# CenterContainer - Centers children
# TabContainer - Tabbed interface

# Example: Vertical menu
extends VBoxContainer

func _ready():
    # Add spacing
    add_theme_constant_override("separation", 10)
```

### Common Controls

#### Label
```gdscript
extends Label

func _ready():
    text = "Score: 0"
    horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    add_theme_font_size_override("font_size", 24)
```

#### Button
```gdscript
extends Button

signal play_pressed()

func _ready():
    text = "Play"
    pressed.connect(_on_pressed)
    disabled = false

func _on_pressed():
    play_pressed.emit()
```

#### ProgressBar
```gdscript
extends ProgressBar

@onready var player = $Player

func _ready():
    min_value = 0
    max_value = 100
    value = player.health
    show_percentage = false

func update_health(new_health: int):
    value = new_health
```

#### LineEdit (Text Input)
```gdscript
extends LineEdit

signal name_submitted(new_name: String)

func _ready():
    placeholder_text = "Enter name..."
    text_submitted.connect(_on_text_submitted)

func _on_text_submitted(new_text: String):
    name_submitted.emit(new_text)
    clear()
```

#### TextureRect
```gdscript
extends TextureRect

func _ready():
    texture = preload("res://assets/icon.png")
    expand_mode = TextureRect.EXPAND_IGNORE_SIZE
    stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
```

## CanvasLayer for UI

```gdscript
# UI should be on a CanvasLayer to stay on screen
extends CanvasLayer

@onready var health_bar = $HealthBar
@onready var score_label = $ScoreLabel

func update_score(score: int):
    score_label.text = "Score: %d" % score
```

## Themes

### Setting Theme
```gdscript
# In editor: Set theme property on Control node
# In code:
func _ready():
    var theme = preload("res://themes/game_theme.tres")
    set_theme(theme)
```

### Theme Overrides
```gdscript
# Override specific properties
func style_button(button: Button):
    button.add_theme_font_size_override("font_size", 20)
    button.add_theme_color_override("font_color", Color.WHITE)
    button.add_theme_stylebox_override("normal", create_stylebox())
```

## Anchors & Margins

### Screen Positioning
```gdscript
# Anchor presets:
# 0,0 = Top-left
# 0.5,0.5 = Center
# 1,1 = Bottom-right

# Example: Center on screen
func center_control(control: Control):
    control.set_anchors_preset(Control.PRESET_CENTER)
    control.offset_left = -50
    control.offset_top = -25
    control.offset_right = 50
    control.offset_bottom = 25
```

### Responsive Layout
```gdscript
extends Control

func _ready():
    # Full screen
    set_anchors_preset(Control.PRESET_FULL_RECT)
    
    # Or specific margins
    anchor_left = 0.1
    anchor_top = 0.1
    anchor_right = 0.9
    anchor_bottom = 0.9
```

## Input Handling in UI

```gdscript
extends Control

func _input(event):
    if event is InputEventKey:
        if event.pressed and event.keycode == KEY_ESCAPE:
            toggle_pause_menu()

func _gui_input(event):
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            handle_click()
```

## UI Animation

```gdscript
extends Control

@onready var animation_player = $AnimationPlayer

func show_menu():
    visible = true
    animation_player.play("fade_in")

func hide_menu():
    animation_player.play("fade_out")
    await animation_player.animation_finished
    visible = false
```

## Best Practices

1. **Use CanvasLayer**: Keep UI separate from game world
2. **Anchors over absolute position**: Responsive to screen size
3. **Theme for consistency**: Centralize styling
4. **Signals for interaction**: Decouple UI from game logic
5. **Containers for layout**: Let Godot handle positioning
6. **Focus management**: Support keyboard/gamepad navigation

## Common Patterns

### Pause Menu
```gdscript
extends CanvasLayer

func _ready():
    process_mode = Node.PROCESS_MODE_WHEN_PAUSED
    visible = false

func _input(event):
    if event.is_action_pressed("pause"):
        toggle_pause()

func toggle_pause():
    get_tree().paused = !get_tree().paused
    visible = get_tree().paused
```

### HUD Update
```gdscript
extends CanvasLayer

@onready var score_label = $ScoreLabel
@onready var health_bar = $HealthBar

func _on_score_changed(new_score: int):
    score_label.text = str(new_score)

func _on_health_changed(new_health: int):
    health_bar.value = new_health
```
