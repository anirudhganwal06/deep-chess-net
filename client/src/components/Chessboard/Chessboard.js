import React from "react";
import Chessboardjsx from "chessboardjsx";

import HumanVsHuman from "../Modes/HumanVsHuman";

const Chessboard = (props) => {
  return (
    <div>
      <HumanVsHuman>
        {({
          position,
          onDrop,
          onMouseOverSquare,
          onMouseOutSquare,
          squareStyles,
          dropSquareStyle,
          onDragOverSquare,
          onSquareClick
        }) => (
          <Chessboardjsx
            id="humanVsHuman"
            width={"800"}
            position={position}
            onDrop={onDrop}
            onMouseOverSquare={onMouseOverSquare}
            onMouseOutSquare={onMouseOutSquare}
            // boardStyle={{
            //   borderRadius: "5px",
            //   boxShadow: `0 5px 15px rgba(0, 0, 0, 0.5)`,
            // }}
            squareStyles={squareStyles}
            dropSquareStyle={dropSquareStyle}
            onDragOverSquare={onDragOverSquare}
            onSquareClick={onSquareClick}
          />
        )}
      </HumanVsHuman>
    </div>
  );
};

export default Chessboard;