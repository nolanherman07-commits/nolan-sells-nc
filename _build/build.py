# Builds every page of the Elite site. Run: python3 _build/build.py
import os, html, json
os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
E = html.escape

PHONE, TEL, EMAIL = "828-404-5335", "+18284045335", "nolan@nestlewoodrealty.com"
ADDRESS = "825 Highland Ave SE, Hickory, NC 28602"
MAP = "https://www.google.com/maps/search/?api=1&query=" + ADDRESS.replace(" ", "+")
ZILLOW = "https://www.zillow.com/profile/Nolansellnc"
HOMES = "https://www.homes.com/real-estate-agents/nolan-herman/2672vt8/"
INSTAGRAM = "https://www.instagram.com/nolansellsnc/"
FACEBOOK = "https://www.facebook.com/profile.php?id=61578346302536"
CALENDLY = ""  # optional: paste a Calendly link here (the Book a call button calls you until then)
EXT = 'target="_blank" rel="noopener"'
# Full web address of the site. Change this if you move to a custom domain (e.g. "https://nolansellsnc.com/").
BASE = "https://nolanherman07-commits.github.io/nolan-sells-nc/"
SHARE_IMAGE = "images/share.jpg"  # picture shown when a page link is texted or posted

FEATURED = [
  ("5182 Corbin Ln", "Hickory, NC", "https://www.zillow.com/homedetails/5182-Corbin-Ln-Hickory-NC-28601/92556701_zpid/", "images/listings/5182-corbin-ln.jpg", "$205,000"),
]
SOLD = [
  ("421 18th Ave", "Hickory, NC", ZILLOW, "images/listings/421-18th-ave.jpg"),
  ("7107 Rolling Hills Dr", "Sherrills Ford, NC", "https://www.zillow.com/homedetails/7107-Rolling-Hills-Dr-Sherrills-Ford-NC-28673/71910314_zpid/", "images/listings/7107-rolling-hills-dr.jpg"),
  ("350 14th Ave SW", "Hickory, NC", "https://www.zillow.com/homedetails/350-14th-Ave-SW-Hickory-NC-28602/464120420_zpid/", "images/listings/350-14th-ave-sw.jpg"),
]
AREAS = {
  "hickory": dict(name="Hickory", scene="golden", county="Catawba County", photo="images/hickory-downtown.jpg",
    short="Lively downtown, Lake Hickory, and an easy drive to Charlotte and the mountains.",
    intro="Hickory is the largest city in the Catawba Valley, with a lively downtown, Lake Hickory on the Catawba River, and Lenoir-Rhyne University. You get city amenities, lake life, and an easy drive to Charlotte and the mountains.",
    facts=[("Catawba", "County"), ("~1 hr", "To Charlotte"), ("Lake Hickory", "On the water"), ("~1 hr", "To the Blue Ridge")],
    love=["Downtown restaurants, shops and events", "Lake Hickory for boating and waterfront homes", "Parks, greenways and youth sports", "Quick access to I-40 and US-321"]),
  "conover": dict(name="Conover", scene="dusk", county="Catawba County", photo="images/conover.jpg",
    short="A friendly, growing city right next to Hickory, with a lively downtown and community events.",
    intro="Conover sits right between Hickory and Newton in Catawba County. It has a revitalized downtown with outdoor events and concerts, quiet neighborhoods, and quick access to I-40, so you're minutes from everything the Hickory area offers.",
    facts=[("Catawba", "County"), ("~10 min", "To Hickory"), ("I-40", "Right off the highway"), ("~55 min", "To Charlotte")],
    love=["Downtown events and summer concerts", "Quiet neighborhoods with room to grow", "Minutes from Hickory shopping and jobs", "Easy access to I-40"]),
  "huntersville": dict(name="Huntersville", scene="dawn", county="Mecklenburg County", photo="images/huntersville-sign.jpg",
    short="Lake Norman living just north of Charlotte, established 1873.",
    intro="Huntersville is a fast-growing town in northern Mecklenburg County, just north of Charlotte and close to Lake Norman. It's a great fit if you want suburban neighborhoods, lake access, and an easy commute into the city.",
    facts=[("Mecklenburg", "County"), ("~20 min", "To Charlotte"), ("Lake Norman", "Nearby"), ("I-77", "Commuter corridor")],
    love=["Close to Lake Norman", "Newer neighborhoods and parks", "Easy commute to uptown Charlotte", "Shopping and dining along I-77"]),
  "granite-falls": dict(name="Granite Falls", scene="mist", county="Caldwell County", photo="images/granite-falls.jpg",
    short="Quiet living near Lake Rhodhiss, with room to grow and quick trips into town.",
    intro="Granite Falls is a friendly small town in Caldwell County along US-321, between Hickory and Lenoir. It's close to Lake Rhodhiss and Lake Hickory, and a great fit if you want more space and a slower pace without being far from town.",
    facts=[("Caldwell", "County"), ("~15 min", "To Hickory"), ("Lakes", "Rhodhiss & Hickory"), ("US-321", "Hickory to Lenoir")],
    love=["Small-town community feel", "Close to lakes and the outdoors", "Larger lots and room to grow", "Quick drive to Hickory and Lenoir"]),
  "charlotte": dict(name="Charlotte", scene="sunset", county="Mecklenburg County", photo="images/charlotte-skyline.jpg", video="clt-skyline-day",
    short="North Carolina's largest city: uptown skyline, pro sports, and neighborhoods for every lifestyle.",
    intro="Charlotte is the largest city in North Carolina, with a busy uptown, pro football and basketball, great restaurants, and a huge range of neighborhoods. Whether you're relocating for work or want city energy with easy access to Lake Norman and the foothills, I'll help you find the right fit.",
    facts=[("Mecklenburg", "County"), ("~1 hr", "To Hickory"), ("Largest", "City in NC"), ("$425K", "Metro median price*")],
    love=["Uptown dining, sports and nightlife", "Job opportunities across the region", "Neighborhoods from urban to suburban", "Close to Lake Norman and the foothills"]),
  # ---- Hickory-to-Charlotte corridor towns (photos from Wikimedia Commons; credit shows on each town page) ----
  "newton": dict(name="Newton", scene="golden", county="Catawba County", photo="images/towns/newton.jpg", credit=('Indy beetle', 'https://commons.wikimedia.org/wiki/File:Newton,_North_Carolina_01.jpg', 'CC0', 'https://creativecommons.org/publicdomain/zero/1.0/'),
    short="The Catawba County seat, with a historic courthouse square and small-town charm.",
    intro="Newton is the county seat of Catawba County, just south of Conover and minutes from Hickory. Its historic 1924 courthouse anchors a walkable downtown, and the town is known for Soldiers' Reunion, one of the longest-running community celebrations in the country.",
    facts=[("Catawba", "County"), ("~10 min", "To Hickory"), ("~55 min", "To Charlotte"), ("NC-16", "Straight to Charlotte")],
    love=["Historic downtown and courthouse square", "Soldiers' Reunion every August", "Established neighborhoods and good value", "Easy access to US-321, I-40 and NC-16"]),
  "claremont": dict(name="Claremont", scene="mist", county="Catawba County", photo="images/towns/claremont.jpg", credit=('William Keener', 'https://commons.wikimedia.org/wiki/File:Bunker_Hill_Covered_Bridge_in_Claremont,_N.C._(3).jpg', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    short="A small city on I-40 with a quiet, country feel, just east of Conover.",
    intro="Claremont is a small city along I-40 on the eastern side of Catawba County. You get quiet streets, room to spread out, and a quick hop to Hickory, Conover and Statesville without paying big-city prices.",
    facts=[("Catawba", "County"), ("~15 min", "To Hickory"), ("I-40", "Right off the highway"), ("~25 min", "To Statesville")],
    love=["Quiet, small-town pace", "More land for the money", "Quick I-40 access east and west", "Close to Conover and Newton shopping"]),
  "maiden": dict(name="Maiden", scene="dawn", county="Catawba County", photo="images/towns/maiden.jpg", credit=('Skepticalpoet', 'https://commons.wikimedia.org/wiki/File:Memorial_Reformed_Church.jpg', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    short="A friendly town on US-321 between Newton and Lincolnton.",
    intro="Maiden is a small town in southern Catawba County on US-321. It has a close-knit community, parks and ballfields, and a central spot that puts you about 20 minutes from Hickory and within reach of Lake Norman and Charlotte.",
    facts=[("Catawba", "County"), ("~20 min", "To Hickory"), ("US-321", "North-south access"), ("~50 min", "To Charlotte")],
    love=["Close-knit small-town feel", "Parks, ballfields and community events", "Central to Hickory, Lincolnton and Lake Norman", "Good value on homes and land"]),
  "lincolnton": dict(name="Lincolnton", scene="sunset", county="Lincoln County", photo="images/towns/lincolnton.jpg", credit=('Washuotaku', 'https://commons.wikimedia.org/wiki/File:Lincoln_County_Courthouse_(Lincolnton,_North_Carolina).jpg', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/'),
    short="The Lincoln County seat, with a classic Main Street and the South Fork River.",
    intro="Lincolnton is the county seat of Lincoln County, along US-321 between Hickory and Gastonia. It has a revitalized downtown, the South Fork River running through town, and a mix of historic homes, new neighborhoods and country land.",
    facts=[("Lincoln", "County"), ("~35 min", "To Hickory"), ("~45 min", "To Charlotte"), ("US-321", "North-south access")],
    love=["Revitalized downtown and local restaurants", "South Fork River and outdoor space", "Mix of historic homes and new construction", "Easy drive to Lake Norman and Gastonia"]),
  "denver": dict(name="Denver", scene="dusk", county="Lincoln County", photo="images/towns/denver.jpg", credit=('James St. John', 'https://commons.wikimedia.org/wiki/File:Lake_Norman_(North_Carolina,_USA)_2.jpg', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/'),
    short="Lake Norman's western shore, with newer neighborhoods and a quick NC-16 commute.",
    intro="Denver sits on the western shore of Lake Norman in eastern Lincoln County. It's one of the fastest-growing spots in the region, with waterfront and water-access homes, newer neighborhoods, and NC-16 running straight into Charlotte.",
    facts=[("Lincoln", "County"), ("~35 min", "To Charlotte"), ("Lake Norman", "West shore"), ("NC-16", "Straight to Charlotte")],
    love=["Lake Norman boating and waterfront homes", "Newer neighborhoods and amenities", "Direct NC-16 commute into Charlotte", "Quieter side of the lake"]),
  "lake-norman": dict(name="Lake Norman", scene="dawn", county="Mecklenburg, Iredell, Catawba & Lincoln", photo="images/lake-norman.jpg",
    short="North Carolina's largest lake, with waterfront homes, marinas and an easy commute to Charlotte.",
    intro="Lake Norman is the largest man-made lake in North Carolina, with over 500 miles of shoreline across four counties. Towns like Mooresville, Cornelius, Davidson, Huntersville, Denver and Sherrills Ford surround it, so you can find everything from waterfront estates to lake-access neighborhoods, all within reach of Charlotte and Hickory.",
    facts=[("4", "Counties"), ("500+ mi", "Of shoreline"), ("~35 min", "To Charlotte"), ("~35 min", "To Hickory")],
    love=["Boating, swimming and waterfront dining", "Waterfront and lake-access homes", "Towns all around the lake to choose from", "Easy I-77 commute to Charlotte"]),
  "sherrills-ford": dict(name="Sherrills Ford", scene="dawn", county="Catawba County", photo="images/towns/sherrills-ford.jpg", credit=('James St. John', 'https://commons.wikimedia.org/wiki/File:Lake_Norman_(North_Carolina,_USA)_1.jpg', 'CC BY 2.0', 'https://creativecommons.org/licenses/by/2.0/'),
    short="Lake Norman living on the Catawba County side of the lake.",
    intro="Sherrills Ford is a lakeside community in southeastern Catawba County on Lake Norman's northwest shore. It's popular with buyers who want lake life, golf and bigger lots, with Hickory, Mooresville and Charlotte all within reach.",
    facts=[("Catawba", "County"), ("Lake Norman", "Northwest shore"), ("~30 min", "To Hickory"), ("~45 min", "To Charlotte")],
    love=["Waterfront and lake-access homes", "Golf and lake communities", "Bigger lots and a quieter pace", "Between Hickory, Mooresville and Charlotte"]),
  "mooresville": dict(name="Mooresville", scene="sunset", county="Iredell County", photo="images/towns/mooresville.jpg", credit=('Cdtew at English Wikipedia', 'https://commons.wikimedia.org/wiki/File:Mooresville_Historic_District_(Main_Street).jpg', 'CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0/'),
    short="Race City USA on Lake Norman, with shopping, jobs and an I-77 commute.",
    intro="Mooresville is the largest town on Lake Norman, in southern Iredell County along I-77. Known as Race City USA for its NASCAR teams, it offers a busy retail corridor, a historic downtown, and everything from lake homes to new-build neighborhoods.",
    facts=[("Iredell", "County"), ("~30 min", "To Charlotte"), ("Lake Norman", "East shore"), ("I-77", "Commuter corridor")],
    love=["Lake Norman boating and waterfront living", "Historic downtown and big shopping options", "Racing heritage and local employers", "Quick I-77 drive into Charlotte"]),
  "statesville": dict(name="Statesville", scene="golden", county="Iredell County", photo="images/towns/statesville.jpg", credit=('Witchywoman331', 'https://commons.wikimedia.org/wiki/File:The_Historic_Morrison-Mott_House_in_downtown_Statesville,_NC.jpg', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    short="Where I-40 meets I-77, with a historic downtown and room to grow.",
    intro="Statesville is the county seat of Iredell County, right where I-40 and I-77 cross. That location makes it an easy commute to Hickory, Mooresville and Charlotte, and it pairs a historic downtown with more affordable homes and land.",
    facts=[("Iredell", "County"), ("~35 min", "To Hickory"), ("~45 min", "To Charlotte"), ("I-40 + I-77", "Crossroads")],
    love=["Historic downtown", "More home and land for the money", "I-40 and I-77 in every direction", "Close to Lake Norman"]),
  "cornelius": dict(name="Cornelius", scene="dusk", county="Mecklenburg County", photo="images/towns/cornelius.jpg", credit=('Dough4872', 'https://commons.wikimedia.org/wiki/File:Lake_Norman_beach_in_Ramsey_Creek_Park.jpeg', 'CC BY-SA 4.0', 'https://creativecommons.org/licenses/by-sa/4.0/'),
    short="The heart of Lake Norman, with marinas, waterfront dining and an I-77 commute.",
    intro="Cornelius sits on the southeast shore of Lake Norman in northern Mecklenburg County. It's known for marinas, lakefront restaurants and waterfront neighborhoods, with I-77 putting uptown Charlotte about 25 minutes away.",
    facts=[("Mecklenburg", "County"), ("~25 min", "To Charlotte"), ("Lake Norman", "Southeast shore"), ("I-77", "Commuter corridor")],
    love=["Marinas and waterfront dining", "Lakefront and lake-access neighborhoods", "Quick commute to uptown Charlotte", "Parks and greenways"]),
  "davidson": dict(name="Davidson", scene="mist", county="Mecklenburg County", photo="images/towns/davidson.jpg", credit=('Dacoslett at English Wikipedia', 'https://commons.wikimedia.org/wiki/File:Chambers_Building,_Davidson_College_(Davidson,_North_Carolina).jpg', 'Public domain', 'https://creativecommons.org/publicdomain/mark/1.0/'),
    short="A walkable college town on Lake Norman, home to Davidson College.",
    intro="Davidson is a small, walkable town in northern Mecklenburg County, home to Davidson College. Its classic Main Street, greenways and lake access make it one of the most sought-after towns in the Charlotte area.",
    facts=[("Mecklenburg", "County"), ("~25 min", "To Charlotte"), ("Davidson", "College town"), ("Lake Norman", "Nearby")],
    love=["Walkable Main Street and village green", "Davidson College events and sports", "Greenways and lake access", "Easy I-77 commute"]),
}
# Order of towns from Hickory toward Charlotte (used for "Nearby areas" and the relocation page)
CORRIDOR = ["granite-falls", "hickory", "conover", "newton", "claremont", "maiden", "statesville", "lincolnton",
            "lake-norman", "sherrills-ford", "denver", "mooresville", "davidson", "cornelius", "huntersville", "charlotte"]
HOME_AREAS = ["hickory", "conover", "granite-falls", "lake-norman", "charlotte"]
# Drive times from each town (approximate, normal traffic)
DRIVE = {"lake-norman": ("~35 min", "~35 min"), "granite-falls": ("~15 min", "~1 hr 10 min"), "hickory": ("—", "~1 hr"), "conover": ("~10 min", "~55 min"),
         "newton": ("~10 min", "~55 min"), "claremont": ("~15 min", "~55 min"), "maiden": ("~20 min", "~50 min"),
         "statesville": ("~35 min", "~45 min"), "lincolnton": ("~35 min", "~45 min"), "sherrills-ford": ("~30 min", "~45 min"),
         "denver": ("~40 min", "~35 min"), "mooresville": ("~45 min", "~30 min"), "davidson": ("~50 min", "~25 min"),
         "cornelius": ("~50 min", "~25 min"), "huntersville": ("~55 min", "~20 min"), "charlotte": ("~1 hr", "—")}

# Monthly market update: edit these each month (source + period shown on the page)
MARKET_MONTH = "November 2026"
MARKET = [
  dict(area="Charlotte metro", period="August 2026", source="Homes.com market report", url="https://www.homes.com/reports/charlotte-housing-market/",
       stats=[("$425,000", "Median sale price"), ("+1.6%", "vs. last year"), ("69 days", "Median days on market"), ("4.3 mo", "Supply of homes")]),
  dict(area="Hickory metro", period="Jan to Jun 2026 average", source="Redfin, via WSOC-TV", url="https://www.wsoctv.com/news/hickory-mid-year/M3ZTBUKSAYYEVM7FEOGSNGBS2E/",
       stats=[("$311,924", "Median sale price"), ("+5.0%", "vs. last year"), ("74 days", "Median days on market"), ("4.6 mo", "Supply of homes")]),
]
MARKET_TAKE = [
  ("For buyers", "Homes are taking longer to sell than they did a couple of years ago, and there's more than four months of supply in both markets. That means more choices and more room to negotiate on price, repairs and closing costs."),
  ("For sellers", "Prices are still edging up, but buyers are patient. Homes that are priced right from day one and look great online are the ones that sell fastest. Overpricing now usually means sitting on the market and cutting later."),
  ("Hickory vs. Charlotte", "The typical Hickory-area home costs over $100,000 less than in the Charlotte metro. That gap is why so many buyers are looking up the I-40 and US-321 corridor."),
]

NAV = [("about.html", "About"), ("buy.html", "Buying?"), ("sell.html", "Selling?"), ("relocate.html", "Relocating?"), ("listings.html", "Listings")]
TABS = [("about.html", "About"), ("buy.html", "Buying?"), ("sell.html", "Selling?"), ("relocate.html", "Relocating?"), ("listings.html", "Listings")]  # phone tab bar, same labels as the desktop menu (the logo is the Home link)

def header(active):
    links = "".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    mob = [("index.html", "Home")] + NAV + [("contact.html", "Contact")]
    mlinks = "".join(f'<a href="{h}"{" class=\"active\"" if (h == active or (h == "index.html" and not active)) else ""}><span>{t}</span><i>→</i></a>' for h, t in mob)
    areas = "".join(f'<a href="{k}.html">{a["name"]}</a>' for k, a in AREAS.items())
    return f'''<header class="nav-wrap">
  <nav class="nav-pill"><a href="index.html" class="nav-logo"><img src="images/logo.png" alt="Nestlewood Realty" /></a>{links}</nav>
  <a href="contact.html" class="nav-cta">Let's talk</a>
  <nav class="tabbar" aria-label="Pages">{"".join(f'<a href="{h}"{" class=\"active\"" if h == active else ""}>{t}</a>' for h, t in TABS)}</nav>
</header>'''

FOOTER = f'''<footer class="foot">
  <div class="wrap foot-grid">
    <a href="index.html"><img src="images/logo.png" alt="Nestlewood Realty" /></a>
    <p>Nolan Herman, REALTOR® · Nestlewood Realty<br />{ADDRESS}</p>
    <div class="soc"><a href="about.html">About</a><a href="buy.html">Buy</a><a href="sell.html">Sell</a><a href="relocate.html">Relocate</a><a href="market.html">Market update</a><a href="listings.html">Listings</a><a href="contact.html">Contact</a></div>
    <div class="soc"><a href="{INSTAGRAM}" {EXT}>Instagram</a><a href="{FACEBOOK}" {EXT}>Facebook</a><a href="{ZILLOW}" {EXT}>Zillow</a><a href="{HOMES}" {EXT}>Homes.com</a></div>
  </div>
  <div class="wrap foot-areas"><span>Areas I serve</span>{"".join(f'<a href="{k}.html">{AREAS[k]["name"]}</a>' for k in CORRIDOR)}</div>
  <div class="wrap fine eho-line"><svg class="eho" viewBox="0 0 40 40" role="img" aria-label="Equal Housing Opportunity"><path d="M20 3 2 15v4h4v18h28V19h4v-4z" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linejoin="round"/><rect x="12" y="20" width="16" height="3.4" fill="currentColor"/><rect x="12" y="27" width="16" height="3.4" fill="currentColor"/></svg>
    <span>© <span class="yr">2026</span> Nestlewood Realty · Equal Housing Opportunity · REALTOR® · Lake Norman photo: <a href="https://commons.wikimedia.org/wiki/File:Governors-Island-Lake-Norman.jpg" target="_blank" rel="noopener">Christopher Sheridan</a>, <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a></span></div>
</footer>'''

SCHEMA = json.dumps({
  "@context": "https://schema.org", "@type": "RealEstateAgent",
  "name": "Nolan Herman, REALTOR®", "url": BASE, "image": BASE + "images/headshot.jpg", "logo": BASE + "images/logo.png",
  "telephone": TEL, "email": EMAIL,
  "worksFor": {"@type": "RealEstateOrganization", "name": "Nestlewood Realty"},
  "address": {"@type": "PostalAddress", "streetAddress": "825 Highland Ave SE", "addressLocality": "Hickory", "addressRegion": "NC", "postalCode": "28602", "addressCountry": "US"},
  "areaServed": [{"@type": "City", "name": AREAS[k]["name"] + ", NC"} for k in CORRIDOR],
  "sameAs": [ZILLOW, HOMES, INSTAGRAM, FACEBOOK],
}, ensure_ascii=False)

DEFAULT_DESC = "Nolan Herman, REALTOR® with Nestlewood Realty. Helping buyers and sellers from Hickory to Charlotte, including Conover, Newton, Lake Norman and Huntersville."

def page(fname, title, active, body, curtain=False, desc=DEFAULT_DESC):
    url = BASE + ("" if fname == "index.html" else fname)
    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="Nolan Herman, REALTOR®" />
<meta property="og:title" content="{E(title)}" />
<meta property="og:description" content="{E(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}{SHARE_IMAGE}" />
<meta property="og:image:width" content="1200" /><meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">{SCHEMA}</script>
<link rel="icon" href="images/tree-icon.png" /><link rel="apple-touch-icon" href="images/tree-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" /><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="elite.css" />
</head>
<body{"" if curtain else ' class="page-fade"'}>
{'<div class="curtain" aria-hidden="true"><img src="images/logo.png" alt="" /></div>' if curtain else ""}
<div class="cursor-glow" aria-hidden="true"></div>
{header(active)}
{body}
{FOOTER}
<script src="elite.js"></script>
</body>
</html>'''
    open(fname, "w").write(doc)

def bg(scene, photo=None):
    # a real photo (slow zoom) if we have one, otherwise an animated mountain scene
    return f'<div class="photo-bg" style="background-image:url(\'{photo}\')"></div>' if photo else f'<div class="scene" data-scene="{scene}"></div>'

# Still photo shown behind each hero video. Phones that refuse to autoplay (iPhone Low Power Mode,
# data saver) show this photo instead of the video.
STILLS = {"beach": "images/stills/beach.jpg", "lake": "images/stills/lake.jpg"}

def page_hero(crumb, title_html, sub, scene, photo=None, video=None, still=None):
    photo = photo or still or STILLS.get(video)
    fog = "" if photo else '<div class="fog f1"></div><div class="fog f2"></div>'
    return f'''<section class="page-hero"><div class="frame">
  {bg(scene, photo)}{(f'<video class="hero-video" data-src="{video if video.startswith("http") else f"videos/{video}.mp4"}" muted loop playsinline autoplay hidden disablepictureinpicture disableremoteplayback preload="metadata" aria-hidden="true"></video>' if video else '')}{fog}<div class="shade"></div>
  <div class="ph-copy"><span class="crumb"><i></i> {crumb}</span><h1 class="split-words">{title_html}</h1><p>{sub}</p></div>
</div></section>'''

def card(addr, city, url, photo, ask="", sold=False, price=True):
    pic = f'<img src="{photo}" alt="{E(addr)}" />' if photo else '<div class="scene" data-scene="dawn"></div>'
    sub = f"{city} · {ask}" if (price and ask and not sold) else city  # no price yet: show the city only
    return f'''<a class="home-card" href="{url}" {EXT}><div class="img">{pic}</div>
  <div class="info glass"><span class="badge{" sold" if sold else ""}">{"Sold" if sold else "Featured"}</span><h3>{E(addr)}</h3><p>{sub}</p></div></a>'''

def rail(items, title_html, eyebrow, link=None):
    return f'''<section class="listings">
  <div class="wrap head"><div><p class="eyebrow">{eyebrow}</p><h2>{title_html}</h2></div>
    <div class="arrows">{f'<a class="pill" href="{link}" style="margin-right:.6rem">View all</a>' if link else ""}<button class="arr prev" aria-label="Previous">←</button><button class="arr next" aria-label="Next">→</button></div></div>
  <div class="rail" tabindex="0">{"".join(card(*i, sold=i in SOLD) for i in items)}</div>
  <div class="wrap"><div class="progress"><span></span></div></div>
</section>'''

def panels(keys, title_html="From the foothills to <em>Charlotte</em>"):
    out = "".join(f'''<article class="panel{" open" if n == 0 else ""}" data-href="{k}.html">{bg(AREAS[k]["scene"], AREAS[k].get("photo"))}<div class="p-shade"></div>
  <div class="p-copy"><span class="num">0{n+1}</span><h3>{AREAS[k]["name"]}</h3><p>{AREAS[k]["short"]}</p><a class="pill light sm" href="{k}.html">Explore {AREAS[k]["name"]}</a></div></article>''' for n, k in enumerate(keys))
    return f'''<section class="areas"><div class="wrap head"><div><p class="eyebrow">Explore the area</p><h2>{title_html}</h2></div></div>
  <div class="wrap panels">{out}</div></section>'''

REVIEWS = '''<section class="reviews">
  <div class="wrap rv-wrap">
    <p class="eyebrow">Client reviews · ★★★★★</p>
    <div class="quotes">
      <blockquote class="q on"><p>“He looked out for our best interests, getting us a fantastic deal. You feel like you're their <em>only client.</em>”</p><cite>Lorena &amp; Martin · Home Buyers</cite></blockquote>
      <blockquote class="q"><p>“His professionalism, deep market knowledge, and ability to communicate clearly made the entire process <em>far less stressful.</em>”</p><cite>Jacopo B. · Home Buyer</cite></blockquote>
      <blockquote class="q"><p>“We couldn't have asked for a better realtor than Nolan. We absolutely <em>love our new home.</em>”</p><cite>Alfred &amp; Rashonda Wingate · First-Time Buyers</cite></blockquote>
    </div>
    <div class="q-bars"><i class="on"></i><i></i><i></i></div>
    <a class="under" href="''' + ZILLOW + '''" target="_blank" rel="noopener">Read every review on Zillow →</a>
  </div>
</section>'''

VALUE_FORM = '''<form class="line-form stack lead-form" data-subject="Home value request" data-need-contact><input name="address" placeholder="Your home address" autocomplete="street-address" required /><input name="phone" type="tel" placeholder="Phone number" autocomplete="tel" /><input name="email" type="email" placeholder="or email address" autocomplete="email" /><span class="form-note">Phone or email, whichever you prefer.</span><button class="pill solid" type="submit">Get my value</button></form>'''
GUIDE_FORM = '''<a class="pill solid guide-btn" href="Hickory-Area-Home-Buyers-Guide.pdf" target="_blank" rel="noopener">Open the guide (PDF)</a>'''

SELLER_GUIDE_FORM = '''<a class="pill solid guide-btn" href="Hickory-Area-Home-Sellers-Guide.pdf" target="_blank" rel="noopener">Open the guide (PDF)</a>'''

SELL_TOOLS = f'''<section class="tools" id="value">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free download</p><h3>The Hickory Area <em>Seller's Guide</em></h3>
      <p>Pricing, prep, marketing, offers and closing, plus a pre-listing checklist. Written in plain English.</p>{SELLER_GUIDE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">Free home value report</p><h3>What's your home <em>worth?</em></h3>
      <p>A personalized value report from Nolan, not an algorithm. Usually within 24 hours.</p>{VALUE_FORM}</div>
  </div>
</section>'''

QUOTES = [
  ("He even caught a mistake during closing that got us more money.", "John F.", "Bought &amp; sold in Vale"),
  ("I would highly recommend this young man.", "John F.", "Bought &amp; sold in Vale"),
  ("Nolan was our best realtor! He made the buying process enjoyable.", "Diane S.", "Home buyer"),
  ("Very knowledgeable, responsive, patient, personable, always ready to help.", "Diane S.", "Home buyer"),
  ("Nolan significantly eased the process.", "Pricilla &amp; Jeff L.", "Bought in Granite Falls"),
  ("We couldn't have asked for a better realtor than Nolan.", "Alfred &amp; Rashonda W.", "First-time buyers in Newton"),
  ("He was always quick to answer our questions, incredibly patient.", "Alfred &amp; Rashonda W.", "First-time buyers in Newton"),
  ("You feel like you're their only client.", "Lorena &amp; Martin", "Home buyers"),
  ("He looked out for our best interests, getting us a fantastic deal.", "Lorena &amp; Martin", "Home buyers"),
  ("He is exceptional at what he does.", "Jacopo B.", "Home buyer"),
  ("Always proactive, responsive, and genuinely committed to my best interests.", "Jacopo B.", "Home buyer"),
  ("He responds quickly and was on top of all the paperwork.", "Kalen &amp; Micheal M.", "Home buyers"),
  ("Nolan was courteous, respectful and responsive.", "Darlene P.", "Home buyer"),
  ("Truly a pleasure to work with Nolan.", "Darlene P.", "Home buyer"),
  ("He went above and beyond with all of the little things.", "Mindy D.", "Home buyer"),
  ("I could not have had a better agent.", "David J.", "Home buyer"),
  ("Nolan was there every step of the way to boost me over every hurdle.", "David J.", "Home buyer"),
  ("He made a stressful time easy, efficient, and quick.", "Ashley &amp; Bill", "Home buyers"),
  ("Nolan did a great job with a seller who wasn't motivated to negotiate.", "Dwayne W.", "Home buyer"),
]
# One longer review shown under the moving one-liners. Paste the full Zillow review text here when you have it.
FULL_REVIEW = dict(
  text=["Working with Nolan was an outstanding experience from start to finish.",
        "We couldn't have asked for a better realtor than Nolan. He made us feel supported, informed, and confident.",
        "He was always quick to answer our questions, incredibly patient.",
        "We absolutely love our new home."],
  name="Alfred &amp; Rashonda W.", detail="First-time buyers · Newton, NC · 2026")
FULL_REVIEW_HTML = f'''<figure class="full-review reveal"><div class="fr-stars">★★★★★</div>
  <blockquote>{"".join(f"<p>{E(t)}</p>" for t in FULL_REVIEW["text"])}</blockquote>
  <figcaption><b>{FULL_REVIEW["name"]}</b><span>{FULL_REVIEW["detail"]}</span><a href="{ZILLOW}" {EXT}>Read it on Zillow →</a></figcaption></figure>'''

QUOTE_STRIP = '<section class="quote-strip" aria-label="Client reviews"><div class="wrap qs-inner"><div class="qs-stars">★★★★★ <span>5.0 on Zillow</span></div><div class="qs-stage">' + "".join(
    f'<blockquote class="qs"><p>“{q}”</p><cite>{n} · {w}</cite></blockquote>' for q, n, w in QUOTES) + '</div>' + FULL_REVIEW_HTML + '</div></section>'

REVIEWS = QUOTE_STRIP  # every page uses the fast one-line strip

RESUMES = '''<section class="sec resumes"><div class="wrap">
  <div class="head"><div><p class="eyebrow">Résumé</p><h2>See why clients <em>choose Nolan</em></h2></div></div>
  <div class="res-grid">
    <a class="res-card reveal" href="Nolan-Herman-Listing-Resume.pdf" target="_blank" rel="noopener"><img src="images/resume-listing.jpg" alt="Listing résumé cover" />
      <div><p class="eyebrow">For sellers</p><h3>Listing <em>résumé</em></h3><p>Results, my 15-step listing process, marketing plan and no-risk listing program.</p><span class="pill solid">Open résumé (PDF)</span></div></a>
    <a class="res-card reveal" href="Nolan-Herman-Buyer-Resume.pdf" target="_blank" rel="noopener"><img src="images/resume-buyer.jpg" alt="Buyer résumé cover" />
      <div><p class="eyebrow">For buyers</p><h3>Buyer <em>résumé</em></h3><p>Results, how buying works, my no-risk buyers program and client reviews.</p><span class="pill solid">Open résumé (PDF)</span></div></a>
  </div></div></section>'''

TOOLS = f'''<section class="tools">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free home value report</p><h3>What's your home <em>worth?</em></h3>
      <p>A personalized value report from Nolan, not an algorithm. Usually within 24 hours.</p>{VALUE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">Free download</p><h3>The Hickory Area <em>Buyer's Guide</em></h3>
      <p>Seven steps from budget to keys, plus a home tour checklist. Written in plain English.</p>{GUIDE_FORM}</div>
  </div>
</section>'''

BOOK = CALENDLY or "contact.html#book"
CTA = f'''<section class="contact">
  <div class="frame small">
    <div class="still-bg" style="background-image:url('images/hickory-downtown.jpg')"></div><div class="shade"></div>
    <div class="c-copy">
      <h2>Ready when <em>you</em> are.</h2>
      <p>Call, text, email, or book a time. I respond fast.</p>
      <div class="hero-btns center">
        <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill light" href="sms:{TEL}">Text Nolan</a>
        <a class="pill" href="mailto:{EMAIL}">Email Nolan</a><a class="pill" href="{BOOK}">Book a call</a>
      </div>
    </div>
  </div>
</section>'''

MARQUEE = '''<div class="marquee" aria-hidden="true"><div class="track">''' + ("<span>Hickory</span><i>✦</i><span><em>Conover</em></span><i>✦</i><span>Granite Falls</span><i>✦</i><span><em>Huntersville</em></span><i>✦</i><span>Lake Norman</span><i>✦</i><span>Charlotte</span><i>✦</i><span><em>Blue Ridge</em></span><i>✦</i>" * 2) + "</div></div>"

COUNTERS = '''<div class="counters reveal">
  <div><b data-count="10" data-prefix="$" data-suffix="M+">$10M+</b><span>Total volume</span></div>
  <div><b data-count="8" data-prefix="$" data-suffix="M+">$8M+</b><span>Sold in 2026</span></div>
  <div><b data-count="100" data-suffix="%">100%</b><span>Listings sold</span></div>
  <div><b data-count="600" data-suffix="+">600+</b><span>Families helped by Nestlewood</span></div>
</div>'''

# ================= HOME =================
page("index.html", "Nolan Herman, REALTOR® | Nestlewood Realty | Hickory, NC", "", f'''
<section class="hero" id="top">
  <div class="frame">
    <div class="photo-bg" style="background-image:url('images/stills/charlotte.jpg')"></div>
    <video class="hero-video" data-src="https://videos.pexels.com/video-files/33464075/14238297_1920_1080_30fps.mp4" muted loop playsinline autoplay hidden disablepictureinpicture disableremoteplayback preload="metadata" aria-hidden="true"></video>
    <div class="fog f1"></div><div class="fog f2"></div><div class="fog f3"></div><div class="shade"></div>
    <div class="trace-line" aria-hidden="true"><span class="chip"><i></i> Serving Hickory &amp; Charlotte</span></div>
    <div class="hero-copy">
      <p class="kicker">Nolan Herman · REALTOR® · Nestlewood Realty</p>
      <h1 class="split-words">Let's go <em>home.</em></h1>
      <p class="hero-sub">Buying and selling across Hickory, Conover, Granite Falls, Huntersville and the Charlotte area, made simple.</p>
      <div class="hero-btns"><a class="pill light" href="listings.html">Explore listings</a><a class="pill" href="sell.html#value">What's my home worth?</a></div>
    </div>
    <ul class="hero-stats">
      <li><b data-count="10" data-prefix="$" data-suffix="M+">$10M+</b>total sales volume</li>
      <li><b data-count="8" data-prefix="$" data-suffix="M+">$8M+</b>sold in 2026</li>
      <li><b data-count="100" data-suffix="%">100%</b>of listings sold</li>
    </ul>
    <aside class="glass-card"><small>Meet Nolan</small><p>I carved my own path into real estate. Let's find yours.</p>
      <img src="images/headshot.jpg" alt="Nolan Herman" /><a class="pill solid" href="about.html">My story</a></aside>
    <div class="scroll-cue"><span></span></div>
  </div>
</section>
{MARQUEE}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="Nolan Herman" /></div><span class="tag-glass">2 years · $10M+ sold</span></div>
    <div>
      <p class="eyebrow reveal">Meet Nolan</p>
      <h2 class="words home-story">After realizing the traditional school path wasn't for me, I decided to carve out my own path in real estate, even though no one in my family had experience in the <em>industry.</em></h2>
      <p class="body reveal">My passion for real estate comes from my own experience with how stressful moving can be, and I want to make that process easier, smoother, and more enjoyable for others.</p>
      <p class="body reveal" style="margin-top:-1rem"><a class="pill solid" href="about.html">Read my story</a></p>
      {COUNTERS}
    </div>
  </div>
</section>
{QUOTE_STRIP}
{RESUMES}
{panels(HOME_AREAS)}
{TOOLS}
{rail(FEATURED + SOLD, "Homes I'm <em>proud</em> to represent", "Featured &amp; sold", "listings.html")}
{CTA}''', curtain=True, desc="Nolan Herman, REALTOR® with Nestlewood Realty. Buy, sell or relocate anywhere from Hickory to Charlotte. Free home value report, buyer and seller guides, and featured listings.")

# ================= ABOUT =================
page("about.html", "About Nolan Herman | Nestlewood Realty", "about.html", f'''
{page_hero("About", "Meet <em>Nolan.</em>", "Licensed REALTOR® with Nestlewood Realty, serving Hickory, Conover, Granite Falls, Huntersville and the Charlotte area.", "golden", video="beach")}
<section class="statement">
  <div class="wrap st-grid">
    <div class="st-photo reveal"><div class="kb"><img src="images/headshot.jpg" alt="Nolan Herman" /></div><span class="tag-glass">Nestlewood Realty</span></div>
    <div>
      <p class="eyebrow reveal">My story</p>
      <h2 class="words">Real estate wasn't a family business, and I didn't have a traditional path into the <em>industry.</em></h2>
      <p class="body reveal">School wasn't for me, and after experiencing firsthand how stressful moving can be, I knew I wanted to build a career where I could make that experience easier for others. I took a chance on myself, reached out for an opportunity, and turned that first yes into a career built on hard work, determination, and helping people find a place to call home.</p>
      {COUNTERS}
    </div>
  </div>
</section>
<section class="sec sand"><div class="wrap center"><p class="eyebrow">How I got here</p><h2>From emails to <em>$10M+</em></h2>
  <div class="timeline" style="text-align:left">
    <div class="tl reveal"><i>1</i><h3>Growing up</h3><p>Saw firsthand how stressful moving can be for a family.</p></div>
    <div class="tl reveal"><i>2</i><h3>The emails</h3><p>Out of high school, I emailed brokers asking for a shot.</p></div>
    <div class="tl reveal"><i>3</i><h3>The internship</h3><p>One broker said yes, and I learned every part of the business.</p></div>
    <div class="tl reveal"><i>4</i><h3>REALTOR®</h3><p>Two years in: $10M+ sold and 100% of my listings sold.</p></div>
  </div></div></section>
{REVIEWS}
{CTA}''', desc="Meet Nolan Herman, REALTOR® with Nestlewood Realty in Hickory, NC. $10M+ in sales and 100% of his listings sold.")

# ================= BUY =================
page("buy.html", "Buy a Home | Nolan Herman, REALTOR®", "buy.html", f'''
{page_hero("Buy", "Buy a <em>home.</em>", "From your first showing to closing day, I'll help you find the right home and negotiate the best deal.", "dawn", video="lake")}
<section class="sec"><div class="wrap center"><p class="eyebrow">How it works</p><h2>Your path to the <em>keys</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Talk</h3><p>A quick call about what you want, where, and your budget.</p></div>
    <div class="step reveal"><h3>Get pre-approved</h3><p>I'll connect you with trusted lenders so you can shop with confidence.</p></div>
    <div class="step reveal"><h3>Tour &amp; offer</h3><p>We tour homes together, then write a strong offer that stands out.</p></div>
    <div class="step reveal"><h3>Close</h3><p>I handle inspections, appraisal, and paperwork right up to closing day.</p></div>
  </div></div></section>
<section class="sec sand" id="calculator"><div class="wrap"><p class="eyebrow">Mortgage calculator</p><h2>What will my <em>payment</em> be?</h2>
  <div class="calc reveal">
    <div class="inputs">
      <label>Home price ($)<input id="c-price" type="number" value="350000" min="0" step="1000" /></label>
      <div class="row2"><label>Down payment (%)<input id="c-down" type="number" value="10" min="0" max="100" /></label><label>Interest rate (%)<input id="c-rate" type="number" value="6.5" min="0" step="0.05" /></label></div>
      <div class="row2"><label>Loan term (years)<input id="c-term" type="number" value="30" min="1" /></label><label>Taxes + insurance / mo ($)<input id="c-extra" type="number" value="350" min="0" step="10" /></label></div>
      <p class="fine">Estimate only. Talk to a lender for your exact numbers.</p>
    </div>
    <div class="result"><div class="scene" data-scene="dusk"></div><small style="letter-spacing:.2em;text-transform:uppercase;font-size:.7rem;opacity:.8">Estimated monthly payment</small><div class="pay" id="c-pay">$0</div>
      <div class="bd"><div><span>Principal &amp; interest</span><b id="c-pi">$0</b></div><div><span>Taxes &amp; insurance</span><b id="c-ti">$0</b></div><div><span>Loan amount</span><b id="c-loan">$0</b></div></div></div>
  </div></div></section>
<section class="tools">
  <div class="scene" data-scene="night"></div><div class="stars"></div>
  <div class="wrap tools-grid">
    <div class="glass tool reveal"><p class="eyebrow">Free download</p><h3>The Hickory Area <em>Buyer's Guide</em></h3>
      <p>Seven steps from budget to keys, plus a home tour checklist. Written in plain English.</p>{GUIDE_FORM}</div>
    <div class="glass tool reveal"><p class="eyebrow">What's inside</p><h3>Everything you need to <em>buy smart</em></h3>
      <ul class="checks"><li>How much home you can really afford</li><li>Getting pre-approved (and why it wins offers)</li><li>How to make an offer that stands out</li><li>Due diligence, inspections and closing, explained</li></ul></div>
  </div>
</section>
{rail(FEATURED, "Homes for <em>sale</em>", "Featured listings", "listings.html")}
{CTA}''', desc="Buying a home in the Hickory or Charlotte area? Get Nolan's step-by-step plan, a free buyer's guide and a mortgage payment calculator.")

# ================= SELL =================
page("sell.html", "Sell Your Home | Nolan Herman, REALTOR®", "sell.html", f'''
{page_hero("Sell", "Sell your <em>home.</em>", "Smart pricing, professional photos, and social media marketing that puts your home in front of the right buyers.", "dusk", video="https://videos.pexels.com/video-files/10215996/10215996-hd_1080_1920_30fps.mp4", still="images/stills/mountains.jpg")}
<section class="statement"><div class="wrap">
  <p class="eyebrow reveal">Results</p>
  <h2 class="words" style="max-width:1000px">Every one of my listings has sold. I launch your home like a product, so buyers compete for <em>it.</em></h2>
  <div style="margin-top:3rem">{COUNTERS}</div>
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">My selling plan</p><h2>How I get your home <em>sold</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Price it right</h3><p>A detailed look at recent sales so we list at the right number from day one.</p></div>
    <div class="step reveal"><h3>Make it shine</h3><p>Professional photos and video that make buyers stop scrolling.</p></div>
    <div class="step reveal"><h3>Market everywhere</h3><p>The MLS, Zillow, Homes.com, plus targeted Instagram and Facebook ads.</p></div>
    <div class="step reveal"><h3>Negotiate &amp; close</h3><p>I screen offers, negotiate hard, and handle every detail to closing.</p></div>
  </div></div></section>
{SELL_TOOLS}
{rail(SOLD, "Recently <em>sold</em>", "Results")}
{REVIEWS}
{CTA}''', desc="Selling your home in Hickory, Lake Norman or Charlotte? Get a free home value report from Nolan and see his plan to price, market and sell it.")

# ================= LISTINGS =================
page("listings.html", "Listings | Nolan Herman, REALTOR®", "listings.html", f'''
{page_hero("Listings", "Featured <em>homes.</em>", "My featured homes and recent sales across the Catawba Valley and beyond.", "golden", "images/city-night.jpg")}
<section class="sec dark"><div class="wrap"><div class="head"><div><p class="eyebrow">For sale</p><h2>Featured <em>listings</em></h2></div><a class="pill" href="{ZILLOW}" {EXT}>All on Zillow</a></div>
  <div class="grid3">{"".join(card(*l) for l in FEATURED)}</div></div></section>
<section class="sec"><div class="wrap"><div class="head"><div><p class="eyebrow">Results</p><h2>Recently <em>sold</em></h2></div></div>
  <div class="grid3">{"".join(card(*l, sold=True) for l in SOLD)}</div></div></section>
{CTA}''', desc="Featured homes for sale and recent sales by Nolan Herman, REALTOR® with Nestlewood Realty, across the Catawba Valley and beyond.")

def credit_line(a):
    c = a.get("credit")
    if not c:
        return ""
    who, page_url, lic, lic_url = c
    return (f'<span class="photo-credit">Photo: <a href="{page_url}" {EXT}>{E(who)}</a>, '
            f'<a href="{lic_url}" {EXT}>{E(lic)}</a></span>')

# Area pages (no separate Areas overview page)
for key, a in AREAS.items():
    i = CORRIDOR.index(key)
    others = [k for k in sorted(CORRIDOR, key=lambda k: abs(CORRIDOR.index(k) - i)) if k != key][:4]
    page(f"{key}.html", f"Living in {a['name']}, NC | Nolan Herman, REALTOR®", "areas.html", f'''
{page_hero(f"Areas / {a['name']}", f"Living in <em>{a['name']}.</em>", a["short"], a["scene"], a.get("photo"), a.get("video"))}
<section class="sec"><div class="wrap split2">
  <div class="reveal"><p class="eyebrow">{a["county"]}</p><h2>Why people love <em>{a["name"]}</em></h2><p class="lead">{a["intro"]}</p>
    <ul class="checks">{"".join(f"<li>{E(x)}</li>" for x in a["love"])}</ul>
    <div class="hero-btns" style="margin-top:2rem"><a class="pill solid" href="contact.html">Find a home in {a["name"]}</a></div></div>
  <div class="area-photo reveal">{bg(a["scene"], a.get("photo"))}{credit_line(a)}</div>
</div>
<div class="wrap"><div class="facts">{"".join(f'<div class="fact reveal"><b>{E(x)}</b><span>{E(y)}</span></div>' for x, y in a["facts"])}</div>
  {'<p class="fine" style="margin-top:1rem">*Charlotte metro median sale price, August 2026 (Homes.com). See the <a href="market.html" style="text-decoration:underline">market update</a>.</p>' if any("*" in y for x, y in a["facts"]) else ""}</div></section>
{panels(others, "Nearby <em>areas</em>")}
{TOOLS}
{CTA}''', desc=f"Thinking about living in {a['name']}, NC? {a['short']} Homes, neighborhoods and local tips from Nolan Herman, REALTOR®.")

# ================= CONTACT =================
page("contact.html", "Contact Nolan Herman | Nestlewood Realty", "contact.html", f'''
{page_hero("Contact", "Let's <em>talk.</em>", "Call, text, email, or book a time. I respond fast.", "sunset", video="beach")}
<section class="sec"><div class="wrap split2 top">
  <div class="reveal"><p class="eyebrow">Reach me</p><h2>I'm here to <em>help.</em></h2>
    <div class="contact-list">
      <a class="pill solid" href="tel:{TEL}">Call {PHONE}</a><a class="pill" href="sms:{TEL}">Text Nolan</a><a class="pill" href="mailto:{EMAIL}">{EMAIL}</a>
      <a class="pill" href="{MAP}" {EXT}>{ADDRESS}</a>
    </div></div>
  <form class="form reveal lead-form" data-subject="Website contact form" data-need-contact style="background:#ebe3d8">
    <div class="row2"><label>Name<input name="name" required /></label><label>Phone<input name="phone" type="tel" /></label></div>
    <label>Email<input name="email" type="email" /></label><span class="form-note dark">Phone or email, whichever you prefer.</span>
    <label>I'm interested in<select name="topic"><option>Buying</option><option>Selling</option><option>Home value report</option><option>Something else</option></select></label>
    <label>Message<textarea name="message" rows="4"></textarea></label>
    <button class="pill solid" type="submit">Send message</button>
  </form></div></section>
<section class="sec tight" id="book"><div class="wrap">
  <div class="booking reveal"><div class="scene" data-scene="night"></div><div class="stars"></div>
    <div><p class="eyebrow" style="color:rgba(255,255,255,.7)">Book a call</p><h2>Pick a <em>time.</em></h2>
      <div class="cal">{"".join(f'<i class="{"sel" if d == 14 else "av" if d in (9,10,15,16,17,21,22) else ""}">{d}</i>' for d in range(5, 26))}</div>
      <a class="pill solid" href="{CALENDLY or "tel:" + TEL}" style="margin-top:1rem">Book a call</a></div></div>
</div></section>''', desc="Call, text or email Nolan Herman, REALTOR® at Nestlewood Realty, 825 Highland Ave SE, Hickory, NC. 828-404-5335.")
# ================= RELOCATE =================
def town_card(k):
    a = AREAS[k]; h, c = DRIVE[k]
    return f'''<a class="town reveal" href="{k}.html"><div class="t-top"><h3>{a["name"]}</h3><span>{a["county"]}</span></div>
  <p>{a["short"]}</p><div class="t-drive"><div><b>{h}</b><span>To Hickory</span></div><div><b>{c}</b><span>To Charlotte</span></div></div><i>Explore {a["name"]} →</i></a>'''

page("relocate.html", "Relocating to Hickory, Lake Norman or Charlotte | Nolan Herman, REALTOR®", "relocate.html", f'''
{page_hero("Relocate", "Moving <em>here?</em>", "From the foothills of Hickory to the Charlotte skyline, I'll help you find the right town and the right home, even from out of state.", "golden", "images/hickory-downtown.jpg", video="clt-sunrise")}
<section class="statement"><div class="wrap">
  <p class="eyebrow reveal">Why people move here</p>
  <h2 class="words" style="max-width:1050px">Mountains an hour one way, a major city an hour the other, and lake life in <em>between.</em></h2>
  <div class="facts" style="margin-top:3rem">
    <div class="fact reveal"><b>15</b><span>Towns I cover</span></div>
    <div class="fact reveal"><b>~1 hr</b><span>Hickory to Charlotte</span></div>
    <div class="fact reveal"><b>~1 hr</b><span>Hickory to the Blue Ridge</span></div>
    <div class="fact reveal"><b>$100K+</b><span>Less for a Hickory-area home*</span></div>
  </div>
  <p class="fine" style="margin-top:1rem">*Hickory metro median of about $312K vs. Charlotte metro median of about $425K. See the <a href="market.html" style="text-decoration:underline">market update</a> for sources.</p>
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">How I help from out of town</p><h2>Buy here without <em>flying back and forth</em></h2>
  <div class="steps4" style="text-align:left">
    <div class="step reveal"><h3>Find your town</h3><p>A call about your job, commute, schools and lifestyle, then a short list of towns that fit.</p></div>
    <div class="step reveal"><h3>Live video tours</h3><p>I walk homes and neighborhoods with you on FaceTime and point out what photos don't show.</p></div>
    <div class="step reveal"><h3>Local team</h3><p>Trusted lenders, inspectors and closing attorneys, so every step happens on time.</p></div>
    <div class="step reveal"><h3>Close from anywhere</h3><p>I coordinate the details so you can sign remotely if you need to and arrive to your keys.</p></div>
  </div></div></section>
<section class="sec" id="towns"><div class="wrap"><div class="head"><div><p class="eyebrow">Hickory to Charlotte</p><h2>Find your <em>town</em></h2></div></div>
  <p class="lead" style="max-width:720px">Listed from the foothills down to the city. Drive times are approximate, in normal traffic.</p>
  <div class="towns">{"".join(town_card(k) for k in CORRIDOR)}</div></div></section>
<section class="quote-strip"><div class="wrap qs-inner">
  <figure class="full-review" style="margin-top:0;border-top:0;padding-top:0"><div class="fr-stars">★★★★★</div>
    <blockquote><p>Relocating from the place where we raised our family was anticipated to be challenging, but Nolan significantly eased the process.</p></blockquote>
    <figcaption><b>Pricilla &amp; Jeff L.</b><span>Relocated · Granite Falls, NC · 2026</span><a href="{ZILLOW}" {EXT}>Read it on Zillow →</a></figcaption></figure>
</div></section>
<section class="sec sand"><div class="wrap split2 top">
  <div class="reveal"><p class="eyebrow">Relocation plan</p><h2>Tell me about your <em>move.</em></h2>
    <p class="lead">I'll send a short list of towns and homes that fit, plus what to expect on price, commute and timing.</p>
    <ul class="checks"><li>Free relocation consult</li><li>Area tours by video or in person</li><li>Help finding a trusted agent to sell your current home</li></ul></div>
  <form class="form reveal lead-form" data-subject="Relocation request" data-need-contact style="background:#fff">
    <div class="row2"><label>Name<input name="name" required /></label><label>Moving from<input name="moving_from" placeholder="City, state" /></label></div>
    <div class="row2"><label>Phone<input name="phone" type="tel" /></label><label>Email<input name="email" type="email" /></label></div>
    <span class="form-note dark">Phone or email, whichever you prefer.</span>
    <label>When are you moving?<select name="timeline"><option>In the next 3 months</option><option>3 to 6 months</option><option>6 to 12 months</option><option>Just exploring</option></select></label>
    <label>Anything else?<textarea name="message" rows="3" placeholder="Job location, budget, must-haves..."></textarea></label>
    <button class="pill solid" type="submit">Send my relocation plan</button>
  </form></div></section>
{CTA}''', desc="Relocating to Hickory, Lake Norman or Charlotte, NC? Compare 15 towns, drive times and prices, and get a free relocation plan from Nolan Herman, REALTOR®.")

# ================= MARKET UPDATE =================
def market_block(m):
    return f'''<div class="mk reveal"><div class="mk-head"><h3>{m["area"]}</h3><span>{m["period"]}</span></div>
  <div class="facts" style="margin-top:1.2rem">{"".join(f'<div class="fact"><b>{E(x)}</b><span>{E(y)}</span></div>' for x, y in m["stats"])}</div>
  <p class="fine" style="margin-top:.8rem">Source: <a href="{m["url"]}" {EXT} style="text-decoration:underline">{m["source"]}</a></p></div>'''

page("market.html", f"Hickory & Charlotte Market Update, {MARKET_MONTH} | Nolan Herman, REALTOR®", "market.html", f'''
{page_hero("Market update", "Market <em>update.</em>", "Home prices, days on market and supply for the Hickory and Charlotte areas, plus what it means if you're buying or selling.", "dusk", "images/charlotte-skyline.jpg", video="clt-stadium")}
<section class="sec"><div class="wrap"><p class="eyebrow">{MARKET_MONTH}</p><h2>By the <em>numbers</em></h2>
  {"".join(market_block(m) for m in MARKET)}
</div></section>
<section class="sec dark"><div class="wrap center"><p class="eyebrow">What it means</p><h2>Nolan's <em>take</em></h2>
  <div class="steps4 three" style="text-align:left">{"".join(f'<div class="step reveal"><h3>{E(t)}</h3><p>{E(b)}</p></div>' for t, b in MARKET_TAKE)}</div></div></section>
{SELL_TOOLS}
{CTA}''', desc=f"{MARKET_MONTH} housing market update for Hickory and Charlotte, NC: median prices, days on market and supply, with what it means for buyers and sellers.")
print("built")
