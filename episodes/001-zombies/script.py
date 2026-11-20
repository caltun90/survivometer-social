"""Episode 001. Every line: (spoken text, visual, optional caption override).
Visuals: ("hook", text) ("big", text, sub) ("card", value, label, source) ("icon", key, word)
         ("choice", A, B) ("odds", value) ("list", [items]) ("final", value, label)"""
TITLE = "What If Zombies Took Over Tomorrow?"
SLUG = "zombies"
VOICE = "Algenib"
STYLE = ("Narrate in English as a calm, gripping documentary narrator. Medium pace, low and steady, "
         "a little tension, with a clear short pause after every sentence:")
KOKORO_VOICE = "am_puck:0.3,am_fenrir:0.7"   # Cem chose this blend, 20 Nov 2026 (local Kokoro, same every time)
START_ODDS = 50

CHAPTERS = [
 dict(label="HOUR 0", clock="07:00", tag="THE PHONE WON'T STOP", accent="#FFB020", lines=[
  ("The dead are walking. Now what?", ("hook", "THE DEAD ARE WALKING")),
  ("It's seven in the morning, tomorrow. You're making coffee when your phone buzzes on the counter. Then again. And again. An outbreak at a city hospital, and one word on every screen. Lockdown.", ("big", "7:00 AM", "TOMORROW")),
  ("You go to the window. A car alarm is wailing, someone is screaming, and a man in a torn shirt is walking slowly down the middle of your street.", ("big", "SOMETHING", "IS WALKING DOWN YOUR STREET")),
  ("He doesn't flinch at the noise. He walks toward it. In this story, they are slow, they follow sound and light, and one bite is all it takes.", ("list", ["THEY ARE SLOW", "SOUND AND LIGHT", "ONE BITE"])),
  ("This is The Survivometer. We'll live through it hour by hour, and at the end, we'll see your odds of making it one full year.", ("big", "THE SURVIVOMETER", "HOUR BY HOUR. ONE FULL YEAR.")),
  ("Right now, it's a coin flip. Fifty percent. Every small decision from here moves the needle.", ("odds", 50)),
 ]),
 dict(label="HOUR 1", clock="08:00", tag="A KNOCK AT THE DOOR", accent="#FF8A1F", lines=[
  ("Eight in the morning. Someone is pounding on your door. It's your neighbor from across the hall. You call his name. He doesn't answer. He just keeps pounding.", ("big", "KNOCK KNOCK", "DO NOT OPEN IT")),
  ("You don't open it. You press your back against the door and wait until the pounding fades down the hallway.", ("big", "GOOD CALL", "THE DOOR STAYS SHUT")),
  ("Outside, the whole street has the same idea. Car doors slam, engines start, and everyone grabs their keys and drives.", ("icon", "car", "DRIVE?")),
  ("But a city of a million people can't squeeze through a handful of roads. Within an hour, the highway is a parking lot, and the dead are walking between the cars.", ("card", "1,000,000", "PEOPLE. A HANDFUL OF ROADS.", "")),
  ("You could join them. Most people do. You decide to stay put.", ("choice", "JOIN THE TRAFFIC", "STAY PUT")),
  ("You drag the bookshelf in front of the door, close the curtains, and fill every pot, bottle and bathtub you own while the water still runs.", ("list", ["BARRICADE THE DOOR", "CLOSE THE CURTAINS", "FILL EVERY CONTAINER"])),
  ("Then you sit on the kitchen floor and count what you have. Food for about a week, some painkillers, and a drawer full of half dead batteries.", ("list", ["COUNT YOUR FOOD", "YOUR MEDICINE", "YOUR BATTERIES"])),
  ("And there's a reserve most people forget. The water heater in your closet holds about forty gallons of clean water. Staying put pushes your odds to fifty five.", ("odds", 55)),
 ]),
 dict(label="HOUR 6", clock="13:00", tag="THE SIRENS STOP", accent="#FF6A2A", lines=[
  ("One in the afternoon. Something has changed, and it takes you a moment to notice. The sirens have stopped. Not because it's over. Because no one is left to answer the calls.", ("big", "SILENCE", "THE SIRENS STOPPED")),
  ("From your window you start counting. Ten on your block. Then thirty. Every car alarm and every scream pulls more of them toward the noise.", ("big", "10... 30...", "EVERY SCREAM PULLS MORE")),
  ("Your phone still shows one bar, but not for long. Cell towers run on backup batteries that typically last between two and eight hours.", ("card", "2-8 HRS", "TYPICAL CELL TOWER BATTERY BACKUP", "Sources: FCC backup power rule, industry reports")),
  ("So you use it while you can. One message to the people you love. Where you are, and where you'll meet if the phones die.", ("list", ["ONE MESSAGE", "WHERE YOU ARE", "WHERE YOU WILL MEET"])),
  ("Then you switch the phone to silent. Through a thin door, a ringtone is a dinner bell.", ("big", "SILENT MODE", "A RINGTONE IS A DINNER BELL")),
  ("You write the important numbers on paper and download offline maps. Your GPS doesn't need cell towers. It listens to satellites, and it keeps working long after the network is gone.", ("icon", "map", "OFFLINE MAPS")),
  ("Quiet, prepared, and still unseen. Your odds tick up to fifty eight.", ("odds", 58)),
 ]),
 dict(label="DAY 1", clock="19:40", tag="THE LIGHTS GO OUT", accent="#FF4D3D", lines=[
  ("Seven forty in the evening. The TV flickers, the fridge goes quiet, and the lights go out.", ("icon", "bolt", "BLACKOUT")),
  ("Power plants need fuel deliveries and people at the controls. Energy analysts who gamed out this exact scenario estimated that fossil fuel plants would start shutting down within about twenty four hours.", ("card", "24 HRS", "UNTIL FOSSIL PLANTS START TO TRIP", "Source: Rocky Mountain Institute"), "Power plants need fuel deliveries and people at the controls. Energy analysts who gamed out this exact scenario estimated that fossil fuel plants would start shutting down within about 24 hours."),
  ("Then it falls like dominoes. No gas pumps. No card readers, so suddenly only cash works. No refrigeration, and no elevators.", ("list", ["NO GAS PUMPS", "NO CARD PAYMENTS", "NO FRIDGES", "NO ELEVATORS"])),
  ("That night, the city is darker than it has been in a hundred years. And in the dark, any light is a beacon.", ("big", "LIGHT", "IS A BEACON")),
  ("Across the street, a family lights candles and a camping lantern. You watch the warm glow in their window. Within an hour, a crowd of the dead is pressed against their front door.", ("big", "ONE LANTERN", "ONE HUNGRY CROWD")),
  ("You look down at the box of matches in your hand. Then you put it back in the drawer.", ("choice", "LIGHT A CANDLE", "SIT IN THE DARK")),
  ("You sit in the dark, you whisper when you have to talk, and you wait for morning.", ("big", "DARK AND QUIET", "WAIT FOR MORNING")),
  ("Staying dark keeps you at sixty percent. That one candle would have dropped you to thirty five.", ("odds", 60)),
 ]),
 dict(label="DAY 3", clock="11:50", tag="THE TAPS RUN DRY", accent="#FF2E4D", lines=[
  ("Day three. You turn the kitchen tap. It coughs out a little air, and then nothing.", ("icon", "drop", "TAPS RUN DRY")),
  ("City water pressure depends on electric pumps. The water towers bought you about a day, and now they're empty too.", ("big", "NO POWER", "NO WATER PRESSURE")),
  ("You can last weeks without food, but only about three days without water. The bathtub is almost empty, and the water heater won't last forever.", ("card", "3 DAYS", "WITHOUT WATER", "")),
  ("The grocery store two blocks away is your best chance. A typical city holds only about three days of fresh food, so whatever is left is going fast.", ("card", "3 DAYS", "OF FRESH FOOD IN A TYPICAL CITY", "Source: Evan Fraser, University of Guelph")),
  ("You could wait for the cover of night. But think about how they hunt.", ("choice", "GO AT NOON", "GO AT NIGHT")),
  ("At night, you'd need a flashlight, and a flashlight is a beacon. So you go at noon, when you can see them first.", ("big", "NOON", "YOU SEE THEM FIRST")),
  ("You move low between the parked cars. Soft shoes, an empty backpack, and a crowbar. It's for opening doors, not for fighting.", ("list", ["SOFT SHOES", "EMPTY BACKPACK", "A TOOL FOR DOORS"])),
  ("Inside, the shelves are almost bare. You only take what matters. Water, canned beans, and a first aid kit.", ("list", ["WATER", "CANNED FOOD", "FIRST AID KIT"])),
  ("Then a shopping cart crashes over in the next aisle. Every head in the store turns toward the sound.", ("big", "CRASH", "EVERY HEAD TURNS")),
  ("You don't run. Running is loud. You walk out the back door, slow and silent, while they shuffle toward the noise.", ("big", "DON'T RUN", "WALK. SLOW. SILENT.")),
  ("You get home with five days of water on your back. Your odds rise to sixty two.", ("odds", 62)),
 ]),
 dict(label="WEEK 1", clock="05:55", tag="THE ROAD NORTH", accent="#B05CFF", lines=[
  ("Week one. The city has gone quiet. No traffic, no music, no planes. The living are hiding, and the dead are everywhere.", ("big", "WEEK 1", "THE CITY GOES QUIET")),
  ("Then the smell arrives. Without power, sewer pumps stop. In San Diego's two thousand eleven blackout, sewage started spilling within hours. Disease is now as dangerous as any bite.", ("card", "HOURS", "Until sewage spilled. San Diego, 2011", "Source: Rocky Mountain Institute"), "Then the smell arrives. Without power, sewer pumps stop. In San Diego's 2011 blackout, sewage started spilling within hours. Disease is now as dangerous as any bite."),
  ("You climb to the roof and look out over the city. You already know you can't stay.", ("choice", "STAY", "LEAVE")),
  ("Cities have the most people, the most infected, and the least food per person. Everything that kept you alive here is running out.", ("list", ["MOST PEOPLE", "MOST INFECTED", "LEAST FOOD"])),
  ("There's a lake an hour north. Fresh water, open views, and far fewer of them.", ("list", ["FRESH WATER", "OPEN VIEWS", "FEWER OF THEM"])),
  ("You leave at dawn on a bicycle. No fuel, no engine noise, and it slips between crashed cars where nothing else can.", ("icon", "bike", "BICYCLE")),
  ("On the road out, you hear them before you see them. A low groan, and the scrape of a thousand shoes on asphalt.", ("big", "LISTEN", "A THOUSAND SHOES")),
  ("On the bridge out of town, a herd blocks the road. Hundreds of them, all shuffling east, as if they're following a sound only they can hear.", ("big", "THE HERD", "HUNDREDS OF THEM")),
  ("You lie in a ditch for an hour, face in the wet grass, barely breathing, until the last one passes.", ("big", "ONE HOUR", "IN A DITCH")),
  ("On the other side, you meet five survivors heading north too. Strangers, but alive. With a group, your odds rise to sixty five.", ("odds", 65)),
 ]),
 dict(label="MONTH 1", clock="22:30", tag="LIFE BY THE LAKE", accent="#3A8BFF", lines=[
  ("Month one. Your group has a camp by the lake. A few tents, a fire pit, and an old canoe someone found in a boathouse.", ("big", "MONTH 1", "THE LAKE CAMP")),
  ("You build a fence from pallets and car doors, hang empty cans on a wire as an alarm, and take turns on night watch.", ("list", ["A FENCE", "CAN ALARMS", "NIGHT WATCH"])),
  ("The dangers now are small and boring. A cut that gets infected. Water someone forgot to boil. Nobody getting enough sleep.", ("list", ["INFECTED CUTS", "UNBOILED WATER", "EXHAUSTION"])),
  ("Then one night, you wake up to the sound you hoped you'd never hear. The cans are rattling.", ("big", "RATTLE", "THE ALARM GOES OFF")),
  ("Twelve of them at the fence. Nobody screams. You put out every light, and someone sets a little radio playing music on the far side of the lake.", ("big", "A DECOY", "MUSIC ACROSS THE LAKE")),
  ("One by one, they turn and shuffle toward the music. By sunrise, they're gone. The fence held, and so did the plan.", ("big", "SUNRISE", "THE FENCE HELD")),
  ("Food is the next fight. The cans run out, so you plant potatoes and beans, and you learn to fish properly.", ("list", ["POTATOES", "BEANS", "FISH"])),
  ("One afternoon, another group shows up at the crossroads. They have a nurse and a water filter. You have seeds and a mechanic.", ("choice", "HIDE", "TRADE")),
  ("So you trade instead of hiding. A group with a nurse, a mechanic, and a farmer is a place people will defend. Your odds climb to sixty six.", ("odds", 66)),
 ]),
 dict(label="YEAR 1", clock="06:30", tag="THE DEAD FALL APART", accent="#22D37A", lines=[
  ("Year one. And here is the part the movies always skip.", ("big", "YEAR 1", "THE TWIST THE MOVIES SKIP")),
  ("The dead have a problem too. A body that never rests and never heals slowly falls apart in sun, rain, and frost.", ("list", ["NEVER RESTS", "NEVER HEALS", "SUN. RAIN. FROST."])),
  ("The first winter freezes them in the fields like statues. By spring, the herds are slower, thinner, and fewer.", ("icon", "snow", "THE FIRST WINTER")),
  ("Ham radio operators link the camps together and warn each other when a herd is coming. Survivors even steer the slow herds away with noise, like shepherds.", ("big", "NOISE", "IS NOW A TOOL")),
  ("Your camp becomes a village. Solar panels, a garden, a workshop, and a school in an old barn.", ("list", ["SOLAR PANELS", "A GARDEN", "A WORKSHOP"])),
  ("You're no longer running. You're rebuilding.", ("big", "REBUILDING", "NOT RUNNING ANYMORE")),
  ("So, what were your odds?", ("big", "YOUR ODDS?", "")),
  ("If you jumped in your car in hour one, opened the door to your neighbor, or lit a candle on night one, the Survivometer gives you four percent.", ("final", 4, "THE CAR. THE DOOR. THE CANDLE.")),
  ("If you stayed quiet, saved water, made one careful supply run, left with a group, and built a camp, your odds of seeing year one are sixty eight percent.", ("final", 68, "QUIET. WATER. A GROUP. A CAMP.")),
  ("The difference was never strength. It was the small, quiet decisions you made in the first few hours.", ("big", "SMALL DECISIONS", "NOT STRENGTH")),
  ("Tell us in the comments. What's the first thing you'd grab, and who are you taking with you?", ("big", "WHAT WOULD YOU GRAB?", "TELL US IN THE COMMENTS")),
  ("And tell us which scenario the Survivometer should run next. See you in the next what if.", ("big", "WHAT IF...?", "PICK THE NEXT SCENARIO")),
 ]),
]
# TTS requests: one per group of chapters (voice quota is about 10 requests a day)
GROUPS = [[0, 1], [2, 3], [4, 5], [6, 7]]
