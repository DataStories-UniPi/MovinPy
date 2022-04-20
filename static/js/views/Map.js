import AbstractView from "./AbstractView.js";

export default class extends AbstractView{
    constructor() {
        super();
        this.setTitle('Map');
    }
    //inner html for Map
    async getHtml(){
        return `<button id="plotmarkers">Update Map</button>
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
        
        
        //updating the map by clicking a button
        const updateMap = document.getElementById('plotmarkers').
        addEventListener('click', () => {
            //adding markers to map
            console.log(lat.length);
            console.log(lat);
            console.log(lon);
            for (var i=0; i< lat.length; i++){
                L.circleMarker([lat[i], lon[i]]).setRadius(1).bindPopup("oid:" + oid[i]).addTo(leaflet_map);
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
    async getDates(){
        
    };
    
};


