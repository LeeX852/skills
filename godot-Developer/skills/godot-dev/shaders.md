# Shaders Skill

## Description
Expert skill for Godot's shader system including visual shaders and shader language

## Triggers
- Shader development
- Visual effects
- Material customization
- Post-processing
- Particle shaders

## Shader Types

### CanvasItem Shader (2D)
```gdshader
shader_type canvas_item;

// Uniform variables (exposed in editor)
uniform float brightness : hint_range(0.0, 2.0) = 1.0;
uniform vec4 tint_color : source_color = vec4(1.0);

void fragment() {
    // Sample texture
    vec4 color = texture(TEXTURE, UV);
    
    // Apply brightness
    color.rgb *= brightness;
    
    // Apply tint
    color *= tint_color;
    
    COLOR = color;
}
```

### Spatial Shader (3D)
```gdshader
shader_type spatial;

// Uniforms
uniform vec4 albedo_color : source_color = vec4(1.0);
uniform float metallic : hint_range(0.0, 1.0) = 0.0;
uniform float roughness : hint_range(0.0, 1.0) = 0.5;
uniform sampler2D albedo_texture : source_color;

void fragment() {
    // Albedo
    ALBEDO = texture(albedo_texture, UV).rgb * albedo_color.rgb;
    METALLIC = metallic;
    ROUGHNESS = roughness;
}

void light() {
    // Custom lighting
    DIFFUSE_LIGHT += dot(NORMAL, LIGHT) * ATTENUATION * ALBEDO;
}
```

### Particle Shader
```gdshader
shader_type particles;

uniform float spread = 45.0;
uniform float initial_velocity = 10.0;
uniform float gravity = 9.8;

void vertex() {
    if (RESTARTING) {
        // Initial particle setup
        VELOCITY = vec3(
            cos(UNIFORM.x) * initial_velocity,
            sin(UNIFORM.x) * initial_velocity,
            0.0
        );
    }
    
    // Apply gravity
    VELOCITY.y -= gravity * DELTA;
}
```

## Common Shader Effects

### Dissolve Effect
```gdshader
shader_type canvas_item;

uniform float dissolve_amount : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D noise_texture;
uniform vec4 dissolve_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);

void fragment() {
    vec4 color = texture(TEXTURE, UV);
    float noise = texture(noise_texture, UV).r;
    
    if (noise < dissolve_amount) {
        discard;
    }
    
    // Edge glow
    float edge = smoothstep(dissolve_amount, dissolve_amount + 0.1, noise);
    color.rgb = mix(dissolve_color.rgb, color.rgb, edge);
    
    COLOR = color;
}
```

### Outline Shader
```gdshader
shader_type canvas_item;

uniform float outline_width = 2.0;
uniform vec4 outline_color : source_color = vec4(0.0, 0.0, 0.0, 1.0);

void fragment() {
    vec4 color = texture(TEXTURE, UV);
    
    // Sample neighboring pixels
    float size = outline_width / float(textureSize(TEXTURE, 0).x);
    float alpha = color.a;
    
    alpha = max(alpha, texture(TEXTURE, UV + vec2(size, 0.0)).a);
    alpha = max(alpha, texture(TEXTURE, UV - vec2(size, 0.0)).a);
    alpha = max(alpha, texture(TEXTURE, UV + vec2(0.0, size)).a);
    alpha = max(alpha, texture(TEXTURE, UV - vec2(0.0, size)).a);
    
    // Outline
    if (color.a < 0.1 && alpha > 0.1) {
        COLOR = outline_color;
    } else {
        COLOR = color;
    }
}
```

### Water Effect
```gdshader
shader_type canvas_item;

uniform float wave_speed = 1.0;
uniform float wave_strength = 0.02;
uniform sampler2D noise_texture;

void fragment() {
    vec2 uv = UV;
    
    // Wave distortion
    float time = TIME * wave_speed;
    float noise = texture(noise_texture, uv + vec2(time, 0.0)).r;
    uv.x += (noise - 0.5) * wave_strength;
    
    vec4 color = texture(TEXTURE, uv);
    COLOR = color;
}
```

## Visual Shaders

### Creating in Editor
1. Create new VisualShader resource
2. Add nodes from the toolbar
3. Connect nodes to build the graph
4. Output connects to final fragment/vertex

### Common Visual Shader Nodes
- **Texture2D**: Sample textures
- **Vector Operation**: Math on vectors
- **Float Operation**: Math on scalars
- **Color Constant**: Fixed colors
- **Time**: Animation time
- **UV**: Texture coordinates

## Best Practices

1. **Use hints**: `hint_range`, `source_color` for editor integration
2. **Optimize**: Minimize texture reads in fragment shader
3. **Use varyings**: Pass data from vertex to fragment shader
4. **Comment code**: Shaders can be complex
5. **Test on target hardware**: Performance varies greatly
6. **Use render_mode**: Control blending, culling, etc.

## Render Modes
```gdshader
render_mode blend_mix;      // Standard alpha blending
render_mode blend_add;      // Additive blending
render_mode cull_disabled;  // Double-sided
render_mode unshaded;       // No lighting
render_mode depth_draw_never; // No depth writing
```
