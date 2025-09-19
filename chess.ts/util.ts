/*
  Utilities
*/

export function takeWhile<A>(f: (A) => boolean, lst: A[]): A[] {
    let result: A[] = []
    for (let a of lst) {
        if (f(a)) result.push(a)
        else break;
    }
    return result;
}

export function dropWhile<A>(f: (A) => boolean, lst: A[]): A[] {
    let result: A[] = []
    for (let a of lst) result.push(a)
    for (let a of lst) {
        if (f(a)) result.shift()
        else break;
    }
    return result;
}

