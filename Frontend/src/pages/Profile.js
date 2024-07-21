// import React from 'react';
// import { useUserContext } from '../components/UserContext';
// import { useNavigate } from "react-router-dom";


// function Profile() {
//   const navigate = useNavigate();

//   const { token, userData } = useUserContext();
//   const handleNext = async () => {
//     navigate("/register");
//   };
//   if (token && userData) {
//     return (
//       <div className='text-lg text-left break-words mx-40 mt-6'>
//         <p className='my-12'>Token: {token}</p>
//         <p className='my-12'>Email: {userData.email}</p>
//         <button onClick={handleNext} className='py-2 px-4 bg-green-400 rounded-2xl hover:bg-green-300 mb-4'>Next</button>
//         <img src={userData.image_url}></img>
//         {/* Add more user data as needed */}
        
//       </div>
//     );
//   } else {
//     return <div>Please log in to view your profile.</div>;
//   }
// }

// export default Profile;
