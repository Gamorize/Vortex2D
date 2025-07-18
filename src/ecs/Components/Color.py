from base import Component

class Color(Component):
    def __init__(self, value):
        self._rgb = None
        self._hex = None
        self.set_color(value)

    def set_color(self, value):
        if isinstance(value, str):
            self.hex = value
        elif isinstance(value, (list, tuple)):
            self.rgb = value
        else:
            raise ValueError("Color must be a hex string or RGB list/tuple.")

    @property
    def rgb(self):
        return self._rgb

    @rgb.setter
    def rgb(self, value):
        if not (isinstance(value, (list, tuple)) and len(value) == 3):
            raise ValueError("RGB must be a list or tuple of three values.")
        self._rgb = tuple(int(c) for c in value)
        self._hex = self.rgb_to_hex(self._rgb)

    @property
    def hex(self):
        return self._hex

    @hex.setter
    def hex(self, value):
        if not isinstance(value, str):
            raise ValueError("Hex must be a string.")
        if value.startswith('#'):
            value = value[1:]
        if len(value) != 6:
            raise ValueError("Hex string must be 6 characters.")
        self._hex = '#' + value.upper()
        self._rgb = self.hex_to_rgb(self._hex)

    def rgb_to_hex(self, rgb):
        return '#' + ''.join(f'{c:02X}' for c in rgb)

    def hex_to_rgb(self, hex_str):
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
