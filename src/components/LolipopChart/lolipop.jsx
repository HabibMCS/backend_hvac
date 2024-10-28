import React from 'react';

const LollipopChart = () => {
  // Data representing the chart values for each day
  const data = [
    { day: 'S', value: 50 },
    { day: 'M', value: 70 },
    { day: 'T', value: 50 },
    { day: 'W', value: 100 },
    { day: 'T', value: 20 },
    { day: 'F', value: 60 },
    { day: 'S', value: 40 }
  ];

  return (
    <div className="flex flex-col items-center justify-evenly w-96 h-80 p-6 bg-white rounded-2xl">
      {/* Top percentage value */}
      <div className="bg-lime-400 text-black text-sm font-semibold mb-4">
        <span className="inline-block transform rotate-45">↗</span> 278%
      </div>

      {/* Lollipop chart container */}
      <div className="flex justify-between items-end w-full max-w-md">
        {data.map((item, idx) => (
          <div key={idx} className="flex flex-col items-center">
            {/* Circle */}
            <div className="w-4 h-4 bg-lime-400 rounded-full"></div>

            {/* Vertical Line */}
            <div
              className="w-1 bg-gray-200"
              style={{ height: `${item.value}px` }}
            ></div>

            {/* Day Label */}
            <div className="text-sm text-gray-700 mt-2">{item.day}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LollipopChart;
