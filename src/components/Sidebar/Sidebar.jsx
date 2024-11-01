import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Circle from '../CricleIcon/Circle';
import Wind from '../../Icons/wind';
import SpO2 from '@/Icons/sp2';
import Pulse from '@/Icons/pulse';
import BMD from '@/Icons/bmd';
import Rx from '@/Icons/rx';

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Helper function to determine the active state based on pathname
  const getActiveStyles = (path) => {
    const isActive = location.pathname === path;
    return {
      color: isActive ? '#d7fd6a' : '#ffffff',
      svgColor: isActive ? '#00454a' : '#8d8d8d',
    };
  };

  // Handler to navigate to the selected path
  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <div className='bg-white w-[5vw] h-[90vh] flex flex-col'>
      <div className='bg-[#f4f4f4] flex flex-col h-fit w-fit ml-4 rounded-t-full rounded-b-full'>
        <div className='mt-2 mb-2 gap-2 w-14 flex flex-col items-center'>
          <Circle
            height='50'
            width='50'
            color={getActiveStyles('/dashboard').color}
            svg={Wind}
            svgColor={getActiveStyles('/dashboard').svgColor}
            linkTo={() => handleNavigation('/dashboard')}
          />
          <Circle
            height='50'
            width='50'
            color={getActiveStyles('/charts').color}
            svg={SpO2}
            svgColor={getActiveStyles('/charts').svgColor}
            linkTo={() => handleNavigation('/charts')}
          />
          <Circle
            height='50'
            width='50'
            color={getActiveStyles('/energy').color}
            svg={Pulse}
            svgColor={getActiveStyles('/energy').svgColor}
            linkTo={() => handleNavigation('/energy')}
          />
          <Circle
            height='50'
            width='50'
            color={getActiveStyles('/profile').color}
            svg={BMD}
            svgColor={getActiveStyles('/profile').svgColor}
            linkTo={() => handleNavigation('/profile')}
          />
          <Circle
            height='50'
            width='50'
            color='#ffffff'
            svg={Rx}
            svgColor='#8d8d8d'
          />
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
