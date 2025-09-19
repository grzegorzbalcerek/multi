import { Color, colorRow } from './color'

/*
  The game of chess is played on a board with 64 fields.
  The board has the shape of a square with eight rows — from 1 to 8
  — and eight columns — from `a` to `h`.
  The 'Field' represents a board field.
  It has members representing the column and the row —
  the field coordinates on the chess board.
  Valid fields have coordinates in the range between 1 and 8.
*/
export class Field {
    col: number;
    row: number;

    /*
      Construct a field
    */
    constructor(c: number, r: number) {
        this.col = c;
        this.row = r;
    }

    /*
      Shows field coordinates as a pair of characters:
      a letter representing the column and a number representing the row.
    */
    show() {
        return String.fromCharCode(96+this.col) + this.row;
    }

    /*
      Returns a new field with coordinates moved
      by the given number of rows and columns relative to the original field.
    */
    relative([col,row]: [number,number]) {
        return new Field(this.col + col, this.row + row);
    }

    /*
      Returns fields with coordinates moved by the given moves.
    */
    relativeFields(moves: [number,number][]) {
        return moves.map(move => this.relative(move))
    }

    /*
      Returns a boolean value indicating
      whether the given field belongs to the last row from
      the point of view of a player.
    */
    isLastRow(color: Color) {
        return this.row === colorRow(color, 8)
    }

    /*
      Returns a boolean value indicating
      whether the field has valid coordinates, that is
      whether it belongs to the board.
    */
    isValid() {
        return this.col >= 1 && this.col <= 8 && this.row >= 1 && this.row <= 8;
    }
}

/*
  Construct the Field based on its 2-character coordinates.
*/
export function readField(input: String): Field {
    return new Field(
        input.toLowerCase().charCodeAt(0) - 96,
        input.charCodeAt(1) - 48);
}

