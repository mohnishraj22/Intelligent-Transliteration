/* In comments ko koi delete nahi karna 

// const reactLogo = "react.svg"
// const viteLogo = "vite.svg"

// const reactLogoPath = `static/${reactLogo}`
// const viteLogoPath = `static/${viteLogo}`

*/

import { useState } from "react";
import axios from 'axios';

function App() {
  const [input, setInput] = useState("");

  const [formData, setFormData] = useState({});

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('/api/post_data/', formData)
            .then(response => {
                console.log(response.data);
                // Handle response data
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };

  return (
    // <div className="bg-black w-screen h-screen p-8">
    //   <div className="grid grid-cols-1 max-w-[600px] mx-auto gap-9 place-items-center">
    //     <div>
    //       <label htmlFor="areainput"></label>
    //       <textarea
    //         name="areainput"
    //         className="bg-slate-900 w-full text-white p-4 rounded-lg drop-shadow-2xl !outline-none"
    //         id=""
    //         cols="100"
    //         rows="5"
    //         placeholder="Enter the text...."
    //         onChange={(e) => {
    //             setInput(e.target.value)
    //             console.log(input)
    //         }}
    //       ></textarea>
    //     </div>
    //     <div className="flex gap-4 w-full">
    //       <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
    //         Image
    //       </button>
    //       <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
    //         Audio
    //       </button>
    //     </div>
    //     <button className="bg-orange-500 p-3 rounded-lg font-bold w-full">
    //       Submit
    //     </button>
    //   </div>
    // </div>
    <form onSubmit={handleSubmit} className="flex flex-col justify-center items-center gap-4 w-screen h-screen">
      <input type="text" name="username" className="border" onChange={handleChange} />
      <input type="email" name="email" className="border" onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}

export default App;

// const Component = () => {
//     const [formData, setFormData] = useState({});

//     const handleChange = (e) => {
//         setFormData({ ...formData, [e.target.name]: e.target.value });
//     };

//     const handleSubmit = (e) => {
//         e.preventDefault();
//         axios.post('/api/post_data/', formData)
//             .then(response => {
//                 console.log(response.data);
//                 // Handle response data
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//             });
//     };

//     return (
//         <form onSubmit={handleSubmit}>
//             <input type="text" name="username" onChange={handleChange} />
//             <input type="email" name="email" onChange={handleChange} />
//             <button type="submit">Submit</button>
//         </form>
//     );
// };