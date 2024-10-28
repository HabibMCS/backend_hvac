function MenuIcon({ height, width, color }) {
    return (
      <svg 
        clipRule="evenodd" 
        fillRule="evenodd" 
        strokeLinejoin="round" 
        strokeMiterlimit="2" 
        viewBox="0 0 24 24" 
        xmlns="http://www.w3.org/2000/svg" 
        height={height} 
        width={width}
      >
        <path 
          d="M21 15.75c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75zm0-4c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75zm0-4c0-.414-.336-.75-.75-.75h-16.5c-.414 0-.75.336-.75.75s.336.75.75.75h16.5c.414 0 .75-.336.75-.75z" 
          fill={color} 
          fillRule="nonzero"
        />
      </svg>
    );
  }
  
  export default MenuIcon;
  