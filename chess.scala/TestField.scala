package chess

import zio.test.TestAspect.{jvmOnly, silent}
import zio.test.Assertion.{equalTo, isLessThan, isSome}
import zio.test.{DefaultRunnableSpec, assert}

object TestField extends DefaultRunnableSpec {
  override def spec =
    suite("Field test suite")(
      test("toString") {
        assert(Field(1,1).toString)(equalTo("a1")) &&
          assert(Field(2,1).toString)(equalTo("b1")) &&
          assert(Field(2,3).toString)(equalTo("b3")) &&
          assert(Field(8,8).toString)(equalTo("h8"))
      },
      test("relative") {
        assert(Field(2,3).relative(1,1))(equalTo(Field(3,4))) &&
        assert(Field(2,3).relative(4,5))(equalTo(Field(6,8)))
      },
      test("isLastRow") {
        assert(Field(8,8).isLastRow(White))(equalTo(true)) &&
        assert(Field(7,8).isLastRow(White))(equalTo(true)) &&
        assert(Field(7,8).isLastRow(Black))(equalTo(false)) &&
        assert(Field(7,1).isLastRow(Black))(equalTo(true)) &&
        assert(Field(2,2).isLastRow(White))(equalTo(false))
      },
      test("isValid") {
        assert(Field(2,2).isValid)(equalTo(true)) &&
        assert(Field(0,2).isValid)(equalTo(false)) &&
        assert(Field(2,0).isValid)(equalTo(false)) &&
        assert(Field(2,9).isValid)(equalTo(false)) &&
        assert(Field(9,2).isValid)(equalTo(false))
      }
    )
}
