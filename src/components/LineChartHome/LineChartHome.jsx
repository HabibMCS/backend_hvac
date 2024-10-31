import React, { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const AnalyticsTracker = () => {
  const [data, setData] = useState([]);
  const [activeData, setActiveData] = useState("System1");

  // Fetch data from the backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`https://35.247.137.96:5000/data?type=${activeData}`);
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [activeData]);

  // Custom tooltip component for showing detailed information on hover
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const { name, value, cooling_load } = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded p-2">
          <p className="text-lg font-semibold">{name.split("-")[0]}</p>
          <p className="text-sm">COP: {(value * 10).toFixed(2)}%</p>
          <p className="text-sm">Cooling Load: {cooling_load} KW</p>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="w-full h-full bg-white flex flex-col items-start justify-start border-2 border-transparent rounded-2xl p-4">
      <div className="text-start ml-3 w-full">
        <div className="text-lg font-bold">COP - {activeData}</div>
        <div className="mt-2 flex justify-between w-full">
          <div className="flex items-center">
            <span className="text-xl">{activeData}</span>
          </div>
        </div>
      </div>

      <div className="flex flex-col items-start justify-start mt-4 w-full">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} margin={{ top: 20, right: 30, left: 5, bottom: 5 }}>
            <XAxis
              dataKey="name"
              tickFormatter={(tick) => ["Jan", "Mar", "May", "Jul"].includes(tick) ? tick : ""}
              tick={{ fontSize: 12 }}
              interval={0}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tickFormatter={(value) => {
                if (value === 0) return "00%";
                if (value === 0.8) return "08%";
                if (value === 1) return "10%";
                return `${value * 100}%`;
              }}
              ticks={[0, 0.8, 1]}
              tick={{ fontSize: 12 }}
              domain={[0, 1]}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="value" barSize={25} radius={[20, 20, 20, 20]}>
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.green ? "#a3e635" : "#d1d5db"} // Green for 'COP' > threshold, gray otherwise
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-6 ml-6 flex justify-start space-x-2 w-full">
          {["System0", "System1", "System2", "System3"].map((type) => (
            <button
              key={type}
              onClick={() => setActiveData(type)}
              className={`py-2 px-4 rounded-full ${
                activeData === type ? "bg-lime-400" : "bg-gray-100"
              }`}
            >
              {type}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AnalyticsTracker;
