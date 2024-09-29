import React from "react";
import "../../client/public/general.css";
import asdf from "../../client/public/head4.png";

const Footer = () => {
    return (
        <>
        <div className="bg-lightbrown h-[6vh] w-full"></div>
        <footer className="text-white py-4 bg-darkbrown h-auto w-full asdfasdf">
            <div className="container mx-auto text-center">
                <h2 className="text-lg font-bold mb-2"> Project Creators </h2>
                <ul className="flex space-y-1">
                    {/* <Image src={asdf} alt={""} className="" />  */}
                    <li>
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthewtershi@tamu.com" className="text-blue-400 hover:underline"> matthewtershi@tamu.edu </a>
                    </li>
                    <li>
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthewtershi@tamu.com" className="text-blue-400 hover:underline"> matthewtershi@tamu.edu </a>
                    </li>
                    <li>
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthewtershi@tamu.com" className="text-blue-400 hover:underline"> matthewtershi@tamu.edu </a>
                    </li>
                    <li>
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthewtershi@tamu.com" className="text-blue-400 hover:underline"> matthewtershi@tamu.edu </a>
                    </li>
                </ul>
                <p className="mt-4 text-sm">© 2024 Texas A&M University Hackathon. All Rights Reserved.</p>
            </div>
        </footer>
        </>

    );
}

export default Footer