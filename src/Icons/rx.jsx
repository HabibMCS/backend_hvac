{/* <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <text x="50%" y="45%" font-family="Arial" font-size="50" fill="black" text-anchor="middle" alignment-baseline="middle">R</text>
  <line x1="30" y1="60" x2="70" y2="90" stroke="black" stroke-width="5"/>
</svg> */}

function Rx({ height, width, color }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 100 100" 
      width={width} 
      height={height}
    >
      <text x="50%" y="45%" font-family="Arial" font-size="50" fill={color} text-anchor="middle" alignment-baseline="middle">R</text>
      <line x1="30" y1="60" x2="70" y2="90" stroke={color} strokeWidth="5"/>
    </svg>
  );
}

export default Rx;
