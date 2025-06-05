import { useEffect, useState , useMemo} from "preact/hooks";
import { Category, Location } from "./models.ts";
import { getCategories, getLocation } from "./api.ts";

const BLANK_LOCATION: Location = { id: 0, name: "", parent: null, children: [], categories: [], x:0, y:0, dx:0, dy:0 };

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

    // Overflow ellipsis sur les tuiles
    
    const containerWidth = useMemo(() => Math.max(...location.children.map(child => (child.x) + (child.dx)), 0), [location]) ; 
    const containerHeight = useMemo(() => Math.max(...location.children.map(child => (child.y) + (child.dy)), 0), [location]) ; 

    return (
        <div>
            <h1>Location n°{location.id} ({location.name})</h1>
            <div onClick={() => setLocationId(location.parent ?? 1)} className="parent">
                Parent
            </div>

            <CategorySelector value={searchedCategoryId} onChange={setSearchedCategoryId} />

            <h2>Sub-locations :</h2>
            <div  className="tile-container"
                style={{ width: `${containerWidth}px`, height: `${containerHeight}px`   }}>
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

function CategorySelector({ value, onChange }: CategorySelectorProps) {
    const [categories, setCategories] = useState<Category[]>([]);

    useEffect(() => {
        getCategories().then(setCategories);
    }, []);

    return (
        <div>
            <p>Select a category to look for :</p>
            <select value={value} onChange={ev => onChange(Number(ev.currentTarget.value) || 0)}>
                <option value={0}></option>
                {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>
        </div>
    );
}
