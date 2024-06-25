import {useEffect, useState} from "preact/hooks";

import {Location} from "./models.ts";
import {getLocation} from "./api.ts";

const BLANK_LOCATION: Location = {id: 0, name: "", parent: null, subLocations: [], categoryNames: []};

export function App() {
    const [locationId, setLocationId] = useState(1);
    const [location, setLocation] = useState<Location>(BLANK_LOCATION);

    useEffect(() => {
        console.log("locationId has changed to", locationId);
        (async function () {
            setLocation(await getLocation(locationId));
        })();
    }, [locationId]);

    return (
        <div>
            <h1>Location n°{location.id} ({location.name})</h1>
            <div
                onClick={() => setLocationId(location.parent ?? 1)}
                className={"tile"}
            >
                Parent
            </div>
            <h2>Sub-locations :</h2>
            <div className={"tile-container"}>
                {location.subLocations.map((sub, idx) => (
                    <div
                        key={idx}
                        onClick={() => setLocationId(sub.id)}
                        className={"tile"}
                    >
                        {sub.name}
                    </div>
                ))}
            </div>
            <h2>Contains :</h2>
            <ul>
                {location.categoryNames.map((catName, idx) => (
                    <li key={idx}>{catName}</li>
                ))}
            </ul>
        </div>
    );
}
