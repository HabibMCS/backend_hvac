import React from 'react';

const NumberCard = ({ first, number, icon, last, color }) => {
  return (
    <div
      style={{ backgroundColor: color }} // Use inline styles for dynamic color
      className="h-64 w-72 flex flex-col items-start justify-between rounded-2xl p-4"
    >
        <div className='flex flex-col gap-3'>
        <span className='text-[#8b8a8a]'>{first}</span>
      <span className='text-8xl gap-2 text-black font-normal'>
        {number} <span className='text-4xl text-black font-normal'>{icon}</span>
      </span>
        </div>
      
      <span className='text-[#8b8a8a]'>{last}</span>
    </div>
  );
};

export default NumberCard;
