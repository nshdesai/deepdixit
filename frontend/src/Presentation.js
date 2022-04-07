import React, { useState, useEffect } from 'react';
import './index.css';

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

function Presentation({ pageSetter }) {

    const [randImage, setRandImage] = useState({ image: null, prompts: [] });
    const [btnColors, setBtnColors] = useState(['bg-amber-100', 'bg-amber-100', 'bg-amber-100', 'bg-amber-100']);
    const [choiceSelected, setChoiceSelected] = useState(-1);
    const [score, setScore] = useState(0);
    const [rounds, setRounds] = useState(0);
    const [nexts, setNexts] = useState(0);
    const [nextImgIds, setNextImgIds] = useState([]);

    useEffect(() => {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nextImgIds: nextImgIds })
        };

        fetch(`${process.env.REACT_APP_BACKEND_URL}/random-image`, requestOptions)
            .then(res => res.json())
            .then(data => {
                shuffleArray(data.prompts);
                console.log(rounds);
                setRandImage({ image: data.image, prompts: data.prompts });
                setNextImgIds(data.nextImgIds);
            })
            .catch(err => console.log(err));
    }, [nexts]);

    return (
        <div className='wrapper'>
            <div className="nav-buttons">
                <button className="nav-button" onClick={() => { pageSetter('home') }}>Home</button>
                <button className="nav-button" onClick={() => { pageSetter('results') }}>Results</button>
                <button className="nav-button" onClick={() => { pageSetter('game') }}>Normal</button>
            </div>
            <div className='score-presentation max-w-2xl rounded-2xl overflow-hidden shadow-2xl bg-stone-50 p-5 mt-20'>
                {score}/{rounds}
            </div>
            <div class="max-w-2xl rounded-2xl overflow-hidden shadow-2xl bg-orange-400 p-10 mt-20 img-card-presentation">
                <img src={`data:image/png;base64, ${randImage.image}`} className="rounded-2xl" />
            </div>
            <div className="multiple-choice-presentation">
                {randImage.prompts.map((prompt, index) => {
                    return (
                        <button className={`choice ${btnColors[index]} ` + `${choiceSelected != -1 ? (index === choiceSelected ? 'text-white ' : '') : 'hover:bg-amber-50'} rounded-full shadow-xl p-2 text-center text-4xl w-80`} onClick={() => {
                            if (prompt.real === true && choiceSelected === -1) {
                                let newBtnColors = btnColors.slice();
                                newBtnColors[index] = 'bg-emerald-400';
                                setBtnColors(newBtnColors);
                                setChoiceSelected(index);
                                setScore(score + 1);
                                setRounds(rounds + 1);
                            } else if (prompt.real === false && choiceSelected === -1) {
                                let newBtnColors = btnColors.slice();
                                newBtnColors[index] = 'bg-red-500';
                                newBtnColors[randImage.prompts.map((p) => { return p.real === true }).indexOf(true)] = 'bg-emerald-400';
                                setBtnColors(newBtnColors);
                                setChoiceSelected(index);
                                setRounds(rounds + 1);
                            }
                        }}>{prompt.prompt}</button>
                    )
                }, this)}
            </div>
            {choiceSelected !== -1 && (
                <button className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-4 font-title text-4xl mb-12 next-btn" onClick={() => {
                    let newBtnColors = btnColors.slice();
                    newBtnColors.fill('bg-amber-100');
                    setBtnColors(newBtnColors);
                    setChoiceSelected(-1);
                    setNexts(nexts + 1);
                }}>
                    Next Round
                </button>
            )}
        </div>

    );
}

export default Presentation;
