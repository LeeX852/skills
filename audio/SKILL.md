---
name: audio
description: Implement audio in Godot including sound effects, music playback, audio buses, and 3D spatial audio. Use this skill when setting up audio players, managing audio buses, creating music systems with crossfade, pooling audio sources, or adding positional audio to 2D/3D scenes.
metadata:
  author: godot-dev
  version: "1.0"
---

# Audio System

## AudioStreamPlayer (Non-positional)

### Basic Playback

```gdscript
extends Node

@onready var audio_player = $AudioStreamPlayer

func _ready():
    audio_player.play()
    audio_player.play(0.5)  # Start at 0.5 seconds
    audio_player.volume_db = -10
    audio_player.pitch_scale = 1.2

func play_sfx():
    audio_player.play()

func stop_sfx():
    audio_player.stop()
```

### One-Shot Sound Effects

```gdscript
extends Node

var sfx_scene = preload("res://audio/sfx_player.tscn")

func play_sfx(stream: AudioStream, volume: float = 0.0):
    var player = sfx_scene.instantiate()
    player.stream = stream
    player.volume_db = volume
    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)
```

## AudioStreamPlayer2D (2D Positional)

```gdscript
extends Node2D

@onready var audio = $AudioStreamPlayer2D

func _ready():
    audio.max_distance = 500
    audio.attenuation = 2.0
    audio.play()
```

## AudioStreamPlayer3D (3D Positional)

```gdscript
extends Node3D

@onready var audio = $AudioStreamPlayer3D

func _ready():
    audio.max_distance = 20.0
    audio.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE
    audio.play()
```

## Audio Bus Management

### Setup in Code

```gdscript
extends Node

func _ready():
    var music_bus = AudioServer.get_bus_index("Music")
    var sfx_bus = AudioServer.get_bus_index("SFX")

    AudioServer.set_bus_volume_db(music_bus, linear_to_db(0.8))
    AudioServer.set_bus_volume_db(sfx_bus, linear_to_db(1.0))
    AudioServer.set_bus_mute(music_bus, true)
```

### Adding Effects

```gdscript
func add_reverb_to_bus(bus_name: String):
    var bus_idx = AudioServer.get_bus_index(bus_name)
    var reverb = AudioEffectReverb.new()
    reverb.room_size = 0.8
    reverb.damping = 0.5
    reverb.wet = 0.3
    AudioServer.add_bus_effect(bus_idx, reverb)
```

## Music System

```gdscript
extends Node

@onready var music_player = $AudioStreamPlayer
@onready var ambient_player = $AudioStreamPlayer2

var current_track: String = ""

func play_music(track_path: String, fade_time: float = 1.0):
    if current_track == track_path:
        return

    current_track = track_path
    var tween = create_tween()
    tween.tween_property(music_player, "volume_db", -80.0, fade_time)
    await tween.finished

    music_player.stream = load(track_path)
    music_player.volume_db = -80.0
    music_player.play()

    tween = create_tween()
    tween.tween_property(music_player, "volume_db", 0.0, fade_time)

func crossfade_music(new_track: String, duration: float = 2.0):
    var new_player = AudioStreamPlayer.new()
    new_player.stream = load(new_track)
    new_player.volume_db = -80.0
    add_child(new_player)
    new_player.play()

    var tween = create_tween()
    tween.set_parallel(true)
    tween.tween_property(music_player, "volume_db", -80.0, duration)
    tween.tween_property(new_player, "volume_db", 0.0, duration)

    await tween.finished
    music_player.stop()
    music_player = new_player
    current_track = new_track
```

## Dynamic Audio

```gdscript
extends Node

@onready var engine_sound = $AudioStreamPlayer

func _process(delta):
    var speed_ratio = current_speed / max_speed
    engine_sound.pitch_scale = lerp(0.8, 2.0, speed_ratio)
    engine_sound.volume_db = lerp(-20, 0, speed_ratio)
```

## Audio Pooling

```gdscript
extends Node

var pool_size = 10
var audio_pool: Array[AudioStreamPlayer] = []

func _ready():
    for i in pool_size:
        var player = AudioStreamPlayer.new()
        add_child(player)
        audio_pool.append(player)

func play_sound(stream: AudioStream) -> AudioStreamPlayer:
    for player in audio_pool:
        if not player.playing:
            player.stream = stream
            player.play()
            return player

    var player = audio_pool[0]
    player.stream = stream
    player.play()
    return player
```

## Best Practices

1. **Use audio buses**: Organize Music, SFX, Voice
2. **Pool audio players**: Reuse for performance
3. **Fade transitions**: Smooth music changes
4. **Positional audio**: Use 2D/3D players for spatial sound
5. **Compression**: Use OGG for music, WAV for short SFX
6. **Volume normalization**: Consistent levels across sounds
