import React, { useState, useEffect } from "react";
import CustomShapeIcon from "@/Icons/attherate";
import Circle from "../CricleIcon/Circle";

const BreathComponent = () => {
  const [timer, setTimer] = useState(2); // Initialize the timer for 2 seconds

  // Timer countdown logic
  useEffect(() => {
    if (timer > 0) {
      const interval = setInterval(() => {
        setTimer((prevTimer) => prevTimer - 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [timer]);

  return (
    <div className="flex flex-col items-start justify-between p-7 w-[700px] rounded-2xl h-80 bg-gray-50">
      {/* Main Text */}
      <div className="w-full flex flex-row justify-between">
        <h1 className="text-4xl w-64 font-bold text-gray-800 mb-4">TAKE A BREATH NOW</h1>
        {/* Timer and Instruction */}
        <p className="text-sm text-gray-500">
          {timer > 0 ? `Wait ${timer} sec, and then take a deep breath!` : "Take a deep breath!"}
        </p>
      </div>

      {/* Breath Level Box */}
      <div className="mt-8 bg-[#f4f4f4] shadow-md rounded-lg px-6 py-4 flex flex-row items-center justify-between w-full">
        <div className="flex gap-3 items-center">
          <p className="text-sm text-gray-600 p-2 rounded-r-full rounded-l-full bg-white">35, m2</p>
          <p className="text-gray-800 font-semibold">Breath Level is Normal now 12</p>

        </div>

        <div>
        </div>

        {/* Placeholder for Speaker Icon */}
    <Circle height={50} width={50} color="#ffffff" svg={CustomShapeIcon} svgColor="#000000" />
      </div>
    </div>
  );
};

export default BreathComponent;
