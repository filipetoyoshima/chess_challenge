from django.test import TestCase
from .models import Piece

BOARD = """__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
wN __ __ __ __ __ __ __"""


class KnightMoveTestCase(TestCase):
    def setUp(self):
        Piece.objects.create(**{
            'type': 'n',
            'color': True,
            'x_coord': 0,
            'y_coord': 0,
        })

    def test_get_board(self):
        self.maxDiff = None
        response = self.client.get('/knight_move/get_board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            BOARD
        )
