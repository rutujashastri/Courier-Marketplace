import React, { useEffect } from 'react';
import { useNavigate } from "react-router-dom";

const Calendar = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Retrieve the access_token from the URL fragment
    const token = new URLSearchParams(window.location.hash.substring(1)).get('access_token');

    if (token) {
      // Store the access_token in a variable
      const accessToken = token;

      // Print the access_token to the console
      console.log('Access Token from calendar.js:', accessToken);
      localStorage.setItem('acessToken:', accessToken);

      navigate("/auth-mobile")

      // You can perform further actions with the access_token as needed
    } else {
      console.error('Access Token not found in URL fragment');
    }
  }, []);

  // Render your calendar component or any other content
  return (
    null
  );
};

export default Calendar;
