# Pickle

This simple web app helps to pick the best video from YouTube playlist. Backend is written with Django and Django REST Framework, frontend - with React!

## Backend posibilities

### User
- Register / Login user

### PickPlaylist
- Create Youtube playlist to pick for it's owner (`/api/create_pick_playlist/` ready endpoint)
- Created playlist must be open to read for all users! (TODO)
- Update (Edit) playlist name for it's owner or superuser only (TODO)
- Delete playlist for it's owner or superuser only! (TODO)
- Read playlist for all users (TODO)

### PickSession
- Create session for it's owner (`/api/create_pick_session` ready endpoint)
- Created session must be open to read for it's owner or superuser only! (TODO)
- Update session only through PickPair (`/api/pick_pair_video` endpoint) and PickSessionRound (`/api/get_next_session_round` endpoint) modification and their completion submit.
- Complete session through endpoint `submit_pick_session_completion` (onle by session owner or superuser).

