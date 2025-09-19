import { Field, readField } from './field'
import { Figure, FigureType } from './figure'
import { figureTargetss } from './figuremoves'
import { Color, colorRow, otherColor } from './color'
import { Move, RegularMove, PromotionMove, EnPassantMove, CastlingMove } from './move'
import { Board, startingBoard, updateBoard, isFieldEmpty, freeDestinations, findColorFigureFields } from './board'

export interface Game {
  color: Color
  board: Board
}

export class GameStart implements Game {
  color: Color
  board: Board
  constructor() {
    this.color = 'White';
    this.board = startingBoard;
  }
}

export class OngoingGame implements Game {
    color: Color
    board: Board
    prevGame: Game
    lastMove: Move
    constructor(c: Color, b: Board, g: Game, m: Move) {
        this.color = c;
        this.board = b;
        this.prevGame = g;
        this.lastMove = m;
    }
    showMove() {
        return `${otherColor(this.color)} ${this.lastMove.from.show()} to ${this.lastMove.to.show()}`
    }
}

export function gameMessage(game: Game): string {
    if (game instanceof GameStart) {
        return "White to begin"
    } else if (game instanceof OngoingGame) {
        return `Last move: ${game.showMove()}`
    }
    return ""
}

export function gameMoves(game: Game): string[] {
    if (game instanceof OngoingGame) {
        let prevMoves = Array.from(gameMoves(game.prevGame))
        prevMoves.push(game.showMove())
        return prevMoves
    }
    return []
}


export function showGameHist(game: Game): string {
    function prefix(n: number) { return (n % 2 === 0) ? (n/2+1).toString().padStart(3, " ")+". " : ", " }
    function suffix(n: number) { return (n % 2 === 0) ? "" : "\n" }
    let init: [number, string] = [0,""]
    function step([n, str]: [number, string], curr: string): [number, string] {
        return [n+1,str + prefix(n) + curr + suffix(n)]
    }
    return gameMoves(game).reduce(step, init)[1]
}


// Returns a new game, updated with a move.
export function updateGame(game: Game, move: Move): OngoingGame {
    return new OngoingGame(otherColor(game.color),
                           updateBoard(game.board, move),
                           game, move)
}

// Verifies if the en passant capture move is possible
export function isEnPassantCapture(game: Game, from: Field, to: Field): boolean {
    if (game instanceof OngoingGame) {
        return game.board[game.lastMove.to.show()].show() === new Figure('Pawn', otherColor(game.color)).show() &&
            game.lastMove.from.col === game.lastMove.to.col &&
            game.lastMove.from.row === colorRow(otherColor(game.color), 2) &&
            game.lastMove.to.row === colorRow(otherColor(game.color), 4) &&
            (from.col === game.lastMove.from.col + 1 || from.col === game.lastMove.from.col - 1) &&
            from.row === colorRow(game.color, 5) &&
            to.col === game.lastMove.to.col &&
            to.row === colorRow(game.color, 6)
    }
    return false
}

export function nextGamesAfterPawnEnPassantMoves(game: Game, from: Field, pawn: Figure): OngoingGame[] {
    let possibleDestinations = freeDestinations(game.board, figureTargetss(pawn, from, true))
    let possibleEnPassantCaptureDestinations = possibleDestinations.filter(to => isEnPassantCapture(game, from, to))
    return possibleEnPassantCaptureDestinations.map(to => updateGame(game, new EnPassantMove(from, to, new Field(to.col, from.row))))
}

export function nextGamesAfterPawnRegularAndPromotionMoves(game: Game, from: Field, pawn: Figure): OngoingGame[] {
    let fd = freeDestinations(game.board, figureTargetss(pawn, from, false))
    let cd = findColorFigureFields(game.board, figureTargetss(pawn, from, true), otherColor(game.color))
    let destinations = [...fd, ...cd]
    let promotionFigures: FigureType[] = ['Queen', 'Rook', 'Bishop', 'Knight']
    let results = destinations.map(to => {
        if (to.isLastRow(game.color))
            return promotionFigures. map(ft => new Figure(ft, game.color)).
                map(fig => updateGame(game, new PromotionMove(from, to, fig)))
        else
            return [ updateGame(game, new RegularMove(from, to)) ]
    })
    return ([] as OngoingGame[]).concat(...results)
}

export function nextGamesAfterFigureMoves(game: Game, from: Field, fig: Figure): OngoingGame[] {
    let fieldss = figureTargetss(fig, from, true)
    let fd = freeDestinations(game.board, fieldss)
    let cd = findColorFigureFields(game.board, fieldss, otherColor(game.color))
    let destinations = [...fd, ...cd]
    return destinations.map(to => updateGame(game, new RegularMove(from, to)))
    // TODO castling
}

export function nextGamesAfterMoves(game: Game, from: Field, figure: Figure): OngoingGame[] {
    if (figure.figureType === 'Pawn')
        return [...nextGamesAfterPawnRegularAndPromotionMoves(game, from, figure), ...nextGamesAfterPawnEnPassantMoves(game, from, figure)]
  else
      return nextGamesAfterFigureMoves(game, from, figure)
}

export function maybeNextGamesAfterMoves(game: Game, from: string, figure: Figure): OngoingGame[] {
    let field = readField(from)
    if (field === undefined) return []
    else return nextGamesAfterMoves(game, field, figure)
}

// Returns next games after possible next moves moves (including those
// moves after which the King is checked).
// The code iterates over all figures that have the same color as
// the color of the next move. The 'g' value contains sequences of game states
// corresponding to the possible next moves of the given figure.
// Figure moves depend on its kind. The Rook, the Knight, the Queen, the Bishop
// and the King are treated in a similar way, except for the King, for which
// the castling moves are included as well.
// Potentially there are two possible castling moves.
// Each of them is handled by a call to the 'castling' method.
// The most complex case handled by the method is the case of the Pawn moves.
// The Pawn may move forward onto a free field or forward and left or right onto
// a field occupied by an enemy figure. In both cases, if the destination field
// lies on the last row, the set of possible moves includes the possible
// promotions to other figures. In addition to that, the Pawn may make the so
// called en passant capture, which consists of moving the Pawn forward and left
// or right onto a free field which has been passed-by by an enemy Pawn in the
// previous move.
export function nextGames(game: Game): OngoingGame[] {
    return ([] as OngoingGame[]).concat(...Object.entries(game.board).
        filter(entry => entry[1].figureColor === game.color).
        map(entry => maybeNextGamesAfterMoves(game, entry[0], entry[1])))
}

function isOtherKingOnBoard(game: Game): boolean {
    return Object.values(game.board).some(fig => fig.figureType === 'King' && fig.figureColor === otherColor(game.color))
}

// Verifies if the enemy King is under check
export function isOtherKingUnderCheck(game: Game): boolean {
    return !nextGames(game).every(isOtherKingOnBoard)
}

// Verifies if the King of the player who is about to make a move is under check. -}
export function isKingUnderCheck(game: Game): boolean {
    let flippedColorGame = new OngoingGame(otherColor(game.color), game.board, game,
                                           new RegularMove(new Field(0,0), new Field(0,0)))
    return isOtherKingUnderCheck(flippedColorGame)
}


export function validGames(game: Game): OngoingGame[] {
    return nextGames(game).filter(g => !isOtherKingUnderCheck(g))
}

export function validPromotionMoves(game: Game, from: Field, to: Field): Figure[] {
    if (to.isLastRow(game.color) &&
        game.board[from.show()] !== undefined &&
        game.board[from.show()].figureType === 'Pawn') {
        return validGames(game).flatMap(nextGame =>
            nextGame.lastMove instanceof PromotionMove &&
            nextGame.lastMove.from.show() === from.show() &&
            nextGame.lastMove.to.show() === to.show() ? [nextGame.lastMove.figure] : [])
    } else return []
}

export function isGameFinished(game: Game): boolean {
    return nextGames(game).every(isOtherKingUnderCheck)
    // TODO
}

export function winner(game: Game): Color | undefined {
    if (isGameFinished(game) && isKingUnderCheck(game))
        return otherColor(game.color)
    else
        return undefined
}

export function makeMove(game: Game, from: Field, to: Field, promotion: Figure | undefined): OngoingGame | undefined {
    return validGames(game).find(g =>
        g.lastMove instanceof PromotionMove &&
        g.lastMove.from.show() === from.show() &&
        g.lastMove.to.show() === to.show() &&
        g.lastMove.figure === promotion ||
        g.lastMove.from.show() === from.show() &&
        g.lastMove.to.show() === to.show() &&
        promotion === undefined)        
}
