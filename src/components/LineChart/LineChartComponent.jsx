import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

const LineChartComponent = ({ data, xAxisKey }) => {
  // Get y-axis keys by filtering out the xAxisKey from the data keys
  const yAxisKeys = Object.keys(data[0] || {}).filter(key => key !== xAxisKey);

  // Function to calculate the next step value
  const getNextStep = (maxValue) => {
    const step = 3; // Change this based on your required step size
    return Math.ceil((maxValue + 1) / step) * step; // Round up to the next step
  };

  // Define your colors
  const colors = ['#4B0082', '#006400']; // Dark purple and dark green

  return (
    <div className="mt-4 space-y-8">
      {yAxisKeys.map((key, index) => {
        // Calculate the maximum value for the current y-axis key
        const maxValue = Math.max(...data.map(item => item[key] || 0));

        return (
          <div key={key} className="p-4 border rounded shadow">
            <h2 className="text-center text-xl font-semibold mb-4">{key} over Time</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey={xAxisKey} />
                <YAxis domain={[0, getNextStep(maxValue)]} /> {/* Set the Y-axis domain */}
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey={key}
                  stroke={colors[index % colors.length]} // Alternate between dark purple and dark green
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        );
      })}
    </div>
  );
};

export default LineChartComponent;
