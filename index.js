//import webscraber or api
//for loop that runs through all the data searching for matches or call all the api's for matches
//adds matches to a list
//returns list to user
//allow the user to select an item and it will be added to the groceryList variable
//show final price of their groceryList and the cheapest possible list
var {PythonShell} = require( 'python-shell');

//allow user to select which stores they can/want to go to

//some example code, wont work without data

function getGroceries(term, location){
  let options = {
    mode: 'text',
    //pythonPath:'', for if its in a venv
    pythonOptions: ['-u'],
    pythonPath:'C:/Users/edweh/venv/Scripts/Python.exe',
    args: [term, location]
  };
    PythonShell.run('./dataCollection/dataCollection.py', options, async function (err, result) {
    if (err)
        throw err;
        return result;
      });
}



exports.getGroceries = getGroceries;