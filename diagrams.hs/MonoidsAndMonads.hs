{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

import System.Environment

import Diagrams.Prelude
import Diagrams.Backend.SVG.CmdLine
import Diagrams.TwoD.Vector
import Diagrams.TwoD.Arrow
import Diagrams.TwoD.Arrowheads

main = mainWith diagram

diagram :: Diagram B
diagram = (makeDiagram
  [ (-75,0, objectL "A")
  , (-25,0, objectL "B")
  , (25,0, objectL "C")
  , (75,0, objectL "D")
  , (-150,0, objectI)
  , (150,0, objectI)
  , (0,55, text "Monoids and Monads" # fontSizeL 12)
  , (0,-40, text "Grzegorz Balcerek" # fontSizeL 8)
  ])
  # connectOutside' arrowDef "B" "C" 
  # lc black
  # connectOutside' arrowDef "A" "B"
  # connectPerim' (arrowArc (-45)) "B" "D" (30 @@ deg) (150 @@ deg)
  # connectPerim' (arrowArc (-75) & shaftStyle %~ lc blue)
       "A" "D" (60 @@ deg) (120 @@ deg)
  # connectPerim' (arrowArc (-75) & shaftStyle %~ dashingG [4,4] 0)
       "A" "D" (60 @@ deg) (120 @@ deg)
  # lc red
  # connectOutside' arrowDef "C" "D"
  # connectPerim' (arrowArc 45) "A" "C" (-30 @@ deg) (210 @@ deg)
  # lc blue
  # frame 5

makeDiagram spec = position $ map (\(x,y,d) -> (p2 (x,y),d)) spec
objectL label = text label # fontSizeL 6 <> circle 5 # fc yellow # named label
objectI = circle 1 # lw none
arrowDef =  def & arrowTail .~ lineTail
arrowArc n = arrowDef & arrowShaft .~ arc xDir (n @@ deg)

