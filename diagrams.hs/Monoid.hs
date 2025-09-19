{-# LANGUAGE NoMonomorphismRestriction #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE TypeFamilies #-}

import Diagrams.Prelude
import Diagrams.Backend.SVG.CmdLine
import Diagrams.TwoD.Vector
import Diagrams.TwoD.Arrow
import Diagrams.TwoD.Arrowheads

main = mainWith diagrams

diagrams :: [(String, Diagram B)]
diagrams =
  [ ("algebraMonoid",algebraMonoid)
  , ("monoid1",monoid1)
  , ("monoid2",monoid2)
  , ("monoid3",monoid3)
  , ("monoid10",monoid10)
  , ("monoid12",monoid12)
  , ("clock1",clock1)
  , ("clock347",clock3 3 4 7)
  , ("clock783",clock3 7 8 3)
  , ("clock9129",clock3 9 12 9)
  ]

makeDiagram spec = position $ map (\(x,y,d) -> (p2 (x,y),d)) spec

arrowM n = def & arrowTail .~ lineTail & arrowShaft .~ arc xDir (n @@ deg)
objectI = circle 1 # lw none
objectN name = circle 5 # fc yellow # lw thin # named name
label2 txt = text txt # fontSizeL 2

algebraMonoid = (makeDiagram
  [ (0,0, text "(A, a ⊕ a → a, e ∈ A)" # fontSizeL 10)
  , (0,-30, text "e ⊕ a = a" # fontSizeL 10)
  , (0,-50, text "a ⊕ e = a" # fontSizeL 10)
  , (0,-70, text "(a ⊕ a) ⊕ a = a ⊕ (a ⊕ a)" # fontSizeL 10)
  ])
  # frame 20

monoidBase = (makeDiagram
  [ (0,0, objectN "b")
  , (-65,44, objectI)
  , (65,44, objectI)
  ])
  # frame 4

addhourLabel h d =
  (d <> makeDiagram [(0,15.6 + (h*2.6), label2 ((if h == 12 then "id = " else "") ++ show (truncate h)))])

addhourArrow h d =
  d # connectPerim' (arrowM ((-1)*(239+29.9*(h**0.4)))) "b" "b" (110+(h*6) @@ deg) (70-(h*6) @@ deg)

monoid1 = foldr addhourArrow monoidBase [1]
monoid2 = foldr addhourArrow monoidBase [1,2]
monoid3 = foldr addhourArrow monoidBase [1..3]
monoid10 = foldr addhourArrow monoidBase [1..10]
monoid12' = foldr addhourArrow monoidBase [1..12]
monoid12 = foldr addhourLabel monoid12' [1..12]

clockPoints = rotateBy (1/24) $ polygon $ def & polyType .~ PolyRegular 12 1

clock n = 
  circle 11 <>
  (fromOffsets [r2 (8,0)] # rotateBy ((3-n)/12)) <>
  (mconcat $ zip (reverse[1..12]) clockPoints # map (\(h,v) -> atPoints [10 *^ v, 9 *^ v] [
   fromVertices [1 *^ v,2 *^ v] # strokeLine, text (show (1+(h+2) `mod` 12))]))

clock1 = atPoints [p2 (-30,12), p2 (30,-12)] (repeat objectI) <> clock 1

clock3 a b c = strutX 8 ||| clock a ||| strutX 8 |||
           text "+" # fontSizeL 8 |||
           strutX 8 ||| clock b ||| strutX 8 |||
           text "=" # fontSizeL 8 |||
           strutX 8 ||| clock c ||| strutX 8
