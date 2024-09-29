import React from "react";
import Image from "next/image";
import { GlobeDemo } from "./ui/gridglobe";
import temp from "../../client/public/head2.png";
import frame from "../../client/public/frame2.png";
import yellow from "../../client/public/yellowflame.png";
import orange from "../../client/public/orangeflame.png";
import red from "../../client/public/redflame.png";
import "../../client/public/general.css";

const Hero = () => {
    return (
        <div className="w-full mx-auto h-[88vh] flex text-black">
            <div className="gap-x-10 mx-auto flex py-20 left-10">
                <div> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </div>
                <div className="flex-col flex mb-10 p-4 justify-center items-center">
                    <Image src={temp} alt={""} className="w-23"/> 
                    <button className="ihatevegans btn-34"> <span> Learn More! </span> </button>
                </div>

                <div className="flex flex-col relative right-0 top-[-25vh] w-[600px] h-[600px]">
                    <GlobeDemo />
                    <div className="" style= {{
                        transform: "translateX(65.77px) translateY(300px)",
                        width: "900px",
                        height: "auto",
                    }}
                    >

                        <Image src={frame} alt={""} className="w-23"/> 
                    </div>
                </div>
            </div>
        </div>

    );
}

export default Hero