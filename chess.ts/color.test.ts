import { expect, test } from '@jest/globals'
import { otherColor, colorRow } from './color'

test('otherColor', () => {
    expect(otherColor('White')).toBe('Black')
    expect(otherColor('Black')).toBe('White')
})

test('colorRow', () => {
    expect(colorRow('White',1)).toBe(1)
    expect(colorRow('White',2)).toBe(2)
    expect(colorRow('Black',1)).toBe(8)
    expect(colorRow('Black',2)).toBe(7)
})

