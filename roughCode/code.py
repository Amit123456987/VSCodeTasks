import os


def create_folders_file(path,code):
  
  indexOfSlash = path.rfind("/")
  
  folder = path[:indexOfSlash].join("/")
  os.makedirs(folder, exist_ok=True)
  
  fileName = path[indexOfSlash+1:] 
  with open(path, 'wa') as f:
    f.write(code)  


path='Example 1-1.js'
code='''
function a() { b(); }
function b() { c(); } function c() { /**/ }

function x() { y(); }
function y() { z(); } function z() { /**/ }

setTimeout(x, 0); a();
'''

path='Example 1-2.js'
code='''setTimeout(() => console.log('A'), 0); console.log('B');
setTimeout(() => console.log('C'), 100); setTimeout(() => console.log('D'), 0);

let i = 0;
while (i < 1_000_000_000) { // Assume this takes ~500ms let ignore = Math.sqrt(i);
i++;
}

console.log('E');
'''

path='Example 1-3.js'
code='''#!/usr/bin/env node
const fs = require('fs'); fs.readFile('/etc/passwd', 
(err, data) => {  if (err) throw err; console.log(data);
});

setImmediate(  () => { 
console.log('This runs while file is being read');

});'''

path='Example 1-4.js'
code='''const t1 = setTimeout(() => {}, 1_000_000);  const t2 = setTimeout(() => {}, 2_000_000); 
// ...
t1.unref(); 
// ... clearTimeout(t2);'''

path='Example 1-5.js'
code='''const fs = require('fs');

setImmediate(() => console.log(1)); Promise.resolve().then(() => console.log(2)); process.nextTick(() => console.log(3)); fs.readFile(  filename, () => {
console.log(4);
setTimeout(() => console.log(5)); setImmediate(() => console.log(6)); process.nextTick(() => console.log(7));
});
console.log(8);
'''

path='recipe-api/producer-http-basic.js'
code='''#!/usr/bin/env node

// npm install fastify@3.2
const server = require('fastify')();
const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;
console.log(`worker pid=${process.pid}`); server.get('/recipes/:id', async (req, reply) => {
console.log(`worker request pid=${process.pid}`); const id = Number(req.params.id);
if (id !== 42) { reply.statusCode = 404;
return { error: 'not_found' };
}
return {
producer_pid: process.pid, recipe: {
id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [
{ id: 1, name: "Chicken", quantity: "1 lb", },
{ id: 2, name: "Sauce", quantity: "2 cups", }
]
}
};
});

server.listen(PORT, HOST, () => {
console.log(`Producer running at http://${HOST}:${PORT}`);
});
'''

path='web-api/consumer-http-basic.js'
code='''#!/usr/bin/env node

// npm install fastify@3.2 node-fetch@2.6 const server = require('fastify')(); const fetch = require('node-fetch');
const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 3000;
const TARGET = process.env.TARGET || 'localhost:4000';

server.get('/', async () => {
const req = await fetch(`http://${TARGET}/recipes/42`); const producer_data = await req.json();

return {
consumer_pid: process.pid, producer_data
};
});

server.listen(PORT, HOST, () => {
console.log(`Consumer running at http://${HOST}:${PORT}/`);
});

'''


path='Example 2-1.js'
code='''#!/usr/bin/env node

// npm install node-fetch@2.6
const fetch = require('node-fetch');

(async() => {
const req = await fetch('http://localhost:3002/data', {

method: 'POST', headers: {
'Content-Type': 'application/json',
'User-Agent': `nodejs/${process.version}`, 'Accept': 'application/json'
},
body: JSON.stringify({ foo: 'bar'
})
});
const payload = await req.json(); console.log(payload);
})();
'''

path='Example 2-2.js'
code='''POST /data HTTP/1.1 
Content-Type: application/json  User-Agent: nodejs/v14.8.0 Accept: application/json
Content-Length: 13
Accept-Encoding: gzip,deflate 
Connection: close
Host: localhost:3002
'''

path='Example 2-3.js'
code='''HTTP/1.1 403 Forbidden  Server: nginx/1.16.0 
Date: Tue, 29 Oct 2019 15:29:31 GMT
Content-Type: application/json; charset=utf-8 Content-Length: 33
Connection: keep-alive 
Cache-Control: no-cache 
Vary: accept-encoding
'''


path='server-gzip.js'
code='''#!/usr/bin/env node

// Adapted from https://nodejs.org/api/zlib.html
// Warning: Not as efficient as using a Reverse Proxy const zlib = require('zlib');
const http = require('http'); const fs = require('fs');

http.createServer((request, response) => {
const raw = fs.createReadStream(  dirname + '/index.html'); const acceptEncoding = request.headers['accept-encoding'] || ''; response.setHeader('Content-Type', 'text/plain'); console.log(acceptEncoding);

if (acceptEncoding.includes('gzip')) { console.log('encoding with gzip'); response.setHeader('Content-Encoding', 'gzip');

raw.pipe(zlib.createGzip()).pipe(response);
} else {
console.log('no encoding'); raw.pipe(response);
}
}).listen(process.env.PORT || 1337);
'''

path='recipe-api/producer-https-basic.js'
code='''#!/usr/bin/env node

// npm install fastify@3.2
// Warning: Not as efficient as using a Reverse Proxy const fs = require('fs');
const server = require('fastify')({ https: { 
key: fs.readFileSync(  dirname+'/tls/basic-private-key.key'),
cert: fs.readFileSync(  dirname+'/../shared/tls/basic-certificate.cert'),
}
});
const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;

server.get('/recipes/:id', async (req, reply) => { const id = Number(req.params.id);
if (id !== 42) { reply.statusCode = 404;
return { error: 'not_found' };
}
return {
producer_pid: process.pid,

recipe: {
id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [
{ id: 1, name: "Chicken", quantity: "1 lb", },
{ id: 2, name: "Sauce", quantity: "2 cups", }
]
}
};
});

server.listen(PORT, HOST, () => {
console.log(`Producer running at https://${HOST}:${PORT}`);
});
'''

path='web-api/consumer-https-basic.js'
code='''#!/usr/bin/env node

// npm install fastify@3.2 node-fetch@2.6
// Warning: Not as efficient as using a Reverse Proxy

const server = require('fastify')(); const fetch = require('node-fetch'); const https = require('https'); const fs = require('fs');
const HOST = '127.0.0.1';
const PORT = process.env.PORT || 3000;
const TARGET = process.env.TARGET || 'localhost:4000';

const options = {
agent: new https.Agent({ 
ca: fs.readFileSync(  dirname+'/../shared/tls/basic-certificate.cert'),
})
};

server.get('/', async () => {
const req = await fetch(`https://${TARGET}/recipes/42`, options);
const payload = await req.json();

return {
consumer_pid: process.pid, producer_data: payload
};
});

server.listen(PORT, HOST, () => {
console.log(`Consumer running at http://${HOST}:${PORT}/`);
});
'''

path='shared/graphql-schema.gql'
code='''type Query {  recipe(id: ID): Recipe pid: Int
}
type Recipe {  id: ID!
name: String! steps: String
ingredients: [Ingredient]! 
}
type Ingredient { id: ID!
name: String! quantity: String
}
'''

path='recipe-api/producer-graphql.js'
code='''#!/usr/bin/env node
// npm install fastify@3.2 fastify-gql@5.3 const server = require('fastify')();
const graphql = require('fastify-gql'); const fs = require('fs');
const schema = fs.readFileSync( dirname + '/../shared/graphql-schema.gql').toString(); 
const HOST = process.env.HOST || '127.0.0.1'; const PORT = process.env.PORT || 4000;

const resolvers = {  Query: { 
pid: () => process.pid,
recipe: async (_obj, {id}) => {
if (id != 42) throw new Error(`recipe ${id} not found`); return {
id, name: "Chicken Tikka Masala", steps: "Throw it in a pot...",
}
}
},
Recipe: { 
ingredients: async (obj) => { return (obj.id != 42) ? [] : [
{ id: 1, name: "Chicken", quantity: "1 lb", },
{ id: 2, name: "Sauce", quantity: "2 cups", }
]
}
}
};

server
.register(graphql, { schema, resolvers, graphiql: true }) 
.listen(PORT, HOST, () => {
console.log(`Producer running at http://${HOST}:${PORT}/graphql`);
});
'''

path='web-api/consumer-graphql.js'
code='''#!/usr/bin/env node
// npm install fastify@3.2 node-fetch@2.6 const server = require('fastify')(); const fetch = require('node-fetch'); const HOST = '127.0.0.1';
const PORT = process.env.PORT || 3000;
const TARGET = process.env.TARGET || 'localhost:4000'; const complex_query = `query kitchenSink ($id:ID) { 
recipe(id: $id) { id name ingredients {
name quantity
}
}
pid
}`;

server.get('/', async () => {
const req = await fetch(`http://${TARGET}/graphql`, { method: 'POST',
headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ 
query: complex_query, variables: { id: "42" }
}),
});
return {
consumer_pid: process.pid, producer_data: await req.json()
};
});

server.listen(PORT, HOST, () => {
console.log(`Consumer running at http://${HOST}:${PORT}/`);
});
'''
path='shared/grpc-recipe.proto'
code='''syntax = "proto3"; package recipe;
service RecipeService { 
rpc GetRecipe(RecipeRequest) returns (Recipe) {} rpc GetMetaData(Empty) returns (Meta) {}
}
message Recipe { int32 id = 1;  string name = 2; string steps = 3;
repeated Ingredient ingredients = 4; 
}
message Ingredient { int32 id = 1; string name = 2;
string quantity = 3;
}
message RecipeRequest { int32 id = 1;
}
message Meta {  int32 pid = 2;

}
message Empty {}
'''

path='recipe-api/producer-grpc.js'
code='''#!/usr/bin/env node

// npm install @grpc/grpc-js@1.1 @grpc/proto-loader@0.5 const grpc = require('@grpc/grpc-js');
const loader = require('@grpc/proto-loader'); const pkg_def = loader.loadSync( dirname +
'/../shared/grpc-recipe.proto'); 
const recipe = grpc.loadPackageDefinition(pkg_def).recipe; const HOST = process.env.HOST || '127.0.0.1';
const PORT = process.env.PORT || 4000; const server = new grpc.Server();
server.addService(recipe.RecipeService.service, {  getMetaData: (_call, cb) => { 
cb(null, {
pid: process.pid,
});
},
getRecipe: (call, cb) => { 

if (call.request.id !== 42) {
return cb(new Error(`unknown recipe ${call.request.id}`));
}
cb(null, {
id: 42, name: "Chicken Tikka Masala", steps: "Throw it in a pot...", ingredients: [
{ id: 1, name: "Chicken", quantity: "1 lb", },
{ id: 2, name: "Sauce", quantity: "2 cups", }
]
});
},
});

server.bindAsync(`${HOST}:${PORT}`, grpc.ServerCredentials.createInsecure(),  (err, port) => {
if (err) throw err; server.start();
console.log(`Producer running at http://${HOST}:${port}/`);
});
'''

path='web-api/consumer-grpc.js'
code='''#!/usr/bin/env node

// npm install @grpc/grpc-js@1.1 @grpc/proto-loader@0.5 fastify@3.2 const util = require('util');
const grpc = require('@grpc/grpc-js'); const server = require('fastify')();
const loader = require('@grpc/proto-loader'); const pkg_def = loader.loadSync( dirname +
'/../shared/grpc-recipe.proto'); 
const recipe = grpc.loadPackageDefinition(pkg_def).recipe; const HOST = '127.0.0.1';
const PORT = process.env.PORT || 3000;
const TARGET = process.env.TARGET || 'localhost:4000';

const client = new recipe.RecipeService(  TARGET,
grpc.credentials.createInsecure() 
);
const getMetaData = util.promisify(client.getMetaData.bind(client)); const getRecipe = util.promisify(client.getRecipe.bind(client));

server.get('/', async () => {
const [meta, recipe] = await Promise.all([ getMetaData({}), 
getRecipe({id: 42}), 
]);

return {
consumer_pid: process.pid, producer_data: meta, recipe
};
});

server.listen(PORT, HOST, () => {
console.log(`Consumer running at http://${HOST}:${PORT}/`);

});
'''


path='recipe-api/producer-http-basic-master.js'
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''


path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''
path=''
code='''
'''

path=''
code='''
'''


create_folders_file(path,code)



