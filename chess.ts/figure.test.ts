import { expect, test } from '@jest/globals'
import { Figure } from './figure'

test('game', () => {
    expect(new Figure('King', 'White').show()).toBe('k')
})
