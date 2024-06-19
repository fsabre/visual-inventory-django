export interface Location {
    id: number;
    name: string;
    parent: number | null;
    subLocations: Location[];
    categoryNames: string[];
}
