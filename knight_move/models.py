from django.db import models

PIECE_CHOICES = (
    ('k', 'King'),
    ('q', 'Queen'),
    ('r', 'Rook'),
    ('b', 'Bishop'),
    ('n', 'Knight'),
    ('p', 'Pawn'),
)

COLOR_CHOICES = (
    (True, 'White'),
    (False, 'Black'),
)


class Piece(models.Model):
    type = models.CharField(max_length=1, choices=PIECE_CHOICES)
    color = models.BooleanField(choices=COLOR_CHOICES)
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()

    def get_values(self):
        return {
            'id': self.id,
            'type': self.type,
            'type_display': self.get_type_display(),
            'color': self.color,
            'color_display': self.get_color_display(),
            'x_coord': self.x_coord,
            'x_coord_display': chr(self.x_coord + ord('A')),
            'y_coord': self.y_coord,
            'y_coord_display': self.y_coord + 1,
        }

    def __repr__(self):
        return str(self.get_values())

    def __str__(self):
        color = 'White' if self.color else 'Black'
        columnName = chr(self.x_coord + ord('A'))
        return f'{color}_{self.type.upper()}{columnName}{self.y_coord + 1}'
