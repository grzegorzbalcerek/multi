import { Field } from './field'
import { Figure } from './figure'

type Move = [number,number]

/*
  Sequences of relative figure positions for rook moves.
*/
export function rookMovess(): Move[][] {
    return [
        [[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0]],
        [[-1,0],[-2,0],[-3,0],[-4,0],[-5,0],[-6,0],[-7,0]],
        [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]],
        [[0,-1],[0,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]]
    ];
}

/*
  Sequences of relative figure positions for bishop moves.
*/
export function bishopMovess(): Move[][] {
    return [
        [[1,1],[2,2],[3,3],[4,4],[5,5],[6,6],[7,7]],
        [[1,-1],[2,-2],[3,-3],[4,-4],[5,-5],[6,-6],[7,-7]],
        [[-1,1],[-2,2],[-3,3],[-4,4],[-5,5],[-6,6],[-7,7]],
        [[-1,-1],[-2,-2],[-3,-3],[-4,-4],[-5,-5],[-6,-6],[-7,-7]]
    ];
}

/*
  Sequences of relative figure positions for queen moves.
*/
export function queenMovess(): Move[][] {
    return rookMovess().concat(bishopMovess());
}

/*
  Sequences of relative figure positions for knight moves.
*/
export function knightMovess(): Move[][] {
    return [[[1,2]],[[2,1]],[[-1,2]],[[2,-1]],[[-1,-2]],[[-2,-1]],[[1,-2]],[[-2,1]]];
}

/*
  Sequences of relative figure positions for king moves.
*/
export function kingMovess(): Move[][] {
    return queenMovess().map(moves => moves.slice(0,1));
}

/*
  Choose the sequences of relative figure positions
  based on the figure position, type, color,
  and whether the move is a capture move or not.
*/
export function figureMovess({figureType, figureColor}: Figure, {row}: Field, capture: Boolean): Move[][] {
    if (figureType === 'Rook') return rookMovess();
    else if (figureType === 'Bishop') return bishopMovess();
    else if (figureType === 'Queen') return queenMovess();
    else if (figureType === 'Knight') return knightMovess();
    else if (figureType === 'King') return kingMovess();
    else if (figureType === 'Pawn' && figureColor === 'White' && row === 2 && !capture) return [[[0,1],[0,2]]];
    else if (figureType === 'Pawn' && figureColor === 'White' && !capture) return [[[0,1]]];
    else if (figureType === 'Pawn' && figureColor === 'White' && capture) return [[[1,1]],[[-1,1]]];
    else if (figureType === 'Pawn' && figureColor === 'Black' && row === 7 && !capture) return [[[0,-1],[0,-2]]];
    else if (figureType === 'Pawn' && figureColor === 'Black' && !capture) return [[[0,-1]]];
    else if (figureType === 'Pawn' && figureColor === 'Black' && capture) return [[[1,-1]],[[-1,-1]]];
}

export function figureTargetss(figure: Figure, field: Field, capture: Boolean): Field[][] {
    return figureMovess(figure, field, capture).map(moves =>
        field.relativeFields(moves).filter(target => target.isValid()));
}

export function showFieldss(fieldss: Field[][]): String[][] {
    return fieldss.map(targets => targets.map(target => target.show()));
}

