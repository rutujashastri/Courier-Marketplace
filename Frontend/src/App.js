import "./App.css";
import Login from "./pages/login";
import Auth from "./pages/auth";
import Profile from "./pages/Profile";
import Register from "./pages/registration";
import PhoneInput from "./pages/phoneInput";
import { UserContextProvider } from "./components/UserContext"
import { Route, BrowserRouter, Routes } from "react-router-dom";
import LightShade from "./assets/light-shade.svg"
import StarDust from "./assets/content-hub-star-dust.svg"
import Reactangle from "./assets/footer-left-rectangle.svg"
import RectLeft from "./assets/content-hub-rectangle.svg"

function App() {
  return (
    <UserContextProvider>
      <div className=" flex flex-col  bg-[#000d3d] min-h-screen">
      <img
        src={StarDust}
        alt="rectangle-image"
        className="absolute right-20 top-5 z-[10] hidden md:block"
        width={200}
        height={200}
      />
      <img
        src={LightShade}
        alt="rectangle-image"
        className="absolute right-10 z-[10] hidden md:block"
        width={250}
        height={250}
      />
      <img
        src={Reactangle}
        alt="rectangle-image"
        className="absolute left-0 top-20 z-[10] hidden md:block"
        width={180}
        height={180}
      />
      <img
        src={RectLeft}
        alt="rectangle-image"
        className="absolute right-0 z-[10] hidden md:block"
        width={160}
        height={160}
      />
      <div className="contentHubDark absolute -z-40 hidden h-[600px] w-full md:block">
        <div className="contentHubShade absolute -z-50 hidden h-[700px] w-full md:block"></div>
      </div>
      <div className="z-[20]">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/register" element={<Register />} />
          <Route path="/calendar-login" element={<Register />} />
          <Route path="/auth-mobile" element={<PhoneInput />} />


          {/* Add other routes here */}
        </Routes>
      </BrowserRouter>
      </div>
    </div>

    </UserContextProvider>
  );
}

export default App;
