{/* <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">
  <text x="50%" y="50%" font-family="Arial" font-size="30" fill="black" text-anchor="middle" alignment-baseline="middle">BMD</text>
</svg> */}

function BMD({ height, width, color }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 100 100" 
      width={width} 
      height={height}
    >
      <text x="50%" y="50%" font-family="Arial" font-size="30" fill={color} text-anchor="middle" alignment-baseline="middle">BMD</text>
    </svg>
  );
}

export default BMD;
