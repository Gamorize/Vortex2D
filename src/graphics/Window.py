import glfw
from OpenGL.GL import *
from ecs.Components.Color import Color

class Window:
    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Vortex2D Window",
        bg_color: Color = None,
        fullscreen: bool = False,
        resizable: bool = True
    ):
        self.width = width
        self.height = height
        self.title = title
        self.fullscreen = fullscreen
        self.resizable = resizable
        self.bg_color = bg_color if bg_color else Color('#000000')
        self.window = None
        self.monitor = None

    def initialize(self) -> None:
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE if self.resizable else glfw.FALSE)
        if self.fullscreen:
            self.monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(self.monitor)
            self.width, self.height = mode.size.width, mode.size.height
            self.window = glfw.create_window(self.width, self.height, self.title, self.monitor, None)
        else:
            self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        glfw.make_context_current(self.window)
        self.setup_viewport()
        self.set_background_color(self.bg_color)

    def setup_viewport(self) -> None:
        glViewport(0, 0, self.width, self.height)

    def set_background_color(self, color: Color) -> None:
        rgb = color.rgb
        glClearColor(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0, 1.0)

    def should_close(self) -> bool:
        return glfw.window_should_close(self.window)

    def update(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def terminate(self) -> None:
        glfw.terminate()

    # Runtime options
    def set_fullscreen(self, enable: bool) -> None:
        if enable == self.fullscreen:
            return
        self.fullscreen = enable
        glfw.destroy_window(self.window)
        if enable:
            self.monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(self.monitor)
            self.width, self.height = mode.size.width, mode.size.height
            self.window = glfw.create_window(self.width, self.height, self.title, self.monitor, None)
        else:
            self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        glfw.make_context_current(self.window)
        self.setup_viewport()

    def set_resizable(self, resizable: bool) -> None:
        self.resizable = resizable
        glfw.window_hint(GLFW_RESIZABLE, glfw.TRUE if resizable else glfw.FALSE)
        # Note: Changing resizable at runtime may require recreating window
        # For simplicity, you can destroy and recreate window if needed

    def set_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        glfw.set_window_size(self.window, width, height)
        self.setup_viewport()

    def set_title(self, title: str) -> None:
        self.title = title
        glfw.set_window_title(self.window, title)

    def set_bg_color(self, color: Color) -> None:
        self.bg_color = color
        self.set_background_color(color)

    def set_position(self, x: int, y: int) -> None:
        glfw.set_window_pos(self.window, x, y)

if __name__ == "__main__":
    win = Window(800, 600, "My Game", bg_color=Color('#4D607D'), resizable=False)
    win.initialize()

    # Toggle fullscreen
    # win.set_fullscreen(True)

    # Change background color at runtime
    # win.set_bg_color(Color('#FF0000'))

    while not win.should_close():
        # Your game logic
        win.update()

    win.terminate()
