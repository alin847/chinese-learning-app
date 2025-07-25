import "./ProgressBar.css";

function ProgressBar({ currentIndex, length }) {
    return (
        <div className="progress-bar">
            <div className="progress-bar-text">{Math.round((currentIndex / length) * 100)}%</div>
            <div className="progress-bar-fill" style={{ width: `${(currentIndex / length) * 100}%` }}></div>
        </div>
    );
}

export default ProgressBar;



