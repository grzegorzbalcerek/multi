import { Color } from "./color"

/*
  Represents chess figure types.
*/
export type FigureType = 'King' | 'Queen' | 'Rook' | 'Bishop' | 'Knight' | 'Pawn'

/*
  Represents a figure, which has a type and a color.
*/
export class Figure {

    figureType: FigureType;
    figureColor: Color;

    constructor(ft: FigureType, fc: Color) {
        this.figureType = ft;
        this.figureColor = fc;
    }

    /*
      Returns a one-character string representing the figure
    */
    show() {
        switch(this.figureColor) {
        case 'White':
            switch(this.figureType) {
            case 'King':   return 'k';
            case 'Queen':  return 'q';
            case 'Rook':   return 'r';
            case 'Bishop': return 'b';
            case 'Knight': return 'n';
            case 'Pawn':   return 'p';
            };
        case 'Black':
            switch(this.figureType) {
            case 'King':   return 'K';
            case 'Queen':  return 'Q';
            case 'Rook':   return 'R';
            case 'Bishop': return 'B';
            case 'Knight': return 'N';
            case 'Pawn':   return 'P';
            }
        }
    }
}

