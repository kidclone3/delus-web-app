const gridSize = 500;
const gridCount = 50; // No. of squares in each direction
const squareSize = gridSize / gridCount;
const fetchInterval = 1000;
const refreshInterval = 16;
const turnDuration = refreshInterval * 8;
const animationOverhead = 200;

const config = {
  gridSize,
  gridCount,
  squareSize,
  fetchInterval,
  refreshInterval,
  turnDuration,
  animationOverhead,
};

export default config;
