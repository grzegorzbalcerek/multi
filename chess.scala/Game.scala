package chess
import java.lang.System.lineSeparator
import Board._
import FigureMoves._

abstract sealed class Game {
  val color: Color
  val board: Board

  def figurePositionForbidsCastling(castlingColor: Color, rookFrom: Int): Boolean
  def boards: List[Board]

  /**
    * Verifies if the given field is empty.
    */
  def isFieldEmpty(field: Field): Boolean =
    !board.contains(field)

  /**
    * Returns free fields onto which the figure may be moved.
    */
  def freeDestinations(fieldss: Seq[Seq[Field]]) =
    fieldss.flatMap(fields => fields.takeWhile(isFieldEmpty))

  /**
    * Returns fields occupied by the enemy figures
    * (including the case when that figure is the King)
    * onto which the figure may be moved.
    */
  def captureDestinations(fieldss: Seq[Seq[Field]]) = {
    def hasEnemyFigure(field: Field) =
      board.get(field).map(_.figureColor) == Some(color.other)
    fieldss.flatMap(_.dropWhile(isFieldEmpty).take(1).filter(hasEnemyFigure))
  }

  /**
    * Returns fields occupied by the same color figures
    * (including the case when that figure is the King)
    * onto which the figure might be moved (if the field
    * was taken by an enemy figure).
    */
  def defendedDestinations(fieldss: Seq[Seq[Field]]) = {
    def hasSameColorFigure(field: Field) =
      board.get(field).map(_.figureColor) == Some(color)
    fieldss.flatMap(_.dropWhile(isFieldEmpty).take(1).filter(hasSameColorFigure))
  }

  /**
    * Returns a new game, updated with a move.
    */
  def updated(move: Move) =
    new OngoingGame(color.other,
      Board.updateBoard(board, move),
      this,
      move)

  /**
    * Verifies if the enemy King is under check.
    */
  def isOtherKingUnderCheck: Boolean = {
    def isKingOnBoard(g: Game) = g.board.values.exists(fig => fig == Figure(King,color.other))
    !nextGames.forall(isKingOnBoard)
  }

  /**
    * Verifies if the King of the player who is about to make a move is under check.
    */
  def isKingUnderCheck: Boolean =
    new OngoingGame(color.other, board, this,
      RegularMove(Field(0,0),Field(0,0))).isOtherKingUnderCheck

  /**
    * Verifies the conditions of when the castling move is permitted:
    * whether the King and the Rook are on their initial positions,
    * whether they were there from the begining of the game,
    * whether the fields between them are free and
    * whether the field to be passed by the King is checked or not.
    * If the given castling move is permitted, the method returns a one-element sequence.
    * Otherwise it returns an empty sequence.
    */
  def castling(kingTo: Int, rookFrom: Int, rookTo: Int, otherCol: Int) = {
    val row = color.firstRow
    if (!figurePositionForbidsCastling(color, rookFrom) &&
        board.get(Field(rookTo,row)) == None &&
        board.get(Field(kingTo,row)) == None &&
        board.get(Field(otherCol,row)) == None &&
       !updated(RegularMove(Field(4,row),Field(rookTo,row))).isOtherKingUnderCheck)
      Seq(updated(CastlingMove(Field(4,row), Field(kingTo,row),
        Field(rookFrom,row), Field(rookTo,row))))
    else Seq()
  }

  /**
    * Verifies if the en passant capture move is possible.
    */
  def isEnPassantCapture(from: Field, to: Field) = this match {
    case GameStart => false
    case g:OngoingGame =>
      g.board.get(g.lastMove.to) == Some(Figure(Pawn,color.other)) &&
      g.lastMove.to == Field(to.col, from.row) &&
      g.lastMove.from == Field(to.col, from.row + 2*(to.row-from.row))
  }

  /**
    * Returns next games after possible next moves moves (including those
    * moves after which the King is checked).
    * The code itereates over all figures that have the same color as
    * the color of the next move. The 'g' value contains sequences of game states
    * corresponding to the possible next moves of the given figure.
    * Figure moves depend on its kind. The Rook, the Knight, the Queen, the Bishop
    * and the King are treated in a similar way, except for the King, for which
    * the castling moves are included as well.
    * Potentially there are two possible castling moves.
    * Each of them is handled by a call to the 'castling' method.
    * The most complex case handled by the mthod is the case of the Pawn moves.
    * The Pawn may move forward onto a free field or forward and left or right onto
    * a field occupied by an enemy figure. In both cases, if the destination field
    * lies on the last row, the set of possible moves includes the possible
    * promotions to other figures. In addition to that, the Pawn may make the so
    * called en passant capture, which consists of moving the Pawn forward and left
    * or right onto a free field which has been passed-by by an enemy Pawn in the
    * previous move.
    */
  def nextGames =
    board.iterator.
      filter{ case (_, figure) => figure.figureColor == color }.
      flatMap{ case (from, figure) => nextGamesAfterMoves(from, figure) }

def nextGamesAfterMoves(from: Field, figure: Figure): Seq[OngoingGame] =
  if (figure.figureType == Pawn) {
    nextGamesAfterPawnRegularAndPromotionMoves(from, figure) ++ nextGamesAfterPawnEnPassantMoves(from, figure)
  } else
    nextGamesAfterFigureMoves(from, figure)

def nextGamesAfterFigureMoves(from: Field, figure: Figure): Seq[OngoingGame] = {
  val fieldss = figureMoves(figure, from, false)
  val gamesAfterRegularMoves =
    (freeDestinations(fieldss) ++ captureDestinations(fieldss)).
      map(to => updated(RegularMove(from, to)))
  val gamesAfterCastlingMoves =
    if (figure.figureType == King) castling(3, 1, 4, 2) ++ castling(7, 8, 6, 7)
    else Seq()
  gamesAfterRegularMoves ++ gamesAfterCastlingMoves
  }

def nextGamesAfterPawnRegularAndPromotionMoves(from: Field, figure: Figure): Seq[OngoingGame] =
  (captureDestinations(figureMoves(figure, from, true)) ++
    freeDestinations(figureMoves(figure, from, false))).
    flatMap((to: Field) =>
      if (to.isLastRow(color))
        Seq(Figure(Queen, color), Figure(Rook, color), Figure(Bishop, color), Figure(Knight, color)).
          map(figure => updated(PromotionMove(from, to, figure)))
      else Seq(updated(RegularMove(from, to))))

def nextGamesAfterPawnEnPassantMoves(from: Field, figure: Figure): Seq[OngoingGame] =
  freeDestinations(figureMoves(figure, from, true)).
    filter(isEnPassantCapture(from, _)).map(to =>
    updated(EnPassantMove(from, to, Field(to.col, from.row))))

  /**
    * Filters out the next games in which the king is under check.
    */
  def validGames = nextGames.filter{ g => !g.isOtherKingUnderCheck }

  /**
    * Verifies if the game is over.
    * The following end game conditions are handled:
    * + after every possible move the King is under check,
    * + only the two Kings are left on the board,
    * + only the two Kings, one Bishop and one Knight are left on the board,
    * + only the two Kings and two Knights of the same color are left on the board,
    * + the same position occurred three times.
    */
  def isGameFinished: Boolean =
    nextGames.forall(_.isOtherKingUnderCheck) ||
    Set[Set[Figure]](Set(Figure(King,White),Figure(King,Black)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Bishop,White)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Bishop,Black)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,White)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,Black)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,White),Figure(Knight,White)),
                     Set(Figure(King,White),Figure(King,Black),Figure(Knight,Black),Figure(Knight,Black))).
      contains(board.values.toSet) ||
      !boards.groupBy(identity).values.toSet.filter(_.size >= 3).isEmpty

  /**
    * Returns an option with the color of the game winner.
    */
  def winner: Option[Color] = if (isGameFinished && isKingUnderCheck)
    Some(color.other) else None

  /**
    * Returns an option with a new game state after moving a figure.
    */
  def move(from: Field, to: Field, promotion: Option[Figure] = None) = {
    def isMatching(game: OngoingGame) =
      game.lastMove.from == from &&
      game.lastMove.to == to &&
      (game.lastMove match {
        case PromotionMove(_,_,prom) => Some(prom) == promotion
        case _ => promotion == None })
    validGames.filter(isMatching).toList.headOption
  }
}

object GameStart extends Game {
  override val color = White
  override val board = startingBoard
  override def toString = "White to begin:\n"+showBoardU(board)

  override def figurePositionForbidsCastling(castlingColor: Color, rookFrom: Int): Boolean = false
  def boards: List[Board] = List(startingBoard)
}

final class OngoingGame(
  override val color: Color,
  override val board: Board,
  val prev: Game,
  val lastMove: Move
) extends Game {
  override def toString = "Last move: "+color.other+" "+
    lastMove.from+" to "+lastMove.to+lineSeparator+showBoardU(board)
  def figurePositionForbidsCastling(castlingColor: Color, rookFrom: Int) =
    prev.figurePositionForbidsCastling(castlingColor.other, rookFrom) ||
      (castlingColor == color &&
        (board.get(Field(4,color.firstRow)) != Some(Figure(King,color)) ||
          board.get(Field(rookFrom,color.firstRow)) != Some(Figure(Rook,color))))
  def boards: List[Board] = board :: boards

}
