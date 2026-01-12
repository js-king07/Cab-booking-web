let map;
let pickupPlace, destinationPlace;

const rates = {
    "Bike": 10,
    "Auto": 12,
    "Mini": 15,
    "Prime SUV": 20
};

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 13.0827, lng: 80.2707 }, // Chennai
        zoom: 13
    });

    const pickupInput = document.getElementById("pickup");
    const destinationInput = document.getElementById("destination");

    const pickupAuto = new google.maps.places.Autocomplete(pickupInput);
    const destinationAuto = new google.maps.places.Autocomplete(destinationInput);

    pickupAuto.addListener("place_changed", () => {
        pickupPlace = pickupAuto.getPlace();
    });

    destinationAuto.addListener("place_changed", () => {
        destinationPlace = destinationAuto.getPlace();
    });
}

function calculateFare() {
    if (!pickupPlace || !destinationPlace) {
        alert("Please select pickup and destination locations");
        return;
    }

    const cabType = document.getElementById("cabType").value;
    if (!cabType) {
        alert("Please select a cab type");
        return;
    }

    const service = new google.maps.DistanceMatrixService();

    service.getDistanceMatrix({
        origins: [pickupPlace.geometry.location],
        destinations: [destinationPlace.geometry.location],
        travelMode: google.maps.TravelMode.DRIVING
    }, (response, status) => {
        if (status !== "OK") return;

        const distanceMeters = response.rows[0].elements[0].distance.value;
        const distanceKm = (distanceMeters / 1000).toFixed(2);

        document.getElementById("distance").innerText = distanceKm;

        const fare = Math.round(distanceKm * rates[cabType]);
        document.getElementById("fare").innerText = fare;
    });
}
