import { useState, useEffect } from 'react';
import type { Class } from '../types/class.types';
import { classApi } from '../services/classApi';

export const useClasses = () => {
    const [classes, setClasses] = useState<Class[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const fetchClasses = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await classApi.getAllClasses();
            setClasses(data);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to fetch classes');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchClasses();
    }, []);

    return {
        classes,
        loading,
        error,
        refetch: fetchClasses,
    };
};