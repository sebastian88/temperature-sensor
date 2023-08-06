
let colours = ['blue', 'green', 'black', 'pink', 'purple', 'brown', 'orange', 'grey', 'red']
const params = new URLSearchParams(window.location.search);

function pad(i){
  if(i < 10)
    return "0" + i
  return "" + i
}

function getUrl() {
  let currentUrl = window.location.href
  return new URL(currentUrl)
}

function addDays(date, days) {
  var result = new Date(date);
  result.setDate(result.getDate() + days);
  return result;
}

function getTodaysDate() {
  let today = new Date()
  return today.getFullYear() + '-' + pad(today.getMonth()+1) + '-' + pad(today.getDate())
}

function today() {
  let url = getUrl()
  if(!url.searchParams.get('s'))
    url.searchParams.set('s', 'th')

  let dateString = getTodaysDate()
  url.searchParams.set('d', dateString)
  window.location.href = url
}

function back() {
  move(-1)
}

function forward() {
  move(1)
}

function move(i) {
  let currentUrl = window.location.href
  let url = new URL(currentUrl)
  let d = date()

  let dateMinusOne = addDays(d, i)
  let dateString = dateMinusOne.getFullYear() + '-' + pad(dateMinusOne.getMonth()+1) + '-' + pad(dateMinusOne.getDate())
  url.searchParams.set('d', dateString)
  window.location.href = url
}

class Room {
  constructor(id, name, date, data, colour) {
    this.id = id
    this.name = name
    this.date = date
    this.data = data
    this.colour = colour
    this.temperatures = []
    this.humidities = []
    this.response = null
  }

  get getTemperatures() {
    for (let item of this.data) {
      this.temperatures.push({ x: Date.parse(item.t), y: item.c })
    }
    return this.temperatures
  }

  get getHumidities() {
    for (let item of this.data) {
      this.humidities.push({ x: Date.parse(item.t), y: item.h })
    }
    return this.humidities
  }
}

async function get(roomName, date) {
  const response = await fetch(`https://3mya4jha58.execute-api.eu-west-1.amazonaws.com/live/${roomName}/${date}`)

  if (!response.ok) {
    throw new Error(`Request failed with status ${reponse.status}`)
  }

  return response.json()
}

function roomNames() {
  let rooms = []

  for (let i = 1; i <= 9; i++) {
    if (params.get(i)) {
      id = i
      rooms.push({
        'id': id,
        'name': params.get(i)
      })
    }
  }
  return rooms
}

function date() {
  let date = params.get('d')
  if(date === 'today')
    date = getTodaysDate()
  return date
}

function getRollingAverage() {
  return parseInt(params.get('r') ?? 0)
}

function showTemp() {
  return params.get('s').includes('t')
}

function showHumidity() {
  return params.get('s').includes('h')
}

function getColour() {
  return colours.shift();
}

function movingAvg(array){
  const rollingAverage = getRollingAverage()
  if(rollingAverage <= 1){
    return array
  }

  var avg = function(array){

      var sum = 0, count = 0, val;
      for (var i in array){
          val = parseFloat(array[i].y);
          sum += val;
          count++;
      }

      return sum / count;
  };

  var result = [], val;

  for (var i=0, len=array.length - rollingAverage; i <= len; i++){

      val = avg(array.slice(i, i + rollingAverage));
      if (isNaN(val))
          console.log('nan')
      else{
        array[i].y = val
        result.push(array[i]);
      }
  }

  return result;
}

async function drawGraph() {
  if(!getUrl().searchParams.get('s')) return
  let rooms = []
  for (let roomName of roomNames()) {
    const data = await get(roomName.id, date())
    rooms.push(new Room(roomName.id, roomName.name, date(), data, getColour()))
  }

  let datasets = []
  let isShowTemp = showTemp()
  let isShowHumidity = showHumidity()
  for (let room of rooms) {
    if (isShowTemp) {
      datasets.push({
        label: room.name + ' temperature',
        pointRadius: 0,
        borderColor: room.colour,
        fill: false,
        // lineTension: 1,
        data: movingAvg(room.getTemperatures),
        yAxisID: 'y1'
      })
    }

    if (isShowHumidity) {
      datasets.push({
        label: room.name + ' humidity',
        pointRadius: 0,
        borderColor: room.colour,
        fill: false,
        data: room.getHumidities,
        borderDash: [5, 5],
        yAxisID: 'y2'
      })
    }
  }
  let yAxes = []
  if(isShowTemp) {
    yAxes.push({
      id: 'y1',
      position: 'left',
    })
  }
  if(isShowHumidity) {
    yAxes.push({
      id: 'y2',
      position: 'right'
    })
  }

  new Chart("myChart", {
    type: "line",
    data: {
      datasets: datasets
    },
    options: {
      animation: false,
      scales: {
        xAxes: [{
          type: 'time',
        }],
        yAxes: yAxes
      }
    }
  });
}
drawGraph()

