import { Color } from "./color"
import { Field } from "./field"
import { Figure } from "./figure"
import { Move, RegularMove, PromotionMove, EnPassantMove, CastlingMove  } from "./move"
import * as U from './util'

export type Board = { [key: string]: Figure }
export const startingBoard: Board = {}
startingBoard[new Field(1,1).show()] = new Figure('Rook','White')
startingBoard[new Field(2,1).show()] = new Figure('Knight','White')
startingBoard[new Field(3,1).show()] = new Figure('Bishop','White')
startingBoard[new Field(4,1).show()] = new Figure('Queen','White')
startingBoard[new Field(5,1).show()] = new Figure('King','White')
startingBoard[new Field(6,1).show()] = new Figure('Bishop','White')
startingBoard[new Field(7,1).show()] = new Figure('Knight','White')
startingBoard[new Field(8,1).show()] = new Figure('Rook','White')
startingBoard[new Field(1,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(2,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(3,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(4,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(5,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(6,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(7,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(8,2).show()] = new Figure('Pawn','White')
startingBoard[new Field(1,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(2,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(3,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(4,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(5,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(6,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(7,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(8,7).show()] = new Figure('Pawn','Black')
startingBoard[new Field(1,8).show()] = new Figure('Rook','Black')
startingBoard[new Field(2,8).show()] = new Figure('Knight','Black')
startingBoard[new Field(3,8).show()] = new Figure('Bishop','Black')
startingBoard[new Field(4,8).show()] = new Figure('Queen','Black')
startingBoard[new Field(5,8).show()] = new Figure('King','Black')
startingBoard[new Field(6,8).show()] = new Figure('Bishop','Black')
startingBoard[new Field(7,8).show()] = new Figure('Knight','Black')
startingBoard[new Field(8,8).show()] = new Figure('Rook','Black')

export function updateBoard(board: Board, move: Move): Board {
    let figure = board[move.from.show()]
    if (figure === undefined) return board;
    let result: Board = Object.assign({}, board);
    if (move instanceof RegularMove) {
        delete result[move.from.show()];
        result[move.to.show()] = figure;
        return result;
    } else if (move instanceof PromotionMove) {
        delete result[move.from.show()];
        result[move.to.show()] = move.figure;
        return result;
    } else if (move instanceof EnPassantMove) {
        delete result[move.from.show()];
        delete result[move.captured.show()];
        result[move.to.show()] = figure;
        return result;
    } else if (move instanceof CastlingMove) {
        let rookFigure = board[move.rookFrom.show()];
        if (rookFigure === undefined) return board;
        delete result[move.from.show()];
        delete result[move.rookFrom.show()];
        result[move.to.show()] = figure;
        result[move.rookTo.show()] = rookFigure;
        return result;
    }
}

// Verifies if the given field is empty
export function isFieldEmpty(board: Board, field: Field): boolean {
    return board[field.show()] === undefined;
}

// Take while condition holds from a list of field lists.
export function takeFieldsWhile(board: Board, fieldss: Field[][], condition: (board: Board, field: Field) => boolean): Field[] {
    return fieldss.flatMap(fields => U.takeWhile(field => condition(board, field), fields))
}


// Returns free fields onto which the figure may be moved
export function freeDestinations(board: Board, fieldss: Field[][]): Field[] {
    return takeFieldsWhile(board, fieldss, isFieldEmpty)
}

// Checks whether the field holds a figure with the given color
export function hasFigureOfColor(board: Board, field: Field, color: Color): boolean {
    let figure = board[field.show()]
    if (figure === undefined) return false;
    else return figure.figureColor === color
}

// Returns fields occupied by the figures of a specific color that are first in each field sequence after an optional series of empty fields
export function findColorFigureFields(board: Board, fieldss: Field[][], color: Color): Field[] {
    return fieldss.flatMap(fields => U.dropWhile(field => isFieldEmpty(board, field), fields).slice(0,1)).filter(f => hasFigureOfColor(board, f, color))
}
