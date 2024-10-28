import React from "react";
import Anotomy from '../../Icons/anotomy.png';

const StatsCard = () => {
  return (
    <div className="relative flex items-start justify-start gap-10 bg-[#d6ff65] p-4 rounded-xl shadow-lg w-1/2">
      {/* Left Section */}
      <div className="space-y-4 flex flex-col justify-evenly h-full">
        {/* Percentage */}
        <div className="text-sm text-gray-600 flex items-center space-x-1">
          <span className="text-black bg-white w-14 flex items-center justify-center rounded-r-full rounded-l-full">↗ 06%</span>
        </div>
        
        {/* Dots indicator */}
        <div className="flex items-center space-x-1">
          <div className="w-10 h-10 rounded-full bg-[#aacc52]"></div>
          <div className="w-10 h-10 rounded-full bg-[#aacc52]"></div>
          <div className="w-10 h-10 rounded-full flex items-center justify-center  border-2 border-black"><div className="w-5 h-5 rounded-full bg-[#000000]"></div></div>
          <div className="w-10 h-10 rounded-full bg-[#aacc52]"></div>
          <div className="w-10 h-10 rounded-full bg-[#aacc52]"></div>
        </div>

        {/* db Text */}
        <div>
          <p className="text-lg text-black">db</p>
          <p className="text-7xl font-normal">10.57</p>
        </div>
      </div>

      {/* Right Section with anatomy image */}
      <div className="absolute right-[-90px] top-[-20px]">
        <img
          src={Anotomy}
          alt="Human Illustration"
          className="w-56 h-96"
        />
      </div>
    </div>
  );
};

export default StatsCard;
