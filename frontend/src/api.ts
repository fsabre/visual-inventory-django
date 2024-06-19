import {Location} from "./models.ts";

const URL = "http://localhost:8000/api";

export async function getLocation(locationId: number): Promise<Location> {
    const res = await fetch(`${URL}/location/${locationId}?depth=1`, {method: "GET"});
    return await res.json();
}
