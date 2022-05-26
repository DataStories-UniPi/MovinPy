export default class{
    constructor(){
        
    }
    //updating the browser tab title
    setTitle(title){
        document.title = title;
    }
    async getHtml(){
        return ``;
    }
    static getCSV(){
    //upload csv file by clicking a button
        const tsdata= []; 
        const oiddata=[];
        const lat=[];
        const lon=[];

        const upload_button = document.getElementById('csvfile').
        addEventListener('click', () => {
        //reading the csv file with papa parse library
        Papa.parse(document.getElementById('csvfile').files[0],
        {
            download: true,
            header: true,
            skipEmptyLines: true,
            complete: function(results){
            //creating an array with all the timestamps and an array with all the oid
                for (var i=0; i< results.data.length; i++){
                    tsdata.push(results.data[i].ts);
                    oiddata.push(results.data[i].oid);
                    lat.push(results.data[i].lat);
                    lon.push(results.data[i].lon);
                }  
            
            console.log(tsdata);
            console.log(oiddata);
            console.log(lat);
            console.log(lon);
            }
        });

    });

    return [lat, lon, oiddata, tsdata];
    }
   
}