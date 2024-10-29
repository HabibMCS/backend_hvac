import React from 'react'
import Sidebar from '@/components/Sidebar/Sidebar';
import CsvTable from '@/components/CsvHandler/Csvhandler';



 const Charts = () => {
    return (
        <div className='flex'>
            <Sidebar />
            <section className="max-h-[90vh] p-7 w-full overflow-y-auto hide-scrollbar bg-[#f4f4f4] custom-rounded">
                <div className="text-5xl mt-5 font-normal">Energy Consumption</div>
                

                {/* Container for LineChartHome and NumberCards */}
                <div className="flex gap-6 mb-4 mt-5">
                    <div className="w-full pr-2">
                        <CsvTable />
                    </div>
                   
                </div>

                {/* Container for LollipopCharts aligned with LineChartHome */}
                

                {/* Additional sections (e.g., CoolingTime, UnitChart, PowerChart) can go here */}
            </section>
        </div>
    );
}

export default Charts;
