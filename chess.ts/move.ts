import { Field } from './field'
import { Figure } from './figure'

export class RegularMove {
    from: Field;
    to: Field;

    constructor(f: Field, t: Field) {
        this.from = f;
        this.to = t;
    }
}

export class PromotionMove {
    from: Field;
    to: Field;
    figure: Figure;

    constructor(f: Field, t: Field, fi: Figure) {
        this.from = f;
        this.to = t;
        this.figure = fi;
    }
}

export class EnPassantMove {
    from: Field;
    to: Field;
    captured: Field;

    constructor(f: Field, t: Field, c: Field) {
        this.from = f;
        this.to = t;
        this.captured = c;
    }
}

export class CastlingMove {
    from: Field;
    to: Field;
    rookFrom: Field;
    rookTo: Field;

    constructor(f: Field, t: Field, rf: Field, rt: Field) {
        this.from = f;
        this.to = t;
        this.rookFrom = rf;
        this.rookTo = rt;
    }
}

export type Move = RegularMove | PromotionMove | EnPassantMove | CastlingMove

