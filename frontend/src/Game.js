import './index.css';

function Game({ pageSetter }) {
    return (
        <div className='wrapper'>
            <div className="nav-buttons">
                <button className="nav-button" onClick={() => { pageSetter('home') }}>Home</button>
            </div>
            <h1>Game</h1>
        </div>

    );
}

export default Game;