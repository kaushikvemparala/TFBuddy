import './App.css';
import React, { useState } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [displayText, setDisplayText] = useState('');
  const [plot, setPlot] = useState(null);

  const handleInputChange = (e) => {
    setInputText(e.target.value);
  }

  const handleFileUpload = async (event) => {
    setSelectedFile(event.target.files[0]);
    const formData = new FormData();
    formData.append('file', event.target.files[0]);
    try {
      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log(data);
      setDisplayText(data.res);
    } catch (error) {
      console.error('Error:', error);
    }
  }

  const handleTextInput = (input = inputText) => {
    console.log("yooo", JSON.stringify({ text: input }))
    try {
      const response = fetch('http://127.0.0.1:5000/plot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Specify the content type as JSON
        },
        body: JSON.stringify({ text: input }),
      })
      .then(response => response.json())
      .then(data => {
          setTimeout(() => {
            setPlot(data.res);
          });
      });
    } catch (error) {
      console.error('Error:', error);
    }
  }

  if (selectedFile == null) {
    return (
      <div className="App">
        <header className="App-header" style={{background: 'linear-gradient(to bottom, orange, black)'}}>
          <img src={process.env.PUBLIC_URL + '/tensorflowlogo.png'} className="App-logo" alt="logo" />
          <p>
            Upload a TFEvent file to begin!
          </p>
          <input type="file" onChange={handleFileUpload} />
        </header>
      </div>
    );
  } else {
    return (
      <div className="App">
        <header className="App-header" style={{background: 'linear-gradient(to bottom, orange, black)'}}>
          <img src={process.env.PUBLIC_URL + '/tensorflowlogo.png'} className="App-logo" alt="logo" />
          <p>
            File uploaded!
          </p>
          <p>
            {displayText}
          </p>
          <p>
            Which one do you want to plot?
          </p>
          <input type="string" value={inputText} onChange={handleInputChange}/>
          <button onClick={() => handleTextInput()}>Submit</button>
          <img src={plot} alt="Plot" />
          <p>
            Or choose a new file.
          </p>
          <input type="file" onChange={handleFileUpload} />
        </header>
      </div>
    );
  }
}

export default App;
