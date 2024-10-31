import React, { useState } from "react";
import Papa from "papaparse";
import { FiUpload } from "react-icons/fi";
import LineChartComponent from "../LineChart/LineChartComponent";

const CsvUploader = () => {
  const [data, setData] = useState([]);
  const [isChart, setIsChart] = useState(true);
  const [tableData, setTableData] = useState([]);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          const parsedData = result.data.map((row) => {
            if (row["Time Stamp"]) {
              const date = new Date(row["Time Stamp"]);
              row["Time Stamp"] = date.toLocaleTimeString([], {
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
              });
            }
            return row;
          });
          setData(parsedData);
        },
      });

      Papa.parse(file, {
        header: true,
        skipEmptyLines: true,
        complete: (result) => {
          const parsedData = result.data.map((row) => {
            if (row["Time Stamp"]) {
              const date = new Date(row["Time Stamp"]);
              row["Time Stamp"] = date.toLocaleString([], {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
                hour12: false,
              });
            }
            // Adding mock data for new columns
            row["Heat Gain (RT)"] = Math.random() * 100; // Mock random data for Heat Gain
            row["Heat Rejected (RT)"] = Math.random() * 100; // Mock random data for Heat Rejected
            row["Percent Heat Balance (%)"] = Math.random() * 100; // Mock random data for Percent Heat Balance
            return row;
          });
          setTableData(parsedData);
        },
      });
    }
  };

  const extractUnit = (key) => {
    const match = key.split(" ");
    const unit = match[match.length - 1].match(/\(([^)]+)\)\s*(\w+)?/);
    return unit ? unit[1] || "" : "";
  };

  const getDescriptionWithoutColumnLetter = (key) => {
    return key.replace(/^\((.)\)/, "").trim();
  };

  const handleTabClick = (tab) => {
    setIsChart(tab === "chart");
  };

  return (
    <div className="p-4">
      <div className="mb-4 flex gap-4">
        <button
          className={`px-4 py-2 rounded-l ${
            isChart ? "bg-blue-500 text-white" : "bg-gray-200 text-black"
          }`}
          onClick={() => handleTabClick("chart")}
        >
          Charts
        </button>
        <button
          className={`px-4 py-2 rounded-r ${
            !isChart ? "bg-blue-500 text-white" : "bg-gray-200 text-black"
          }`}
          onClick={() => handleTabClick("table")}
        >
          Table
        </button>
      </div>

      {data.length > 0 ? (
        isChart ? (
          <LineChartComponent data={data} xAxisKey="Time Stamp" />
        ) : (
          <div className="overflow-auto">
            <table className="min-w-full border overflow-auto border-gray-300">
              <thead>
                <tr>
                  {/* First Column: Time Stamp without heading */}
                  <th className="border-b border-gray-300 px-4 py-2 text-center">
                    {/* No heading for Time Stamp */}
                  </th>
                  {Object.keys(tableData[0])
                    .filter((key) => key !== "Time Stamp") // Exclude "Time Stamp" from headers
                    .map((key, index) => {
                      const description = getDescriptionWithoutColumnLetter(key);
                      return (
                        <th
                          key={key}
                          className="border-2 border-gray-300 px-4 py-2 text-center"
                        >
                          <div className="flex flex-col items-center justify-center">
                            <span className="font-bold">{`(${String.fromCharCode(
                              98 + index
                            )})`}</span>
                            <span className="text-sm text-gray-500 ">
                              {description}
                            </span>
                          </div>
                        </th>
                      );
                    })}
                </tr>

                {/* Second Row: Units */}
                <tr>
                  <th className="border-2 border-gray-300 px-4 py-2 text-center">
                    dd/mm/yy hh:mm
                  </th>
                  {Object.keys(tableData[0])
                    .filter((key) => key !== "Time Stamp") // Exclude "Time Stamp" from units row
                    .map((key) => {
                      const unit = extractUnit(key);
                      return (
                        <th
                          key={key}
                          className="border-2 border-gray-300 px-4 py-2 text-center"
                        >
                          {unit || ""}
                        </th>
                      );
                    })}
                </tr>
              </thead>

              <tbody>
                {tableData.map((row, index) => (
                  <tr key={index} className="hover:bg-gray-100">
                    {/* Render Time Stamp in the first column of each row */}
                    <td className="border-2 border-gray-300 px-4 py-2 text-center">
                      {row["Time Stamp"]} {/* Full date and time */}
                    </td>
                    {Object.entries(row)
                      .filter(([key]) => key !== "Time Stamp") // Exclude "Time Stamp" from row data
                      .map(([key, value], idx) => (
                        <td
                          key={idx}
                          className="border-2 border-gray-300 px-4 py-2 text-center"
                        >
                          {value}
                        </td>
                      ))}
                  </tr>
                ))}
                <tr>
                  <td align="center">Total</td>
                  {Object.keys(tableData[0])
                    .filter((key) => key !== "Time Stamp") // Exclude "Time Stamp" from total row
                    .map((key) => {
                      const total = tableData.reduce(
                        (acc, row) => acc + parseFloat(row[key]) || 0,
                        0
                      );
                      return (
                        <td
                          key={key}
                          className=" border-dotted border-2 border-gray-300 px-4 py-2 text-center"
                        >
                          {total.toFixed(2)}
                        </td>
                      );
                    })}
                </tr>

                <tr>
                  <td className="border-2 border-gray-300 px-4 py-2 text-center" align="center"></td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-end" colSpan={tableData.length+2} align="right" >Total Data Count </td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-center"   >53(change value)</td>

                </tr>

                <tr>
                  <td className="border-2 border-gray-300 px-4 py-2 text-center" align="center"></td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-end" colSpan={tableData.length+2} align="right" > Data Count &lt; +5% error </td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-center"   >53(change value)</td>

                </tr>


                <tr>
                  <td className="border-2 border-gray-300 px-4 py-2 text-center" align="center"></td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-end" colSpan={tableData.length+2} align="right" >Data Count &gt; +5% error </td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-center"   >53(change value)</td>

                </tr>

                <tr>
                  <td className="border-2 border-gray-300 px-4 py-2 text-center" align="center"></td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-end" colSpan={tableData.length+2} align="right" >Percentage of heat balance within ± 5% </td>
                 <td className="border-2 border-gray-300 px-4 py-2 text-center"   >53(change value)</td>

                </tr>
              </tbody>
            </table>
          </div>
        )
      ) : (
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
