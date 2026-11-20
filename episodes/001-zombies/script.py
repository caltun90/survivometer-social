"""Episode 001. Every line: (spoken text, visual, optional caption override).
Visuals: ("hook", text) ("big", text, sub) ("card", value, label, source) ("icon", key, word)
         ("choice", A, B) ("odds", value) ("list", [items]) ("final", value, label)"""
TITLE = "What If Zombies Took Over Tomorrow?"
SLUG = "zombies"
VOICE = "Algenib"
STYLE = ("Narrate in English as a calm, gripping documentary narrator. Medium pace, low and steady, "
         "a little tension, with a clear short pause after every sentence:")
KOKORO_VOICE = "am_michael"   # Cem chose it, 20 Nov 2026 (local Kokoro voice, same every time)
START_ODDS = 50

CHAPTERS = [
 dict(label="HOUR 0", clock="07:00", tag="THE OUTBREAK", accent="#FFB020", lines=[
  ("The dead are walking. Now what?", ("hook", "THE DEAD ARE WALKING")),
  ("It's seven a.m. tomorrow. Your phone explodes with alerts. A strange outbreak started overnight at a city hospital.", ("big", "7:00 AM", "TOMORROW")),
  ("Then you hear it outside. A scream, a car alarm, and something walking slowly down the middle of your street.", ("big", "SOMETHING", "IS WALKING DOWN YOUR STREET")),
  ("In this scenario, the rules are classic. They are slow. They follow sound and light. And one bite is all it takes.", ("list", ["THEY ARE SLOW", "SOUND AND LIGHT", "ONE BITE"])),
  ("This is The Survivometer. We run the scenario hour by hour, and at the end, we estimate your odds of surviving one full year.", ("big", "THE SURVIVOMETER", "HOUR BY HOUR. ONE FULL YEAR.")),
  ("Right now, your odds are fifty percent. Every choice you make moves the needle.", ("odds", 50)),
 ]),
 dict(label="HOUR 1", clock="08:00", tag="THE FIRST INSTINCT", accent="#FF8A1F", lines=[
  ("Hour one. Someone is pounding on your door. It's your neighbor from across the hall, and he does not answer when you call his name.", ("big", "KNOCK KNOCK", "DO NOT OPEN IT")),
  ("You don't open it. Good call.", ("big", "GOOD CALL", "THE DOOR STAYS SHUT")),
  ("Out the window, the whole city has the same idea. Grab the keys and drive.", ("icon", "car", "DRIVE?")),
  ("But a city of a million people cannot empty through a handful of roads. Within an hour, the highway is a parking lot, and the dead are walking between the cars.", ("card", "1,000,000", "PEOPLE. A HANDFUL OF ROADS.", "")),
  ("Choice one. Join the traffic, or stay put?", ("choice", "JOIN THE TRAFFIC", "STAY PUT")),
  ("Stay. Push the heaviest furniture against the door, close the curtains, and fill every container you own with tap water while it still runs.", ("list", ["BARRICADE THE DOOR", "CLOSE THE CURTAINS", "FILL EVERY CONTAINER"])),
  ("Then take stock. Count your food, your medicine, and your batteries.", ("list", ["COUNT YOUR FOOD", "YOUR MEDICINE", "YOUR BATTERIES"])),
  ("You stayed, and your odds climb to fifty five percent.", ("odds", 55)),
 ]),
 dict(label="HOUR 6", clock="13:00", tag="THE CITY FALLS", accent="#FF6A2A", lines=[
  ("Hour six. The sirens have stopped. That is not a good sign.", ("big", "SILENCE", "THE SIRENS STOPPED")),
  ("From your window you count them. Ten on your block. Then thirty. Every scream pulls more of them toward the noise.", ("big", "10... 30...", "EVERY SCREAM PULLS MORE")),
  ("Your phone still has a signal, but not for long. Cell towers fall back on batteries that typically last between two and eight hours.", ("card", "2-8 HRS", "TYPICAL CELL TOWER BATTERY BACKUP", "Sources: FCC backup power rule, industry reports")),
  ("So use it now. Send one message to the people you love. Where you are, and where you will meet.", ("list", ["ONE MESSAGE", "WHERE YOU ARE", "WHERE YOU WILL MEET"])),
  ("Then put the phone on silent. A ringtone through a thin door is a dinner bell.", ("big", "SILENT MODE", "A RINGTONE IS A DINNER BELL")),
  ("Download offline maps, write the important numbers on paper, and plan your way out of the city.", ("icon", "map", "OFFLINE MAPS")),
  ("Quiet and prepared, you gain three points.", ("odds", 58)),
 ]),
 dict(label="DAY 1", clock="19:40", tag="THE LIGHTS GO OUT", accent="#FF4D3D", lines=[
  ("Day one. The lights flicker, then go out.", ("icon", "bolt", "BLACKOUT")),
  ("Power plants need fuel deliveries and people at the controls. Energy analysts who gamed out this exact scenario estimated that fossil fuel plants would start shutting down within about twenty four hours.", ("card", "24 HRS", "UNTIL FOSSIL PLANTS START TO TRIP", "Source: Rocky Mountain Institute"), "Power plants need fuel deliveries and people at the controls. Energy analysts who gamed out this exact scenario estimated that fossil fuel plants would start shutting down within about 24 hours."),
  ("Then the blackout spreads like dominoes. No gas pumps, no card payments, no refrigeration, and no elevators.", ("list", ["NO GAS PUMPS", "NO CARD PAYMENTS", "NO FRIDGES", "NO ELEVATORS"])),
  ("That night, the city is darker than it has been in a hundred years. And in the dark, light is a beacon.", ("big", "LIGHT", "IS A BEACON")),
  ("Across the street, a family lights candles and a camping lantern. Within an hour, a crowd of the dead is pressed against their front door.", ("big", "ONE LANTERN", "ONE HUNGRY CROWD")),
  ("Choice two. Light a candle, or sit in the dark?", ("choice", "LIGHT A CANDLE", "SIT IN THE DARK")),
  ("You sit in the dark, you whisper, and you wait for morning.", ("big", "DARK AND QUIET", "WAIT FOR MORNING")),
  ("If you stayed dark, you climb to sixty. If you lit up your window, you just dropped to thirty five.", ("odds", 60)),
 ]),
 dict(label="DAY 3", clock="11:50", tag="THE SUPPLY RUN", accent="#FF2E4D", lines=[
  ("Day three. The taps run dry.", ("icon", "drop", "TAPS RUN DRY")),
  ("City water pressure depends on electric pumps. Water towers buy you about a day, and then nothing comes out.", ("big", "NO POWER", "NO WATER PRESSURE")),
  ("A person can last weeks without food, but only about three days without water.", ("card", "3 DAYS", "WITHOUT WATER", "")),
  ("The grocery store two blocks away is your best chance. A typical city holds only about three days of fresh food, so whatever is left will not last.", ("card", "3 DAYS", "OF FRESH FOOD IN A TYPICAL CITY", "Source: Evan Fraser, University of Guelph")),
  ("Choice three. Go now, at noon, or wait for the cover of night?", ("choice", "GO AT NOON", "GO AT NIGHT")),
  ("Go at noon. They hunt by sound and light, and at night you would need a flashlight. In daylight, you see them first.", ("big", "NOON", "YOU SEE THEM FIRST")),
  ("You move low between parked cars. Soft shoes, an empty backpack, and a crowbar for opening doors, not for fighting.", ("list", ["SOFT SHOES", "EMPTY BACKPACK", "A TOOL FOR DOORS"])),
  ("Inside, the shelves are almost bare. You grab water, canned beans, and a first aid kit.", ("list", ["WATER", "CANNED FOOD", "FIRST AID KIT"])),
  ("Then a shopping cart crashes in the next aisle. Every head in the store turns toward the sound.", ("big", "CRASH", "EVERY HEAD TURNS")),
  ("You don't run. You walk out the back door, slow and silent, while they shuffle toward the noise.", ("big", "DON'T RUN", "WALK. SLOW. SILENT.")),
  ("You made it home with five days of water. Your odds rise to sixty two.", ("odds", 62)),
 ]),
 dict(label="WEEK 1", clock="05:55", tag="THE ESCAPE", accent="#B05CFF", lines=[
  ("Week one. The city has gone quiet. The living are hiding, and the dead are everywhere.", ("big", "WEEK 1", "THE CITY GOES QUIET")),
  ("Without power, sewers back up. In San Diego's two thousand eleven blackout, sewage started spilling within hours. Disease is now as dangerous as any bite.", ("card", "HOURS", "UNTIL SEWAGE SPILLED. SAN DIEGO, 2011", "Source: Rocky Mountain Institute"), "Without power, sewers back up. In San Diego's 2011 blackout, sewage started spilling within hours. Disease is now as dangerous as any bite."),
  ("Choice four. Stay in the city, or leave?", ("choice", "STAY", "LEAVE")),
  ("Leave. Cities have the most people, the most infected, and the least food per person.", ("list", ["MOST PEOPLE", "MOST INFECTED", "LEAST FOOD"])),
  ("Your target is a lake an hour north. Fresh water, open views, and far fewer of them.", ("list", ["FRESH WATER", "OPEN VIEWS", "FEWER OF THEM"])),
  ("You leave at dawn on a bicycle. It is silent, it needs no fuel, and it fits between crashed cars.", ("icon", "bike", "BICYCLE")),
  ("You hear them before you see them. A low groan, and the scrape of a thousand shoes on asphalt.", ("big", "LISTEN", "A THOUSAND SHOES")),
  ("On the bridge out of town, a herd blocks the road. Hundreds of them, shuffling east.", ("big", "THE HERD", "HUNDREDS OF THEM")),
  ("You lie in a ditch for an hour, barely breathing, until the last one passes.", ("big", "ONE HOUR", "IN A DITCH")),
  ("On the other side, you meet five survivors heading north. Leaving with a group, your odds rise to sixty five.", ("odds", 65)),
 ]),
 dict(label="MONTH 1", clock="22:30", tag="THE CAMP", accent="#3A8BFF", lines=[
  ("Month one. Your group has a camp by the lake.", ("big", "MONTH 1", "THE LAKE CAMP")),
  ("You build a fence from pallets and car doors, hang empty cans on a wire as an alarm, and take turns on night watch.", ("list", ["A FENCE", "CAN ALARMS", "NIGHT WATCH"])),
  ("The dangers now are small and boring. A cut that gets infected. Water you forgot to boil.", ("list", ["INFECTED CUTS", "UNBOILED WATER", "EXHAUSTION"])),
  ("Then one night, the cans start rattling.", ("big", "RATTLE", "THE ALARM GOES OFF")),
  ("Twelve of them at the fence. Nobody screams. You turn off every light, and you lure them away with a radio playing music on the far side of the lake.", ("big", "A DECOY", "MUSIC ACROSS THE LAKE")),
  ("By sunrise, they are gone. The fence held, and so did the plan.", ("big", "SUNRISE", "THE FENCE HELD")),
  ("Food is the next fight. The cans run out, so you plant fast crops and learn to fish.", ("list", ["POTATOES", "BEANS", "FISH"])),
  ("Choice five. Hide from other survivors, or trade with them?", ("choice", "HIDE", "TRADE")),
  ("Trade. A group with a nurse, a mechanic, and a farmer is a place people will defend. Your odds climb to sixty six.", ("odds", 66)),
 ]),
 dict(label="YEAR 1", clock="06:30", tag="THE TWIST", accent="#22D37A", lines=[
  ("Year one. Here is the twist the movies skip.", ("big", "YEAR 1", "THE TWIST THE MOVIES SKIP")),
  ("The dead have a problem too. A body that never rests and never heals slowly falls apart in sun, rain, and frost.", ("list", ["NEVER RESTS", "NEVER HEALS", "SUN. RAIN. FROST."])),
  ("The first winter freezes them in the fields like statues. By spring, the herds are slower, thinner, and fewer.", ("icon", "snow", "THE FIRST WINTER")),
  ("Survivors even learn to steer the slow herds away with noise, like shepherds with a radio.", ("big", "NOISE", "IS NOW A TOOL")),
  ("Your camp becomes a village. Solar panels, a garden, a workshop, and a school in an old barn.", ("list", ["SOLAR PANELS", "A GARDEN", "A WORKSHOP"])),
  ("You are no longer running. You are rebuilding.", ("big", "REBUILDING", "NOT RUNNING ANYMORE")),
  ("So, what were your odds?", ("big", "YOUR ODDS?", "")),
  ("If you jumped in your car in hour one, opened the door to your neighbor, or lit a candle on night one, the Survivometer gives you four percent.", ("final", 4, "THE CAR. THE DOOR. THE CANDLE.")),
  ("If you stayed quiet, stored water, made one careful supply run, left with a group, and built a camp, your odds of seeing year one are sixty eight percent.", ("final", 68, "QUIET. WATER. A GROUP. A CAMP.")),
  ("The difference was never strength. It was staying calm, and staying quiet.", ("big", "CALM AND QUIET", "NOT STRENGTH")),
  ("Tell us in the comments. What is the first thing you would grab, and who are you taking with you?", ("big", "WHAT WOULD YOU GRAB?", "TELL US IN THE COMMENTS")),
  ("And tell us which scenario the Survivometer should run next. See you in the next what if.", ("big", "WHAT IF...?", "PICK THE NEXT SCENARIO")),
 ]),
]
# TTS requests: one per group of chapters (voice quota is about 10 requests a day)
GROUPS = [[0, 1], [2, 3], [4, 5], [6, 7]]
