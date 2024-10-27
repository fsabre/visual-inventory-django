import {Location, Category} from "./models.ts";

const URL = "http://localhost:8000/api";

export async function getLocation(locationId: number): Promise<Location> {
    const res = await fetch(`${URL}/location/${locationId}?depth=1&categories=1`, {method: "GET"});
    return await res.json();
}

export async function getCategories(): Promise<Category[]> {
    const res = await fetch(`${URL}/category`, {method: "GET"});
    return await res.json();
}
