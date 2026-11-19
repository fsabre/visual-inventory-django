import type {Category, Location} from "./models.ts";

const URL = "http://localhost:8000/api";

export async function getLocation(locationId: number, searchedLocationId: number): Promise<Location> {
    const querystring: string = searchedLocationId ? `?search=${searchedLocationId}` : "";
    const res = await fetch(`${URL}/locations/${locationId}/${querystring}`, {method: "GET"});
    const data = await res.json();
    return {
        id: data.id,
        name: data.name,
        parent: data.parent,
        children: data.children,
        categories: data.categories,
        x: data.x,
        y: data.y,
        dx: data.dx,
        dy: data.dy,
        searchResults: data.search_result ?? [],
    };
}

export async function getCategories(): Promise<Category[]> {
    const res = await fetch(`${URL}/categories/`, {method: "GET"});
    return await res.json();
}
