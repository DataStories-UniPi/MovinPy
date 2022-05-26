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
        return `<div id="output"></div>
                <div>Number of records: </div>
                <div id="s1"></div>
                <div>Number of records (signals) per day: </div>
                <div id="s2"></div>
                <div>Number of records(signals) per object: </div>
                <div id="s3"></div>
                <div>Average number of records (signals) per vessel daily: </div>
                <div id="s4"></div>
                <div>Distribution of number of records (signals) per vessel: </div>
                <div id="plt1"></div>
                <div>Distribution of number of records per vessel daily: </div>
                <div id="plt2"></div>
                <div>Distribution of number of records (signals) per weekday: </div>
                <div id="plt3"></div>`;
    };
    
}

