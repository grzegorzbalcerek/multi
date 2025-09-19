from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from itertools import chain

from board import (find_color_figure_fields, free_destinations, starting_board,
                   update_board)
from color import Color, color_row, other_color
from field import Field
from figure import Figure, FigureType
from figure_move import figure_targetss
from move import EnPassantMove, Move, PromotionMove, RegularMove


@dataclass
class Game:
    color: Color
    board: dict[(int, int), Figure]


@dataclass
class GameStart(Game):
    def __init__(self):
        self.color = Color.White
        self.board = starting_board()


@dataclass
class OngoingGame(Game):
    prev_game: Game
    last_move: Move

    def show_move(self):
        return f"{str(other_color(self.color))[6:]} {self.last_move.frm} to {self.last_move.to}"


def game_message(game: Game):
    match game:
        case GameStart(_, _):
            return "White to begin"
        case OngoingGame(_, _, _, _):
            return f"Last move: {game.show_move()}"


def game_moves(game: Game):
    match game:
        case GameStart(_, _):
            return []
        case OngoingGame(_, _, prev_game, _):
            prev_moves = game_moves(prev_game)
            prev_moves.append(game.show_move())
            return prev_moves


def show_game_hist(game: Game):
    def prefix(n):
        return str(n // 2 + 1).rjust(3) + ". " if n % 2 == 0 else ", "

    def suffix(n):
        return "" if n % 2 == 0 else "\n"

    init = (0, "")

    def step(acc: (int, str), curr: str) -> (int, str):
        return (acc[0] + 1, acc[1] + prefix(acc[0]) + curr + suffix(acc[0]))

    return reduce(step, game_moves(game), init)[1]


def update_game(game: Game, move: Move):
    return OngoingGame(
        other_color(game.color), update_board(game.board, move), game, move
    )


def is_en_passant_capture(game: Game, frm: Field, to: Field) -> bool:
    """
    Verifies if the en passant capture move is possible
    """
    match game:
        case OngoingGame(color, board, _, RegularMove(last_move_frm, last_move_to)) if (
            board.get(last_move_to.as_pair())
            == Figure(FigureType.Pawn, other_color(color))
            and last_move_frm.col == last_move_to.col == to.col
            and last_move_frm.row == color_row(color, 7)
            and last_move_to.row == color_row(color, 5)
            and (frm.col == last_move_frm.col + 1 or frm.col == last_move_frm.col - 1)
            and frm.row == color_row(color, 5)
            and to.row == color_row(color, 6)
        ):
            return True
        case _:
            return False


def next_games_after_pawn_en_passant_moves(game: Game, frm: Field, pawn: Figure):
    possible_destinations = free_destinations(
        game.board, figure_targetss(pawn, frm, True)
    )
    possible_en_passant_capture_destinations = filter(
        lambda to: is_en_passant_capture(game, frm, to), possible_destinations
    )
    return list(
        map(
            lambda to: update_game(
                game, EnPassantMove(frm, to, Field(to.col, frm.row))
            ),
            possible_en_passant_capture_destinations,
        )
    )


def next_games_after_pawn_regular_and_promotion_moves(
    game: Game, frm: Field, pawn: Figure
):
    fd = free_destinations(game.board, figure_targetss(pawn, frm, False))
    cd = find_color_figure_fields(
        game.board, figure_targetss(pawn, frm, True), other_color(game.color)
    )
    destinations = [*fd, *cd]
    promotion_figures = [
        FigureType.Queen,
        FigureType.Rook,
        FigureType.Bishop,
        FigureType.Knight,
    ]

    def games(to):
        if color_row(game.color, to.row) == 8:
            return map(
                lambda fig: update_game(game, PromotionMove(frm, to, fig)),
                map(lambda ft: Figure(ft, game.color), promotion_figures),
            )
        else:
            return [update_game(game, RegularMove(frm, to))]

    results = map(games, destinations)
    return list(chain(*results))


def next_games_after_figure_moves(game: Game, frm: Field, fig: Figure):
    fieldss = figure_targetss(fig, frm, True)
    fd = free_destinations(game.board, fieldss)
    cd = find_color_figure_fields(game.board, fieldss, other_color(game.color))
    destinations = [*fd, *cd]
    return list(map(lambda to: update_game(game, RegularMove(frm, to)), destinations))
    # TODO castling

def next_games_after_moves(game: Game, frm: Field, fig: Figure):
    if (fig.figure_type == FigureType.Pawn):
        return [*next_games_after_pawn_regular_and_promotion_moves(game, frm, fig), *next_games_after_pawn_en_passant_moves(game, frm, fig)]
    else:
        return next_games_after_figure_moves(game, frm, fig)
