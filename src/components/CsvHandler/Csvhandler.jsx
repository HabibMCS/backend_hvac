import React, { useState } from 'react';
import Papa from 'papaparse';
import { FiUpload } from 'react-icons/fi';
import LineChartComponent from '../LineChart/LineChartComponent';

const CsvUploader = () => {
  const [data, setData] = useState([]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          const parsedData = result.data.map((row) => {
            if (row["Time Stamp"]) {
              // Convert "Time Stamp" to HH:MM format
              const date = new Date(row["Time Stamp"]);
              row["Time Stamp"] = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
            }
            return row;
          });
          setData(parsedData);
        },
      });
    }
  };

  return (
    <div className="p-4">
      

      {data.length > 0 ? (
       <LineChartComponent
       data={data}
       xAxisKey="Time Stamp" // specify the column name for x-axis
     />
      ):
      (
        <label className="flex items-center gap-2 bg-[#d7fd6a] text-green-950 px-4 py-2 w-44 h-14 rounded cursor-pointer hover:bg-lime-700">
        <FiUpload className="text-xl" />
        <span>Upload CSV</span>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          className="hidden"
        />
       </label>
      )}
    </div>
  );
};

export default CsvUploader;
