import { useState, useEffect } from 'react';
import { CoolingTime } from '@/components/CoolingTime/CoolingTime';
import CopTime from '@/components/CopTime/CopTime';
import LineChartHome from '@/components/LineChartHome/LineChartHome';
import { PowerChart } from '@/components/PowerChart/PowerChart';
import Sidebar from '@/components/Sidebar/Sidebar';
import { UnitChart } from '@/components/UnitChart/UnitChart';
import  NumberCard  from '@/components/NumberCard/numberCard';
import WellnessMetrics from '@/components/WellnessMatrix/WellnessMatrix';
import LollipopChart from '@/components/LolipopChart/lolipop';
import StatsCard from '@/components/Dbchart/dbchart';
import BreathComponent from '@/components/BreathingComponent/breathing';
import BellIcon from '@/Icons/bell';
import Circle from '@/components/CricleIcon/Circle';
import RotatedArrowIcon from '@/Icons/downarrow';
import ClockIcon from '@/Icons/clock';
import ArrowRightIcon from '@/Icons/rightarrow';
import CalendarIcon from '@/Icons/calender';
import DateSelector from '@/components/Dateselector/Dateselector';
const Dashboard = () => {
    const [summaryData, setSummaryData] = useState({
        total_data: 0,
        data_above_10_error: 0,
        data_below_minus_10_error: 0,
        percent_energy_balance: 0,
    });

    // Fetch summary data from backend
    useEffect(() => {
        const fetchSummaryData = async () => {
            try {
                const response = await fetch('http://localhost:5000/summary');
                const data = await response.json();
                setSummaryData(data);
            } catch (error) {
                console.error('Error fetching summary data:', error);
            }
        };
        fetchSummaryData();
    }, []);

    return (
        <div className='flex'>
            <Sidebar />
            <section className="max-h-[90vh] p-7 w-full overflow-y-auto hide-scrollbar bg-[#f4f4f4] custom-rounded">
                <div className="text-5xl mt-5 font-normal">Operational Overview</div>
                <div className="text-3xl text-[#b6b5b8] w-[1680px] mt-2 font-normal flex items-center justify-between">
                    <span> HVAC Record</span>
                    <div className='flex gap-3' >
                        <div className='w-fit h-10 bg-[#ffffff] rounded-r-full rounded-l-full flex items-center justify-start px-1 gap-1 pr-3 cursor-pointer'>
                            <div className='flex flex-row gap-2 items-center'>
                                <DateSelector />
                            </div>
                        </div>
                    </div>
                </div>

                {/* Container for LineChartHome and Summary Data */}
                <div className="flex gap-6 mb-4 mt-5">
                    <div className="w-2/3 pr-2">
                        <LineChartHome />
                    </div>
                    <div className="w-1/6 pr-2">
                        <div className='flex flex-col gap-8'>
                            <div className='flex flex-col gap-8'>
                                <NumberCard first='Total Data' number={summaryData.total_data}  color='#FFFFFF' />
                                <NumberCard first='Percent Energy Balance' number={summaryData.percent_energy_balance} color='#deeff9' />
                            </div>
                            {/* <div className="bg-white p-4 rounded shadow">
                                <h3 className="font-bold text-lg">Data  10.0% Error</h3>
                                <p className="text-2xl">{summaryData.data_above_10_error}</p>
                            </div>
                            <div className="bg-white p-4 rounded shadow">
                                <h3 className="font-bold text-lg">Data  -10.0% Error</h3>
                                <p className="text-2xl">{summaryData.data_below_minus_10_error}</p>
                            </div> */}
                        </div>
                    </div>
                    <div className="w-1/3">
                        <WellnessMetrics />
                    </div>
                </div>

                {/* Container for LollipopCharts aligned with LineChartHome */}
                <div className='flex w-full gap-5 items-start justify-start'>
                    <div className="my-6 w-[920px] flex justify-between">
                        <StatsCard />
                        <LollipopChart />
                    </div>
                    <div className='mt-4'>
                        <BreathComponent />
                    </div>
                </div>

                {/* Additional sections (e.g., CoolingTime, UnitChart, PowerChart) can go here */}
            </section>
        </div>
    );
};

export default Dashboard;
