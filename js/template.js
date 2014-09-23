function locateCompany(map, lat, lon, marker_id)
{
    document.getElementById('popup').style.visibility = 'hidden';
    map.setView([lat, lon], 15, {animation: false});
    markers[marker_id].openPopup();

    return false;
}

var map = L.map('map').setView([48.8595, 2.3548], 6);
var markers = [];
var cur_marker = null;

// L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
// 	maxZoom: 18,
// 	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
// 		     '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
// 		     'Imagery © <a href="http://mapbox.com">Mapbox</a>',
// 		     id: 'examples.map-i86knfo3'
// }).addTo(map);

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

map.on('popupopen', function (e) {
    delete map._popup;
});

{{content}}

// Last marker
cur_marker = markers[markers.length-1];
cur_marker.openPopup();

function showAllAround()
{
    bounds = map.getBounds();
    cur_marker.closePopup();

    for(i=0; i<markers.length; i++)
    {
	if (bounds.contains(markers[i].getLatLng()))
	    markers[i].openPopup();
    }

    return false;
}

function hideAllAround()
{
    bounds = map.getBounds();
    cur_marker.closePopup();

    for(i=0; i<markers.length; i++)
    {
	if (bounds.contains(markers[i].getLatLng()))
	    markers[i].closePopup();
    }

    return false;
}

/*
var popup = L.popup();

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
}

map.on('click', onMapClick);
*/
