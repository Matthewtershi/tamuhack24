import React from "react";
import Map from "./ui/Map.jsx";

const Hero = () => {
    return (
        <div className="w-full h-[80vh] flex text-black">
            <div> 
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt ut labore et dolore 
                magna aliqua. Ut enim ad minim veniam, quis nostrud 
                exercitation ullamco laboris nisi ut aliquip ex ea 
                commodo consequat. 
            </div>

            <div>
                <Map />
            </div>
        </div>
    );
}

export default Hero