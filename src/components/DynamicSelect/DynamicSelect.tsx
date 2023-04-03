import { useState, useEffect, useRef } from "react";

const DynamicSelect = () => {
    //const [message, setMessage] = useState<{ [id: number]: string }>({});
    const [inputCount, setInputCount] = useState(2);
    //const [anotherOne, setAnotherOne] = useState(false);
    const [inputValues, setInputValues] = useState<string[]>([]);
    const inputRefs = useRef([]);
    const selectRefs = useRef();

    useEffect(() => {
        inputRefs.current = inputRefs.current.slice(0, inputCount);
    }, [inputCount]);

    const handleInputChange = (event, index) => {
        const { value } = event.target;
        setInputValues((prevValues) => {
            const newValues = [...prevValues];
            newValues[index] = value;
            return newValues;
        });

        if (index === inputCount - 1 && value !== "") {
            setInputCount(inputCount + 1);
        } else if (index === inputCount - 2 && value === "") {
            setInputCount(inputCount - 1);
            setInputValues((prevValues) => prevValues.slice(0, -1));
        }
    };
    const FKeysInput = ({ id }: { id: number }) => {
        //setInputCount(id);
        //setAnotherOne(false);

        console.log(inputCount);
        return (
            <>
                <select ref={selectRefs}>
                    <option value="F1">F1</option>
                    <option value="F2">F2</option>
                    <option value="F3">F3</option>
                    <option value="F4">F4</option>
                    <option value="F5">F5</option>
                    <option value="F6">F6</option>
                    <option value="F7">F7</option>
                    <option value="F8">F8</option>
                    <option value="F9">F9</option>
                    <option value="F10">F10</option>
                    <option value="F11">F11</option>
                    <option value="F12">F12</option>
                </select>
                <input
                    key={id}
                    id={`greet-input ${id}`}
                    onChange={(e) => {
                        //message[id] = e.currentTarget.value;
                        //let temp = structuredClone(message);
                        //temp[id] = e.currentTarget.value;
                        //setMessage(temp);
                        handleInputChange(e, id);
                        console.log("deposi");

                        //appendInput();
                    }}
                    placeholder="Enter the message"
                    value={inputValues[id]}
                    ref={(el) => (inputRefs.current[id] = el)}
                    onBlur={(event) => handleInputChange(event, id)}
                />
                <br />
            </>
        );
    };

    //useEffect(() => {
    //console.log("update");
    //if (message[inputCount] !== "") {
    //setAnotherOne(true);
    //setAnotherOne(false);
    //}
    //}, [message, inputCount]);

    //const renderedInputs = [];

    //for (let i = 0; i < inputCount; i++) {
    //renderedInputs.push(
    //<input
    //key={i}
    //type="text"
    //onChange={(event) => handleInputChange(event, i)}
    ///>
    ////<FKeysInput id={i} />
    //);
    //}

    return (
        <div id="dynamic-input">
            {[...Array(inputCount)].map((_, index) => (
                //<input
                //key={index}
                //type="text"
                //value={inputValues[index]}
                //onChange={(event) => handleInputChange(event, index)}
                ///>
                <FKeysInput id={index} />
            ))}
            {/*{renderedInputs.map((Input) => (
                <Input />
            ))} */}
        </div>
    );
};

export default DynamicSelect;
