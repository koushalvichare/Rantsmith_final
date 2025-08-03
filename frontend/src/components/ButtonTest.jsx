import React from 'react';

const ButtonTest = () => {
  const handleClick = () => {
    alert('Button clicked successfully!');
    console.log('Button clicked!');
  };

  return (
    <div className="fixed top-4 right-4 z-50 bg-red-500 p-4 rounded-lg">
      <h3 className="text-white mb-2">Button Test</h3>
      <button 
        onClick={handleClick}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded cursor-pointer"
        style={{ zIndex: 9999, position: 'relative' }}
      >
        Click Me!
      </button>
      <button 
        onClick={() => {
          console.log('Second button clicked!');
          alert('Second button works!');
        }}
        className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded ml-2 cursor-pointer"
        style={{ zIndex: 9999, position: 'relative' }}
      >
        Test 2
      </button>
    </div>
  );
};

export default ButtonTest;
