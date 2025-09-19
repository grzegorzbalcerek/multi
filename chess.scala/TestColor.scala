package chess

import zio.test.TestAspect.{jvmOnly, silent}
import zio.test.Assertion.{equalTo, isLessThan, isSome}
import zio.test.{DefaultRunnableSpec, assert}

object TestColor extends DefaultRunnableSpec {
  override def spec =
    suite("Color test suite")(
      test("other") {
        assert(White.other)(equalTo(Black)) && assert(Black.other)(equalTo(White))
      },
      test("first row") {
        assert(White.firstRow)(equalTo(1)) && assert(Black.firstRow)(equalTo(8))
      }
    )
}
