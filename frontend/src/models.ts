export interface Location {
    id: number;
    name: string;
    parent: number | null;
    children: Location[] | null;
    categories: Category[];
    x: number;
    y: number;
    dx: number;
    dy: number;
    searchResults: number[];
}

export interface Category {
    id: number;
    name: string;
}
