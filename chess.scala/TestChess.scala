package chess

import zio.test.TestAspect.{jvmOnly, silent}
import zio.test.Assertion.{equalTo, isLessThan, isSome}
import zio.test.{DefaultRunnableSpec, assert}

object TestChess extends DefaultRunnableSpec {
  override def spec =
    suite("Chess test suite")(
      TestColor.spec,
      TestField.spec,
      TestFigure.spec,
      TestFigureMoves.spec,
      TestBoard.spec,
      TestRank.spec,
      TestGame.spec,
      TestComputerPlayer.spec
    )
}
