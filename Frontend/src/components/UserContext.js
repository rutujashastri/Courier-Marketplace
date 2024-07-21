import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const useUserContext = () => {
  return useContext(UserContext);
};

export const UserContextProvider = ({ children }) => {
  const [token, setToken] = useState(null);
  const [userData, setUserData] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState(''); // Initialize with an empty string or default value

  const setTokenAndUserData = (newToken, newUserData) => {
    setToken(newToken);
    setUserData(newUserData);
  };

  const setPhoneNumberValue = (newPhoneNumber) => {
    setPhoneNumber(newPhoneNumber);
  };

  const clearUserData = () => {
    setToken(null);
    setUserData(null);
    setPhoneNumber(''); // Clear the phone number
  };

  return (
    <UserContext.Provider value={{ token, userData, phoneNumber, setTokenAndUserData, setPhoneNumberValue, clearUserData }}>
      {children}
    </UserContext.Provider>
  );
};
