let map = null;
function initMap(){
    var options = {
        zoom:4,
        center:{lat:37.0902,lng:-95.7129}
    }
    map = new google.maps.Map(document.getElementById('map'), options);
}

function addMarker(lat, lng, address){
    if(lat == 0 && lng == 0 ){
        getlatlng(address);
    }
    initMap();
    new google.maps.Marker({
    position:{lat:lat, lng:lng},
    map:map
    })
}

function getlatlng(address){
    let latlng = []
    axios.get('https://maps.googleapis.com/maps/api/geocode/json',{
        params:{
          address:address,
          key:'AIzaSyBDxgIyZ3quG2Td6ZTr7SwcMkoj1MnDAQ4'
        }
      })
      .then(function(response){
        latlng.push(response.data.results[0].geometry.location.lat);
        latlng.push(response.data.results[0].geometry.location.lng);
        addMarker(response.data.results[0].geometry.location.lat, response.data.results[0].geometry.location.lng);
      })
      .catch(function(error){
        console.log(error);
      });
}