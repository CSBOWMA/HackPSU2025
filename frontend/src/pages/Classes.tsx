import { useNavigate } from 'react-router-dom';
import { useClasses } from '../hooks/useClasses';
import ClassCard from '../components/class/ClassCard';
import './Classes.css';

const Classes = () => {
    const { classes, loading, error, refetch } = useClasses();
    const navigate = useNavigate();

    const handleClassClick = (classId: string) => {
        navigate(`/class/${classId}`);
    };

    if (loading) {
        return (
            <div className="classes-container">
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Loading your classes...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="classes-container">
                <div className="error-message">
                    <h2>Error Loading Classes</h2>
                    <p>{error}</p>
                    <button onClick={refetch} className="retry-button">
                        Try Again
                    </button>
                </div>
            </div>
        );
    }

    if (classes.length === 0) {
        return (
            <div className="classes-container">
                <div className="empty-state">
                    <h2>No Classes Found</h2>
                    <p>You don't have any classes yet. Start by adding your first class!</p>
                </div>
            </div>
        );
    }

    return (
        <div className="classes-container">
            <div className="classes-header">
                <h1>My Classes</h1>
                <p className="classes-subtitle">
                    Manage your courses and access AI-powered learning assistance
                </p>
            </div>
            <div className="classes-grid">
                {classes.map((classData) => (
                    <ClassCard
                        key={classData.id}
                        classData={classData}
                        onClick={() => handleClassClick(classData.id)}
                    />
                ))}
            </div>
        </div>
    );
};

export default Classes;