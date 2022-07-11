import AbstractView from "./AbstractView.js";

export default class extends AbstractView{
    constructor() {
        super();
        this.setTitle('Map');
    }
    //inner html for Map
    async getHtml(){
        return `<div>After uploading the csv file, click the following button to generate the map:</div>
                <button pys-onClick="generate_map" class="pill" id="plotmarkers">Generate Map</button>
                <div>Or give the exact range of timestamps:</div>
                <input type="text" id="min" name="min" placeholder="Min">
                <input type="text" id="max" name="max" placeholder="Max">
                <input pys-onClick="date_picker" class="pill" type="submit" id="btn-form" value="submit">
                <br>
                <div id="folium" style="width: 100%; height: 100%"></div>`;
    };
    
};


