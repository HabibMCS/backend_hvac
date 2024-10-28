import { EnergyTable } from '@/components/EnergyTable/EnergyTable'
import { PowerChart } from '@/components/PowerChart/PowerChart'
import Sidebar from '@/components/Sidebar/Sidebar'
import { UnitChart } from '@/components/UnitChart/UnitChart'
import React from 'react'

const Energy = () => {
  return (
    <div className='flex'>
      <Sidebar />
      <section className="max-h-[90vh] p-4 w-[85vw] overflow-y-scroll">
        <div className="flex justify-between">
          <UnitChart />
          <PowerChart />
        </div>
        <div className="my-8">
          <EnergyTable />
        </div>
      </section>
    </div>
  )
}

export default Energy
