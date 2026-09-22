const http = require("http");

const PORT = 3001;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.write("Welcome to Node.js");
    res.end();
});

server.listen(PORT, () => {
    console.log("Server running at http://localhost:" + PORT);
});
