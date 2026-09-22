const http = require('http');
const PORT = 3003;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello! This is data sent over HTTP.\n');
});

server.listen(PORT, () => {
    console.log('Server is running at http://localhost:' + PORT);

    const options = {
        hostname: 'localhost',
        port: PORT,
        path: '/',
        method: 'GET'
    };

    const req = http.request(options, (res) => {
        let data = '';

        console.log('Status Code:', res.statusCode);
        res.on('data', (chunk) => {
            data += chunk;
        });

        res.on('end', () => {
            console.log('Response from server:', data);
            server.close();
        });
    });

    req.on('error', (error) => {
        console.error('Error occurred:', error);
        server.close();
    });

    req.end();
});
