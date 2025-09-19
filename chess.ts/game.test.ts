import { expect, test } from '@jest/globals'
import { startingBoard } from './board'
import { RegularMove } from './move'
import { Field } from './field'
import { Figure } from './figure'
import * as G from './game'

let g1 = new G.GameStart()
let g2 = new G.OngoingGame('Black', startingBoard, g1, new RegularMove(new Field(2,2), new Field(2,3)))
let g3 = new G.OngoingGame('White', startingBoard, g2, new RegularMove(new Field(2,7), new Field(2,5)))
let g4 = new G.OngoingGame('Black', startingBoard, g3, new RegularMove(new Field(4,2), new Field(4,4)))

test('gameMessage', () => {
    expect(G.gameMessage(g1)).toBe("White to begin");
    expect(G.gameMessage(g2)).toBe("Last move: White b2 to b3");
});

test('showMove', () => {
    expect(g2.showMove()).toBe("White b2 to b3");
})

test('gameMoves', () => {
    expect(G.gameMoves(g1)).toStrictEqual([]);
    expect(G.gameMoves(g2)).toStrictEqual(["White b2 to b3"]);
    expect(G.gameMoves(g3)).toStrictEqual(["White b2 to b3", "Black b7 to b5"]);
});

test('showGameHist', () => {
    expect(G.showGameHist(g4)).toStrictEqual("  1. White b2 to b3, Black b7 to b5\n  2. White d2 to d4");
});


test('updateGame', () => {
    let g2 = G.updateGame(g1, new RegularMove(new Field(2,2), new Field(2,4)))
    expect(g2.color).toBe('Black')
    expect(g2.board['b2']).toBe(undefined)
    expect(g2.board['b4'].show()).toBe('p')
});

test('isEnPassantCapture', () => {
    expect(G.isEnPassantCapture(g1, new Field(2,2), new Field(2,4))).toBe(false)
    let g2 = G.updateGame(g1, new RegularMove(new Field(2,2), new Field(2,4)))
    let g3 = G.updateGame(g2, new RegularMove(new Field(7,7), new Field(7,5)))
    let g4 = G.updateGame(g3, new RegularMove(new Field(2,4), new Field(2,5)))
    let g5 = G.updateGame(g4, new RegularMove(new Field(7,5), new Field(7,4)))
    let g6 = G.updateGame(g5, new RegularMove(new Field(6,2), new Field(6,4)))
    let g7 = G.updateGame(g6, new RegularMove(new Field(7,4), new Field(6,3)))
    expect(G.isEnPassantCapture(g6, new Field(7,4), new Field(6,3))).toBe(true)
    expect(G.isEnPassantCapture(g7, new Field(2,5), new Field(3,6))).toBe(false)
});


test('nextGamesAfterPawnEnPassantMoves', () => {
    expect(G.nextGamesAfterPawnEnPassantMoves(g1, new Field(2,2), new Figure('Pawn', 'White'))).toStrictEqual([])
    let g2 = G.updateGame(g1, new RegularMove(new Field(2,2), new Field(2,4)))
    let g3 = G.updateGame(g2, new RegularMove(new Field(7,7), new Field(7,5)))
    let g4 = G.updateGame(g3, new RegularMove(new Field(2,4), new Field(2,5)))
    let g5 = G.updateGame(g4, new RegularMove(new Field(7,5), new Field(7,4)))
    let g6 = G.updateGame(g5, new RegularMove(new Field(6,2), new Field(6,4)))
    let g7 = G.updateGame(g6, new RegularMove(new Field(7,4), new Field(6,3)))
    expect(G.nextGamesAfterPawnEnPassantMoves(g6, new Field(7,4), new Figure('Pawn', 'White')).length).toBe(0)
    expect(G.nextGamesAfterPawnEnPassantMoves(g6, new Field(7,4), new Figure('Pawn', 'Black')).length).toBe(1)
    expect(G.nextGamesAfterPawnEnPassantMoves(g7, new Field(2,5), new Figure('Pawn', 'White')).length).toBe(0)
});


test('nextGamesAfterPawnRegularAndPromotionMoves', () => {
    expect(G.nextGamesAfterPawnRegularAndPromotionMoves(g1, new Field(2,2), new Figure('Pawn', 'White')).length).toBe(2)
});

test('nextGamesAfterFigureMoves', () => {
    expect(G.nextGamesAfterFigureMoves(g1, new Field(2,1), new Figure('Knight', 'White')).length).toBe(2)
    expect(G.nextGamesAfterFigureMoves(g1, new Field(2,1), new Figure('Rook', 'White')).length).toBe(0)
    expect(G.nextGamesAfterFigureMoves(g1, new Field(2,2), new Figure('Queen', 'White')).length).toBe(11)
    expect(G.nextGamesAfterFigureMoves(g1, new Field(2,2), new Figure('King', 'White')).length).toBe(3)
});

test('makeMove', () => {
    expect(G.makeMove(g1, new Field(2,2), new Field(2,3), undefined)).toBeInstanceOf(G.OngoingGame)
    expect(G.makeMove(g1, new Field(2,2), new Field(2,4), undefined)).toBeInstanceOf(G.OngoingGame)
    expect(G.makeMove(g1, new Field(2,2), new Field(2,5), undefined)).toBe(undefined)
});

