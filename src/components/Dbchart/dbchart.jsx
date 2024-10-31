import React, { useState, useEffect } from "react";
import Anotomy from '../../Icons/anotomy.png';

const StatsCard = () => {
  const [percentage, setPercentage] = useState(6); // Default initial value

  // Fetch the percentage value from an API
  useEffect(() => {
    const fetchPercentage = async () => {
      try {
        const response = await fetch('https://35.247.137.96:5000/percentage'); // Replace with your actual API endpoint
        const data = await response.json();
        setPercentage(data.percentage); // Assume the API returns { "percentage": 40 }
      } catch (error) {
        console.error("Error fetching percentage:", error);
      }
    };

    fetchPercentage();
  }, []);

  return (
    <div 
      className="relative flex items-start justify-start gap-10 p-4 rounded-xl shadow-lg w-1/2 overflow-hidden"
      style={{
        background: `linear-gradient(to top, #d6ff65 ${percentage}%, #ffffff ${percentage}%)`
      }}
    >
      {/* Left Section */}
      <div className="space-y-4 flex flex-col justify-evenly h-full z-10">
        {/* Percentage Display */}
        <div className="text-sm text-gray-600 flex items-center space-x-1">
          <span className="text-black bg-white w-14 flex items-center justify-center rounded-r-full rounded-l-full">↗ {percentage}%</span>
        </div>
        
        {/* Dots indicator */}
        <div className="flex items-center space-x-1">
          {[...Array(5)].map((_, index) => (
            <div
              key={index}
              className={`w-10 h-10 rounded-full ${
                index < Math.floor((percentage / 100) * 5) ? "bg-[#aacc52]" : "bg-gray-300"
              } transition-colors duration-500 ease-in-out`}
            ></div>
          ))}
        </div>

        {/* db Text */}
        <div>
          <p className="text-lg text-black">db</p>
          <p className="text-7xl font-normal">10.57</p>
        </div>
      </div>

      {/* Right Section with anatomy image */}
      <div className="absolute right-0 top-0 bottom-0 z-0 opacity-75">
        <img
          src={Anotomy}
          alt="Human Illustration"
          className="h-full object-cover"
        />
      </div>
    </div>
  );
};

export default StatsCard;
