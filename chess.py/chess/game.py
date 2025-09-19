
from itertools import chain, dropwhile, takewhile
from board import starting_board, show_board, update_board
from color import Color
from field import Field
from figure import Figure, FigureType
from figure_moves import figure_moves
from move import Move, MoveType

class Game:

    
    def __init__(self, color, board, hist, last_move):
        self.color = color
        self.board = board
        self.hist = hist
        self.last_move = last_move


    def new():
        """
        Return a new game with initial state.

        >>> print(Game.new())
        White to begin:
         abcdefgh
        8RNBQKBNR8
        7PPPPPPPP7
        6........6
        5........5
        4........4
        3........3
        2pppppppp2
        1rnbqkbnr1
         abcdefgh
        """
        return Game(Color.White, starting_board(), [], None)

        
    def __str__(self):
        if self.last_move == None:
            return "White to begin:\n" + show_board(self.board)
        else:
            return "Last move: {} {} to {}\n{}".format(self.color.other(), self.last_move.frm, self.last_move.to, show_board(self.board))

        
    def __repr__(self):
        return str(self)

    
    def _has_enemy_figure(self, field):
        """
        >>> Game.new()._has_enemy_figure(Field(3,4))
        False

        >>> Game.new()._has_enemy_figure(Field(2,7))
        True

        >>> Game.new()._has_enemy_figure(Field(2,2))
        False
        """
        figure = self.board.get((field.col, field.row))
        if figure == None:
            return False
        else:
            return figure.figure_color == self.color.other()


    def capture_destinations(self, fieldss):
        """
        Returns fields occupied by the enemy figures
        (including the case when that figure is the King)
        onto which the figure may be moved.

        >>> Game.new().capture_destinations(figure_moves(Figure(FigureType.Rook, Color.White), Field(3,4), False))
        [c7]

        >>> Game.new().capture_destinations(figure_moves(Figure(FigureType.Bishop, Color.White), Field(3,4), False))
        [f7]
        """
        return list(chain(*map(lambda fields:
                        filter(self._has_enemy_figure, list(dropwhile(self.is_field_empty, fields))[:1]), fieldss)))



    def _has_same_color_figure(self, field):
        """
        >>> Game.new()._has_same_color_figure(Field(3,4))
        False

        >>> Game.new()._has_same_color_figure(Field(2,7))
        False

        >>> Game.new()._has_same_color_figure(Field(2,2))
        True
        """
        figure = self.board.get((field.col, field.row))
        if figure == None:
            return False
        else:
            return figure.figure_color == self.color


    def defended_destinations(self, fieldss):
        """
        Returns fields occupied by the same color figures
        (including the case when that figure is the King)
        onto which the figure might be moved (if the field
        was taken by an enemy figure).

        >>> Game.new().defended_destinations(figure_moves(Figure(FigureType.Rook, Color.White), Field(3,4), False))
        [c2]

        >>> Game.new().defended_destinations(figure_moves(Figure(FigureType.Bishop, Color.White), Field(3,4), False))
        [e2, a2]
        """
        return list(chain(*map(lambda fields:
                        filter(self._has_same_color_figure, list(dropwhile(self.is_field_empty, fields))[:1]), fieldss)))


    def updated(self, move):
        """
        Returns a new game, updated with a move.
        """
        return Game(self.color.other(), update_board(self.board, move), self.hist.append(self), move)


    def _castling(self, king_to, rook_from, rook_to, other_col):
        """
        Verifies the conditions of when the castling move is permitted:
        whether the King and the Rook are on their initial positions,
        whether they were there from the begining of the game,
        whether the fields between them are free and
        whether the field to be passed by the King is checked or not.
        If the given castling move is permitted, the method returns a one-element sequence.
        Otherwise it returns an empty sequence.
        """
        return [] #TODO
        #row = self.color.first_row()
        #if self.board.get((4,row)) == Figure(FigureType.King, color)) and
        #   self.board.get((rook_from,row)) == Figure(FigureType.Rook,color)) and
        #board.get(Field(rookTo,row)) == None &&
        #board.get(Field(kingTo,row)) == None &&
        #board.get(Field(otherCol,row)) == None &&
        #hist.forall(_.board.get(Field(4,row)) == Some(Figure(King,color))) &&
        #hist.forall(_.board.get(Field(rookFrom,row)) == Some(Figure(Rook,color))) &&
        #!updated(RegularMove(Field(4,row),Field(rookTo,row))).isOtherKingUnderCheck)
        # Seq(updated(CastlingMove(Field(4,row), Field(kingTo,row),
        #    Field(rookFrom,row), Field(rookTo,row))))
        # else Seq()

    
    def _next_games_for_figure(self, field, figure):
        """
        >>> 1
        1
        """
        if figure.figure_type == FigureType.Pawn:
            return []
        else:
            fieldss = figure_moves(figure, field, False)
            print(figure, field, fieldss, self.free_destinations(fieldss))
            games_after_regular_moves = map(
                lambda to: self.updated(Move(MoveType.RegularMove, field, to)),
                self.free_destinations(fieldss) + self.capture_destinations(fieldss))
            if figure.figure_type == FigureType.King:
                games_after_castling_moves = self._castling(3,1,4,2) + self._castling(7,8,6,7)
            else:
                games_after_castling_moves = []
            return list(games_after_regular_moves)

    
    def next_games(self):
        """
        Returns next games after possible next moves moves (including those
        moves after which the King is checked).
        The code itereates over all figures that have the same color as
        the color of the next move. The 'g' value contains sequences of game states
        corresponding to the possible next moves of the given figure.
        Figure moves depend on its kind. The Rook, the Knight, the Queen, the Bishop
        and the King are treated in a similar way, except for the King, for which
        the castling moves are included as well.
        Potentially there are two possible castling moves.
        Each of them is handled by a call to the 'castling' method.
        The most complex case handled by the mthod is the case of the Pawn moves.
        The Pawn may move forward onto a free field or forward and left or right onto
        a field occupied by an enemy figure. In both cases, if the destination field
        lies on the last row, the set of possible moves includes the possible
        promotions to other figures. In addition to that, the Pawn may make the so
        called en passant capture, which consists of moving the Pawn forward and left
        or right onto a free field which has been passed-by by an enemy Pawn in the
        previous move.

        >>> list(Game.new().next_games())
        """
        return list(chain(*map(
            lambda item: self._next_games_for_figure(Field(item[0][0], item[0][1]), item[1]),
            filter(
                lambda item: item[1].figure_color == self.color,
                self.board.items()))))
#      flatMap{ case (from, figure) => 
#        figure.figureType match {
#          case Pawn =>
#            val regularAndPromotionMoves =
#              (capture_destinations(figureMoves(figure,from,true))++
#                free_destinations(figureMoves(figure,from,false))).
#                flatMap(to =>
#                  if (to.isLastRow(color))
#                    Seq(Figure(Queen,color),Figure(Rook,color),Figure(Bishop,color),Figure(Knight,color)).
#                    map(figure => updated(PromotionMove(from,to,figure)))
#                  else Seq(updated(RegularMove(from,to))))
#            val enPassantMoves =
#              free_destinations(figureMoves(figure,from,true)).
#                filter(isEnPassantCapture(from,_)).map(to =>
#                  updated(EnPassantMove(from, to, Field(to.col,from.row))))
#            regularAndPromotionMoves ++ enPassantMoves
#          case _ => Seq.empty
#        }
#      }
#
#  def isOtherKingUnderCheck: Boolean = {
#    * Verifies if the enemy King is under check.
#    """
#    def isKingOnBoard(g: Game) = g.board.values.exists(fig => fig == Figure(King,color.other))
#    !nextGames.forall(isKingOnBoard)
#  }
#
#  def isKingUnderCheck: Boolean =
#    * Verifies if the King of the player who is about to make a move is under check.
#    """
#    new OngoingGame(color.other, board, this :: hist,
#      RegularMove(Field(0,0),Field(0,0))).isOtherKingUnderCheck
#
#
#  def isEnPassantCapture(from: Field, to: Field) = this match {
#    * Verifies if the en passant capture move is possible.
#    """
#    case GameStart => false
#    case g:OngoingGame =>
#      g.board.get(g.lastMove.to) == Some(Figure(Pawn,color.other)) &&
#      g.lastMove.to == Field(to.col, from.row) &&
#      g.lastMove.from == Field(to.col, from.row + 2*(to.row-from.row))
#  }
#
#
#  def validGames = nextGames.filter{ g => !g.isOtherKingUnderCheck }
#    * Filters out the next games in which the king is under check.
#    """
#
#  def isGameFinished: Boolean =
#    * Verifies if the game is over.
#    * The following end game conditions are handled:
#    * + after every possible move the King is under check,
#    * + only the two Kings are left on the board,
#    * + only the two Kings, one Bishop and one Knight are left on the board,
#    * + only the two Kings and two Knights of the same color are left on the board,
#    * + the same position occurred three times.
#    nextGames.forall(_.isOtherKingUnderCheck) ||
#    Set[Set[Figure]](Set(Figure(King,White),Figure(King,Black)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Bishop,White)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Bishop,Black)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,White)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,Black)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,White),Figure(Knight,White)),
#                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,Black),Figure(Knight,Black))).
#      contains(board.values.toSet) ||
#      !(board :: hist.map(_.board)).
#        groupBy(identity).values.toSet.filter(_.size >= 3).isEmpty
#
#  def winner: Option[Color] = if (isGameFinished && isKingUnderCheck)
#    * Returns an option with the color of the game winner.
#    """
#    Some(color.other) else None
#
#  def move(from: Field, to: Field, promotion: Option[Figure] = None) = {
#    * Returns an option with a new game state after moving a figure.
#    """
#    def isMatching(game: OngoingGame) =
#      game.lastMove.from == from &&
#      game.lastMove.to == to &&
#      (game.lastMove match {
#        case PromotionMove(_,_,prom) => Some(prom) == promotion
#        case _ => promotion == None })
#    validGames.filter(isMatching).toList.headOption
#  }
#}
#GameStart.isOtherKingUnderCheck // false
#GameStart.isKingUnderCheck // false
#GameStart.isGameFinished // false
#GameStart.winner // None
#GameStart.nextGames.size // 20
#GameStart.validGames.size // 20
#GameStart.move(Field(1,2),Field(1,5),None) // None
#val g1 = GameStart.move(Field(7,2),Field(7,4),None).get
#val g2 = g1.move(Field(5,7),Field(5,6),None).get
#val g3 = g2.move(Field(6,2),Field(6,4),None).get
#val g4 = g3.move(Field(4,8),Field(8,4),None).get
#g4.isOtherKingUnderCheck // false
#g4.isKingUnderCheck // true
#g4.isGameFinished // true
#g4.winner // Some(Black)
#g4.nextGames.size // 20
#g4.validGames.size // 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()

