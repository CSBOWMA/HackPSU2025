import type {Class, ClassesResponse} from '../types/class.types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
const USER_ID = import.meta.env.VITE_USER_ID;

export const classApi = {
    getAllClasses: async (): Promise<Class[]> => {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${USER_ID}/classes`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: ClassesResponse = await response.json();
            return data.classes;
        } catch (error) {
            console.error('Error fetching classes:', error);
            throw error;
        }
    },

    getClassById: async (classId: string): Promise<Class> => {
        try {
            const response = await fetch(`${API_BASE_URL}/users/${USER_ID}/classes/${classId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data: Class = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching class:', error);
            throw error;
        }
    },
};