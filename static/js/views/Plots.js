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
        return `<button id="createplots">Generate Plots</button>
                <div class="chartBox"><canvas id="plots" width="200" height="200"></canvas></div>`;
    };
    //initializing the plot
    async getPlot(){
        //setup block
        const data = {
            labels: xlabels,
            datasets: [{
                label: 'Distribution of the number of records (signals) per vessel',
                data: xdata,
                backgroundColor: [
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]  
        };
        //config block
        const config = {
            type: 'bar',
            data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
        //init render block
        const myChart = new Chart(
            document.getElementById('plots'),
            config
        );
        //getCSV() function from AbstractView
        const csvdata = AbstractView.getCSV();
        const lat = csvdata[0];
        const lon = csvdata[1];
        const oid = csvdata[2];
        
        //updating the plot by clicking a button
        const updateChart = document.getElementById('createplots').
        addEventListener('click', () => {
            //myChart.data.datasets[0].data = tdata;
            //groupBy(oiddata);
            console.log(oid.length);
            myChart.data.labels = oid;
            myChart.data.datasets[0].data = oid;
            myChart.update();
        });
    };
}

