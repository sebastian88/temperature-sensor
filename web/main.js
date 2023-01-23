
colours = ['blue','green', 'black', 'pink', 'purple', 'brown', 'orange', 'grey', 'red', 'yellow']

class Room {  
  constructor(name, date, data, colour) {
    this.name = name;
    this.date = date;
    this.data = data;
    this.colour = colour
    this.temperatures = []
    this.humidities = []
    this.response = null
  }

  get getTemperatures() {
    for(let item of this.data){
      this.temperatures.push({x:Date.parse(item.t),y:item.c})
    }
    return this.temperatures
  }

  get getHumidities() {
    for(let item of this.data){
      this.humidities.push({x:Date.parse(item.t),y:item.h})
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

function roomNames(){
  return [
    'external'
  ]
}

function date() {
  return '2023-01-23'
}

function getRandomColour() {
  const index = Math.floor(Math.random()*colours.length)
  ret = colours[index]
  colours.splice(index, 1);
  return ret
}



async function drawGraph() {
  rooms = []
  for(let roomName of roomNames()) {
    const data = await get(roomName, date())
    rooms.push(new Room(roomName, date(), data, getRandomColour()))
  }

  datasets = []
  for(let room of rooms) {
    datasets.push({
      label: room.name + ' temperature',
      borderColor: room.colour,
      fill: false,
      data: room.getTemperatures,
      yAxisID: 'y1'
    })

    datasets.push({
      label: room.name + ' humidity',
      borderColor: room.colour,
      fill: false,
      data: room.getHumidities,
      borderDash: [10,5],
      yAxisID: 'y2'
    })
  }

  new Chart("myChart", {
    type: "line",
    data: {
      datasets: datasets
    },
    options: {
      scales: {
        xAxes: [{
          type: 'time',
        }],
        yAxes: [{
          id: 'y1',
          position: 'left',
        }, {
          id: 'y2',
          position: 'right'
        }]
      }
    }
  });
}
drawGraph()

