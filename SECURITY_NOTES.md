09/15/2026
- [ANON] GET /recipes -> 200 OK, returns full list of recipes
- [ANON] DELETE /recipes/1 -> 204 No Content, recipe
removed from list
Anyone who can reach the API (no login, no token) can read all recipes and delete specific recipes. The responses look correct, but there is no security.