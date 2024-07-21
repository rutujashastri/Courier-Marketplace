import React from 'react';

const Login = () => {
  const handleLogin = () => {
    const redirectUri = encodeURIComponent("http://localhost:3000/auth");
    const loginUrl = `https://accounts.fetch.ai/login/?redirect_uri=${redirectUri}&client_id=courierMarketplace&response_type=code`;

    // Navigate to the login URL
    window.location.href = loginUrl;
  };

  return (
    <div className='text-center mx-auto'>
      <h1 className='text-4xl text-white  mt-[20vh]'>Courier Marketplace</h1>
      <button className='mt-8 text-green-200 rounded-md hover:text-green-700 hover:bg-green-100 border-green-400 border-solid p-3 border-2' onClick={handleLogin}>Click to Login</button>
    </div>
  );
};

export default Login;
