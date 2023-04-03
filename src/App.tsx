import { useState } from "react";
import reactLogo from "./assets/react.svg";
import githubLogo from "./assets/github.svg";
import { invoke } from "@tauri-apps/api/tauri";
import DynamicSelect from "./components/DynamicSelect/DynamicSelect";
import "./App.css";

function App() {
    const [greetMsg, setGreetMsg] = useState("");
    const [name, setName] = useState("");

    async function greet() {
        setGreetMsg(await invoke("greet", { name }));
        console.log("d");
    }

    return (
        <div className="container">
            <h1>Welcome to Auto-Spammer!</h1>

            <div className="row">
                <a
                    href="https://github.com/lucascompython/auto-spammer"
                    target="_blank"
                >
                    <img
                        src={githubLogo}
                        className="logo github"
                        alt="Github logo"
                    />
                </a>
            </div>

            <p>Click on the Github link to learn more.</p>

            <div className="row">
                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        greet();
                    }}
                >
                    <DynamicSelect />
                    {/*
                    <input
                        id="greet-input"
                        onChange={(e) => setName(e.currentTarget.value)}
                        placeholder="Enter the message"
                    />
                  */}
                    <br />
                    <button type="submit">Apply</button>
                </form>
            </div>
            <p>{greetMsg}</p>
        </div>
    );
}

export default App;
