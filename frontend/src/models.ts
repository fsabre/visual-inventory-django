export interface Location {
    id: number;
    name: string;
    parent: number | null;
    children: Location[];
    categories: Category[];
}

export interface Category {
    id: number;
    name: string;
}
