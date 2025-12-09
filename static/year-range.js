// // Updates the "from" input when the "from" slider/input changes
// function controlfromYear(fromSlider, fromYear, toYear, controlSlider) {
//     // Parse current values of fromYear and toYear into integers
//     const [from, to] = getParsed(fromYear, toYear);

//     // Fill the slider track with gradient colors between from and to
//     fillSlider(fromYear, toYear, '#C6C6C6', '#25daa5', controlSlider);

//     // If "from" exceeds "to", clamp it to "to"
//     if (from > to) {
//         fromSlider.value = to;
//         fromYear.value = to;
//     } else {
//         // Otherwise, just set the slider to the "from" value
//         fromSlider.value = from;
//     }
// }

// // Updates the "to" input when the "to" slider/input changes
// function controltoYear(toSlider, fromYear, toYear, controlSlider) {
//     // Parse current values
//     const [from, to] = getParsed(fromYear, toYear);

//     // Update slider gradient
//     fillSlider(fromYear, toYear, '#C6C6C6', '#25daa5', controlSlider);

//     // Handle overlapping slider z-index
//     setToggleAccessible(toYear);

//     // Clamp "to" value if necessary
//     if (from <= to) {
//         toSlider.value = to;
//         toYear.value = to;
//     } else {
//         toYear.value = from;
//     }
// }

// // Updates the "from" slider when the user drags it
// function controlFromSlider(fromSlider, toSlider, fromYear) {
//     // Parse slider values
//     const [from, to] = getParsed(fromSlider, toSlider);

//     // Update the gradient track
//     fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);

//     // Clamp "from" if it exceeds "to"
//     if (from > to) {
//         fromSlider.value = to - 1;
//         fromYear.value = to - 1;
//     } else {
//         fromYear.value = from;
//     }
// }

// // Updates the "to" slider when the user drags it
// function controlToSlider(fromSlider, toSlider, toYear) {
//     // Parse slider values
//     const [from, to] = getParsed(fromSlider, toSlider);

//     // Update the gradient track
//     fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);

//     // Handle z-index to make sliders draggable over each other
//     setToggleAccessible(toSlider);

//     // Clamp "to" if it goes below "from"
//     if (to <= from) {
//         toSlider.value = from +1;
//         toYear.value = from + 1;
//     } else {
//         toYear.value = to;
//         toSlider.value = to;
//     }
// }

// // Helper function: parse two input elements into integers
// function getParsed(currentFrom, currentTo) {
//     const from = parseInt(currentFrom.value, 10);
//     const to = parseInt(currentTo.value, 10);
//     return [from, to];
// }

// // Fills the slider track with gradient colors between "from" and "to"
// function fillSlider(from, to, sliderColor, rangeColor, controlSlider) {
//     const rangeDistance = to.max - to.min;              // Total slider range
//     const fromPosition = from.value - to.min;           // "from" relative position
//     const toPosition = to.value - to.min;              // "to" relative position

//     // Set the background as a linear gradient to show selected range
//     controlSlider.style.background = `linear-gradient(
//       to right,
//       ${sliderColor} 0%,
//       ${sliderColor} ${(fromPosition)/(rangeDistance)*100}%,
//       ${rangeColor} ${((fromPosition)/(rangeDistance))*100}%,
//       ${rangeColor} ${(toPosition)/(rangeDistance)*100}%, 
//       ${sliderColor} ${(toPosition)/(rangeDistance)*100}%, 
//       ${sliderColor} 100%)`;
// }

// // Adjust z-index of sliders so thumbs can overlap correctly
// function setToggleAccessible(currentTarget) {
//     const toSlider = document.querySelector('#toSlider');

//     // If the value is at minimum, bring it to front
//     if (Number(currentTarget.value) <= 0 ) {
//         toSlider.style.zIndex = 2;
//     } else {
//         toSlider.style.zIndex = 0;
//     }
// }

// // -------------------- Initialization --------------------

// // Get DOM elements
// const fromSlider = document.querySelector('#fromSlider');
// const toSlider = document.querySelector('#toSlider');
// const fromYear = document.querySelector('#fromYear');
// const toYear = document.querySelector('#toYear');

// // Initially fill the slider gradient
// fillSlider(fromSlider, toSlider, '#C6C6C6', '#25daa5', toSlider);

// // Set proper z-index for overlapping sliders
// setToggleAccessible(toSlider);

// // Attach event listeners for sliders and input fields
// fromSlider.oninput = () => controlFromSlider(fromSlider, toSlider, fromYear);
// toSlider.oninput = () => controlToSlider(fromSlider, toSlider, toYear);
// fromYear.oninput = () => controlfromYear(fromSlider, fromYear, toYear, toSlider);
// toYear.oninput = () => controltoYear(toSlider, fromYear, toYear, toSlider);


const fromSlider = document.getElementById('fromSlider');
const toSlider = document.getElementById('toSlider');
const fromYear = document.getElementById('fromYear');
const toYear = document.getElementById('toYear');

const min = parseInt(fromSlider.min);
const max = parseInt(toSlider.max);

// Update gradient for both sliders
function fillGradient() {
    const range = max - min;
    const fromPercent = ((parseInt(fromSlider.value) - min) / range) * 100;
    const toPercent = ((parseInt(toSlider.value) - min) / range) * 100;

    [fromSlider, toSlider].forEach(slider => {
        slider.style.background = `linear-gradient(
            to right,
            #C6C6C6 0%,
            #C6C6C6 ${fromPercent}%,
            #ffc107 ${fromPercent}%,
            #dc3545 ${toPercent}%,
            #C6C6C6 ${toPercent}%,
            #C6C6C6 100%
        )`;
    });
}

// Sync sliders → inputs with minimum gap 1
function updateFromSlider() {
    let from = parseInt(fromSlider.value);
    let to = parseInt(toSlider.value);

    if (from >= to) from = to - 1; // minimum gap 1
    fromSlider.value = from;
    fromYear.textContent = from;

    fillGradient();
}

function updateToSlider() {
    let from = parseInt(fromSlider.value);
    let to = parseInt(toSlider.value);

    if (to <= from) to = from + 1; // minimum gap 1
    toSlider.value = to;
    toYear.textContent = to;

    fillGradient();
}

// Initial fill
fillGradient();

// Event listeners
fromSlider.addEventListener('input', updateFromSlider);
toSlider.addEventListener('input', updateToSlider);
