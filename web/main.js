
async function get(room, date) {
  const response = await fetch(`https://3mya4jha58.execute-api.eu-west-1.amazonaws.com/live/${room}/${date}`)

  if (!response.ok) {
    throw new Error(`Request failed with status ${reponse.status}`)
  }

  return response.json()
}

function rooms() {
  return [`external`]
}

function date() {
  return '2023-01-22'
}

async function drawGraph() {
  gets = []
  for(let room of rooms()) {
    gets.push(get(room, date()))
  }
  let responses = await Promise.all(gets);

  for(let response of responses) {
    trace(response)
  }
}

function trace(items) {
  x = []
  y = []
  for(let item of items){
    
  }
}
