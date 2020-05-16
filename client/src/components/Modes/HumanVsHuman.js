import { useState, useEffect } from "react";
import Chess from "chess.js";

const HumanVsHuman = (props) => {
    // static propTypes = { children: PropTypes.func };

  const [fen, setFen] = useState("start");
  // square styles for active drop square
  const [dropSquareStyle, setDropSquareStyle] = useState({});
  // custom square styles
  const [squareStyles, setSquareStyles] = useState({});
  // square with the currently clicked piece
  const [pieceSquare, setPieceSquare] = useState("");
  // currently clicked square
  // const [square, setSquare] = useState("");
  // array of past game moves
  const [history, setHistory] = useState([]);
  const [game, setGame] = useState("");

  useEffect(() => {
    setGame(new Chess());
  }, []);

  // keep clicked square style and remove hint squares
  const removeHighlightSquare = () => {
    setSquareStyles(squareStyling({ pieceSquare, history }));
  };

  // show possible moves
  const highlightSquare = (sourceSquare, squaresToHighlight) => {
    const highlightStyles = [sourceSquare, ...squaresToHighlight].reduce(
      (a, c) => {
        return {
          ...a,
          ...{
            [c]: {
              background:
                "radial-gradient(circle, #fffc00 36%, transparent 40%)",
              borderRadius: "50%",
            },
          },
          ...squareStyling({
            history: history,
            pieceSquare: pieceSquare,
          }),
        };
      },
      {}
    );
    setSquareStyles({ ...squareStyles, ...highlightStyles });
  };

  const onDrop = ({ sourceSquare, targetSquare }) => {
    // see if the move is legal
    let move = game.move({
      from: sourceSquare,
      to: targetSquare,
      promotion: "q", // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;
    setSquareStyles(squareStyling({ pieceSquare, history }));
    setFen(game.fen());
    setHistory(game.history({ verbose: true }));
  };

  const onMouseOverSquare = (square) => {
    // get list of possible moves for this square
    let moves = game.moves({
      square: square,
      verbose: true,
    });

    // exit if there are no moves available for this square
    if (moves.length === 0) return;

    let squaresToHighlight = [];
    for (var i = 0; i < moves.length; i++) {
      squaresToHighlight.push(moves[i].to);
    }

    highlightSquare(square, squaresToHighlight);
  };

  const onMouseOutSquare = (square) => removeHighlightSquare(square);

  // central squares get diff dropSquareStyles
  const onDragOverSquare = (square) => {
    setDropSquareStyle(
      square === "e4" || square === "d4" || square === "e5" || square === "d5"
        ? { backgroundColor: "cornFlowerBlue" }
        : { boxShadow: "inset 0 0 1px 4px rgb(255, 255, 0)" }
    );
  };

  const onSquareClick = (square) => {
    setSquareStyles(squareStyling({ pieceSquare: square, history }));
    setPieceSquare(square);

    let move = game.move({
      from: pieceSquare,
      to: square,
      promotion: "q", // always promote to a queen for example simplicity
    });

    // illegal move
    if (move === null) return;

    setFen(game.fen());
    setHistory(game.history({ verbose: true }));
    setPieceSquare("");
  };

  return props.children({
    squareStyles,
    position: fen,
    onMouseOverSquare: onMouseOverSquare,
    onMouseOutSquare: onMouseOutSquare,
    onDrop: onDrop,
    dropSquareStyle,
    onDragOverSquare: onDragOverSquare,
    onSquareClick: onSquareClick,
    //   onSquareRightClick: onSquareRightClick,
  });
};

const squareStyling = ({ pieceSquare, history }) => {
  const sourceSquare = history.length && history[history.length - 1].from;
  const targetSquare = history.length && history[history.length - 1].to;

  return {
    [pieceSquare]: { backgroundColor: "rgba(255, 255, 0, 0.4)" },
    ...(history.length && {
      [sourceSquare]: {
        backgroundColor: "rgba(255, 255, 0, 0.4)",
      },
    }),
    ...(history.length && {
      [targetSquare]: {
        backgroundColor: "rgba(255, 255, 0, 0.4)",
      },
    }),
  };
};

export default HumanVsHuman;
