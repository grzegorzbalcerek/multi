import { expect, test } from '@jest/globals'
import { startingBoard, updateBoard, isFieldEmpty, freeDestinations, hasFigureOfColor, findColorFigureFields } from './board'
import { RegularMove } from "./move"
import { Field } from "./field"

test('updateBoard', () => {
    expect(startingBoard['a1'].show()).toBe('r')
    expect(startingBoard['b2'].show()).toBe('p')
    expect(startingBoard['b4']).toBe(undefined)
    expect(startingBoard['c2'].show()).toBe('p')
    expect(startingBoard['d3']).toBe(undefined)
    expect(startingBoard['h8'].show()).toBe('R')
    
    let a2_a4 = new RegularMove(new Field(2,2),new Field(2,4))
    expect(updateBoard(startingBoard,a2_a4)['b4'].show()).toBe('p')
    expect(updateBoard(startingBoard,a2_a4)['b2']).toBe(undefined)
})

test('isFieldEmpty', () => {
    expect(isFieldEmpty(startingBoard, new Field(1,1))).toBe(false)
    expect(isFieldEmpty(startingBoard, new Field(3,3))).toBe(true)
});

test('hasFigureOfColor', () => {
    expect(hasFigureOfColor(startingBoard, new Field(4,4), 'White')).toBe(false)
    expect(hasFigureOfColor(startingBoard, new Field(2,2), 'White')).toBe(true)
    expect(hasFigureOfColor(startingBoard, new Field(7,7), 'White')).toBe(false)
    expect(hasFigureOfColor(startingBoard, new Field(8,8), 'White')).toBe(false)
    expect(hasFigureOfColor(startingBoard, new Field(4,4), 'Black')).toBe(false)
    expect(hasFigureOfColor(startingBoard, new Field(2,2), 'Black')).toBe(false)
    expect(hasFigureOfColor(startingBoard, new Field(7,7), 'Black')).toBe(true)
    expect(hasFigureOfColor(startingBoard, new Field(8,8), 'Black')).toBe(true)
});

test('freeDestinations', () => {
    expect(freeDestinations(startingBoard, [[new Field(4,4), new Field(3,3), new Field(2,2), new Field(1,1)]])).toStrictEqual([new Field(4,4), new Field(3,3)])
    expect(freeDestinations(startingBoard, [[new Field(4,3), new Field(4,2)], [new Field(4,4), new Field(3,3), new Field(2,2), new Field(1,1)]])).toStrictEqual([new Field(4,3), new Field(4,4), new Field(3,3)])
});

test('findColorFigureFields', () => {
    expect(findColorFigureFields(startingBoard, [[new Field(4,4), new Field(3,3), new Field(2,2), new Field(1,1)]], 'Black')).toStrictEqual([])
    expect(findColorFigureFields(startingBoard, [[new Field(4,4), new Field(3,3), new Field(2,2), new Field(1,1)]], 'White')).toStrictEqual([new Field(2,2)])
    expect(findColorFigureFields(startingBoard, [[new Field(4,3), new Field(4,2)], [new Field(4,4), new Field(3,3), new Field(2,2), new Field(1,1)]], 'White')).toStrictEqual([new Field(4,2), new Field(2,2)])
});

