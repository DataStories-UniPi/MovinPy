const express = require('express');
const path = require('path');

const app = express();

app.use('/static',express.static(path.resolve(__dirname, 'static')));

app.use(express.json({limit: '1mb'}));

app.get('/*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'visuals.html'));
});

app.post('/*', (request, response) => {
    console.log(request);
});

app.listen(process.env.PORT || 3000, () => console.log('Server running...'));

