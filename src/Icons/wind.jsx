function Wind({ height, width, color }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 100 100" 
      width={width} 
      height={height}
    >
      <line x1="50" y1="10" x2="50" y2="90" stroke={color} strokeWidth="5" />
      <line x1="10" y1="50" x2="90" y2="50" stroke={color} strokeWidth="5" />
      <line x1="20" y1="20" x2="80" y2="80" stroke={color} strokeWidth="5" />
      <line x1="80" y1="20" x2="20" y2="80" stroke={color} strokeWidth="5" />
    </svg>
  );
}

export default Wind;
