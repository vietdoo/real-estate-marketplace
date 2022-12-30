function getRandomArrayElements(arr, count) {
    var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}





var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
    }),
    latlng = L.latLng(10.773081, 106.6829); 

var map = L.map('map', {center: latlng, zoom: 13, layers: [tiles]});

var markers = L.markerClusterGroup({ chunkedLoading: true });


// var houses = getRandomArrayElements(addressPoints, 8000);

// async function load() {
//     let url = 'http://localhost:1337/tutorials';
//     let obj = await fetch(url).json()
//     .then(text => {
//         text; // => 'Page not found'
//     });;
//     console.log(obj);
// }

// load();
let houses = [];

async function githubUsers() {
    let response = await fetch('points.json');
    let users = await response.json();

    return (users);
}

async function f1 () {
    resp = githubUsers();
    resp.then(res => {houses = res});

}

function f1a () {
    console.log(houses.length);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];
        var price = houses[i]['price'];
        console.log(lat, long, title, price);
        var marker = L.marker(L.latLng(lat, long), { title: title });
        marker.bindPopup(title);
        markers.addLayer(marker);
    }
}


f1().then(console.log(houses.length))


// async function xxx() {
//     await draw();
// }

// xxx();

function resetLayer() {
    markers.clearLayers();

    var radios = document.getElementsByName('district');
    var option = 0;
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            option = radios[i].value;
        }
    }
    
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];
        var price = houses[i]['price'];
        if (title % option === 0) {
            var marker = L.marker(L.latLng(lat, long), { title: title });
            marker.bindPopup(title);
            markers.addLayer(marker);
        }
    }
}

map.addLayer(markers);