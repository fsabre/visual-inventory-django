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
            <h1 className={"loc"}>Location n°{location.id} ({location.name})</h1>
            <div
                onClick={() => setLocationId(location.parent ?? 1)}
                className={"parent-back"}
            >
                <><svg xmlns="http://www.w3.org/2000/svg" className={"back-arrow"} height="24px" viewBox="0 -960 960 960" width="24px" fill="#1e1e1e80"><path d="m313-440 224 224-57 56-320-320 320-320 57 56-224 224h487v80H313Z"/></svg>
                 Parent</>
            </div>
            <CategorySelector value={searchedCategoryId} onChange={setSearchedCategoryId}/>
            
            <div className={"sub-loc-header"}>
                <h2 >Sub-locations : ({location.children.length}) </h2>
                <hr />
            </div>

            <div className={"tile-container"}>
                {location.children.map((child, idx) => (
                    <div
                        key={idx}
                        onClick={() => setLocationId(child.id)}
                        className={child.categories.map(cat => cat.id).includes(searchedCategoryId) ? "tile-highlighted" : "sub-loc-tile"}
                    >
                        {child.name}
                    </div>
                ))}
            </div>
            <div className={"contains-header"}>
                <h2>Contains : ({location.categories.length})</h2>
                <hr/>
            </div>
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
        <div className={"categories-selector"}>
            <div className={"cat-select-txt-select"}>
                <p >Select a category to look for :</p>
                <select
                    value={props.value}
                    onChange={ev => props.onChange(Number(ev.currentTarget.value) ?? 0)}>
                    <option value={0}></option>
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </select>
            </div>
        </div>
    );
}
