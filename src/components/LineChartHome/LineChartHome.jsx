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

  useEffect(() => {
    const generateData = () => [
      { name: "Jan", value: 0.3, green: true, dot: true },
      { name: "Jan-2", value: 0.5, green: false, dot: false },
      { name: "Jan-3", value: 0.6, green: true, dot: true },
      { name: "Feb", value: 0.4, green: false, dot: false },
      { name: "Feb-2", value: 0.6, green: true, dot: true },
      { name: "Feb-3", value: 0.7, green: false, dot: false },
      { name: "Mar", value: 0.7, green: true, dot: true },
      { name: "Mar-2", value: 0.362, green: false, dot: false },
      { name: "Mar-3", value: 0.8, green: true, dot: true },
      { name: "Apr", value: 0.4, green: false, dot: false },
      { name: "Apr-2", value: 0.5, green: true, dot: true },
      { name: "Apr-3", value: 0.6, green: false, dot: false },
      { name: "May", value: 0.4, green: true, dot: true },
      { name: "May-2", value: 0.5, green: false, dot: false },
      { name: "May-3", value: 0.6, green: true, dot: true },
      { name: "Jun", value: 0.7, green: false, dot: false },
      { name: "Jun-2", value: 0.6, green: true, dot: true },
      { name: "Jun-3", value: 0.8, green: false, dot: false },
      { name: "Jul", value: 0.6, green: true, dot: true },
    ];

    setData(generateData());
  }, []);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const { name, value } = payload[0].payload;
      return (
        <div className="bg-white border border-gray-300 rounded p-2">
          <p className="text-lg font-semibold">{name.split('-')[0]}</p>
          <p className="text-sm">{`${(value * 10).toFixed(2)}%`}</p>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="w-full h-full bg-white flex flex-col items-start justify-start border-2 border-transparent rounded-2xl p-4">
      <div className="text-start ml-3 w-full">
        <div className="text-lg font-bold">Analytics</div>
        <div className="mt-2 flex justify-between w-full">
          <div className="flex items-center">
            <span className="text-xl">Tracker</span>
          </div>
          <div className="flex items-center">
            <span className="text-4xl">09:45</span>
            <span className="text-black text-xs ml-2" style={{ position: "relative", top: "-15px" }}>
              AM
            </span>
            <span className="bg-[#d7fd6a] rounded-r-full rounded-l-full text-black w-14 h-6 flex items-center justify-center text-xs ml-2" style={{ position: "relative", top: "-10px" }}>
              30min
            </span>
          </div>


          <div className="flex items-center">
            <span className="text-4xl">98.57°</span>
            <span className="text-black text-xs ml-2" style={{ position: "relative", top: "-15px" }}>
              F
            </span>
            <span className="bg-[#d7fd6a] rounded-r-full rounded-l-full text-black w-14 h-6 flex items-center justify-center text-xs ml-2" style={{ position: "relative", top: "-10px" }}>
              30min
            </span>
          </div>
          <div className="flex flex-col items-center">
            <button className="text-2xl px-2" style={{ marginTop: '10px' }}>+</button>
            <button className="text-2xl px-2" style={{ marginTop: '10px' }}>-</button>
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
                  fill={entry.green ? "#a3e635" : "#d1d5db"}
                />
              ))}
              {data.map((entry, index) => (
                entry.dot ? (
                  <circle
                    key={`dot-${index}`}
                    cx={index * 40 + 20} // Position the circle according to the bar index
                    cy={(1 - entry.value) * 300 - 10} // Adjust for bar height and position the dot above the bar
                    r={5} // Radius of the dot
                    fill="white" // Color of the dot
                    style={{ pointerEvents: 'none' }} // Make the dot non-interactive
                  />
                ) : null
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="mt-6 ml-6 flex justify-start space-x-2 w-full">
          <button className="bg-lime-400 py-2 px-4 rounded-full">Tracker</button>
          <button className="bg-gray-100 py-2 px-4 rounded-full">MedicalAnalytics</button>
          <button className="bg-gray-100 py-2 px-4 rounded-full">FitnessMetrics</button>
          <button className="bg-gray-100 py-2 px-4 rounded-full">PatientInsights</button>
          <button className="bg-gray-100 py-2 px-4 rounded-full">AI Healthcare</button>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsTracker;
