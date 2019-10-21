module Main exposing (Msg(..), main, update, view)

import Browser
import Html exposing (Html, button, div, h1, text, img, table, td, tr)
import Html.Attributes exposing (src, height, width)
import Html.Events exposing (onClick)
import Task
import Process
import Random
import Random.List



-- Model

type alias Image =
    { url : String
    }


type alias Model =
    { board : Board
    }


type alias Board =
    List Card


type alias Card =
    { image : Image
    , selected : Bool
    , completed : Bool
    }

imageList : List Image
imageList = List.map (\n -> {url = "./assets/nasa" ++ String.fromInt n ++ ".jpg"}) [1,1,2,2,3,3,4,4]

unshuffledBoard : Board
unshuffledBoard = List.map (\img -> { image = img, selected = False, completed = False }) imageList


initialModel : Model
initialModel =
    { board = unshuffledBoard } -- we will shuffle this below



gen = Random.List.shuffle unshuffledBoard


init : () -> ( Model, Cmd Msg )
init =
    \_ -> ( initialModel, Random.generate Populate gen )



-- Update


type Msg
    = Click Int
    | Clear
    | Populate Board


update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
    case msg of
      Click index ->
        let
          b1 = List.indexedMap (\n card -> if n == index then { card | selected = True} else card) model.board -- flip selected card
          selected = List.filter (\card -> card.selected && not card.completed) b1
          choseRight =
              (List.length selected) > 1 && -- there is at least 2 items in the list
              List.all (\card -> case List.head selected of 
                                    Nothing -> False
                                    Just c1 -> card == c1) selected -- both items are structurally equal
          b2 = if choseRight
               then List.map (\card -> case List.head selected of 
                                          Nothing -> card
                                          Just c1 -> if card == c1 then { card | completed = True } else card) b1
               else b1
          numberShown = List.foldr (\card acc -> if card.selected && not card.completed then acc + 1 else acc) 0 b2
          cmd = if numberShown == 2 then Task.perform (\_ -> Clear) (Process.sleep 500) else Cmd.none
        in
          ({board = b2}, cmd)
      Clear ->
        ({board = List.map(\card -> {card | selected = False}) model.board}, Cmd.none)
      Populate board ->
        ({board = board}, Cmd.none)
        

-- View

hiddenCard = "./assets/cardback.jpg" -- sample back of card

displayCard : Card -> Html msg
displayCard {image, selected, completed} =
    let
      size = 200
      show = [src image.url, height size, width size]
      hide = [src hiddenCard, height size, width size]
    in 
      case (selected, completed) of
        (_, True) -> img show []
        (True, _) -> img show []
        (False, _) -> img hide []

view { board } =
    let 
      divs = List.indexedMap (\index card -> td [onClick (Click index)] [displayCard card]) board
      topHalf = tr [] (List.take 4 divs)
      bottomHalf = tr [] (List.drop 4 divs)
    in
      table [] [topHalf, bottomHalf]



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none



-- Main


main =
    Browser.element { init = init, update = update, view = view, subscriptions = subscriptions }
