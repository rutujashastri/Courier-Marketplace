import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useUserContext } from "../components/UserContext";
import Profile from "./Profile";

const Auth = () => {
  const { token, userData, setTokenAndUserData, clearUserData } =
    useUserContext();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const code = queryParams.get("code");
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (code && !token && !userData) {
      const tokenRequestBody = {
        grant_type: "authorization_code",
        code: code,
        client_id: "courierMarketplace",
      };

      fetch("https://accounts.fetch.ai/v1/tokens", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(tokenRequestBody),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((tokenData) => {
          if (tokenData.access_token) {
            setTokenAndUserData(tokenData.access_token, null);

            fetch("https://accounts.fetch.ai/v1/profile", {
              headers: {
                Authorization: `Bearer ${tokenData.access_token}`,
              },
            })
              .then((response) => response.json())
              .then((userData) => {
                setTokenAndUserData(tokenData.access_token, userData);
                setIsLoading(false);
                localStorage.setItem('faunaToken:', tokenData.access_token);
                localStorage.setItem('userEmail:', userData.email);
                navigate("/auth-mobile");
              })
              .catch((error) => {
                console.error("Error fetching user data:", error);
                setIsLoading(false);
              });

          } else {
            console.error("No token received");
            setIsLoading(false);
          }
        })
        .catch((error) => {
          console.error("Error during POST request:", error);
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, [code, token, userData, setTokenAndUserData]);

  // const handlePhone=() => {
  //   navigate("/auth-mobile");
  // }
  // const handleLogout = () => {
  //   // Clear user data and navigate to the login page
  //   clearUserData();
  //   navigate("/");
  // };
  // return (
  //   <div>
  //     <div className=" mx-auto text-center ">
  //       <h1 className="text-4xl text-black mt-[20vh]">Auth Page</h1>
      
  //       {/* {isLoading ? <div>Loading...</div> : token && userData && <Profile />} */}
  //       <button onClick={handlePhone} className="px-4 py-2 mt-4 w-20 rounded-full bg-green-500 text-white font-bold hover:bg-green-700 mx-auto">Next</button>
  //       <br></br>
  //       <button
  //         className="px-4 py-2 mt-4 rounded-full w-20 bg-red-500 text-white font-bold hover:bg-red-700 mx-auto"
  //         onClick={handleLogout} // Add a Logout button
  //       >
  //         Logout
  //       </button>
  //     </div> 
  //   </div>
  // );
};

export default Auth;
