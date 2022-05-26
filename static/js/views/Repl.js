import AbstractView from "./AbstractView.js";

export default class extends AbstractView{
    constructor() {
        super();
        this.setTitle('Interactive Repl');
    }
    //inner html for Map
    async getHtml(){
        return `<py-repl id="repl" auto-generate="true"></py-repl>`;
    };
};