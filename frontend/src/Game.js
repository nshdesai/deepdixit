import './index.css';

function Game({ pageSetter }) {
    return (
        <div className='wrapper'>
            <div className="nav-buttons">
                <button className="nav-button" onClick={() => { pageSetter('home') }}>Home</button>
                <button className="nav-button" onClick={() => { pageSetter('results') }}>Results</button>
            </div>
            <img src="https://media.giphy.com/media/3o7btLnjQXZqQQqZ3S/giphy.gif" alt="" />
            <div className="multiple-choice">
                <button>Choice 1</button>
                <button>Choice 2</button>
                <button>Choice 3</button>
                <button>Choice 4</button>
            </div>
        </div>

    );
}

export default Game;