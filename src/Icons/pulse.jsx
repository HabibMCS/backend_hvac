{/* <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <path d="M 10 50 L 30 50 L 40 30 L 50 70 L 60 50 L 80 50" stroke="black" fill="none" stroke-width="5"/>
</svg> */}

function Pulse({ height, width, color }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 100 100" 
      width={width} 
      height={height}
    >
      <path d="M 10 50 L 30 50 L 40 30 L 50 70 L 60 50 L 80 50" stroke={color} fill="none" strokeWidth="5"/>
    </svg>
  );
}

export default Pulse;
