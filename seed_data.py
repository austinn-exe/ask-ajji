"""
Starter content for the Discover catalogue, covering the 8 top-level
categories the rest of the app (models.CulturalEntry.domain,
ai_pipeline.CATEGORIES) is built around. Extend this — or replace it
with real submissions — as the cultural database grows.

Each entry: name, description, why (why_it_matters), steps (ordered
list[str]), and optionally gender/subcategory/region/language/
image_url/source_url. None of the "why" text below claims to be an
authoritative historical record — it's framed as commonly-told
context, suitable for a hackathon demo, not a scholarly source.
"""

DOMAINS = [
    {"id": "food", "icon": "🍲", "color": "#a8412f"},
    {"id": "clothing", "icon": "🧵", "color": "#22304f"},
    {"id": "music", "icon": "🎶", "color": "#5c7a5e"},
    {"id": "rituals", "icon": "🪔", "color": "#7a4f9c"},
    {"id": "festivals", "icon": "🎉", "color": "#c1622d"},
    {"id": "practices", "icon": "🌿", "color": "#3f7a5c"},
    {"id": "language", "icon": "📖", "color": "#2f5f8a"},
    {"id": "games", "icon": "🪨", "color": "#e0a020"},
]

# Human-readable category names — these MUST match ai_pipeline.CATEGORIES
# exactly, since a completed Story's `category` field is one of these
# strings and /api/stats/cultural groups CulturalEntry + Story together.
FOOD = "Food & Recipes"
CLOTHING = "Clothing & Draping"
MUSIC = "Folk Music & Songs"
RITUALS = "Rituals & Traditions"
FESTIVALS_CAT = "Festivals"
PRACTICES = "Traditional Practices"
LANGUAGE = "Languages, Proverbs & Stories"
GAMES = "Games & Crafts"

ENTRIES = {
    FOOD: {
        "Maharashtra": [
            {"name": "Puran Poli", "subcategory": "Sweets", "region": "Western India", "language": "Marathi",
             "description": "A sweet flatbread stuffed with jaggery and split gram, rolled thin and cooked on a griddle.",
             "why": "Commonly made for Holi and Ganesh Chaturthi — households often treat the filling ratio as a closely guarded family recipe.",
             "steps": ["Cook split gram with jaggery until soft, then mash into a sweet puran filling.",
                       "Knead a soft wheat dough and let it rest.",
                       "Stuff a portion of dough with puran and roll it out gently into a thin round.",
                       "Cook on a hot griddle with ghee until golden on both sides."]},
            {"name": "Modak", "subcategory": "Sweets", "region": "Western India", "language": "Marathi",
             "description": "Steamed rice-flour dumplings filled with coconut and jaggery, pleated by hand into a teardrop shape.",
             "why": "Traditionally offered to Lord Ganesha; the pleating technique is often taught hand-over-hand by an elder.",
             "steps": ["Cook grated coconut with jaggery to make a soft filling.",
                       "Make a rice-flour dough with hot water and a little oil.",
                       "Shape small discs into cups and pleat the edges by hand.",
                       "Fill, seal into a point, and steam for about 10 minutes."]},
            {"name": "Misal Pav", "subcategory": "Street Food", "region": "Western India", "language": "Marathi",
             "description": "A spicy sprouted-lentil curry topped with farsan, onion and lime, eaten with soft bread rolls.",
             "why": "Grew out of a working-class breakfast and is now one of Maharashtra's most-loved street foods.",
             "steps": ["Sprout and boil moong or matki beans until tender.",
                       "Cook a spicy onion-tomato curry base with misal masala.",
                       "Add the sprouts to the curry and simmer.",
                       "Top with crunchy farsan, onion and lime, and serve with pav."]},
        ],
        "Punjab": [
            {"name": "Sarson da Saag", "subcategory": "Curries", "region": "North India", "language": "Punjabi",
             "description": "A slow-cooked mustard-greens curry, finished with a spoon of white butter.",
             "why": "Usually cooked through winter, timed to when mustard fields are in season.",
             "steps": ["Boil mustard and spinach leaves until soft.",
                       "Mash the greens into a coarse paste.",
                       "Simmer the paste with ginger, garlic and green chili.",
                       "Finish with a spoon of white butter before serving."]},
            {"name": "Chole Bhature", "subcategory": "Street Food", "region": "North India", "language": "Punjabi",
             "description": "Spiced chickpea curry served with deep-fried leavened bread.",
             "why": "A Sunday-morning dish in many Punjabi households.",
             "steps": ["Soak and boil chickpeas until soft.",
                       "Simmer them in a spiced onion-tomato gravy.",
                       "Knead a soft leavened dough for the bhature and let it rest.",
                       "Roll and deep-fry the bhature until puffed and golden."]},
        ],
        "Tamil Nadu": [
            {"name": "Pongal", "subcategory": "Breakfast", "region": "South India", "language": "Tamil",
             "description": "A savory rice-and-lentil dish tempered with ghee, cumin and black pepper.",
             "why": "Shares its name with the harvest festival it's traditionally cooked for.",
             "steps": ["Dry-roast rice and moong dal lightly.",
                       "Cook them together with water until soft and porridge-like.",
                       "Temper ghee with cumin, pepper and cashews.",
                       "Pour the tempering over the pongal and mix well."]},
            {"name": "Dosa", "subcategory": "Breakfast", "region": "South India", "language": "Tamil",
             "description": "A thin, crisp fermented rice-and-lentil crepe, cooked on a hot griddle.",
             "why": "The batter-grinding stone was traditionally a wedding gift, passed from mother to daughter.",
             "steps": ["Soak and grind rice and urad dal into a smooth batter.",
                       "Ferment the batter overnight.",
                       "Pour a ladle onto a hot griddle and spread thin in circles.",
                       "Drizzle oil around the edges and cook until crisp."]},
        ],
        "West Bengal": [
            {"name": "Shorshe Ilish", "subcategory": "Curries", "region": "Eastern India", "language": "Bengali",
             "description": "Hilsa fish cooked in a pungent mustard-seed and green-chili gravy.",
             "why": "Considered a centerpiece dish during Bengali festive meals, especially in monsoon season.",
             "steps": ["Grind mustard seeds with green chili into a smooth paste.",
                       "Marinate hilsa pieces lightly with turmeric and salt.",
                       "Simmer the mustard paste in mustard oil with the fish.",
                       "Cook gently until the gravy thickens and serve with rice."]},
        ],
        "Gujarat": [
            {"name": "Dhokla", "subcategory": "Snacks", "region": "Western India", "language": "Gujarati",
             "description": "A steamed, spongy savory cake made from fermented gram-flour batter.",
             "why": "A staple snack across Gujarati households, often served with a mustard-seed tempering.",
             "steps": ["Mix gram flour, yogurt and water into a batter and let it ferment slightly.",
                       "Add a leavening agent just before steaming.",
                       "Steam the batter in a greased tray until a toothpick comes out clean.",
                       "Temper with mustard seeds, curry leaves and green chili, then pour over the top."]},
        ],
        "Karnataka": [
            {"name": "Bisi Bele Bath", "subcategory": "Rice Dish", "region": "South India", "language": "Kannada",
             "description": "A spiced rice, lentil and vegetable one-pot dish flavored with a distinct bisi bele bath masala.",
             "why": "A comfort food across Karnataka households, often the centerpiece of a simple weekday meal.",
             "steps": ["Cook rice and toor dal together until soft.",
                       "Prepare a spice blend of dried red chilies, coriander and other whole spices.",
                       "Simmer vegetables with tamarind and the spice blend.",
                       "Combine with the cooked rice and dal, finishing with a ghee tempering."]},
        ],
        "Uttar Pradesh": [
            {"name": "Kebabs of Lucknow (Galouti)", "subcategory": "Mughlai Cuisine", "region": "North India", "language": "Urdu/Hindi",
             "description": "Finely minced, melt-in-the-mouth meat kebabs associated with the royal kitchens of Lucknow.",
             "why": "Said to have been created for a nawab who could no longer chew tougher cuts of meat.",
             "steps": ["Finely mince the meat and tenderize it with raw papaya paste.",
                       "Blend in a layered mix of roasted spices.",
                       "Rest the mixture to let the flavors and tenderizer work.",
                       "Shape into small patties and shallow-fry on a griddle until browned."]},
        ],
    },
    CLOTHING: {
        "Maharashtra": [
            {"name": "Nauvari Saree", "gender": "Women", "subcategory": "Saree Draping", "region": "Western India", "language": "Marathi",
             "description": "A nine-yard saree draped without a petticoat, tucked between the legs like a dhoti for ease of movement.",
             "why": "Traditionally worn by women who worked the fields or rode horses alongside men.",
             "steps": ["Tuck one end of the cloth firmly at the waist at the back.",
                       "Wrap it around the waist once to form the base.",
                       "Pass the length between the legs and tuck it in at the back, like a dhoti.",
                       "Pleat the remaining cloth and drape it over the shoulder."]},
        ],
        "Punjab": [
            {"name": "Phulkari Dupatta", "gender": "Women", "subcategory": "Embroidery", "region": "North India", "language": "Punjabi",
             "description": "A hand-embroidered shawl covered edge-to-edge in geometric silk-thread floral patterns.",
             "why": "Traditionally embroidered by female relatives as part of a bride's wedding trousseau.",
             "steps": ["Stretch a coarse cotton or khaddar fabric on a frame.",
                       "Mark out a geometric floral pattern across the cloth.",
                       "Fill the pattern using long-and-short darn stitches in colored silk thread.",
                       "Work from the reverse side so the stitch pattern shows evenly on the front."]},
            {"name": "Kurta Pajama with Pagri", "gender": "Men", "subcategory": "Turban", "region": "North India", "language": "Punjabi",
             "description": "A loose tunic and trouser set worn with a wrapped turban (pagri).",
             "why": "The way a pagri is tied can indicate region, occasion or social standing.",
             "steps": ["Wear the kurta over the pajama trousers.",
                       "Stretch the turban cloth out to its full length.",
                       "Wind it around the head in overlapping layers, tucking the end in neatly."]},
        ],
        "Kerala": [
            {"name": "Kasavu Saree", "gender": "Women", "subcategory": "Saree Draping", "region": "South India", "language": "Malayalam",
             "description": "An off-white cotton saree with a gold-thread (zari) border, worn plain without a printed pattern.",
             "why": "Closely associated with Onam and Vishu, when it's worn across generations of a family together.",
             "steps": ["Tuck the plain end of the saree at the waist and wrap around once.",
                       "Pleat the front section evenly and tuck it in at the center.",
                       "Wrap the remaining cloth around and drape the gold-bordered end over the shoulder."]},
        ],
        "Rajasthan": [
            {"name": "Bandhani Odhni", "gender": "Women", "subcategory": "Tie-Dye", "region": "North India", "language": "Rajasthani",
             "description": "A tie-dye veil cloth made by tying thousands of tiny knots before dyeing to create dot patterns.",
             "why": "Certain colors and patterns traditionally signal a wearer's community or marital status.",
             "steps": ["Pinch and tie small sections of fabric tightly with thread to resist dye.",
                       "Dye the tied cloth in a base color and let it dry.",
                       "Repeat tying and dyeing for each additional color in the pattern.",
                       "Untie all the knots to reveal the finished dotted design."]},
        ],
        "Tamil Nadu": [
            {"name": "Kanjeevaram Saree", "gender": "Women", "subcategory": "Saree Draping", "region": "South India", "language": "Tamil",
             "description": "A silk saree woven with thick zari borders, traditionally worn for weddings and temple visits.",
             "why": "Woven in Kanchipuram by families of weavers, often passed down as an heirloom across generations.",
             "steps": ["Select a contrasting silk thread for the border ahead of weaving.",
                       "Weave the body and border of the saree as separate sections, then interlock them by hand.",
                       "Weave the zari (metallic thread) pattern into the pallu.",
                       "Finish and press the saree before it's ready to wear."]},
        ],
        "Assam": [
            {"name": "Mekhela Chador", "gender": "Women", "subcategory": "Draping", "region": "Northeast India", "language": "Assamese",
             "description": "A two-piece traditional garment consisting of a wrapped bottom skirt (mekhela) and a draped upper cloth (chador).",
             "why": "Woven from local silks like muga and worn especially during Bihu celebrations.",
             "steps": ["Wrap the mekhela around the waist in wide pleats, tucking it in at the front.",
                       "Tuck the chador at the waist under the mekhela's upper edge.",
                       "Bring the chador across the chest and over the shoulder.",
                       "Secure the loose end neatly at the shoulder or waist."]},
        ],
    },
    MUSIC: {
        "Maharashtra": [
            {"name": "Lavani", "subcategory": "Folk Dance-Song", "region": "Western India", "language": "Marathi",
             "description": "A high-energy folk song and dance form performed to the beat of the dholki drum.",
             "why": "Said to have originally boosted the morale of soldiers, later growing into a full theatrical form.",
             "steps": ["The dholki player sets a fast, driving beat.",
                       "The lead singer performs verses with expressive gestures.",
                       "Dancers respond to the rhythm with sharp, energetic footwork."]},
        ],
        "West Bengal": [
            {"name": "Baul Gaan", "subcategory": "Devotional", "region": "Eastern India", "language": "Bengali",
             "description": "Mystic wandering-minstrel songs blending Hindu and Sufi ideas, sung with a one-stringed ektara.",
             "why": "Historically passed only from guru to disciple by voice, rarely written down.",
             "steps": ["The singer tunes the single-stringed ektara.",
                       "They begin with a simple, repeating melody.",
                       "Verses are often improvised, blending mystic themes as they sing."]},
        ],
        "Rajasthan": [
            {"name": "Manganiyar Folk Music", "subcategory": "Devotional", "region": "North India", "language": "Rajasthani",
             "description": "Devotional and celebratory songs performed by hereditary musician communities, using the kamaicha and dholak.",
             "why": "Passed down through families for generations, often performed for both Hindu and Muslim patrons.",
             "steps": ["The kamaicha player sets a droning melodic base.",
                       "The lead vocalist sings verses often centered on devotion or desert life.",
                       "The dholak and khartal add rhythm as the group responds in chorus."]},
        ],
        "Punjab": [
            {"name": "Boliyan", "subcategory": "Folk Verse", "region": "North India", "language": "Punjabi",
             "description": "Short, witty rhyming couplets sung and danced to during Bhangra and Giddha performances.",
             "why": "Often improvised on the spot to comment on family, love or daily village life.",
             "steps": ["A performer calls out a short rhyming couplet.",
                       "The group responds with a matching dance step or refrain.",
                       "Successive performers take turns adding new couplets."]},
        ],
        "Kerala": [
            {"name": "Sopana Sangeetham", "subcategory": "Devotional", "region": "South India", "language": "Malayalam",
             "description": "A slow, meditative style of devotional singing traditionally performed on temple steps.",
             "why": "Sung to accompany temple rituals, using minimal instrumentation to keep focus on the voice.",
             "steps": ["The singer stands near the temple sanctum steps.",
                       "They sing in a slow, sustained melodic style called raga-based phrasing.",
                       "An edakka drum player provides light, spare percussion.",
                       "The performance follows the pace of the accompanying ritual."]},
        ],
    },
    RITUALS: {
        "Maharashtra": [
            {"name": "Ganesh Visarjan", "subcategory": "Festival Ritual", "region": "Western India", "language": "Marathi",
             "description": "The immersion of the Ganesh idol in water at the close of Ganesh Chaturthi, carried out in a public procession.",
             "why": "Marks the god's journey home and is treated by many families as a farewell to a beloved guest.",
             "steps": ["Worship the idol at home each day of the festival with an aarti.",
                       "On the final day, carry the idol out in a procession with music and dance.",
                       "Reach a river, lake or the sea.",
                       "Immerse the idol in the water as a farewell."]},
        ],
        "West Bengal": [
            {"name": "Durga Puja Sindoor Khela", "subcategory": "Festival Ritual", "region": "Eastern India", "language": "Bengali",
             "description": "Married women smear vermillion on the Durga idol and each other on the festival's final day.",
             "why": "Celebrates the goddess's homecoming and is one of the few rituals traditionally led entirely by women.",
             "steps": ["Complete the final day's worship of the goddess.",
                       "Married women gather around the idol together.",
                       "They offer sweets and betel leaves to the goddess.",
                       "They smear vermillion on the idol and then on one another."]},
        ],
        "Punjab": [
            {"name": "Baisakhi Nagar Kirtan", "subcategory": "Religious Procession", "region": "North India", "language": "Punjabi",
             "description": "A procession of hymn-singing and martial displays marking the harvest and the founding of the Khalsa.",
             "why": "Combines a harvest celebration with a religious observance, traditionally led by five ceremonial guards.",
             "steps": ["Gather at the gurdwara for hymn-singing at dawn.",
                       "Form a procession led by five ceremonial guards.",
                       "Carry the Guru Granth Sahib through the streets.",
                       "Perform martial arts displays and music along the route."]},
        ],
        "Tamil Nadu": [
            {"name": "Kolam Drawing", "subcategory": "Daily Ritual", "region": "South India", "language": "Tamil",
             "description": "Geometric patterns drawn each morning at the doorstep using rice flour.",
             "why": "Traditionally believed to welcome prosperity into the home and, practically, feed small insects and birds.",
             "steps": ["Sweep and dampen the entryway floor.",
                       "Mark a grid of dots evenly spaced on the ground.",
                       "Connect the dots with continuous looping lines using rice flour.",
                       "Fill in and refresh the pattern each morning."]},
        ],
        "Gujarat": [
            {"name": "Garba Ritual Dance", "subcategory": "Festival Ritual", "region": "Western India", "language": "Gujarati",
             "description": "A circular dance performed around a central lamp or image of the goddess during Navratri.",
             "why": "The circular motion is traditionally said to represent the cycle of life honoring the divine feminine.",
             "steps": ["Place a decorated lamp or image of the goddess at the center of the space.",
                       "Dancers form concentric circles around the center.",
                       "They move in rhythm, clapping or striking small sticks (dandiya).",
                       "The circles rotate together as the music builds in tempo."]},
        ],
        "Karnataka": [
            {"name": "Yakshagana Ritual Theatre", "subcategory": "Ritual Performance", "region": "South India", "language": "Kannada",
             "description": "A traditional night-long theatre form combining dance, music, elaborate costume and dialogue, often performed near temples.",
             "why": "Traditionally performed as an offering tied to temple festival calendars in coastal Karnataka.",
             "steps": ["Performers apply elaborate face paint and don large headdresses.",
                       "A vocalist and drummer set the narrative pace from the side of the stage.",
                       "Actors enact mythological episodes through stylized dance and dialogue.",
                       "The performance often continues through the night until dawn."]},
        ],
    },
    FESTIVALS_CAT: {
        "Kerala": [
            {"name": "Onam Sadhya", "subcategory": "Festival Feast", "region": "South India", "language": "Malayalam",
             "description": "A multi-course vegetarian feast served on a banana leaf during the ten-day Onam festival.",
             "why": "Traditionally shared communally to mark the homecoming of King Mahabali.",
             "steps": ["Lay a fresh banana leaf lengthwise in front of each guest.",
                       "Serve rice at the center with dishes arranged around it in a set order.",
                       "Add payasam (a sweet dessert) last, closest to the diner.",
                       "Eat by hand, mixing rice with each curry in turn."]},
        ],
        "Assam": [
            {"name": "Bihu Dance Celebration", "subcategory": "Harvest Festival", "region": "Northeast India", "language": "Assamese",
             "description": "A community dance and music celebration marking the Assamese New Year and harvest season.",
             "why": "Bihu is celebrated by communities across Assam regardless of religion, centered on renewal and the farming calendar.",
             "steps": ["Villagers gather in an open field or courtyard.",
                       "Drummers set a rhythm on the dhol and pepa (buffalo-horn pipe).",
                       "Dancers perform in coordinated lines with quick footwork.",
                       "The celebration continues with feasting and gift-giving."]},
        ],
        "Punjab": [
            {"name": "Lohri Bonfire", "subcategory": "Winter Festival", "region": "North India", "language": "Punjabi",
             "description": "A bonfire gathering marking the end of winter, with offerings of sesame seeds, jaggery and popcorn thrown into the flames.",
             "why": "Traditionally tied to the harvest of the rabi crop and celebrated with singing around the fire.",
             "steps": ["Gather firewood and build a bonfire in an open space at dusk.",
                       "Family and neighbors gather around the fire together.",
                       "Offerings of til, gajak and popcorn are thrown into the flames.",
                       "The evening continues with folk songs and dancing around the fire."]},
        ],
        "Gujarat": [
            {"name": "Navratri Festival Nights", "subcategory": "Religious Festival", "region": "Western India", "language": "Gujarati",
             "description": "Nine nights of community dance, fasting and worship honoring the goddess Durga in her nine forms.",
             "why": "One of Gujarat's most widely celebrated festivals, drawing entire neighborhoods into shared nightly dance gatherings.",
             "steps": ["Set up a shrine or lamp honoring the goddess at the venue.",
                       "Community members gather each evening for garba and dandiya raas.",
                       "Many observe a partial fast during the day through the nine nights.",
                       "The festival closes with a final day of special worship."]},
        ],
    },
    PRACTICES: {
        "Kerala": [
            {"name": "Ayurvedic Oil Massage Tradition", "subcategory": "Wellness Custom", "region": "South India", "language": "Malayalam",
             "description": "A traditional practice of full-body herbal oil massage passed down within families and local wellness communities.",
             "why": "Widely practiced as part of everyday self-care routines in Kerala; described here as a cultural custom, not medical advice.",
             "steps": ["Warm a herbal oil blend gently before use.",
                       "Apply the oil using long, rhythmic strokes along the body.",
                       "Allow the oil to sit for a period of rest.",
                       "Follow with a warm bath to complete the routine."]},
        ],
        "Punjab": [
            {"name": "Pinni Making Tradition", "subcategory": "Seasonal Custom", "region": "North India", "language": "Punjabi",
             "description": "A winter tradition of preparing dense, nutrient-rich sweet balls from whole wheat flour, nuts and jaggery.",
             "why": "Traditionally prepared by families ahead of winter and shared with neighbors as part of seasonal hospitality.",
             "steps": ["Roast whole wheat flour slowly in ghee until deep golden and fragrant.",
                       "Mix in crushed nuts and edible gum as it cools slightly.",
                       "Bind the mixture with melted jaggery syrup.",
                       "Shape into small balls while still warm and let them set."]},
        ],
        "Tamil Nadu": [
            {"name": "Thanjavur Doll Making", "subcategory": "Craft Practice", "region": "South India", "language": "Tamil",
             "description": "A traditional craft of making bobble-head clay dolls known for their distinctive gentle rocking motion.",
             "why": "Practiced by artisan families in Thanjavur for generations, often given as wedding and housewarming gifts.",
             "steps": ["Shape the doll's body and head separately from a clay-and-plaster mixture.",
                       "Balance the head on a rounded weight so it rocks freely.",
                       "Let each piece dry fully before assembly.",
                       "Paint the doll in bright colors and finish with fine detailing."]},
        ],
        "Rajasthan": [
            {"name": "Block Printing (Bagru Style)", "subcategory": "Textile Craft", "region": "North India", "language": "Rajasthani",
             "description": "A hand-carved wooden block printing technique used to stamp repeating patterns onto cotton fabric.",
             "why": "Practiced by artisan families in Bagru for generations, using natural dyes drawn from local materials.",
             "steps": ["Carve a pattern into a wooden block by hand.",
                       "Dip the block into natural dye and press it firmly onto stretched fabric.",
                       "Repeat the stamping in a careful, even grid across the cloth.",
                       "Wash and dry the fabric to set the pattern."]},
        ],
        "Maharashtra": [
            {"name": "Warli Painting", "subcategory": "Wall Art", "region": "Western India", "language": "Marathi",
             "description": "A traditional tribal art form using simple white geometric shapes on a mud-red background to depict daily and ceremonial life.",
             "why": "Historically painted on the walls of homes by the Warli community to mark harvests and weddings.",
             "steps": ["Prepare a base of red or brown mud paste on the wall or canvas.",
                       "Mix rice paste with water to make a simple white paint.",
                       "Sketch basic circles, triangles and squares to build human and animal figures.",
                       "Fill out the scene with everyday activities like farming or dancing."]},
        ],
    },
    LANGUAGE: {
        "Maharashtra": [
            {"name": "Marathi Proverb — Ati Tethe Mati", "subcategory": "Proverb", "region": "Western India", "language": "Marathi",
             "description": "A widely used Marathi proverb about the consequences of excess.",
             "why": "Commonly said to caution against overindulgence in food, spending, or ambition.",
             "steps": ["The proverb is spoken as a short, memorable phrase.",
                       "It's typically used to advise moderation in a specific situation.",
                       "Elders often repeat it to younger family members as informal guidance."]},
        ],
        "Tamil Nadu": [
            {"name": "Tamil Oral Storytelling (Villu Paatu)", "subcategory": "Storytelling", "region": "South India", "language": "Tamil",
             "description": "A traditional storytelling form combining narration and song, performed using a bow-shaped instrument as percussion.",
             "why": "Historically used to pass down epics and folk tales in villages before written texts were widely available.",
             "steps": ["The lead performer sets up the bow instrument as a percussive base.",
                       "They narrate a story in verse, alternating with sung passages.",
                       "A supporting group provides rhythm and occasional chorus responses.",
                       "The story unfolds over an extended performance, often through the night."]},
        ],
        "West Bengal": [
            {"name": "Thakurmar Jhuli Folk Tales", "subcategory": "Folk Tales", "region": "Eastern India", "language": "Bengali",
             "description": "A well-known collection of Bengali folk tales traditionally told by grandmothers to children at bedtime.",
             "why": "First compiled in the early 20th century, but the stories themselves were passed down orally long before that.",
             "steps": ["A grandmother or elder gathers children before bedtime.",
                       "She narrates a tale featuring princes, demons, or clever animals.",
                       "The story usually closes with a simple moral lesson.",
                       "Children often ask for the same favorite tales to be repeated."]},
        ],
        "Punjab": [
            {"name": "Punjabi Proverb — Jehi Karni Tehi Bharni", "subcategory": "Proverb", "region": "North India", "language": "Punjabi",
             "description": "A widely used Punjabi proverb about actions and their consequences.",
             "why": "Commonly said to remind listeners that one's own actions determine what comes back to them.",
             "steps": ["The proverb is spoken as a short, memorable phrase.",
                       "It's typically used after someone faces a consequence of their own choices.",
                       "Elders often use it as gentle, informal moral guidance."]},
        ],
    },
    GAMES: {
        "Maharashtra": [
            {"name": "Lagori (Seven Stones)", "subcategory": "Street Game", "region": "Western India", "language": "Marathi",
             "description": "Two teams race to stack seven flat stones into a tower while dodging a thrown ball.",
             "why": "Played on any open street with only stones and a ball — no equipment needed.",
             "steps": ["Stack seven flat stones into a small tower.",
                       "One team throws a ball to knock the stones down.",
                       "That team races to rebuild the tower before the other team tags them with the ball.",
                       "The defending team wins by tagging all raiders before the tower is rebuilt."]},
        ],
        "Tamil Nadu": [
            {"name": "Pallanguzhi", "subcategory": "Board Game", "region": "South India", "language": "Tamil",
             "description": "A mancala-style game played by moving cowrie shells or tamarind seeds between carved pits in a wooden board.",
             "why": "Traditionally taught by grandmothers to granddaughters during afternoon rest hours.",
             "steps": ["Fill each pit of the wooden board with an equal number of shells.",
                       "On your turn, pick up all the shells from one pit.",
                       "Drop one shell into each pit as you move around the board.",
                       "Collect shells by the game's capture rules until all pits are empty."]},
        ],
        "Punjab": [
            {"name": "Kabaddi", "subcategory": "Team Sport", "region": "North India", "language": "Punjabi",
             "description": "A contact team sport where a raider crosses into the opposing half, tags players, and returns while chanting 'kabaddi' in one breath.",
             "why": "Said to have grown out of village wrestling akharas and remains one of Punjab's most-watched folk sports.",
             "steps": ["Split into two teams on opposite halves of the court.",
                       "A raider crosses into the opponents' half, chanting 'kabaddi' without pausing for breath.",
                       "The raider tries to tag as many defenders as possible.",
                       "The raider must return to their own half before running out of breath to score."]},
        ],
        "Gujarat": [
            {"name": "Bandhani Craft Games (Gilli Danda)", "subcategory": "Street Game", "region": "Western India", "language": "Gujarati",
             "description": "A traditional street game played with a small wooden stick (gilli) that's struck into the air with a longer stick (danda).",
             "why": "A common neighborhood pastime for generations, needing only two carved sticks.",
             "steps": ["Balance the small gilli stick over a shallow pit.",
                       "Strike one end of the gilli with the danda to flip it into the air.",
                       "Hit the airborne gilli as far as possible.",
                       "Opposing players try to catch it or return it toward the pit."]},
        ],
        "Karnataka": [
            {"name": "Chennemane (Ali Guli Mane)", "subcategory": "Board Game", "region": "South India", "language": "Kannada",
             "description": "A mancala-style counting and strategy game played on a wooden board with carved pits and seeds or shells.",
             "why": "Traditionally played by women and children during leisure hours, valued for the mental arithmetic it builds.",
             "steps": ["Distribute an equal number of seeds into each pit.",
                       "Pick up all seeds from one pit on your turn.",
                       "Sow them one by one into successive pits around the board.",
                       "Capture seeds according to the game's rules when a pit reaches a set count."]},
        ],
        "Kerala": [
            {"name": "Uriyadi", "subcategory": "Festival Game", "region": "South India", "language": "Malayalam",
             "description": "A game where a blindfolded player tries to strike and break a pot of curd or water suspended overhead using a stick.",
             "why": "Traditionally played during festivals like Onam and Krishna Jayanthi as a lighthearted community contest.",
             "steps": ["Suspend a clay pot filled with curd or water from a rope overhead.",
                       "Blindfold the player and spin them gently to disorient direction.",
                       "Guide them verbally as they swing a stick to try to strike the pot.",
                       "The crowd cheers and calls out directions until the pot breaks."]},
        ],
    },
}

FESTIVALS = [
    {"name": "Onam", "month": "AUG", "day": "22", "description": "Kerala's flower-carpet harvest festival."},
    {"name": "Ganesh Chaturthi", "month": "SEP", "day": "05", "description": "Ten-day festival honoring Lord Ganesha."},
    {"name": "Pongal", "month": "JAN", "day": "14", "description": "Harvest festival dedicated to the Sun."},
    {"name": "Baisakhi", "month": "APR", "day": "13", "description": "Punjab's spring harvest festival, also marking the founding of the Khalsa."},
    {"name": "Durga Puja", "month": "OCT", "day": "02", "description": "West Bengal's major festival honoring the goddess Durga."},
    {"name": "Bihu", "month": "APR", "day": "14", "description": "Assam's harvest and New Year festival."},
]

PROVERBS = [
    {"text_original": "अति तेथे माती", "language": "Marathi", "transliteration": "Ati tethe māti", "meaning": "Excess of anything turns to dust."},
    {"text_original": "ஆடிப் பாடி வேலை செய்", "language": "Tamil", "transliteration": "Aadip paadi velai sei", "meaning": "Work while singing and dancing — do your work joyfully."},
]


def seed_if_empty(db):
    """Populate an empty database with the starter dataset above. Safe to call on every startup."""
    from models import CulturalEntry, Festival, Proverb

    if db.query(CulturalEntry).first() is None:
        for domain, states in ENTRIES.items():
            for state, items in states.items():
                for item in items:
                    db.add(CulturalEntry(
                        domain=domain,
                        subcategory=item.get("subcategory"),
                        state=state,
                        region=item.get("region"),
                        language=item.get("language"),
                        name=item["name"],
                        gender=item.get("gender"),
                        description=item["description"],
                        why_it_matters=item["why"],
                        steps=item["steps"],
                        image_url=item.get("image_url"),
                        source_url=item.get("source_url"),
                    ))

    if db.query(Festival).first() is None:
        for f in FESTIVALS:
            db.add(Festival(**f))

    if db.query(Proverb).first() is None:
        for p in PROVERBS:
            db.add(Proverb(**p))

    db.commit()
