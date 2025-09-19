import { expect, test } from '@jest/globals'
import * as U from './util'

test('takeWhile', () => {
    expect(U.takeWhile(x => true, [])).toStrictEqual([]);
    expect(U.takeWhile(x => true, [1,2,5,4])).toStrictEqual([1,2,5,4]);
    expect(U.takeWhile(x => x < 5, [1,2,5,4])).toStrictEqual([1,2]);
});

test('dropWhile', () => {
    expect(U.dropWhile(x => true, [])).toStrictEqual([]);
    expect(U.dropWhile(x => true, [1,2,5,4])).toStrictEqual([]);
    expect(U.dropWhile(x => x < 5, [1,2,5,4])).toStrictEqual([5,4]);
});

