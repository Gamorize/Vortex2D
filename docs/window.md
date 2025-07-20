# Window

## Creating a `Window`

```python
from vortex2d.graphics.window import Window

win = Window()
win.initialize()

while not win.should_close():
    # game loop
    win.update()

win.terminate()
```

## Constructor Parameters

```python
Window(
    width: int = 800,
    height: int = 600,
    title: str = "Game Window",
    bg_color: Color = None,
    fullscreen: bool = False,
    resizable: bool = True
)
```

| Parameter     | Type   | Default | Description                                              |
|---------------|--------|---------|----------------------------------------------------------|
| `width`       | int    | 800     | Initial window width in pixels                           |
| `height`      | int    | 600     | Initial window height in pixels                          |
| `title`       | str    | "Game Window" | Window title displayed in the title bar             |
| `bg_color`    | Color  | None    | Background color (uses black if None)                   |
| `fullscreen`  | bool   | False   | Start in fullscreen mode if True                        |
| `resizable`   | bool   | True    | Allow window resizing at runtime                        |

## Methods

### `initialize()`

Initializes GLFW, creates the window, sets up OpenGL context, and applies initial settings.

```python
win.initialize()
```

### `should_close() -> bool`

Returns `True` if the window should close (e.g., user pressed close button).

```python
if win.should_close():
    # Exit game loop
```

### `update()`

Clears the screen with the background color, swaps buffers, and polls events. Call once per frame.

```python
win.update()
```

### `terminate()`

Cleans up GLFW resources. Call once when your game exits.

```python
win.terminate()
```

## Runtime Configuration

### Set Background Color

```python
win.set_bg_color(Color('#FF0000'))  # Sets background to red
```

### Toggle Fullscreen

```python
win.set_fullscreen(True)   # Switch to fullscreen
win.set_fullscreen(False)  # Switch back to windowed mode
```

### Enable/Disable Resizing

```python
win.set_resizable(False)  # Disable resizing
win.set_resizable(True)   # Enable resizing
```

> **Note:** Changing resizable at runtime may require recreating the window for some platforms.

### Change Window Size

```python
win.set_size(1024, 768)
```

### Change Window Title

```python
win.set_title("New Title")
```

### Change Window Position

```python
win.set_position(100, 100)
```

---

## Additional Notes

- When toggling fullscreen or resizing, the window may need to be recreated for changes to take effect properly.
- The background color is set via a `Color` object, which accepts hex strings or RGB tuples.
