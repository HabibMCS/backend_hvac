
const Circle = ({ height, width, color, svg: SvgIcon, svgColor, linkTo , changeColor  }) => {
    return (
        <div
            className='flex items-center justify-center rounded-full border-2 border-[#F4F4F4] cursor-pointer'
            style={{
                height: `${height}px`,
                width: `${width}px`,
                backgroundColor: color,
            }}
            onClick={async()  => {
              await  changeColor();
              linkTo();

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

Circle.defaultProps = {
   linkTo: () => {},
    changeColor: () => {},
};

export default Circle;
