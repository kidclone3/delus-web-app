const gridSize = 500;
const gridCount = 50; // No. of squares in each direction
const squareSize = gridSize / gridCount;
const fetchInterval = 500;
const refreshInterval = 16;
const turnDuration = refreshInterval * 4;
const animationOverhead = 100;

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
