const problemType = document.getElementById('problemType');
const dynamicInputs = document.getElementById('dynamicInputs');
const solveButton = document.getElementById('solveButton');
const stepsContainer = document.getElementById('stepsContainer');
const resultContainer = document.getElementById('resultContainer');

// Show inputs dynamically
problemType.addEventListener('change', () => {
  const type = problemType.value;
  dynamicInputs.innerHTML = '';

  if(type === "derivative" || type === "integral" || type === "simplify" || type === "arithmetic") {
    dynamicInputs.innerHTML = `<input type="text" id="expression" placeholder="Enter expression">`;
  } 
  else if(type === "solve_quadratic") {
    dynamicInputs.innerHTML = `
      <input type="number" id="a" placeholder="Coefficient a">
      <input type="number" id="b" placeholder="Coefficient b">
      <input type="number" id="c" placeholder="Coefficient c">
    `;
  } 
  else if(type === "solve_linear") {
    dynamicInputs.innerHTML = `
      <input type="number" id="a" placeholder="Coefficient a">
      <input type="number" id="b" placeholder="Coefficient b">
    `;
  } 
  else if(type === "percentage") {
    dynamicInputs.innerHTML = `
      <input type="number" id="part" placeholder="Part value">
      <input type="number" id="total" placeholder="Total value">
    `;
  } 
  else if(type === "matrix") {
    dynamicInputs.innerHTML = `<textarea id="matrix" placeholder="Enter matrix as [[1,2],[3,4]]"></textarea>`;
  }
});

// Solve button
solveButton.addEventListener('click', async () => {
  const type = problemType.value;
  if(!type) return;

  let values = {};

  if(type === "derivative" || type === "integral" || type === "simplify" || type === "arithmetic") {
    values.expression = document.getElementById('expression').value;
  } 
  else if(type === "solve_quadratic") {
    values.a = document.getElementById('a').value;
    values.b = document.getElementById('b').value;
    values.c = document.getElementById('c').value;
  } 
  else if(type === "solve_linear") {
    values.a = document.getElementById('a').value;
    values.b = document.getElementById('b').value;
  } 
  else if(type === "percentage") {
    values.part = document.getElementById('part').value;
    values.total = document.getElementById('total').value;
  } 
  else if(type === "matrix") {
    try {
      values.matrix = JSON.parse(document.getElementById('matrix').value);
    } catch {
      alert("Invalid matrix format! Example: [[1,2],[3,4]]");
      return;
    }
  }

  stepsContainer.innerHTML = '';
  resultContainer.innerHTML = 'Calculating...';

  try {
    const response = await fetch('http://127.0.0.1:5000/solve', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({type, values})
    });
    const data = await response.json();

    if(data.error){
      resultContainer.innerHTML = `Error: ${data.error}`;
      return;
    }

    // Display steps one by one with typing effect
    let i=0;
    function typeStep(){
      if(i < data.steps.length){
        const step = document.createElement('p');
        step.textContent = data.steps[i];
        stepsContainer.appendChild(step);
        i++;
        setTimeout(typeStep, 700);
      } else {
        resultContainer.innerHTML = `<b>Result: ${data.result}</b>`;
      }
    }
    typeStep();

  } catch(err){
    resultContainer.innerHTML = `Error: ${err}`;
  }
});