{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

import System.Environment

import Diagrams.Prelude
import Diagrams.Backend.SVG.CmdLine
import Diagrams.TwoD.Vector
import Diagrams.TwoD.Arrow
import Diagrams.TwoD.Arrowheads

main = mainWith diagrams

diagrams :: [(String, Diagram B)]
diagrams =
  [ ("clock", clock )
  ]

makeDiagram spec = position $ map (\(x,y,d) -> (p2 (x,y),d)) spec
objectL label = text label # fontSizeL 6 <> circle 5 # fc yellow # named label
objectLL label = text label # fontSizeL 6 <> circle 10 # fc yellow # named label
objectI = circle 1 # lw none
label txt = text txt # fontSizeL 6
arrowDef =  def & arrowTail .~ lineTail & lengths .~ large
arrowArc n = arrowDef & arrowShaft .~ arc xDir (n @@ deg)
arrowDash = def & lengths .~ large & shaftStyle %~ dashingG [2,2] 0
boxL' n w h label = text label # fontSizeL n <> rect w h # named label
boxL = boxL' 5

clock =
  (clockDisplay # showEnvelope)
  ===
  (boxL' 1 5 2 "switch" ||| strutX 4 ||| boxL' 1 5 2 "mode")

clockDisplay =
  rect 12 4 # translateX 0.5 <>
  (strutX 4 ||| text "00:00" # fontSizeL 5 ||| strutX 4 ||| text "00" # fontSizeL 3 # translateY (-0.4))

