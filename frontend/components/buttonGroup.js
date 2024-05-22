import React from "react";

// This button group component will be used to start, stop and reset the simulation

const ButtonGroup = ({ children }) => {
  const [isStart, setIsStart] = React.useState(false);
  const [isStop, setIsStop] = React.useState(false);
  const [isReset, setIsReset] = React.useState(false);

  const handleStart = () => {
    setIsStart(true);
    setIsStop(false);
    setIsReset(false);
    alert("Start simulation");
  };

  const handleStop = () => {
    setIsStart(false);
    setIsStop(true);
    setIsReset(false);
    alert("Stop simulation");
  };
  return (
    <div className="absolute top-4 left-4 flex flex-row justify-center space-x-4">
      <button
        className="w-[5vw] h-[5vh] bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-full"
        onClick={handleStart}
      >
        Start
      </button>
      <button
        className="w-[5vw] h-[5vh] bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded-full"
        onClick={handleStop}
      >
        Stop
      </button>
      <button
        className="w-[5vw] h-[5vh] bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-full"
        onClick={() => {
          alert("Reset simulation");
        }}
      >
        Reset
      </button>
    </div>
  );
};

export default ButtonGroup;
