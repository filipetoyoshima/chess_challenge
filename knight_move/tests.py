from django.test import TestCase
from .models import Piece
import json

BOARD_STRING = """__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
__ __ __ __ __ __ __ __
wN __ __ __ __ __ __ __"""

BOARD_JSON = [
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['__', '__', '__', '__', '__', '__', '__', '__'],
    ['wN', '__', '__', '__', '__', '__', '__', '__']
]
# tried to [['__'] * 8] * 7, but got a giant single list
# instead of a list of lists


class KnightMoveTestCase(TestCase):
    def setUp(self):
        self.test_piece = Piece.objects.create(**{
            'type': 'n',
            'color': True,
            'x_coord': 0,
            'y_coord': 0,
        })

    def test_get_piece_values(self):
        values = {
            'id': self.test_piece.id,
            'type': 'n',
            'type_display': 'Knight',
            'color': True,
            'color_display': 'White',
            'x_coord': 0,
            'x_coord_display': 'A',
            'y_coord': 0,
            'y_coord_display': 1,
        }
        self.assertEqual(
            self.test_piece.get_values(),
            values
        )
        self.assertEqual(
            self.test_piece.__repr__(),
            str(values)
        )

    def test_get_piece_string(self):
        self.assertEqual(
            str(self.test_piece),
            'White_NA1'
        )

    def test_register_piece_forbidden_method(self):
        response = self.client.get('/knight_move/register_piece/')
        self.assertEqual(response.status_code, 405)

    def test_register_piece_exist_in_location(self):
        response = self.client.post(
            '/knight_move/register_piece/',
            json.dumps({
                'type': 'n',
                'color': True,
                'x_coord': 0,
                'y_coord': 0,
            }),
            content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_register_piece_success(self):
        response = response = self.client.post(
            '/knight_move/register_piece/',
            json.dumps({
                'type': 'n',
                'color': False,
                'x_coord': 1,
                'y_coord': 1,
            }),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_body = json.loads(response.content)
        self.assertEqual(
            response_body,
            {
                'id': response_body['id'],  # any id will do
                'type': 'n',
                'type_display': 'Knight',
                'color': False,
                'color_display': 'Black',
                'x_coord': 1,
                'x_coord_display': 'B',
                'y_coord': 1,
                'y_coord_display': 2,
            }
        )

    def test_get_board_forbidden_method(self):
        response = self.client.post('/knight_move/get_board/')
        self.assertEqual(response.status_code, 405)

    def test_get_board_invalid_type(self):
        response = self.client.get('/knight_move/get_board/invalid/')
        self.assertEqual(response.status_code, 400)

    def test_get_board_success_string(self):
        self.maxDiff = None
        response = self.client.get('/knight_move/get_board/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            BOARD_STRING
        )

    def test_get_board_success_json(self):
        self.maxDiff = None
        response = self.client.get('/knight_move/get_board/json/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode('utf-8'),
            json.dumps(BOARD_JSON)
        )

    def test_get_knight_moves_forbbiden_method(self):
        response = self.client.post(
            '/knight_move/get_knight_movements/A1'
        )
        self.assertEqual(response.status_code, 405)

    def test_get_knight_moves_basic_case_coordinate(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/A1'
        )
        self.assertEqual(response.status_code, 200)
        valid_movements = json.loads(response.content)
        expected_answer = [[1, 2], [2, 1]]
        for valid_movement in valid_movements:
            self.assertIn(valid_movement, expected_answer)

    def test_get_knight_moves_basic_case_piece_id(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/1'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[1, 2], [2, 1]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_get_knight_moves_case_new_piece(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/bh8?force_origin=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[6, 5], [5, 6]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_get_knight_moves_case_new_piece2(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/bG7?force_origin=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[5, 4], [4, 5], [4, 7], [7, 4]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)

    def test_get_knight_moves_case_new_piece3(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/g7?force_origin=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[5, 4], [4, 5], [4, 7], [7, 4]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)

    def test_get_knight_moves_non_existent_piece(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/99'
        )
        self.assertEqual(response.status_code, 404)

    def test_get_knight_moves_invalid_coordinate(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/A9'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_knight_moves_invalid_coordinate_2(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/9A'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_knight_moves_not_knight(self):
        piece = Piece.objects.create(**{
            'type': 'p',
            'color': True,
            'x_coord': 4,
            'y_coord': 4,
        })
        response = self.client.get(
            f'/knight_move/get_knight_movements/{piece.id}'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_knight_moves_natural_notation(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/1?natural_notation=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [["C", 2], ["B", 3]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_knight_moves_allow_capture(self):
        Piece.objects.create(**{
            'type': 'n',
            'color': False,
            'x_coord': 2,
            'y_coord': 1,
        })
        response = self.client.get(
            '/knight_move/get_knight_movements/1?allow_capture=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[2, 1], [1, 2]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_knight_moves_not_allow_capture(self):
        Piece.objects.create(**{
            'type': 'n',
            'color': False,
            'x_coord': 2,
            'y_coord': 1,
        })
        response = self.client.get(
            '/knight_move/get_knight_movements/1'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[1, 2]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_knight_moves_allow_capture_but_not_same_color(self):
        Piece.objects.create(**{
            'type': 'n',
            'color': True,
            'x_coord': 2,
            'y_coord': 1,
        })
        response = self.client.get(
            '/knight_move/get_knight_movements/1?allow_capture=true'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [[1, 2]]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_knight_moves_2_steps(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/1?steps=2'
        )
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        expected_answer = [
            [0, 0], [0, 4], [2, 4], [3, 3], [4, 2], [4, 0], [3, 1], [1, 3],
            [2, 0], [0, 2]
        ]
        for valid_movement in response_body:
            self.assertIn(valid_movement, expected_answer)
        self.assertEqual(len(response_body), len(expected_answer))

    def test_knight_moves_too_much_steps(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/1?steps=11'
        )
        self.assertEqual(response.status_code, 400)

    def test_knight_moves_negative_steps(self):
        response = self.client.get(
            '/knight_move/get_knight_movements/1?steps=-1'
        )
        self.assertEqual(response.status_code, 400)
