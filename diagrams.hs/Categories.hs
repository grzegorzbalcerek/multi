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
  [ ("category1",category1)
  , ("category2",category2)
  , ("category3",category3)
  , ("category4",category4)
  , ("category5",category5)
  , ("category6",category6)
  , ("categoryCompositionAssoc",categoryCompositionAssoc)
  , ("functionCompositionAssoc",functionCompositionAssoc)
  , ("kleisliCompositionAssoc",kleisliCompositionAssoc)
  , ("categoryCompositionId",categoryCompositionId)
  , ("functionCompositionId",functionCompositionId)
  , ("kleisliCompositionId",kleisliCompositionId)
  , ("option1",option1)
  , ("option2",option2)
  , ("optionKleisli",optionKleisli)
  , ("listKleisli",listKleisli)
  , ("monadKleisli",monadKleisli)
  , ("typesAndFunctions1",typesAndFunctions1)
  , ("typesAndFunctions2",typesAndFunctions2)
  , ("typesAndFunctions3",typesAndFunctions3)
  , ("typesAndFunctions4",typesAndFunctions4)
  , ("monoidKleisli",monoidKleisli)
  ]

makeDiagram spec = position $ map (\(x,y,d) -> (p2 (x,y),d)) spec
objectI = circle 1 # lw none
objectN name = circle 5 # fc yellow # lw thin # named name
objectI' t = circle 5 # lw none # named t
objectL label = text label # fontSizeL 6 <> circle 5 # fc yellow # named label
arrowDef =  def & arrowTail .~ lineTail & lengths .~ large
arrowArc n = arrowDef & arrowShaft .~ arc xDir (n @@ deg)
arrowSelf = arrowArc (-220)
arrowDash = def & lengths .~ large & shaftStyle %~ dashingG [2,2] 0
label' n txt = text txt # fontSizeL n
label = label' 6
boxL w h label = text label # fontSizeL 6 <> roundedRect w h h # fc yellow # named label
objectLL label = text label # fontSizeL 6 <> circle 10 # fc yellow # named label

category1 = (makeDiagram
  [ (-75,-30, objectI)
  , (-50,0, objectL "A")
  , (75,30, objectI)
  ])

category2 = ((makeDiagram
  [ (-50,17, label "id")
  , (-46,15, label' 4 "A")
  ]) <> category1)
  # connectPerim' arrowSelf "A" "A" (110 @@ deg) (70 @@ deg)

category3 = ((makeDiagram
  [ (-27,3, label "f")
  , (0,0, objectI' "B")
  ]) <> category2)
  # connectOutside' arrowDef "A" "B"

category4 = ((makeDiagram
  [ (0,0, objectL "B")
  , (0,17, label "id")
  , (4,15, label' 4 "B")
  ]) <> category3)
  # connectPerim' arrowSelf "B" "B" (110 @@ deg) (70 @@ deg)

category5 = ((makeDiagram
  [ (23,3, label "g")
  , (50,0, objectL "C")
  , (50,17, label "id")
  , (54,15, label' 4 "C")
  ]) <> category4)
  # connectPerim' arrowSelf "C" "C" (110 @@ deg) (70 @@ deg)
  # connectOutside' arrowDef "B" "C"

category6 = (makeDiagram
  [ (0,-20, label "g∘f")
  ]) <> category5 # connectPerim' (arrowArc 60) "A" "C" (-30 @@ deg) (210 @@ deg)

categoryLawsId a b c d idA f idf idD g gid = (makeDiagram
  [ (-90,-20, objectI)
  , (-70,17, label idA)
  , (-70,0, objectL a # named "A")
  , (-43,3, label f)
  , (-43,-4, label idf)
  , (-10,0, objectL b # named "B")
  , (10,0, objectL c # named "C")
  , (37,-4, label gid)
  , (37,3, label g)
  , (70,0, objectL d # named "D")
  , (70,17, label idD)
  , (90,20, objectI)
  ])
  # connectOutside' arrowDef "A" "B" 
  # connectPerim' (arrowArc (-220)) "A" "A" (110 @@ deg) (70 @@ deg)
  # connectOutside' arrowDef "C" "D"
  # connectPerim' (arrowArc (-220)) "D" "D" (110 @@ deg) (70 @@ deg)

categoryCompositionId = categoryLawsId
  "" "" "" ""
  "id" "f" "f∘id"
  "id" "g" "id∘g"

functionCompositionId = categoryLawsId
  "A" "B" "C" "D"
  "id[A]" "f" "compose(id[A],f)"
  "id[D]" "g" "compose(g,id[D])"

kleisliCompositionId = categoryLawsId
  "A" "B" "C" "D"
  "id : A ⇒ M[A]" "f : A ⇒ M[B]" "compose(id,f) = f"
  "id : D ⇒ M[D]" "g : C ⇒ M[D]" "compose(g,id) = g"

categoryLawsAssoc a b c d f g h fg gh fgh = (makeDiagram
  [ (0,0, objectL a # named "A")
  , (28,3, label f)
  , (60,0, objectL b # named "B")
  , (88,3, label g)
  , (120,0, objectL c # named "C")
  , (148,3, label h)
  , (180,0, objectL d # named "D")
  , (120,19, label gh)
  , (60,-19, label fg)
  , (90,40, label fgh)
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

categoryCompositionAssoc = categoryLawsAssoc
  "" "" "" ""
  "f" "g" "h"
  "g∘f" "h∘g"
  "h∘(g∘f) = (h∘g)∘f"

functionCompositionAssoc = categoryLawsAssoc
  "A" "B" "C" "D"
  "f" "g" "h"
  "compose(f,g)" "compose(g,h)"
  "compose(compose(f,g),h) = compose(f,compose(g,h))"

kleisliCompositionAssoc = categoryLawsAssoc
  "A" "B" "C" "D"
  "f : A ⇒ M[B]" "g : B ⇒ M[C]" "h : C ⇒ M[D]"
  "compose(f,g)" "compose(g,h)"
  "compose(compose(f,g),h) = compose(f,compose(g,h))"

option1 = (makeDiagram
  [ (0,0, objectL "A")
  , (66,0, objectL "B")
  , (66,30, boxL 28 9 ("Option[B]"))
  , (132,30, boxL 28 9 ("Option[C]"))
  , (25,14, label "f")
  , (89,14, label "g")
  , (116,-10, label "compose(f,g)")
  , (170,0, objectL "D")
  , (170,30, boxL 28 9 ("Option[D]"))
  , (167,14, label "id")
  , (190,40, objectI)
  , (0,-30, objectI)
  ])
  # connectOutside' arrowDef "A" ("Option[B]")
  # connectOutside' arrowDef "B" ("Option[C]") 
  # connectPerim' (arrowArc 90) "A" ("Option[C]") (-60 @@ deg) (270 @@ deg)
  # connectOutside' arrowDef "D" ("Option[D]") 
  # frame 5

option2 = option1
  # connectOutside' arrowDash "Option[B]" "B"
  # connectOutside' arrowDash "Option[B]" "Option[C]"

kleisli name = (makeDiagram
  [ (0,0, objectL "A")
  , (66,0, objectL "B")
  , (132,0, objectL "C")
  , (30,4, label $ "f : A ⇒ "++name++"[B]")
  , (96,4, label $ "g : B ⇒ "++name++"[C]")
  , (66,-25, label "compose(f,g)")
  , (170,0, objectL "D")
  , (170,20, label $ "id : D ⇒ "++name++"[D]")
  , (190,40, objectI)
  , (0,-30, objectI)
  ])
  # connectOutside' arrowDef "A" "B"
  # connectOutside' arrowDef "B" "C"
  # connectPerim' (arrowArc 60) "A" "C" (-30 @@ deg) (210 @@ deg)
  # connectPerim' (arrowArc (-220)) "D" "D" (110 @@ deg) (70 @@ deg)
  # frame 5

optionKleisli = kleisli "Option"
listKleisli = kleisli "List"
monadKleisli = kleisli "M"

typesAndFunctions1 = (makeDiagram
  [ (-75,-30, objectI)
  , (-40,0, objectLL "String")
  , (0,4, label "s2d")
  , (40,0, objectLL "Double")
  , (70,30, objectI)
  ])
  # connectOutside' arrowDef "String" "Double"
  # frame 6

typesAndFunctions2 = (makeDiagram
  [ (40,-25, label "sqrt")
  ]) <>
  typesAndFunctions1
  # connectPerim' (arrowArc (220)) "Double" "Double" (-110 @@ deg) (-70 @@ deg)

typesAndFunctions3 = (makeDiagram
  [ (0,-19, label "stringSqrt")
  ]) <>
  typesAndFunctions2
  # connectPerim' (arrowArc 60) "String" "Double" (-30 @@ deg) (210 @@ deg)

typesAndFunctions4 = (makeDiagram
  [ (-40,25, label "id[String]")
  , (40,25, label "id[Double]")
  ]) <>
  typesAndFunctions3
  # connectPerim' (arrowArc (-220)) "String" "String" (110 @@ deg) (70 @@ deg)
  # connectPerim' (arrowArc (-220)) "Double" "Double" (110 @@ deg) (70 @@ deg)

monoidKleisli = (makeDiagram
  [ (0,0, objectLL "Double")
  , (0,33, label "sqrtO")
  , (0,43, label "acosO")
  , (0,53, label "divTenO")
  ])
  # connectPerim' (arrowArc (-260)) "Double" "Double" (130 @@ deg) (50 @@ deg)
  # connectPerim' (arrowArc (-286)) "Double" "Double" (140 @@ deg) (40 @@ deg)
  # connectPerim' (arrowArc (-300)) "Double" "Double" (150 @@ deg) (30 @@ deg)
  # frame 12
