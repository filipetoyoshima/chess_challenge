from django.http import HttpResponse
import json
from .models import Piece


def index(request):
    return HttpResponse("Hello, world. You're at the knight_move index.")


def register_piece(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    body = json.loads(request.body.decode('utf-8'))
    existing_piece = Piece.objects.filter(
        x_coord=body['x_coord'], y_coord=body['y_coord'])
    if existing_piece:
        return HttpResponse(
            status=409,
            content='Piece already exists at this location'
        )
    piece = Piece.objects.create(**body)
    return HttpResponse(status=201, content=json.dumps(piece.__repr__()))


def get_board(request, type='string'):
    if request.method != 'GET':
        return HttpResponse(status=405)

    matrix = generate_board_matrix(natural_board=True)

    if type == 'string':
        return HttpResponse(
            status=200,
            content='\n'.join([' '.join(row) for row in matrix])
        )
    elif type == 'json':
        return HttpResponse(status=200, content=json.dumps(matrix))
    else:
        return HttpResponse(status=400, content='Invalid type')


def get_horse_movements(
    request, piece_id
):
    force_origin = request.GET.get('force_origin', False)
    allow_capture = request.GET.get('allow_capture', False)
    natural_notation = request.GET.get('natural_notation', False)
    steps = 0
    if request.method != 'GET':
        return HttpResponse(status=405)
    piece = Piece.objects.get(id=piece_id)
    if not piece:
        return HttpResponse(status=404, content='Piece not found')
    if piece.type != 'n' and not force_origin:
        return HttpResponse(status=400, content='Piece is not a knight')

    piece_matrix = generate_board_matrix()
    x = piece.x_coord
    y = piece.y_coord
    originColor = 'w' if piece.color else 'b'
    valid_movements = calc_horse_movement(
        x, y, piece_matrix, allow_capture, steps, originColor
    )

    if natural_notation:
        valid_movements = [
            (chr(x + ord('A')), y + 1) for (x, y) in valid_movements
        ]

    return HttpResponse(status=200, content=json.dumps(valid_movements))


def calc_horse_movement(
    x, y, piece_matrix, allow_capture=False, remmaing_steps=0, originColor='w'
):
    print(x, y)
    _piece_matrix = piece_matrix.copy()
    valid_movements = []
    for x_offset, y_offset in [
        (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2)
    ]:
        x_destination = x + x_offset
        y_destination = y + y_offset
        if 0 <= x_destination <= 7 and 0 <= y_destination <= 7:
            print(f'{x} -> {x_destination}')
            print(f'{y} -> {y_destination}')
            print('-' * 20)
            if _piece_matrix[y_destination][x_destination] == '__':
                valid_movements.append((x_destination, y_destination))
            elif (allow_capture and
                  (_piece_matrix[y_destination][x_destination][0] !=
                   originColor)):
                valid_movements.append((x_destination, y_destination))

    return valid_movements

# just for the record: this elif is horrible, but flake8 seems to like it


def generate_board_matrix(natural_board=False):
    matrix = [['__' for _ in range(8)] for _ in range(8)]
    for piece in Piece.objects.all():
        y = 7 - piece.y_coord if natural_board else piece.y_coord
        matrix[y][piece.x_coord] = \
            f'{"w" if piece.color else "b"}{piece.type.upper()}'
    return matrix
