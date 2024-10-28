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

const Dashboard = () => {
    return (
        <div className='flex'>
            <Sidebar />
            <section className="max-h-[90vh] p-7 w-full overflow-y-auto hide-scrollbar bg-[#f4f4f4] custom-rounded">
                <div className="text-5xl mt-5 font-normal">Dashboard</div>
                <div className="text-3xl text-[#b6b5b8] w-[1680px] mt-2 font-normal flex items-center justify-between">
                    <span> Health Records</span>
                    <div className='flex gap-3' >

                    <div className='w-fit h-10 bg-[#ffffff] rounded-r-full rounded-l-full flex items-center justify-start px-1 gap-1 pr-3 cursor-pointer  '>

                    <Circle height='30' width='30' color='#f4f4f4' svg={CalendarIcon} svgColor='#000000' />
                    <div className='flex flex-row gap-2 items-center'>
                        <span className='text-xs text-[#000000] font-bold'>Sep 02 - Sep 09 </span>
                        <RotatedArrowIcon height={10} width={10} color='#000000' /> 

                    </div>
                    </div>

                    <div className='w-fit h-10 bg-[#ffffff] rounded-r-full rounded-l-full flex items-center justify-start px-1 gap-1 pr-3 cursor-pointer  '>

                        <Circle height='30' width='30' color='#f4f4f4' svg={ClockIcon} svgColor='#000000' />
                        <div className='flex flex-row gap-4 items-center'>
                            <span className='text-xs text-[#000000] font-bold'>24 hr </span>
                            <RotatedArrowIcon height={10} width={10} color='#000000' /> 

                        </div>
                        </div>


                    <div className='w-fit h-15 bg-[#000000] rounded-r-full rounded-l-full flex items-center justify-center px-1 gap-1  cursor-pointer '>

                   
                    <div className='flex flex-row'>
                        <span className='text-xs text-[#ffffff] font-bold'>Weekly  </span>

                    </div>
                    <Circle height='30' width='30' color='#f4f4f4' svg={ArrowRightIcon} svgColor='#000000' />
                    </div>

                    </div>
                    
                </div>

                {/* Container for LineChartHome and NumberCards */}
                <div className="flex gap-6 mb-4 mt-5">
                    <div className="w-2/3 pr-2">
                        <LineChartHome />
                    </div>
                    <div className="w-1/6 pr-2">
                        <div className='flex flex-col gap-8'>
                            <NumberCard first='Oxygen' number='97.5' icon='%' last='±0.2% from last week' color='#FFFFFF' />
                            <NumberCard first='12:02' number='89' icon='bpm' last='±0.2% from last week' color='#deeff9' />
                        </div>
                    </div>
                    <div className="w-1/3">
                        <WellnessMetrics />
                    </div>
                </div>

                {/* Container for LollipopCharts aligned with LineChartHome */}
                <div className='flex w-full gap-5 items-start justify-start'>
                    <div className="my-6 w-[920px] flex justify-between  ">
                        <StatsCard />
                        <LollipopChart />
                    </div>
                    <div className='mt-4 ' >

                    <BreathComponent />
                    </div>
                </div>

                {/* Additional sections (e.g., CoolingTime, UnitChart, PowerChart) can go here */}
            </section>
        </div>
    );
}

export default Dashboard;

