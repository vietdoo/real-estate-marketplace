var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
    }),
    latlng = L.latLng(10.773081, 106.6829); 

var map = L.map('map', {center: latlng, zoom: 13, layers: [tiles]});
var markers = L.markerClusterGroup({ chunkedLoading: true });

function makePopup(house) {
    var title = house['title'];
    var price = house['price'];
    var url = house['url']
    var img = house['img'];
    var imgStr = '<img src = "' + img +  '" style="width: 100px; height: 100px; object-fit: cover;" ></img>'
    var imgLink = '<a href = "' + url + '">Chi tiết</a>'

    return '<div class="row"><div class="column1" style="">' + imgStr + '</div><div class="column2" style="">' + title + '<h2>' + price + '</h2>' + imgLink + '</div></div>'
}

function makeAdvertise(house) {
    var title = house['title'];
    var price = house['price'];
    var url = house['url']
    var img = house['img'];
    var imgStr = '<img src = "' + img +  '" style="width: 100%; height: 150px; object-fit: cover; border-radius: 5px;" ></img>'
    var imgLink = '<a href = "' + url + '">Chi tiết</a>'

    return imgStr + '<div style="margin: 10px;">' + title + '<h4>' + price + '</h4>' + imgLink + '</div>'
}

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

async function getJSON(dist) {
    return fetch('https://vietdoo.engineer/api/v1.0/houses/?dist=' + dist)
        .then((response)=>response.json())
        .then((responseJson)=>{return responseJson});
}

async function caller() {
    var startTime = performance.now()
    const houses = await this.getJSON('Quận 5');  
    console.log("Successfully request: ", houses.length, " houses in ", houses[0]['dist']);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];

        var marker = L.marker(L.latLng(lat, long), { title: title});

        var popup = makePopup(houses[i]);
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }

    var agents = getRandomArrayElements(houses, 10);
    var inner = "";
    for(var i = 0; i < 10; i++) {
        var agentInner = '<div class="house" style="width: 47%; height: 250px; float: left; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; border-radius: 5px;">' + makeAdvertise(agents[i]) + '</div>';
        inner += agentInner;
    }

    document.getElementById("house-container").innerHTML = inner;

    console.log("Done in ", performance.now() - startTime, " ms")
}

caller();

async function resetLayer() {
    markers.clearLayers();

    var startTime = performance.now()

    var select = document.getElementById('district');
    var option = '';
    option = select.value;
    
    const houses = await this.getJSON(option); 
    
    var agents = getRandomArrayElements(houses, 10);
    var inner = "";

    for(var i = 0; i < 10; i++) {
        var agentInner = '<div class="house" style="width: 47%; height: 250px; float: left; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px; border-radius: 5px;">' + makeAdvertise(agents[i]) + '</div>';
        inner += agentInner;
    }

    document.getElementById("house-container").innerHTML = inner;

    console.log("Successfully request: ", houses.length, " houses in ", houses[0]['dist']);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses['title'];

        var marker = L.marker(L.latLng(lat, long), { title: title});
        var popup = makePopup(houses[i]);
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }
    console.log("Done in ", performance.now() - startTime, " ms")
}

map.addLayer(markers);

