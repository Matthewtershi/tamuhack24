import React from "react";
import Image from "next/image";
import "../../client/public/general.css";
import asdf from "../../client/public/brownlogo.png";

const Footer = () => {
    return (
        <>
        <div className="bg-lightbrown h-[6vh] w-full"></div>
        <footer className="text-white py-4 bg-darkbrown h-auto w-full asdfasdf">
            <div className="container mx-auto text-center">
                <ul className="space-y-1">
                    <Image src={asdf} alt={""} className="w-[18vw] mx-auto pb-5"/> 
                    <div>
                        <span className="justify-center font-semibold"> Arjun Mahableshwarkar</span> -
                        <a href="mailto:arjunallrounder@tamu.com" className="text-blue-400 hover:underline"> arjunallrounder@tamu.com </a>
                        &nbsp; &nbsp;
                        <span className="font-semibold"> Ananya Bandi </span> -
                        <a href="mailto:ananya_bandi@tamu.edu" className="text-blue-400 hover:underline"> ananya_bandi@tamu.edu </a>
                    </div>
                    <div>
                        <span className="font-semibold"> Noah Garcia </span> -
                        <a href="mailto:ndgarcia@tamu.edu" className="text-blue-400 hover:underline"> ndgarcia@tamu.edu </a>
                        &nbsp; &nbsp;
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthewtershi@tamu.com" className="text-blue-400 hover:underline"> matthewtershi@tamu.edu </a>
                    </div>
                </ul>
                <p className="mt-4 text-sm">© 2024 Texas A&M University Howdy Hack Hackathon. All Rights Reserved.</p>
            </div>
        </footer>
        </>

    );
}

export default Footer