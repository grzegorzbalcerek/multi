/*
  The 'Color' type represents one of the two colors ('Black' or 'White')
  used in the game of Chess.
*/
export type Color = 'White' | 'Black'

/*
  The 'other' method returns the opposite color.
*/
export function otherColor(color: Color): Color {
    switch(color) {
    case 'White': return 'Black';
    case 'Black': return 'White';
    }
}

export function colorRow(color: Color, n: number): number {
    switch(color) {
    case 'White': return n;
    case 'Black': return 9 - n;
    }
}
