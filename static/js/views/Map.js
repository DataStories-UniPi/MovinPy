import AbstractView from "./AbstractView.js";

export default class extends AbstractView{
    constructor() {
        super();
        this.setTitle('Map');
    }
    //inner html for Map
    async getHtml(){
        return `<button id="plotmarkers">Update Map</button>
                <br>
                <input mbsc-slider type="range" value="130" min="80" max="300" data-val="left" data-template="{value}" data-highlight="false" />
                <br>
                <button id="clearMap">Clear Map</button>
                <br>
                <button id="clustering">Clustering</button>
                <div id="leaflet_map"></div>`;
    };
    static getCSV(){
        return super.getCSV();
    }
    
    async getMap(){
        // initialize the leaflet map (after the inner html)
        const leaflet_map = L.map('leaflet_map').setView([38, 25], 7);
        const attribution = '&copy; <a href="https://www.openstreetmap.org/coppyright">OpenStreetMap</a> contributors';
        const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        const tiles = L.tileLayer(tileUrl, { attribution });
        tiles.addTo(leaflet_map);

        //getCSV() function from AbstractView
        const csvdata = AbstractView.getCSV();
        const lat = csvdata[0];
        const lon = csvdata[1];
        const oid = csvdata[2];
        const ts = csvdata[3];
        
        var marker = new Array();

        //updating the map by clicking a button
        const updateMap = document.getElementById('plotmarkers').
        addEventListener('click', () => {
            //making sure the data are loaded
            console.log(lat.length);
            console.log(lat);
            console.log(lon);
            console.log(ts);
            //date slider
            const dates_array = [];
            var j=0;
            for (var i=0; i< lat.length; i++){
                const date = new Date(ts[i]),
                    d = date.getDate();
                console.log("date:", d);
                if (!dates_array.includes(d)){
                    dates_array.push(d);
                }
                //if (d == dates_array[j]){
                    //adding markers to map
                 //   L.circleMarker([lat[i], lon[i]]).setRadius(1).bindPopup("oid:" + oid[i]).addTo(leaflet_map);
               // }
            };
            console.log(dates_array);
            
            for (var i=0; i< lat.length; i++){
                //adding markers to map
                var temp_marker = L.circleMarker([lat[i], lon[i]]).setRadius(1).bindPopup("oid:" + oid[i]);  
                marker.push(temp_marker);
                leaflet_map.addLayer(marker[i]);
            };
            
        });
        //clearing the map from all the markers
        const clearMap = document.getElementById('clearMap').
        addEventListener('click', () => {
            for(var i=0; i<marker.length; i++) {
                leaflet_map.removeLayer(marker[i]);
            };
        });
    };

    async getClusters(){
        //clustering the data
        const colors = {
            orange: '#ffa500',
            blue: '#0000ff',
            green: '#008000',
            pink: '#ffc0cb',
        }
        const clustering = document.getElementById('clustering').
        addEventListener('click', () => {
            //clustering markers with kmeans
            console.log('inside clustering function');
        })
    };
};


