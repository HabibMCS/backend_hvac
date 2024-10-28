import React from 'react';

const Circle = ({ height, width, color, svg: SvgIcon, svgColor }) => {
    return (
        <div
            className='flex items-center justify-center rounded-full border-2 border-[#F4F4F4] cursor-pointer'
            style={{
                height: `${height}px`,
                width: `${width}px`,
                backgroundColor: color,
            }}
        >
            {/* The SVG size adjusts according to the circle size */}
            <SvgIcon
                height={height-15 }
                width={width-15 }
                color={svgColor}
            />
        </div>
    );
};

export default Circle;
