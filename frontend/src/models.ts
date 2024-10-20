export interface Location {
    id: number;
    name: string;
    parent: number | null;
    children: Location[];
    categoryNames: string[];
}
