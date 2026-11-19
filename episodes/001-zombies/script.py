"""Episode 001. Every line: (spoken text, visual, optional caption override).
Visuals: ("hook", text) ("big", text, sub) ("card", value, label, source) ("icon", key, word)
         ("choice", A, B) ("odds", value) ("list", [items]) ("final", value, label)"""
TITLE = "What If Zombies Took Over Tomorrow?"
SLUG = "zombies"
VOICE = "Charon"
STYLE = ("Narrate in English as a calm, gripping documentary narrator. Medium pace, low and steady, "
         "a little tension, with a clear short pause after every sentence:")
START_ODDS = 50

CHAPTERS = [
 dict(label="HOUR 0", tag="THE WARNING", accent="#FFB020", lines=[
  ("The dead are walking. Now what?", ("hook", "THE DEAD ARE WALKING")),
  ("It's seven a.m. tomorrow. The first reports look like a prank.", ("big", "7:00 AM", "TOMORROW")),
  ("By eight, every channel shows the same warning. Stay inside. Lock your doors.", ("big", "STAY INSIDE", "EVERY CHANNEL. SAME WARNING.")),
  ("This is The Survivometer. We run the scenario hour by hour, and at the end, we estimate your odds of surviving one full year.", ("big", "THE SURVIVOMETER", "HOUR BY HOUR. ONE FULL YEAR.")),
  ("Right now, your odds are fifty percent. Every choice you make moves the needle.", ("odds", 50)),
 ]),
 dict(label="HOUR 1", tag="THE FIRST INSTINCT", accent="#FF8A1F", lines=[
  ("Hour one. Your first instinct is to grab your keys and drive.", ("icon", "car", "DRIVE?")),
  ("So is everyone else's.", ("big", "EVERYONE", "HAS THE SAME IDEA")),
  ("In a real evacuation, highways lock up fast. A city of a million people cannot empty through a handful of roads.", ("card", "1,000,000", "PEOPLE. A HANDFUL OF ROADS.", "")),
  ("And a traffic jam is the worst place to be. No walls, no supplies, and no way out.", ("list", ["NO WALLS", "NO SUPPLIES", "NO WAY OUT"])),
  ("Choice one. Leave now, or stay put?", ("choice", "LEAVE NOW", "STAY PUT")),
  ("The smart move is boring. Stay home. Fill every container you own with tap water, and charge everything you have.", ("list", ["STAY HOME", "FILL EVERY CONTAINER", "CHARGE EVERYTHING"])),
  ("Then take stock. Count your food, your medicine, and your batteries. Knowing what you have is the first step to making it last.", ("list", ["COUNT YOUR FOOD", "YOUR MEDICINE", "YOUR BATTERIES"])),
  ("Water first, because it is the one thing you cannot improvise later.", ("icon", "drop", "WATER FIRST")),
  ("If you stayed, your odds climb to fifty five percent.", ("odds", 55)),
 ]),
 dict(label="HOUR 6", tag="THE SIGNAL DIES", accent="#FF6A2A", lines=[
  ("Hour six. Your phone still has a signal, but not for long.", ("icon", "phone", "SIGNAL")),
  ("Cell towers run on grid power. When the grid struggles, they fall back on batteries, and those typically last between two and eight hours.", ("card", "2-8 HRS", "TYPICAL CELL TOWER BATTERY BACKUP", "Sources: FCC backup power rule, industry reports")),
  ("Some towers have generators that can run for days. But someone has to refuel them, and nobody is coming.", ("big", "NOBODY", "IS COMING TO REFUEL")),
  ("So use the network while it exists. Send one message to the people you love. Where you are, and where you will meet.", ("list", ["ONE MESSAGE", "WHERE YOU ARE", "WHERE YOU WILL MEET"])),
  ("Then download offline maps, and write the important phone numbers on paper.", ("icon", "map", "OFFLINE MAPS")),
  ("And do not waste battery scrolling for news. Every station will repeat the same thing, and none of it will change what you need to do.", ("big", "SAVE YOUR BATTERY", "THE NEWS WILL NOT CHANGE YOUR PLAN")),
  ("A plan made now is worth more than anything you can grab later. Do this, and you gain three points.", ("odds", 58)),
 ]),
 dict(label="DAY 1", tag="THE LIGHTS GO OUT", accent="#FF4D3D", lines=[
  ("Day one. The lights flicker, then go out.", ("icon", "bolt", "BLACKOUT")),
  ("Power plants are not as automatic as they look. They need fuel deliveries and human operators around the clock.", ("big", "24 / 7", "FUEL AND HUMAN OPERATORS")),
  ("Energy analysts who gamed out exactly this scenario estimated that fossil fuel plants would start shutting down within about twenty four hours.", ("card", "24 HRS", "UNTIL FOSSIL PLANTS START TO TRIP", "Source: Rocky Mountain Institute"), "Energy analysts who gamed out exactly this scenario estimated that fossil fuel plants would start shutting down within about 24 hours."),
  ("When enough plants drop out, the rest disconnect to protect themselves, and the blackout spreads like dominoes.", ("big", "DOMINOES", "ONE PLANT TRIPS THE NEXT")),
  ("No power means no gas pumps, no card payments, no refrigeration, and no elevators.", ("list", ["NO GAS PUMPS", "NO CARD PAYMENTS", "NO REFRIGERATION", "NO ELEVATORS"])),
  ("If you live on the twentieth floor, you now live on a mountain.", ("big", "20TH FLOOR", "IS NOW A MOUNTAIN")),
  ("And the silence is new. No traffic, no hum of machines. Sound now travels far, and so does light. A single candle in a window can be seen from blocks away.", ("big", "LIGHT AND NOISE", "NOW TRAVEL FAR")),
  ("Hospitals switch to backup generators, but their fuel tanks are measured in days, not weeks.", ("icon", "cross", "DAYS, NOT WEEKS")),
  ("Odds check. If you filled your bathtub in hour one, you hold at fifty five. If you did not, you just dropped to forty.", ("odds", 55)),
 ]),
 dict(label="DAY 3", tag="THE REAL ENEMY", accent="#FF2E4D", lines=[
  ("Day three. This is where the scenario turns.", ("big", "DAY 3", "WHERE THE SCENARIO TURNS")),
  ("Water pressure in most cities depends on electric pumps. Water towers buy you roughly a day. After that, the taps run dry.", ("icon", "drop", "TAPS RUN DRY")),
  ("A person can last weeks without food, but only about three days without water.", ("card", "3 DAYS", "WITHOUT WATER", "")),
  ("And the stores? A typical city holds about a three day supply of fresh food. The whole system is built on trucks arriving just in time.", ("card", "3 DAYS", "OF FRESH FOOD IN A TYPICAL CITY", "Source: Evan Fraser, University of Guelph")),
  ("There is an old saying. Society is nine meals away from chaos.", ("big", "9 MEALS", "AWAY FROM CHAOS")),
  ("By day three, the shelves are empty, and so is the patience of everyone who counted on them.", ("icon", "cart", "EMPTY SHELVES")),
  ("Here is the uncomfortable truth. At this point, zombies are not your main problem. Thirst, bad water, and desperate neighbors are.", ("list", ["THIRST", "BAD WATER", "DESPERATE NEIGHBORS"])),
  ("Choice two. Go out and compete for what is left, or stay quiet and stretch what you have?", ("choice", "GO OUT", "STAY QUIET")),
  ("If you have water, the math says wait. Every day you stay hidden, the crowds outside get smaller.", ("big", "WAIT", "THE CROWDS GET SMALLER")),
  ("Boil or filter anything you collect. After real disasters, dirty water is one of the biggest dangers.", ("icon", "fire", "BOIL IT")),
  ("Stay disciplined, and your odds hold at fifty. Panic, and they fall to twenty five.", ("odds", 50)),
 ]),
 dict(label="WEEK 1", tag="LEAVE THE CITY", accent="#C13CFF", lines=[
  ("Week one. The city is quiet, and quiet is a trap.", ("big", "QUIET", "IS A TRAP")),
  ("Without power, sewage pumps stop. During a one day blackout in San Diego in twenty eleven, sewage systems began backing up in under twelve hours.", ("card", "12 HRS", "UNTIL SEWAGE BACKED UP, SAN DIEGO 2011", "Source: Rocky Mountain Institute"), "Without power, sewage pumps stop. During a one day blackout in San Diego in 2011, sewage systems began backing up in under 12 hours."),
  ("Now imagine a week. Disease moves in where sanitation moves out.", ("icon", "warn", "DISEASE")),
  ("Your food is running low, and your apartment was never built to be a fortress.", ("icon", "house", "NOT A FORTRESS")),
  ("Choice three. Stay in the city, or leave it?", ("choice", "STAY IN THE CITY", "LEAVE IT")),
  ("This time, the answer flips. Cities have the most people, which means the most infected, and the least food per person.", ("list", ["MOST PEOPLE", "MOST INFECTED", "LEAST FOOD PER PERSON"])),
  ("You want distance, fresh water, and land. Think river, lake, small town, or farm.", ("list", ["DISTANCE", "FRESH WATER", "LAND"])),
  ("Travel at dawn. Avoid highways. A bicycle is silent, never needs fuel, and can go around any wreck.", ("icon", "bike", "SILENT. NO FUEL.")),
  ("Pack light. Water, a way to clean more water, food for three days, a first aid kit, and good shoes. Everything else slows you down.", ("list", ["WATER + A FILTER", "3 DAYS OF FOOD", "FIRST AID KIT", "GOOD SHOES"])),
  ("And do not go alone. A small group can keep watch, carry more, and still stay quiet. Four to eight people is the sweet spot.", ("card", "4-8", "PEOPLE. THE SWEET SPOT.", "")),
  ("Leave with a group and a destination, and you rise to sixty percent. Leave alone with no plan, and you sink to fifteen.", ("odds", 60)),
 ]),
 dict(label="MONTH 1", tag="THE SLOW THREATS", accent="#3C8CFF", lines=[
  ("Month one. You made it out. Now the slow threats arrive.", ("big", "MONTH 1", "THE SLOW THREATS")),
  ("The first is infection. Not the zombie kind. A deep cut, a bad tooth, a blister on a long walk. Without medicine, small injuries become serious.", ("icon", "cross", "SMALL INJURIES")),
  ("Before the outbreak, a pharmacy was five minutes away. Now, prevention is your only medicine. Clean every wound. Boil your water. Rest when you are sick.", ("list", ["CLEAN EVERY WOUND", "BOIL YOUR WATER", "REST WHEN SICK"])),
  ("The second is food. Canned goods will not last forever, and hunting is much harder than movies suggest.", ("icon", "cart", "FOOD")),
  ("The calories that built civilizations came from boring things. Potatoes, beans, grain, and eggs.", ("list", ["POTATOES", "BEANS", "GRAIN", "EGGS"])),
  ("The third threat is the one nobody expects. Your own mind.", ("big", "YOUR MIND", "THE THREAT NOBODY EXPECTS")),
  ("Isolation and constant fear wear people down. Groups that keep routines, share the work, and give everyone a job hold together.", ("list", ["KEEP ROUTINES", "SHARE THE WORK", "EVERYONE HAS A JOB"])),
  ("So the most valuable people in month one are not fighters. They are nurses, farmers, mechanics, and the one person who keeps everyone calm.", ("list", ["NURSES", "FARMERS", "MECHANICS", "THE CALM ONE"])),
  ("Choice four. Hide your group from other survivors, or trade with them?", ("choice", "HIDE", "TRADE")),
  ("Trade. A community with a medic, a well, and a garden is a place people will defend.", ("list", ["A MEDIC", "A WELL", "A GARDEN"])),
  ("Find one, and your odds jump to seventy percent. Stay hidden in the woods, and they sink to thirty.", ("odds", 70)),
 ]),
 dict(label="YEAR 1", tag="THE TWIST", accent="#22D37A", lines=[
  ("Year one. Here is the twist the movies skip.", ("big", "YEAR 1", "THE TWIST THE MOVIES SKIP")),
  ("The zombies have a problem too. A body that never rests, never heals, and stays out in sun, rain, and frost slowly breaks down.", ("list", ["NEVER RESTS", "NEVER HEALS", "SUN. RAIN. FROST."])),
  ("In this scenario, time is on your side. The first winter does more damage to them than any army could.", ("icon", "snow", "THE FIRST WINTER")),
  ("If you are alive at the one year mark, you are no longer running. You are rebuilding.", ("big", "REBUILDING", "NOT RUNNING ANYMORE")),
  ("And you are not the same person who heard that first warning. You know your neighbors. You know how to grow food, fix a wheel, and purify water.", ("list", ["GROW FOOD", "FIX A WHEEL", "PURIFY WATER"])),
  ("Solar panels still work. Books still exist. Bicycles, hand tools, and seeds become the new gold.", ("list", ["SOLAR PANELS", "BOOKS", "TOOLS AND SEEDS"])),
  ("So, what were your odds?", ("big", "YOUR ODDS?", "")),
  ("If you ran for the highway in hour one, alone, with no water and no plan, the Survivometer gives you four percent.", ("final", 4, "ALONE. NO WATER. NO PLAN.")),
  ("If you stayed calm, stored water, sent one message, left the city in week one with a small group, and joined a community, your odds of seeing year one are sixty eight percent.", ("final", 68, "CALM. WATER. A GROUP. A COMMUNITY.")),
  ("The difference was never strength. It was the first six hours.", ("big", "THE FIRST 6 HOURS", "NOT STRENGTH")),
  ("Tell us in the comments. Where would you go in week one, and who are you taking with you?", ("big", "WHERE WOULD YOU GO?", "TELL US IN THE COMMENTS")),
  ("And tell us which scenario the Survivometer should run next.", ("big", "WHAT IF...?", "PICK THE NEXT SCENARIO")),
  ("See you in the next what if.", ("big", "THE SURVIVOMETER", "SEE YOU IN THE NEXT WHAT IF")),
 ]),
]
# TTS requests: one per group of chapters (voice quota is about 10 requests a day)
GROUPS = [[0, 1], [2], [3], [4], [5], [6], [7]]
