{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

{-
ghc Compositionality.hs
Compositionality -w %W% -S compositionality1 -o compositionality1.svg
Compositionality -w %W% -S compositionality2 -o compositionality2.svg
Compositionality -w %W% -S compositionality3 -o compositionality3.svg
Compositionality -w %W% -S compositionality4 -o compositionality4.svg
-}

import System.Random
import Diagrams.Prelude
import Diagrams.Backend.SVG.CmdLine
import Diagrams.TwoD.Vector
import Diagrams.TwoD.Arrow
import Diagrams.TwoD.Arrowheads

main = mainWith (diagrams $ mkStdGen 12345678)

diagrams :: StdGen -> [(String, Diagram B)]
diagrams g =
  [ ("compositionalityA",compositionalityA)
  , ("compositionalityAmany",compositionalityAmany g 300 compositionalityA)
  , ("compositionalityABCD",compositionalityABCD)
  , ("compositionalityB",compositionalityB)
  , ("compositionalityB123",compositionalityB123)
  ]

makeDiagram spec = position $ map (\(x,y,d) -> (p2 (x,y),d)) spec
boxL w h label = text label # fontSizeL 6 <> rect w h # fc yellow # named label
objectI = circle 1 # lw none
boxC color w h label = text label # fontSizeL 6 <> rect w h # fc color # named label

compositionalityA = (makeDiagram
  [ (0,0, boxL 60 40 "A")
  , (-50,0, objectI)
  , (50,0, objectI)
  ])
  # frame 4

compositionalityAmany _ 0 d = d
compositionalityAmany g n d =
  let (w, g1) = randomR (2, 4) g
      (h, g2) = randomR (2, 4) g1
      (x, g3) = randomR (-28, 28) g2
      (y, g4) = randomR (-18, 18) g3
      (c, g5) = randomR (0, 4) g4
      color = [red,cyan,green,blue,magenta] !! c
  in
    if (x <= 5 && x >= (-5) && y <= 5 && y >= (-5))
    then
      compositionalityAmany g5 n d
    else
      compositionalityAmany g5 (n-1) $ (makeDiagram [ (x, y, boxC color w h "") ]) <> d

compositionalityABCD = (makeDiagram
  [ (20,0, boxC red 15 15 "D")
  , (-15,10, boxC orange 20 15 "B")
  , (-15,-10, boxC magenta 10 10 "C")
  , (0,0, boxL 60 40 "A")
  , (-50,0, objectI)
  , (50,0, objectI)
  ])
  # connectOutside' (def & arrowHead .~ noHead) "D" "B"
  # connectOutside' (def & arrowHead .~ noHead) "D" "C"
  # connectOutside' (def & arrowHead .~ noHead) "C" "B"
  # frame 4

compositionalityB = (makeDiagram
  [ (0,0, boxC orange 60 45 "B")
  , (-50,0, objectI)
  , (50,0, objectI)
  ])
  # frame 4

compositionalityB123 = (makeDiagram
  [ (20,10, boxC brown 15 15 "B1")
  , (-15,10, boxC green 20 15 "B2")
  , (-15,-10, boxC blue 10 10 "B3")
  , (0,0, boxC orange 60 45 "B")
  , (-50,0, objectI)
  , (50,0, objectI)
  ])
  # connectOutside' (def & arrowHead .~ noHead) "B1" "B2"
  # connectOutside' (def & arrowHead .~ noHead) "B2" "B3"
  # frame 4

