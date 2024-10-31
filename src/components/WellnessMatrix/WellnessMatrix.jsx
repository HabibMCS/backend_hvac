import React, { useState, useEffect } from 'react';

const WellnessMatrix = () => {
  const [wellnessData, setWellnessData] = useState({
    total_kcal: 0,
    calories_burned: 0,
    workouts: 0
  });

  // Fetch data from the backend
  useEffect(() => {
    const fetchWellnessData = async () => {
      try {
        const response = await fetch('https://35.247.137.96:5000/wellness_metrics');
        const data = await response.json();
        setWellnessData(data);
      } catch (error) {
        console.error("Error fetching wellness data:", error);
      }
    };

    fetchWellnessData();
  }, []);

  return (
    <div className="bg-white h-full rounded-2xl shadow-lg max-w-sm">
      {/* Outer container with p-6 */}
      <div className="p-6">
        {/* Top Section */}
        <div className="flex justify-between items-center mb-4">
          <div className="text-sm font-semibold text-gray-700 flex flex-row items-center">
            <div className="bg-[#d4fd60] rounded-full w-6 h-6 mr-2"></div>Wellness
          </div>
          <div className="text-sm font-semibold text-gray-700 flex flex-row items-center">
            <div className="bg-gray-500 rounded-full w-6 h-6 mr-2"></div>News
          </div>
        </div>

        {/* Main Metrics */}
        <div className="mb-4">
          <h2 className="text-6xl font-normal mt-6 text-gray-900">{wellnessData.total_kcal.toLocaleString()}</h2>
          <p className="text-md text-black">KCAL Totally</p>
        </div>

        {/* Description */}
        <div className="mb-4 mt-28">
          <p className="text-sm font-semibold text-gray-600">
            PERFECT WELLNESS METRICS BASED ON BLOCKCHAIN
          </p>
        </div>
      </div>

      {/* Calories and Workouts Section without p-6 */}
      <div className="flex w-full mt-5">
        {/* Calories */}
        <div className="text-start w-full flex flex-col justify-between h-36 border-t-2 border-r-2 border-[#f4f4f4] p-4">
          <div className='flex flex-col'>
            <h3 className="text-4xl font-normal text-gray-900">{wellnessData.calories_burned}</h3>
            <p className="text-sm text-gray-500">KCAL</p>
          </div>
          <p className="text-sm text-gray-500 ">Calories Burned</p>
        </div>

        {/* Workouts */}
        <div className="text-start w-full border-t-2 flex flex-col justify-between border-[#f4f4f4] p-4">
          <h3 className="text-4xl font-normal text-gray-900">{wellnessData.workouts}</h3>
          <p className="text-sm text-gray-500 ">Workouts</p>
        </div>
      </div>
    </div>
  );
};

export default WellnessMatrix;
