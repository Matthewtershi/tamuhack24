'use client'

import React, { useState, useEffect } from 'react'; 
import Image from "next/image";  
import { ComposableMap, Geographies, Geography, Marker, useZoomPanContext, ZoomableGroup } from "react-simple-maps";
import countries from "../../client/public/countries-50m.json";
import redflame from "../../client/public/redflame.png";
import orangeflame from "../../client/public/orangeflame.png";
import yellowflame from "../../client/public/yellowflame.png";

const FireMarker = (props) => {
    const ctx = useZoomPanContext();

    let imageSrc = "";
    if (props.confidence > 0.8) {
        imageSrc = redflame.src;
    } else if (props.confidence > 0.6) {
        imageSrc = orangeflame.src;
    } else {
        imageSrc = yellowflame.src;
    }

    return (
        <Marker key={props.index} coordinates={props.coordinates}>
            <g>
                <image href={imageSrc} height={20} y={-15} x={-6.5}/>
            </g>
        </Marker>
    );
};

export default function Map() {
    const [hotspots, setHotspots] = useState(null);
    const [overlayVisible, setOverlayVisible] = useState(true); // State to control overlay visibility

    useEffect(() => {
        fetch('http://localhost:5000/api/hotspots')  // Flask runs on port 5000 by default
            .then(response => response.json())
            .then(data => setHotspots(data))
            .catch(error => console.error("Error fetching data:", error));
    }, []);

    const handleOverlayClick = () => {
        setOverlayVisible(false); // Hide the overlay on click
    };

    return (
        <div className="py-20 mx-40 asdfasdf" id="map">
            <h2 className="heading text-left text-7xl text-darkbrown font-extrabold"> WHAT WE DO </h2>
            <div className="text-darkbrown text-3xl p-20">
            Forecast is an interactive wildfire predictor that allows the average user to identify potential wildfire regions 
            without all the convoluted jargon. Whether you’re just curious to learn about wild fires or checking to see if your 
            area might be susceptible, Forecast provides an accessible solution for all.
            </div>
            {/* <h2 className="heading text-left text-7xl text-darkbrown font-extrabold py-5"> VIEW FIRE MAP </h2> */}

            <div className="w-fit h-auto items-center mx-auto border-8 border-darkbrown relative">
                {overlayVisible && (
                    <div
                        className="absolute top-0 left-0 bg-white opacity-60 z-10"
                        style={{ width: "80vw", height: "40vw" }}
                        onClick={handleOverlayClick}
                    ></div>
                )}

                {/* Centered text over the map */}
                {overlayVisible && (
                    <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center z-20">
                        <p className="text-5xl font-extrabold text-darkbrown">View Fire Map</p>
                    </div>
                )}

                <ComposableMap style={{ width: "80vw", height: "40vw", background: "#BFE9E0" }} projection="geoMercator">
                    <ZoomableGroup center={[0, 0]} zoom={1}>
                        <Geographies geography={countries}>
                            {({ geographies }) =>
                                geographies.map((geo) => (
                                    <Geography
                                        fill="#A2D998"
                                        strokeWidth={0.5}
                                        stroke="#fff"
                                        key={geo.rsmKey}
                                        geography={geo}
                                    />
                                ))
                            }
                        </Geographies>
                        {hotspots && hotspots.map((hotspot, i) => (
                            <FireMarker key={i} index={i} coordinates={[hotspot.point[1], hotspot.point[0]]} confidence={hotspot.confidence}/>
                        ))}
                    </ZoomableGroup>
                </ComposableMap>
            </div>
        </div>
    );
}
