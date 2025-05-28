import {Category, Location} from "./models.ts";

const URL = "http://localhost:8000/api";

export async function getLocation(locationId: number): Promise<Location> {
    const res = await fetch(`${URL}/locations/${locationId}/`, {method: "GET"});
    return await res.json();
}

export async function getCategories(): Promise<Category[]> {
    const res = await fetch(`${URL}/categories/`, {method: "GET"});
    return await res.json();
}
