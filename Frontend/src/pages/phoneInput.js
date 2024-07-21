import React, { useState, useEffect } from "react";
import axios from "axios";
import PhoneInput from "react-phone-number-input";
import "react-phone-number-input/style.css";
import Spinner from "../components/spinner";
import { useUserContext } from "../components/UserContext";
import { useNavigate } from "react-router-dom";

function MobileNumber() {
  const [otp, setOtp] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [otpError, setOtpError] = useState("");
  const [showOtpInput, setShowOtpInput] = useState(false);
  const { token, userData, phoneNumber, setPhoneNumberValue } =
    useUserContext();
  const [phoneInputValue, setPhoneInputValue] = useState(phoneNumber || "");

  const navigate = useNavigate();
  // const [faunaToken, setFaunaToken] = useState("");
  // const [userEmail, setUserEmail] = useState("");
  // useEffect(() => {
  //   // Retrieve Fauna token from local storage
  //   const token = localStorage.getItem("faunaToken:");
  //   console.log("token" + token);
    

  //     setFaunaToken(token);
  //     console.log("token line-29: " + faunaToken);

    

  //   // Retrieve user email from local storage
  //   const email = localStorage.getItem("userEmail:");

    

  //     setUserEmail(email);
  //   console.log("email line-39: " + userEmail);

    
  //   console.log("line 34:" + faunaToken + userEmail);
  // }, []);
  const handleSendOtp = async () => {
    try {
      setLoading(true);
      setOtpError(""); // Reset otpError when sending a new OTP
      setOtp("");

      if (!phoneInputValue || phoneInputValue.length < 5) {
        setOtpError("Invalid phone number");
        return;
      }

      // Save the phone number to context
      setPhoneNumberValue(phoneInputValue); // Use setPhoneNumberValue instead if you've changed the function name

      const response = await axios.post("http://127.0.0.1:8001/send-otp", {
        phone_number: phoneInputValue,
      });

      setStatus(`Send OTP Status: ${response.data.status}`);
      setShowOtpInput(true);
    } catch (error) {
      console.error("Error sending OTP:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    const email = localStorage.getItem("userEmail:");
    const token = localStorage.getItem("faunaToken:");
      console.log(email);
    try {
      setLoading(true);
    
      const response = await axios.post("http://127.0.0.1:8001/verify-otp", {
        phone_number: phoneInputValue,
        otp_code: otp,
        emailID: email,
        token: token,
      });

      setStatus(`Verify OTP Status: ${response.data.status}`);
      setOtpError(""); // Reset otpError when verification is successful
      navigate("/register");
    } catch (error) {
      console.error("Error verifying OTP:", error);

      setOtpError("Incorrect OTP. Please try again.");
      setStatus("Entered OTP is incorrect."); // Set status for incorrect OTP
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className=" mt-20 md:mx-80">
      <h1 className="text-2xl font-bold mb-4 text-white">OTP Verification</h1>

      {/* Phone Number Input */}
      <div className="mb-4">
        <label className="block mb-2 text-gray-100">Phone Number:</label>
        <PhoneInput
          international
          defaultCountry="US"
          value={phoneNumber}
          onChange={(value) => setPhoneInputValue(value)}
          className=" p-2 w-96 text-gray-900 bg-white"
        />
        {/* Display error only if phoneNumber is invalid */}
        {!showOtpInput && otpError && (
          <p className="text-red-500">{otpError}</p>
        )}
      </div>

      {/* Send OTP Button */}
      <button
        onClick={handleSendOtp}
        className="bg-blue-500 text-white py-2 px-4 rounded mb-4"
      >
        Send OTP
      </button>

      {/* OTP Input - Visible only after sending OTP */}
      {showOtpInput && (
        <div className="mb-4">
          <label className="block mb-2 text-gray-200">Enter OTP:</label>
          <input
            type="text"
            value={otp}
            onChange={(e) => setOtp(e.target.value)}
            className="border p-2 w-96"
          />
          {otpError && <p className="text-red-200">{otpError}</p>}
        </div>
      )}

      {/* Verify OTP Button - Visible only if OTP is entered */}
      {otp && (
        <button
          onClick={handleVerifyOtp}
          className="bg-green-500 text-white py-2 px-4 rounded mb-4"
        >
          Verify OTP
        </button>
      )}

      {/* Status Display */}
      <div>
        <h3 className="text-xl font-semibold mb-2 text-gray-200">Status:</h3>
        <p
          className={
            status.includes("success") ? "text-green-400" : "text-red-400"
          }
        >
          {status}
        </p>
      </div>

      {/* Loading Spinner */}
      {loading && <Spinner />}
    </div>
  );
}

export default MobileNumber;
