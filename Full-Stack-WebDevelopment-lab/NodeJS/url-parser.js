// Parse URL using Node.js built-in url module
const url = require('url');

const webAddress = 'https://www.linkedin.com/in/adhimulambhargavsaiviswanath/';

// Parse the URL using the legacy url.parse() method
const parsedUrl = url.parse(webAddress);

// Display all components of the URL
console.log("=== Parsed URL Components ===");
console.log("Full URL       :", parsedUrl.href);
console.log("Protocol       :", parsedUrl.protocol);
console.log("Host           :", parsedUrl.host);
console.log("Hostname       :", parsedUrl.hostname);
console.log("Port           :", parsedUrl.port);
console.log("Pathname       :", parsedUrl.pathname);
console.log("Search Query   :", parsedUrl.search);
console.log("Query Object   :", parsedUrl.query);
console.log("Fragment/Hash  :", parsedUrl.hash);
console.log("Path           :", parsedUrl.path);