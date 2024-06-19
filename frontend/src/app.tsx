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
            <p><a onClick={() => setLocationId(location.parent ?? 1)}>Go to parent</a></p>
            <p>Sub-locations :</p>
            <ul>
                {location.subLocations.map((sub, idx) => (
                    <li key={idx}><a onClick={() => setLocationId(sub.id)}>{sub.name}</a></li>
                ))}
            </ul>
            <p>Contains :</p>
            <ul>
                {location.categoryNames.map((catName, idx) => (
                    <li key={idx}>{catName}</li>
                ))}
            </ul>
        </div>
    );
}
