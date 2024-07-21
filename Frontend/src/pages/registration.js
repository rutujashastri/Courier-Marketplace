import React, { useState } from "react";
import axios from "axios";
import { useUserContext } from "../components/UserContext";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [name, setName] = useState("");
  const [role, setRole] = useState("consumer");
  const [fastPrice, setFastPrice] = useState("");
  const [normalPrice, setNormalPrice] = useState("");
  const [slowPrice, setSlowPrice] = useState("");
  const { userData, phoneNumber, token } = useUserContext();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [nameError, setNameError] = useState("");
  const [roleError, setRoleError] = useState("");
  const navigate = useNavigate();
  const email = localStorage.getItem("userEmail:");
  const token1 = localStorage.getItem("faunaToken:");
  const calendar_token = localStorage.getItem("acessToken:");
  console.log("Email: " + email);
  console.log("Token: " + token1);
  console.log("Calendar: " + calendar_token);

  const handleRoleChange = (e) => {
    setRole(e.target.value);
  };

  const handleSubmit = async () => {
    // Reset errors
    setNameError("");
    setRoleError("");

    // Validate Name
    if (name.trim() === "") {
      setNameError("Name is required");
      return;
    }

    // Validate Role
    if (role === "") {
      setRoleError("Role is required");
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await axios.post("http://127.0.0.1:8001/register-user", {
        name,
        role,
        fast_price: fastPrice,
        normal_pace_price: normalPrice,
        slow_price: slowPrice,
        phone_number: phoneNumber,
        emailID: email,
        calendar_token: calendar_token,
        token1,
      });

      console.log(response.data.status); // Log the response status

      // Add any additional logic or redirection after successful registration if needed
    } catch (error) {
      console.error("Error during registration:", error);
      // Handle errors as needed
    }
    alert("You have registered successfully");
    setTimeout(() => {
      // Enable the submit button after the simulated API call
      setIsSubmitting(false);
      window.location.href="https://deltav.agentverse.ai/home";
    }, 1000);
  };

  return (
    <div className="container mx-auto md:px-80 mt-20">
      <h1 className="text-2xl font-bold mb-4 text-gray-200">Register</h1>

      <div className="mb-4">
        <label
          htmlFor="name"
          className="block text-sm font-medium text-gray-300"
        >
          Name
        </label>
        <input
          type="text"
          id="name"
          className={`mt-1 p-2 border rounded-md w-full ${
            nameError ? "border-red-500" : ""
          }`}
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        {nameError && <p className="text-red-500">{nameError}</p>}
      </div>

      <div className="mb-4">
        <label
          htmlFor="role"
          className="block text-sm font-medium text-gray-300"
        >
          Role
        </label>
        <select
          id="role"
          className={`mt-1 p-2 border rounded-md w-full ${
            roleError ? "border-red-500" : ""
          }`}
          value={role}
          onChange={handleRoleChange}
        >
          <option value="consumer">Consumer</option>
          <option value="courierProvider">Courier Provider</option>
        </select>
        {roleError && <p className="text-red-500">{roleError}</p>}
      </div>

      {role === "courierProvider" && (
        <div>
          <label className="block text-sm font-medium text-gray-300">
            Courier Prices
          </label>
          <div className="mb-4">
            <label
              htmlFor="fastPrice"
              className="block text-sm font-medium text-gray-300 mt-3"
            >
              Fast Price
            </label>
            <input
              type="number"
              id="fastPrice"
              className="mt-1 p-2 border rounded-md w-full"
              value={fastPrice}
              onChange={(e) => setFastPrice(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="normalPrice"
              className="block text-sm font-medium text-gray-300"
            >
              Normal Price
            </label>
            <input
              type="number"
              id="normalPrice"
              className="mt-1 p-2 border rounded-md w-full"
              value={normalPrice}
              onChange={(e) => setNormalPrice(e.target.value)}
            />
          </div>
          <div className="mb-4">
            <label
              htmlFor="slowPrice"
              className="block text-sm font-medium text-gray-300"
            >
              Slow Price
            </label>
            <input
              type="number"
              id="slowPrice"
              className="mt-1 p-2 border rounded-md w-full"
              value={slowPrice}
              onChange={(e) => setSlowPrice(e.target.value)}
            />
          </div>
        </div>
      )}

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-300">
          Phone Number
        </label>
        <input
          type="text"
          className="mt-1 p-2  rounded-md w-full cursor-not-allowed bg-gray-400"
          placeholder="Phone Number"
          value={phoneNumber}
          readOnly
        />
      </div>

      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-300">Email</label>
        <input
          type="text"
          className="mt-1 p-2  rounded-md w-full cursor-not-allowed bg-gray-400"
          placeholder="Email"
          // Assuming you have a prop or state for the email
          value={email}
          readOnly
        />
      </div>

      {/* Add submit button and handle form submission */}
      <button
        className={`bg-${
          isSubmitting ? "blue-200" : "blue-500"
        } text-white p-2 rounded-md mb-4`}
        onClick={handleSubmit}
        disabled={isSubmitting}
      >
        {isSubmitting ? "Submitting..." : "Submit"}
      </button>
    </div>
  );
};

export default Register;
