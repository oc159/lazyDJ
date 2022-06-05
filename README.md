# Lazy DJ
## Why spend 15 minutes adding songs to a playlist when you can take 6 hours to automate it?
A python consumer of the Spotify API to add playlists and Songs to said playlist

### Usage
1. Add songs to the tunes.txt file in the specified format
`Artist - Song Title`



2. Generate an oAuth token here:
https://developer.spotify.com/console/ 

    Required oAuth Scopes:
    - playlist-modify-private
    - playlist-read-collaborative
    - user-read-private

3. Add your OAuth Credential to the apiToken variable
`apiToken = ""`

4. Add your spotify userID to the user_id variable
`user_id = ""`