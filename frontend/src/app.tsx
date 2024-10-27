import {useEffect, useState} from "preact/hooks";

import {Category, Location} from "./models.ts";
import {getCategories, getLocation} from "./api.ts";

const BLANK_LOCATION: Location = {id: 0, name: "", parent: null, children: [], categories: []};

export function App() {
    const [locationId, setLocationId] = useState(1);
    const [location, setLocation] = useState<Location>(BLANK_LOCATION);
    const [searchedCategoryId, setSearchedCategoryId] = useState(0);

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
            <CategorySelector value={searchedCategoryId} onChange={setSearchedCategoryId}/>
            <h2>Sub-locations :</h2>
            <div className={"tile-container"}>
                {location.children.map((child, idx) => (
                    <div
                        key={idx}
                        onClick={() => setLocationId(child.id)}
                        className={child.categories.map(cat => cat.id).includes(searchedCategoryId) ? "tile highlighted" : "tile"}
                    >
                        {child.name}
                    </div>
                ))}
            </div>
            <h2>Contains :</h2>
            <ul>
                {location.categories.map(cat => (
                    <li key={cat.id}>{cat.name}</li>
                ))}
            </ul>
        </div>
    );
}

interface CategorySelectorProps {
    value: number;
    onChange: (id: number) => void;
}

function CategorySelector(props: CategorySelectorProps) {
    const [categories, setCategories] = useState<Category[]>([]);

    useEffect(() => {
        getCategories().then(cats => setCategories(cats));
    }, []);

    return (
        <div>
            <p>Select a category to look for :</p>
            <select
                value={props.value}
                onChange={ev => props.onChange(Number(ev.currentTarget.value) ?? 0)}
            >
                <option value={0}></option>
                {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>
        </div>
    );
}
