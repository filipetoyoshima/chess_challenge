from django.http import HttpResponse
import json
from .models import Piece


def index(request):
    return HttpResponse("Hello, world. You're at the knight_move index.")


def register_piece(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    body = json.loads(request.body.decode('utf-8'))
    existing_piece = Piece.objects.filter(x_coord=body['x_coord'], y_coord=body['y_coord'])
    if existing_piece:
        return HttpResponse(status=409, content='Piece already exists at this location')
    piece = Piece.objects.create(**body)
    return HttpResponse(status=201, content=json.dumps(piece.__repr__()))