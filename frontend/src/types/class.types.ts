export interface Class {
    id: string;
    name: string;
    code: string;
    instructor: string;
    schedule: string;
    semester: string;
    color?: string;
    description?: string;
}

export interface ClassesResponse {
    classes: Class[];
}