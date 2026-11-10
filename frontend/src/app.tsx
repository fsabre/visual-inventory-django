import {useEffect, useMemo, useRef, useState} from "preact/hooks";

import {getCategories, getLocation} from "./api.ts";
import type {Category, Location} from "./models.ts";

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


    return (
        <div>
            <h1>Location n°{location.id} ({location.name})</h1>
            <div onClick={() => setLocationId(location.parent ?? 1)} className="parent">
                Parent
            </div>

            <CategorySelector value={searchedCategoryId} onChange={setSearchedCategoryId}/>

            <h2>Sub-locations :</h2>
            <TileViewer
                locations={location.children}
                searchedCategoryId={searchedCategoryId}
                onClick={setLocationId}
            />

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

interface ITileViewer {
    locations: Location[];
    searchedCategoryId: number;
    onClick: (locationId: number) => void;
}

function TileViewer(props: ITileViewer) {
    // The component will never use more that this in height.
    const MAX_HEIGHT = 800;

    const wrapperRef = useRef<HTMLDivElement>(null);
    const [wrapperSize, setWrapperSize] = useState({width: 0, height: 0});

    // Compute the total size of the tile container from its tiles
    const totalWidth = useMemo(
        () => Math.max(0, ...props.locations.map(child => child.x + child.dx)),
        [props.locations],
    );
    const totalHeight = useMemo(
        () => Math.max(0, ...props.locations.map(child => child.y + child.dy)),
        [props.locations],
    );
    // Compute the scale, to fill the wrapper while keeping proportions
    const scale = useMemo(() => {
        if (totalWidth === 0 || totalHeight === 0) {
            return 1;
        }
        // Max width is 100% of parent, max height is fixed, no minimums
        const scaleByWidth = wrapperSize.width / totalWidth;
        const scaleByHeight = MAX_HEIGHT / totalHeight;
        return Math.min(scaleByWidth, scaleByHeight);
    }, [totalWidth, totalHeight, wrapperSize]);

    useEffect(() => {
        const updateWrapperSize = () => {
            if (wrapperRef.current) {
                const clientRect = wrapperRef.current.getBoundingClientRect();
                setWrapperSize({width: clientRect.width, height: clientRect.height});
            }
        };
        updateWrapperSize();
        window.addEventListener("resize", updateWrapperSize);
        return () => window.removeEventListener("resize", updateWrapperSize);
    }, []);

    return (
        // The wrapper is used to compute available space to display the tiles.
        <div
            class="tile-container-wrapper"
            ref={wrapperRef}
        >
            {/*The container is used to fill the space, because the tiles inside are floating.*/}
            <div
                className="tile-container"
                style={{
                    width: (totalWidth * scale).toFixed() + "px",
                    height: (totalHeight * scale).toFixed() + "px",
                }}
            >
                {props.locations.map((child, idx) => (
                    <div
                        key={idx}
                        onClick={() => props.onClick(child.id)}
                        className={child.categories.some(cat => cat.id === props.searchedCategoryId) ? "tile highlighted" : "tile"}
                        style={{
                            width: (child.dx * scale).toFixed() + "px",
                            height: (child.dy * scale).toFixed() + "px",
                            left: (child.x * scale).toFixed() + "px",
                            top: (child.y * scale).toFixed() + "px",
                        }}
                    >
                        {child.name}
                    </div>
                ))}
            </div>
        </div>
    );
}