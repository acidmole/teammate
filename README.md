A small guide for peer review:

The app can be tested at http://tsoha-teammate.herokuapp.com/

- For admin rights, use foo/bar for login
- For user rights, just register
- "Pelaajat" guides you to player list to view players' personal information and top performance. You can also compare players' stats with each other.
- "Tapahtumat" guides you to events to view them. Events view has a filter with a couple of time options. Admins can also add, modify and delete events. Single event can also be viewed. Events 
can be commented but comments can't be removed. For each event all users can declare themselves either "in" or "out".
- "Tilastot" guides you to stats page where you can view personal or team match stats, or practice stats. Stats can be added. In case of a typo or other error stat can be input, for the app will 
update any stat line it finds.
- "Käyttäjät" shows every user. Admins can edit or delete any user. Deleting a user takes them to Graveyard where they can be resurrected ie. brought back. Users in graveyard can not log in 
and are not shown in player list but are visible in statistics for coherence.
- "Muokkaa tietojani" brings you to edit your information
- "Kirjaudu ulos" for logout

A short guide for Finnish basketball stat acronyms: 2P/A = 2 points shots made/attempted (1P = free throws, 3P = threepointers), PL = puolustuslevypallo = defensive rebound, HL = hyökkäyslevypallo = offensive rebound, V = virhe = foul, S = syöttö = assist, M = menetys = turnover, R = riisto = steal, B = blokki = block, P = pisteet = points.

Known bugs and unfinished features:
* editing events has troubles with saving starting time
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

