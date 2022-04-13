import './index.css';

function Results({ pageSetter }) {
    return (
        <div className='wrapper'>
            <div className="nav-buttons">
                <button className="nav-button" onClick={() => { pageSetter('home') }}>Home</button>
            </div>
            <h1>Results</h1>
        </div>

    );
}

export default Results;