import { expect, test } from '@jest/globals'
import { Field, readField } from "./field"

test('game', () => {
    expect(new Field(1,1).show()).toBe('a1')
    expect(new Field(3,4).show()).toBe('c4')
    expect(readField('c4').col).toBe(3)
    expect(readField('c4').row).toBe(4)
    expect(readField('C4').col).toBe(3)
    expect(readField('C4').row).toBe(4)
    expect(new Field(3,4).relative([1,1]).col).toBe(4)
    expect(new Field(3,4).relative([1,1]).row).toBe(5)
    expect(new Field(3,4).relativeFields([[1,1],[3,4]])[0].col).toBe(4)
    expect(new Field(3,4).relativeFields([[1,1],[3,4]])[0].row).toBe(5)
    expect(new Field(3,4).relativeFields([[1,1],[3,4]])[1].col).toBe(6)
    expect(new Field(3,4).relativeFields([[1,1],[3,4]])[1].row).toBe(8)
    expect(readField('c4').isLastRow('Black')).toBe(false)
    expect(readField('d8').isLastRow('Black')).toBe(false)
    expect(readField('d8').isLastRow('White')).toBe(true)
    expect(readField('d8').isValid()).toBe(true)
    expect(readField('a0').isValid()).toBe(false)
    expect(readField('i8').isValid()).toBe(false)
    expect(readField('h9').isValid()).toBe(false)
})

