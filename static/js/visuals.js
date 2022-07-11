import Map from './views/Map.js';
import Plots from './views/Plots.js';
import Repl from './views/Repl.js';

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        {path: '/map', view: Map},
        {path: '/plots', view: Plots},
        {path: '/repl', view: Repl}
    ];
    //test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            isMatch: location.pathname === route.path
        };
    });
    let match = potentialMatches.find(potentialMatch => potentialMatch.isMatch);
    
    if (!match){
        match = {
            route: routes[0],
            isMatch: true
        };
    }

    //creating new instance of view at the match route
    const view = new match.route.view();
    console.log(location.pathname);

    //getting the html from the method getHtml() and injecting it inside the inner html of the app element
    document.querySelector('#app').innerHTML = await view.getHtml();
};


//navigating through browser history 
window.addEventListener('popstate', router);


document.addEventListener('DOMContentLoaded', () => {
    //not refreshing the page whenever the user navigates
    document.body.addEventListener('click', e => {
        if (e.target.matches('[data-link]')){
            //preventing default behavour
            e.preventDefault();
            //navigate to href as in <nav>
            navigateTo(e.target.href);
        }
    });
    router();
});

