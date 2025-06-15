export interface Location {
    id: number;
    name: string;
    parent: number | null;
    children: Location[];
    categories: Category[];
    x: number;
    y: number;
    dx: number;
    dy: number;
}

export interface Category {
    id: number;
    name: string;
}
