'use client'

import React, {useState, useEffect} from 'react';   
import { ComposableMap, Geographies, Geography, Marker, useZoomPanContext, ZoomableGroup } from "react-simple-maps";
import countries from "../../client/public/countries-50m.json";

const geoUrl =
  "/countries-50m.json";

const FireMarker = (props) => {
    const ctx = useZoomPanContext();

    return <Marker key={props.index} coordinates={props.coordinates}>
        <circle r={5/ctx.k} strokeWidth={2/ctx.k} fill="#F00" stroke="#fff" />
    </Marker>
}

export default function Map() {
    let [hotspots, setHotspots] = useState(null)

    useEffect(() => {
        fetch('http://localhost:5000/api/hotspots')  // Flask runs on port 5000 by default
          .then(response => response.json())
          .then(data => setHotspots(data))
          .catch(error => console.error("Error fetching data:", error));
      }, []);

    return (
        <ComposableMap style={{width: "800px", background: "#BFE9E0"}} projection="geoMercator">
            <ZoomableGroup center={[0, 0]} zoom={1}>
                <Geographies geography={countries}>
                    {({ geographies }) =>
                        geographies.map((geo) =>
                            <Geography fill="#A2D998" strokeWidth={0.5} stroke="#fff" key={geo.rsmKey} geography={geo} />
                        )
                    }
                </Geographies>
                {hotspots && hotspots.map((hotspot, i) => 
                    <FireMarker key={i} index={i} coordinates={hotspot}/>
                )}
            </ZoomableGroup>
        </ComposableMap>
    )
}