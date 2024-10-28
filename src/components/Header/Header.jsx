import React from 'react'
import { useState } from 'react'
import { Link } from 'react-router-dom'
import Circle from '../CricleIcon/Circle'
import ArrowComponent from '@/Icons/arrows'
import Wind from '@/Icons/wind'
import Sthetoscope from '@/Icons/sthetoscope'
import CustomArrowSVGIcon from '@/Icons/rotate'
import CheckmarkIcon from '@/Icons/tick'
import Heart from '@/Icons/heart'
import BellIcon from '@/Icons/bell'
import MenuIcon from '@/Icons/menuicon'


const Header = () => {
    const [date , setDate] = useState('Sat, 26 Aug')
    return (
        <header className='bg-white h-[10vh] p-3 flex items-center justify-between'>
            <div className='ml-4 flex items-start justify-start gap-10'>
                 <div className='w-32 h-10 bg-[#d7fd6a] rounded-r-full rounded-l-full flex items-center justify-between px-1 gap-1 pr-3  '>
                 <Circle height='30' width='30' color='#00454a' svg={Wind} svgColor='#d7fd6a' />
                 <div className='flex flex-col'>
                        <span className='text-xs text-[#00454a] font-bold'>Wind</span>
                        <span className='text-xs text-[#00454a] font-normal'>Speed</span>

                 </div>
                <ArrowComponent height='20' width='20' color='#00454a' />
                 </div>

                 <div className='flex items-start justify-start gap-3'>
                 <Circle height='40' width='40' color='#FFFFFF' svg={Sthetoscope} svgColor='#000000' />
                 <Circle height='40' width='40' color='#FFFFFF' svg={CustomArrowSVGIcon} svgColor='#000000' />
                 <Circle height='40' width='40' color='#FFFFFF' svg={CheckmarkIcon} svgColor='#000000' />
                 </div>

            </div>
           
            <div className='ml-4 flex items-start justify-start gap-6 pr-7'>
            <div className='flex items-start justify-start gap-1'>
                 <Circle height='40' width='40' color='#F4F4F4' svg={Heart} svgColor='#000000' />
                 <Circle height='40' width='40' color='#F4F4F4' svg={CustomArrowSVGIcon} svgColor='#000000' />
             </div>
                 <div className='w-fit h-10 bg-[#f4f4f4] rounded-r-full rounded-l-full flex items-center justify-start px-1 gap-1 pr-3  '>

                 <Circle height='30' width='30' color='#ffffff' svg={BellIcon} svgColor='#000000' />
                 <div className='flex flex-row'>
                        <span className='text-xs text-[#000000] font-bold'>{date} <span className='bg-black text-white w-5 h-5 p-1 rounded-t-full rounded-b-full' >5</span> </span>

                 </div>
                 </div>
                 <Circle height='50' width='50' color='#000000' svg={MenuIcon} svgColor='#ffffff' />


                

            </div>
        </header>
    )
}

export default Header
