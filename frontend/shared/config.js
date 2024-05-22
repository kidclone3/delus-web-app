const gridSize = 1000;
const gridCount = 100;
const squareSize = gridSize / gridCount;
const fetchInterval = 1500;
const refreshInterval = 4;
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
