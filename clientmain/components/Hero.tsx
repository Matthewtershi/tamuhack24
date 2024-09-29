import React from "react";
import Image from "next/image";
import { GlobeDemo } from "./ui/gridglobe";
import temp from "../../client/public/head3.png";
import frame from "../../client/public/frame2.png";
import "animate.css"
import yellow from "../../client/public/yellowflame.png";
import orange from "../../client/public/orangeflame.png";
import red from "../../client/public/redflame.png";
import "../../client/public/general.css";

const Hero = () => {
    return (
        <div className="w-full mx-auto h-[88vh] flex text-black">
            <div className="gap-x-10 mx-auto flex py-20 left-10 overflow-hidden" style={{
                userSelect: "none",
                transform: "translateX(50px)",
                }}>
                <div> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </div>
                <div className="flex-col flex mb-10 p-4 justify-center items-center">
                    <div className="flex gap-x-10">
                        <Image src={yellow} alt={""} style={{
                            width:"100px",
                            height:"100px",
                        }}/> 
                        <Image src={orange} alt={""} style={{
                            width:"100px",
                            height:"100px",
                        }}/> 
                        <Image src={red} alt={""} style={{
                            width:"100px",
                            height:"100px",
                        }}/> 
                    </div>
                    <Image src={temp} alt={""} className="w-21"/> 
                    <button className="animate_animated animate_slideInLeft btn-34"> <span> Learn More! </span> </button>
                </div>
                <div className="flex flex-col relative right-50px top-[-25vh] w-[600px] h-[600px]" style={{
                    transform: "translateY(50px)",
                }}>
                    <GlobeDemo />
                    <div style= {{
                        transform: "translateX(-435px) translateY(115px)",
                        width: "1100px",
                        height: "1100px",
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