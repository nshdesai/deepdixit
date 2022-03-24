import React, { useState } from 'react';
import './index.css';

function Home({ pageSetter }) {

    return (
        <div className='wrapper'>
            <div className="nav-buttons">
                <button className="nav-button" onClick={() => { pageSetter('about') }}>About</button>
            </div>
            <h1>DeepDixit</h1>
            <h2>an AI-powered image guessing game</h2>

            <button className="bg-orange-500 w-1/5 hover:bg-orange-600 text-white rounded-full p-5 font-title text-3xl upper-gap" onClick={() => { pageSetter("game") }}>Play Now</button>
        </div>
    );
}

export default Home;