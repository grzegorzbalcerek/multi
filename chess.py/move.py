from dataclasses import dataclass

from field import Field
from figure import Figure


@dataclass
class Move:
    frm: Field
    to: Field


@dataclass
class RegularMove(Move):
    pass


@dataclass
class PromotionMove(Move):
    figure: Figure


@dataclass
class EnPassantMove(Move):
    captured: Field


@dataclass
class CastlingMove(Move):
    rook_from: Field
    rook_to: Field
