A small guide for peer review:

The app can be tested at http://tsoha-teammate.herokuapp.com/

- For admin rights, use foo/bar for login
- For user rights, just register
- "Pelaajat" guides you to player list to view players' personal information
- "Tapahtumat" guides you to events to view events. Admins can also add and modify events.
- "Tilastot" guides you to stats page where you can view personal or team match stats, or practice stats

A short guide for Finnish basketball stat acronyms: 2P/A = 2 points shots made/attempted (1P = free throws, 3P = threepointers), PL = puolustuslevypallo = defensive rebound, HL = hyökkäyslevypallo = offensive rebound, V = virhe = foul, S = syöttö = assist, M = menetys = turnover, R = riisto = steal, B = blokki = block, P = pisteet = points.

Known bugs and unfinished features:
* editing events has troubles with saving starting time
* adding statistics unavailable
* personal statistics page missing shot percentages
* awful appearance
* all templates are not extended from layout.html
* null/missing stats shows None or something else weird
* events should be HH:MM and stats MM:SS, not always the case

# teammate
Basketball team's schedule and statistics app

Teammate is a web application designed to assist a basketball team with their everyday schedule management.

The app has three major functions:
1) Practice & Game schedule
2) Player information
3) Team and player game statistics 

Features:

Practices and games:
This feature is to show upcoming and past events and to monitor players' attendance.
- Admins can create practices and games with date, time and location information and a participant list. By default, only future practices and games are shown, in chronological order
- Players and admins can announce their attendance either "in" or "out" for every event
- Events can be coḿmented by players and admins.
- Practice attendance statistics are available

Player information:
Each player has a personal information page.
- Includes general information, such as name, jersey number etc.
- Includes player's brief attendance history 
- Includes summary of game statistics
- Includes top game performance

Game statistics:
Statistics from games.
- Admins can include game statistics for each game
- Summary, top performance and various lists for games, players and teams included

