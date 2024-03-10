/* In comments ko koi delete nahi karna 

// const reactLogo = "react.svg"
// const viteLogo = "vite.svg"

// const reactLogoPath = `static/${reactLogo}`
// const viteLogoPath = `static/${viteLogo}`

// const

*/

import { useState } from "react";

function App() {
  const [input, setInput] = useState("");

  return (
    <div className="bg-black w-screen h-screen p-8">
      <div className="grid grid-cols-1 max-w-[600px] mx-auto gap-9 place-items-center">
        <div>
          <label htmlFor="areainput"></label>
          <textarea
            name="areainput"
            className="bg-slate-900 w-full text-white p-4 rounded-lg drop-shadow-2xl !outline-none"
            id=""
            cols="100"
            rows="5"
            placeholder="Enter the text...."
            onChange={(e) => {
                setInput(e.target.value)
                console.log(input)
            }}
          ></textarea>
        </div>
        <div className="flex gap-4 w-full">
          <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
            Image
          </button>
          <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
            Audio
          </button>
        </div>
        <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
          Submit
        </button>
      </div>
    </div>
  );
}

export default App;
