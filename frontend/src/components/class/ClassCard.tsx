import type { Class } from '../../types/class.types';
import './ClassCard.css';

interface ClassCardProps {
    classData: Class;
    onClick?: () => void;
}

const ClassCard = ({ classData, onClick }: ClassCardProps) => {
    const backgroundColor = classData.color || '#646cff';

    return (
        <div
            className="class-card"
            onClick={onClick}
            style={{ borderLeftColor: backgroundColor }}
        >
            <div className="class-card-header">
                <h3 className="class-name">{classData.name}</h3>
                <span className="class-code">{classData.code}</span>
            </div>
            <div className="class-card-body">
                <p className="class-instructor">
                    <strong>Instructor:</strong> {classData.instructor}
                </p>
                <p className="class-schedule">
                    <strong>Schedule:</strong> {classData.schedule}
                </p>
                <p className="class-semester">
                    <strong>Semester:</strong> {classData.semester}
                </p>
                {classData.description && (
                    <p className="class-description">{classData.description}</p>
                )}
            </div>
        </div>
    );
};

export default ClassCard;