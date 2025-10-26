import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import type { Class } from '../types/class.types';
import { classApi } from '../services/classApi';
import './ClassDetail.css';

const ClassDetail = () => {
    const { classId } = useParams<{ classId: string }>();
    const navigate = useNavigate();
    const [classData, setClassData] = useState<Class | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchClassData = async () => {
            if (!classId) {
                setError('No class ID provided');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);
                const data = await classApi.getClassById(classId);
                setClassData(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch class details');
            } finally {
                setLoading(false);
            }
        };

        fetchClassData();
    }, [classId]);

    const handleStartChat = () => {
        // Navigate to chat with class context
        navigate('/chat', { state: { classId, className: classData?.name } });
    };

    const handleBack = () => {
        navigate('/classes');
    };

    if (loading) {
        return (
            <div className="class-detail-container">
                <div className="loading-spinner">
                    <div className="spinner"></div>
                    <p>Loading class details...</p>
                </div>
            </div>
        );
    }

    if (error || !classData) {
        return (
            <div className="class-detail-container">
                <div className="error-message">
                    <h2>Error Loading Class</h2>
                    <p>{error || 'Class not found'}</p>
                    <button onClick={handleBack} className="back-button">
                        Back to Classes
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="class-detail-container">
            <button onClick={handleBack} className="back-button-top">
                ← Back to Classes
            </button>

            <div className="class-detail-header" style={{ borderLeftColor: classData.color || '#646cff' }}>
                <div className="class-header-content">
                    <div className="class-title-section">
                        <h1 className="class-title">{classData.name}</h1>
                        <span className="class-code-badge">{classData.code}</span>
                    </div>
                    <button onClick={handleStartChat} className="chat-button">
                        💬 Start AI Chat
                    </button>
                </div>
            </div>

            <div className="class-detail-content">
                <div className="info-card">
                    <h2>Class Information</h2>
                    <div className="info-grid">
                        <div className="info-item">
                            <span className="info-label">Instructor:</span>
                            <span className="info-value">{classData.instructor}</span>
                        </div>
                        <div className="info-item">
                            <span className="info-label">Schedule:</span>
                            <span className="info-value">{classData.schedule}</span>
                        </div>
                        <div className="info-item">
                            <span className="info-label">Semester:</span>
                            <span className="info-value">{classData.semester}</span>
                        </div>
                    </div>
                    {classData.description && (
                        <div className="class-description-section">
                            <h3>Description</h3>
                            <p>{classData.description}</p>
                        </div>
                    )}
                </div>

                <div className="actions-card">
                    <h2>Quick Actions</h2>
                    <div className="action-buttons">
                        <button className="action-btn primary" onClick={handleStartChat}>
                            <span className="action-icon">💬</span>
                            <div className="action-content">
                                <h3>Ask AI Assistant</h3>
                                <p>Get help with course materials and assignments</p>
                            </div>
                        </button>

                        <button className="action-btn">
                            <span className="action-icon">📚</span>
                            <div className="action-content">
                                <h3>View Materials</h3>
                                <p>Access lecture notes, slides, and resources</p>
                            </div>
                        </button>

                        <button className="action-btn">
                            <span className="action-icon">📝</span>
                            <div className="action-content">
                                <h3>Assignments</h3>
                                <p>Check upcoming deadlines and submissions</p>
                            </div>
                        </button>

                        <button className="action-btn">
                            <span className="action-icon">📊</span>
                            <div className="action-content">
                                <h3>Progress</h3>
                                <p>Track your performance and grades</p>
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ClassDetail;