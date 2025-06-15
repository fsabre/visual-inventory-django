import {useEffect, useMemo, useRef, useState} from "preact/hooks";

import {getCategories, getLocation} from "./api.ts";
import {Category, Location} from "./models.ts";

// Default location used before loading initial location (with id 1)
const BLANK_LOCATION: Location = {
    id: 0,
    name: "",
    parent: null,
    children: [],
    categories: [],
    x: 0,
    y: 0,
    dx: 0,
    dy: 0
};

export function App() {
    const [locationId, setLocationId] = useState(1);
    const [location, setLocation] = useState<Location>(BLANK_LOCATION);
    const [searchedCategoryId, setSearchedCategoryId] = useState(0);  // 0 means no category searched

    useEffect(() => {
        console.log("locationId has changed to", locationId);
        (async function () {
            setLocation(await getLocation(locationId));
        })();
    }, [locationId]);

    const tileContainerParentRef = useRef<HTMLDivElement>(null);
    // Compute the total size of the tile container from its tiles
    const tileContainerWidth = useMemo(() => Math.max(0, ...location.children.map(child => child.x + child.dx)), [location]);
    const tileContainerHeight = useMemo(() => Math.max(0, ...location.children.map(child => child.y + child.dy)), [location]);
    // Compute the scale of the tile container, to fill the parent while keeping proportions
    const tileContainerScale = useMemo(() => {
        if (tileContainerParentRef.current === null || tileContainerWidth === 0 || tileContainerHeight === 0) {
            return 1;
        }
        return Math.min(
            tileContainerParentRef.current.clientWidth / tileContainerWidth,
            tileContainerParentRef.current.clientHeight / tileContainerHeight,
        );
    }, [tileContainerWidth, tileContainerHeight]);

    return (
        <div>
            <h1>Location n°{location.id} ({location.name})</h1>
            <div onClick={() => setLocationId(location.parent ?? 1)} className="parent">
                Parent
            </div>

            <CategorySelector value={searchedCategoryId} onChange={setSearchedCategoryId}/>

            <h2>Sub-locations :</h2>
            <div ref={tileContainerParentRef} className="tile-container-parent">
                <div
                    className="tile-container"
                    style={{
                        width: `${tileContainerWidth}px`,
                        height: `${tileContainerHeight}px`,
                        transform: `scale(${tileContainerScale})`,
                    }}
                >
                    {location.children.map((child, idx) => (
                        <div
                            key={idx}
                            onClick={() => setLocationId(child.id)}
                            className={child.categories.some(cat => cat.id === searchedCategoryId) ? "tile highlighted" : "tile"}
                            style={{
                                width: `${child.dx}px`,
                                height: `${child.dy}px`,
                                left: `${child.x}px`,
                                top: `${child.y}px`,
                            }}
                        >
                            {child.name}
                        </div>
                    ))}
                </div>
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
        getCategories().then(setCategories);
    }, []);

    return (
        <div>
            <p>Select a category to look for :</p>
            <select value={props.value} onChange={ev => props.onChange(Number(ev.currentTarget.value) || 0)}>
                <option value={0}></option>
                {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>
        </div>
    );
}
