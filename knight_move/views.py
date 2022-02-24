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
        return HttpResponse(status=409, content='Piece already exists at this location')
    piece = Piece.objects.create(**body)
    return HttpResponse(status=201, content=json.dumps(piece.__repr__()))


def get_board(request, type='string'):
    if request.method != 'GET':
        return HttpResponse(status=405)
    pieces = Piece.objects.all()
    matrix = [[f'__' for x in range(8)] for y in range(8)]
    for piece in pieces:
        matrix[7 - piece.y_coord][piece.x_coord] = \
            f'{"w" if piece.color else "b"}{piece.type.upper()}'

    if type == 'string':
        return HttpResponse(status=200, content=f'\n'.join([' '.join(row) for row in matrix]))
    elif type == 'json':
        return HttpResponse(status=200, content=json.dumps(matrix))
    else:
        return HttpResponse(status=400, content='Invalid type')
