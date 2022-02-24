from django.db import models

class Piece(models.Model):
    type = models.CharField(max_length=1, choices=([
        ('k', 'King'),
        ('q', 'Queen'),
        ('r', 'Rook'),
        ('b', 'Bishop'),
        ('n', 'Knight'),
        ('p', 'Pawn'),
    ]))
    color = models.BooleanField(choices=([
        (True, 'White'),
        (False, 'Black'),
    ]))
    x_coord = models.IntegerField()
    y_coord = models.IntegerField()

    def __str__(self):
        color = 'White' if self.color else 'Black'
        columnName = chr(self.x_coord + ord('A'))
        return f'{color}_{self.type}{columnName}{self.y_coord + 1}'
