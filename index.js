//import webscraber or api
//for loop that runs through all the data searching for matches or call all the api's for matches
//adds matches to a list
//returns list to user
//allow the user to select an item and it will be added to the groceryList variable
//show final price of their groceryList and the cheapest possible list


//allow user to select which stores they can/want to go to

//some example code, wont work without data
var groceryList = []
function getGroceries(userInput, webData){
  for (i = 0; i < 100; i++){
    if (webData[i].upc == userInput) {
      groceryList.add(webData[i])
    }
  }
  return groceryList;
}

function krogerApi(term, zipCode){
  let options = {
    mode: 'text',
    //pythonPath:'', for if its in a venv
    pythonOptions: ['-u'],
    pythonPath:'C:/Users/edweh/venv/Scripts/Python.exe',
    args: [term, location]
  };
    PythonShell.run('./kroger.py', options, async function (err, result) {
    if (err)
        throw err;
        return result;
      });
}

function samsClubScraper(){
  let options = {
    mode: 'text',
    //pythonPath:'', for if its in a venv
    pythonOptions: ['-u'],
    pythonPath:'C:/Users/edweh/venv/Scripts/Python.exe'
  };
    PythonShell.run('./samsClub.py', options, async function (err, result) {
    if (err)
        throw err;
        return result;
      });
}

function walgreensScraper(){

}

exports.krogerApi = krogerApi;
exports.samsClubScraper = samsClubScraper;
exports.walgreensScraper = walgreensScraper;
