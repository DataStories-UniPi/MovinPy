import AbstractView from "./AbstractView.js";

const xlabels = [];
const xdata = [];

export default class extends AbstractView{
    constructor(){
        super();
        this.setTitle('Plots');
    }
    //inner html for Plots
    async getHtml(){
        return `<button pys-onClick="plots" class="pill" id="generateplots">Generate Plots</button>
                <div id="output"></div>
                <div class="pill" id="s0"></div>
                <div>Number of records: </div>
                <div class="pill" id="s1"></div>
                <div>Number of records (signals) per day: </div>
                <div class="pill" id="s2"></div>
                <div>Number of records(signals) per object: </div>
                <div class="pill" id="s3"></div>
                <div>Average number of records (signals) per vessel daily: </div>
                <div class="pill" id="s4"></div>
                <div>Distribution of number of records (signals) per vessel: </div>
                <div class="pill" id="plt1"></div>
                <div>Distribution of number of records per vessel daily: </div>
                <div class="pill" id="plt2"></div>
                <div>Distribution of number of records (signals) per weekday: </div>
                <div class="pill" id="plt3"></div>`;
    };
    
}

