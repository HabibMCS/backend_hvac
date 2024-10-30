import React, { useState } from 'react';
import { DateRangePicker } from 'react-date-range';
import { format } from 'date-fns';
import Circle from '@/components/CricleIcon/Circle';
import CalendarIcon from '@/Icons/calender';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css';

const DateSelector = () => {
  const [isDatePickerOpen, setIsDatePickerOpen] = useState(false);
  const [dateRange, setDateRange] = useState([
    {
      startDate: new Date(),
      endDate: new Date(),
      key: 'selection'
    }
  ]);

  // Format the selected date range for display
  const formattedDateRange = `${format(dateRange[0].startDate, 'MMM dd')} - ${format(dateRange[0].endDate, 'MMM dd')}`;

  // Toggle Date Picker visibility
  const toggleDatePicker = () => setIsDatePickerOpen(!isDatePickerOpen);

  // Handle Date Change
  const handleDateChange = (item) => {
    setDateRange([item.selection]);
  };

  return (
    <div className='flex gap-3'>
      <div className='relative'>
        <div 
          className='w-fit h-10 bg-[#ffffff] rounded-r-full rounded-l-full flex items-center justify-start px-1 gap-1 pr-3 cursor-pointer'
          onClick={toggleDatePicker}
        >
          <Circle height='30' width='30' color='#f4f4f4' svg={CalendarIcon} svgColor='#000000' />
          <div className='flex flex-row gap-2 items-center'>
            <span className='text-xs text-[#000000] font-bold'>{formattedDateRange}</span>
          </div>
        </div>

        {isDatePickerOpen && (
          <div className='absolute top-12 right-0 z-50 bg-white shadow-lg rounded-lg max-w-[calc(100vw-1rem)] overflow-hidden'>
            <DateRangePicker
              onChange={handleDateChange}
              showSelectionPreview={true}
              moveRangeOnFirstSelection={false}
              months={2}
              ranges={dateRange}
              direction="horizontal"
              className="p-4"
            />
            <div className="flex justify-end p-2">
              <button
                className="px-4 py-2 text-gray-700 border border-gray-300 rounded-md mr-2"
                onClick={toggleDatePicker}
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 text-white bg-purple-700 rounded-md"
                onClick={toggleDatePicker}
              >
                Done
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default DateSelector;
