import './index.css';

function About({ pageSetter }) {
  return (
    <div className='wrapper'>
      <div className="nav-buttons">
        <button className="nav-button" onClick={() => { pageSetter('home') }}>Home</button>
      </div>
      <h1>About</h1>
    </div>

  );
}

export default About;