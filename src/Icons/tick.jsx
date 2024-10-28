function CheckmarkIcon({ height, width, color }) {
    return (
      <svg 
        viewBox="0 -0.5 25 25" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg" 
        height={height} 
        width={width}
      >
        <path 
          d="M5.5 12.5L10.167 17L19.5 8" 
          stroke={color} 
          strokeWidth={1.5} 
          strokeLinecap="round" 
          strokeLinejoin="round" 
        />
      </svg>
    );
  }
  
  export default CheckmarkIcon;
  