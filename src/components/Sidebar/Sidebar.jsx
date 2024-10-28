import React from 'react';
import { NavLink } from 'react-router-dom';
import Circle from '../CricleIcon/Circle';
import Wind from '../../Icons/wind.jsx';
import SpO2 from '@/Icons/sp2';
import Pulse from '@/Icons/pulse';
import BMD from '@/Icons/bmd';
import Rx from '@/Icons/rx';

const Sidebar = () => {
  const links = [
    { name: "Dashboard", icon: "/dashboard.png", path: "/dashboard" },
    { name: "Energy", icon: "/energy.png", path: "/energy" },
    { name: "Profile", icon: "/profile.png", path: "/profile" },
    { name: "Signout", icon: "/signout.png", path: "/" },
  ];

  return (
    <div className='bg-white w-[5vw] h-[90vh] flex flex-col '>
      <div className='bg-[#f4f4f4] flex flex-col h-fit  w-fit  ml-4 rounded-t-full rounded-b-full '>
        <div className='mt-2 mb-2 gap-2 w-14 flex flex-col items-center'>
        <Circle height='50' width='50' color='#FFFFFF' svg={Wind} svgColor='#8d8d8d' />
        <Circle height='50' width='50' color='#FFFFFF' svg={SpO2} svgColor='#8d8d8d' />
        <Circle height='50' width='50' color='#FFFFFF' svg={Pulse} svgColor='#8d8d8d' />
        <Circle height='50' width='50' color='#FFFFFF' svg={BMD} svgColor='#8d8d8d' />
        <Circle height='50' width='50' color='#FFFFFF' svg={Rx} svgColor='#8d8d8d' />

        </div>

      </div>
    </div>
  );
}

export default Sidebar;
