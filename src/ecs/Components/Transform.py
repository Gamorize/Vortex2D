from base import Component
import numpy as np

class Transform2D(Component):
    def __init__(self, x: int, y: int, width: float = 64, scale_x: float = 1, scale_y: float = 1, height: float = 64, rotation: int = 0, pivot_x = None, pivot_y = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.rotation = rotation # deg

        # Default pivot is center
        self.pivot_x = pivot_x if pivot_x is not None else width / 2
        self.pivot_y = pivot_y if pivot_y is not None else height / 2

    def get_transformation_matrix(self):
        rad = np.radians(self.rotation)
        cos_r = np.cos(rad)
        sin_r = np.sin(rad)

        # Translate to sprite position
        translation = np.array([
            [1, 0, self.x],
            [0, 1, self.y],
            [0, 0, 1]
        ])

        # Translate to pivot point (relative to sprite origin)
        pivot_translation = np.array([
            [1, 0, -self.pivot_x],
            [0, 1, -self.pivot_y],
            [0, 0, 1]
        ])

        # Rotation matrix
        rotation = np.array([
            [cos_r, -sin_r, 0],
            [sin_r, cos_r, 0],
            [0, 0, 1]
        ])

        # Scale matrix
        scale = np.array([
            [self.scale_x, 0, 0],
            [0, self.scale_y, 0],
            [0, 0, 1]
        ])

        # Translate back from pivot
        pivot_back = np.array([
            [1, 0, self.pivot_x],
            [0, 1, self.pivot_y],
            [0, 0, 1]
        ])

        # Combine: T * (PivotBack * Rotation * Scale * PivotTranslation)
        transform = translation @ pivot_back @ rotation @ scale @ pivot_translation
        return transform
