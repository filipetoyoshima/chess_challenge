# Knight Move App

Here is where the magic happens. We have some endpoints to play with:

| Title            | URL                                 | Description                                                |
|------------------|-------------------------------------|------------------------------------------------------------|
| [Create Piece](#create-piece)     | `POST knight_move/register_piece/`                   | Create a piece on the board                                |
| [View the Board](#view-board)   | `GET knight_move/get_board/`                        | Get a visualization of how the board looks now             |
| [Get Knight Moves](#get-knight-moves) | `GET knight_move/get_knight_movements/<str:origin>` | Get a list of where a knight can go to from certain origin |

## Create Piece

Creates a piece on the board. It doesn't accept two pieces on same location.

### Body

Url: `POST knight_move/register_piece/`

You should send all those attributes:

| Attr    | Type    | Description                                                       |
|---------|---------|-------------------------------------------------------------------|
| type    | string  | One char identifying what kind of piece do you have               |
| color   | boolean | True for white and false for black... should I change this order? |
| x_coord | integer | Number from 0 to 7, representing the horizontal axis              |
| y_coord | integer | Number from 0 to 7, representing the horizontal axis              |

## View Board

Url: `GET knight_move/get_board/`

Optional argument `GET knight_move/get_board/natural_board=false`

Returns a cool visualization of the actual set of the board.

Has a optional parameter `natural_board`, which is, by default, `True`, but you can set it up to false if you'd like to see the chessboard as a more "tech natural" matrix (y 0 on top).

## Get Knight Moves

Url: `GET knight_move/get_knight_movements/<str:origin>`

Here is where things goes crazy.

You need to pass a origin in order to see the start cell of the knight jumps. It can be either the `id` of a existing piece, or  you can reffer to a algebric notation (`'a1'`...`'h8'`). Optionally, if you choose by algebric notation, you can pass the color of a new piece in the specified origin, represented by the letters `'w'` or `'b'`, it could be relevant in a capturing simulation.

Examples:

- `knight_move/get_knight_movements/1` to check the moves from the location where the piece with id 1 is.
- `knight_move/get_knight_movements/a1` to check the moves from the a1 location
- `knight_move/get_knight_movements/wb2` to check the moves from a white piece at b2 location

### Optional Parameters

| Parameter        | Examples    | Description                                                                                                           |
|------------------|-------------|-----------------------------------------------------------------------------------------------------------------------|
| force_origin     | true, false | Force the specied origin, even specified piece is not a knight                                                        |
| allow_capture    | true, false | Allow knight jump at opposite color pieces. After this jump, this location become empty, since its piece was captured |
| natural_notation | true, false | Bring the result at algebric notation instead of raw coordinates                                                      |
| steps            | 2           | How many turns can the knight play in a row. Please, be gentle, dude.                                                 |

So, example:

```
knight_move/get_knight_movements/1?force_origin=true&natural_notation=true&steps=2
```

Will return all the possible locations where the piece with id 1 can go with 2 knight movements (even if not a knight, because of the `force_origin` param), and the return will be an array of arrays, in which each inner array contains the column letter and row number.

