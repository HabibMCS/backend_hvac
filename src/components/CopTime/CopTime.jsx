import { useState, useEffect } from "react";
import { Bar, BarChart, CartesianGrid, XAxis, YAxis } from "recharts"; // Import YAxis
import {
    Card,
    CardContent,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import {
    ChartContainer,
    ChartTooltip,
    ChartTooltipContent,
} from "@/components/ui/chart";
import axios from "axios";
import Spinner from "../Spinner/Spinner"; // Import the Spinner component

export const description = "A multiple bar chart";

const chartConfig = {
    cop_values: {
        label: "COP Values",
        color: "#000",
    },
};

const CopTime = () => {
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchChartData = async () => {
        try {
            const response = await axios.post("https://35.247.137.96:5000/download_csv", {
                token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2MjhiZThjNDYzMzU0N2NiZmZhMGZiZSIsImlhdCI6MTcyNzUyNjM0NCwiZXhwIjoxNzQzMDc4MzQ0fQ.RFfQzAVGXc8iLX80Iwhzixb45Xj2yVELBusH1a3MegI", // Replace with actual token
                system_number: 1, // Example system number
            });

            const apiData = response.data;
            console.log("API Data:", apiData); // Log the API data for debugging

            // Extract cop_values and timestamp directly since they're now arrays
            const copValues = apiData["cop_values"]; // This is now an array of COP values
            const timestamp = apiData["timestamp"];   // This is now an array of timestamps

            if (!Array.isArray(copValues) || !Array.isArray(timestamp)) {
                throw new Error("Invalid data format: cop_values or timestamp is not an array");
            }

            // Combine the timestamp and COP values into a single object
            const transformedData = timestamp.map((time, index) => ({
                timestamp: new Date(time).toLocaleTimeString(), // Set the timestamp for X-axis
                cop: copValues[index] || 0, // Safeguard against index issues
            }));

            setChartData(transformedData);
            setLoading(false);
        } catch (error) {
            console.error("Error fetching chart data:", error);
            setError("Failed to load data: " + error.message); // Include the error message for better feedback
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchChartData();
    }, []);

    return (
        <Card className="w-[48%]">
            <CardHeader>
                <CardTitle className="text-xl text-primary">COP Load - Time</CardTitle>
            </CardHeader>
            <CardContent>
                {loading ? (
                    <>
                        <Spinner />  {/* Show the spinner while loading */}
                    </>
                ) : error ? (
                    <p>{error}</p>
                ) : (
                    <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
                        <BarChart data={chartData}>
                            <CartesianGrid vertical={false} />
                            <XAxis
                                dataKey="timestamp" // Set X-axis to timestamp
                                tickLine={false}
                                tickMargin={10}
                                axisLine={false}
                            />
                            <YAxis // Add Y-axis for COP values
                                dataKey="cop"
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(value) => value.toFixed(2)} // Format COP values
                            />
                            <ChartTooltip
                                className="bg-white rounded-[10px]"
                                cursor={false}
                                content={<ChartTooltipContent indicator="dashed" />}
                            />
                            <Bar dataKey="cop" fill="#29132E" radius={4} />
                        </BarChart>
                    </ChartContainer>
                )}
            </CardContent>
        </Card>
    );
};

export default CopTime;
