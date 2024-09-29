import React from "react";
import "../../client/public/general.css";

const Footer = () => {
    return (
        <>
        <div className="bg-lightbrown h-[6vh] w-full"></div>
        <footer className="text-white py-4 bg-darkbrown h-auto w-full asdfasdf">
            <div className="container mx-auto text-center">
                <h2 className="text-lg font-bold mb-2">Hackathon Creators</h2>
                <ul className="space-y-1">
                    <li>
                        <span className="font-semibold">Matthew Shi</span> -
                        <a href="mailto:matthew.shi@example.com" className="text-blue-400 hover:underline"> matthew.shi@example.com</a>
                    </li>
                </ul>
                <p className="mt-4 text-sm">© 2024 Texas A&M University Hackathon. All Rights Reserved.</p>
            </div>
        </footer>
        </>

    );
}

export default Footer