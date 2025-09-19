import { expect, test } from '@jest/globals'
import { Figure } from './figure'
import { Field } from './field'
import { rookMovess, bishopMovess, queenMovess, knightMovess, kingMovess,
       showFieldss, figureTargetss } from './figuremoves'

test('game', () => {
    expect(showFieldss(figureTargetss(new Figure('Rook','White'), new Field(3,4), false)).toString()).toBe(
        [
            ['d4','e4','f4','g4','h4'],
            ['b4','a4'],
            ['c5','c6','c7','c8'],
            ['c3','c2','c1']
        ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Bishop','White'), new Field(2,2), false)).toString()).toBe(
        [
            ['c3','d4','e5','f6','g7','h8'],
            ['c1'],
            ['a3'],
            ['a1']
        ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Queen','Black'), new Field(2,2), false)).toString()).toBe(
        [
            [ 'c2', 'd2', 'e2', 'f2', 'g2', 'h2' ],
            [ 'a2' ],
            [ 'b3', 'b4', 'b5', 'b6', 'b7', 'b8' ],
            [ 'b1' ],
            [ 'c3', 'd4', 'e5', 'f6', 'g7', 'h8' ],
            [ 'c1' ],
            [ 'a3' ],
            [ 'a1' ]
        ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('King','Black'), new Field(2,1), false)).toString()).toBe(
        [
            [ 'c1' ], [ 'a1' ],
            [ 'b2' ], [],
            [ 'c2' ], [],
            [ 'a2' ], []
        ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Knight','Black'), new Field(2,1), false)).toString()).toBe(
        [ [ 'c3' ], [ 'd2' ], [ 'a3' ], [], [], [], [], [] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','White'), new Field(2,2), false)).toString()).toBe(
        [ [ 'b3', 'b4' ] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','White'), new Field(2,3), false)).toString()).toBe(
        [ [ 'b4' ] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','White'), new Field(2,2), true)).toString()).toBe(
        [ [ 'c3' ], [ 'a3' ] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','Black'), new Field(2,7), false)).toString()).toBe(
        [ [ 'b6', 'b5' ] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','Black'), new Field(2,6), false)).toString()).toBe(
        [ [ 'b5' ] ].toString())
    
    expect(showFieldss(figureTargetss(new Figure('Pawn','Black'), new Field(2,7), true)).toString()).toBe(
        [ [ 'c6' ], [ 'a6' ] ].toString())
})

