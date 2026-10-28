## Before invalidation (stale cache)

# 1) GET /recipes
curl -i http://localhost:5000/recipes
# response body:
[ ... old list ... ]

# 2) POST /recipes
curl -i -X POST http://localhost:5000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title": "Stale Cache Test", ...}'
# response body:
{ ... created recipe ... }

# 3) GET /recipes
curl -i http://localhost:5000/recipes
# response body:
[ ... still missing "Stale Cache Test" ... ]


## After invalidation (cache fixed)

# 1) GET /recipes
curl -i http://localhost:5000/recipes
# response body:
[ ... some list ... ]

# 2) POST /recipes
curl -i -X POST http://localhost:5000/recipes \
  -H "Content-Type: application/json" \
  -d '{"title": "Fresh Cache Test", ...}'
# response body:
{ ... created recipe ... }

# 3) GET /recipes
curl -i http://localhost:5000/recipes
# response body:
[ ... includes "Fresh Cache Test" ... ]