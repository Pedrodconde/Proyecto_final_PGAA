let map;
let selectedTakeoffCity = "";
let selectedLandingCity = "";
let markers = [];
let polyline;
let distanceLabel;

//------------------------------------//

function init() {
    map = L.map('map').setView([48.505, -15], 1.5);
    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
}

//-------------------------//

function getCoordinatesForCity(city) {
    const cityCoordinates = {
        'Madrid': [40.4168, -3.7038],
        'London': [51.5074, -0.1278],
        'Berlin': [52.5200, 13.4050],
        'Rome': [41.9028, 12.4964],
        'Paris': [48.8566, 2.3522],
        'Los Angeles': [34.0522, -118.2437],
        'Oregon': [44.0521, -123.0868],
        'Mexico': [19.4326, -99.1332],
        'Chicago': [41.8781, -87.6298],
        'Alaska': [64.2008, -149.4937]
    };
    return cityCoordinates[city];
}

//---------------------------------//

function setTakeoff(city) {
    selectedTakeoffCity = city;
    const coordinates = getCoordinatesForCity(city);
    if (coordinates) {
        const marker = new L.Marker(coordinates);
        marker.addTo(map);
        markers.push(marker);
    }
}

function setLanding(city) {
    selectedLandingCity = city;
    const coordinates = getCoordinatesForCity(city);
    if (coordinates) {
        const marker = new L.Marker(coordinates);
        marker.addTo(map);
        markers.push(marker);
    }
}


//---------------//

function calculateDistances() {
    if (selectedTakeoffCity && selectedLandingCity) {
        const takeoffCoordinates = getCoordinatesForCity(selectedTakeoffCity);
        const landingCoordinates = getCoordinatesForCity(selectedLandingCity);
        if (takeoffCoordinates && landingCoordinates) {
            const distance = getDistance(takeoffCoordinates[0], takeoffCoordinates[1], landingCoordinates[0], landingCoordinates[1]);
            alert(`Distance between ${selectedTakeoffCity} and ${selectedLandingCity}: ${distance.toFixed(2)} km`);
            
            // Mostrar distancia en el mapa
            const labelLatLng = [(takeoffCoordinates[0] + landingCoordinates[0]) / 2, (takeoffCoordinates[1] + landingCoordinates[1]) / 2];
            distanceLabel = L.marker(labelLatLng, {
                icon: L.divIcon({
                    className: 'distance-label',
                    html: `<div>${distance.toFixed(2)} km</div>`
                })
            }).addTo(map);
            polyline = L.polyline([takeoffCoordinates, landingCoordinates], { color: 'red' }).addTo(map);
        } 
    }
}

function getDistance(x1, y1, x2, y2) {
    let y = x2*100- x1*100;
    let x = y2*100- y1*100;
    return Math.sqrt(x * x + y * y);
}

//------------------------//

function resetMap() {
    markers.forEach(marker => {
        map.removeLayer(marker);
    });
    if (polyline) {
        map.removeLayer(polyline);
    }
    if (distanceLabel) {
        map.removeLayer(distanceLabel);
    }
    // Limpiar la lista de marcadores
    markers = [];
}
