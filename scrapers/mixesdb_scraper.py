import urllib2
from bs4 import BeautifulSoup

def scrape_mixesdb(url):
	url = urllib2.urlopen(url)
	soup = BeautifulSoup(url)
	mix_name = soup.h1.text
	mix_data = process_mix_name(mix_name)
	categories = soup.find(id = "mw-normal-catlinks").find_all("a")
	for item in categories:
		n = categories.index(item)
		categories[n] = item.text
	if soup.ol:
		tracks = scrape_ordered(soup.ol)
	elif soup.find(id = "bodytext").find("div",class_= "list").find("p"):
		tracks = scrape_unordered(soup.find(id = "bodytext").find("div",class_= "list").find("p"))
	else:
		tracks = []
		print "No tracks on this page"
	mix_data["tracks"] = tracks
	mix_data["categories"] = categories
	return mix_data

def process_mix_name(mix_name):
	matches = re.match(r"[\d\-]*\s\-(.*)",mix_name)
	original_slug = matches.group(1)
	title = matches.group(1)
	if "@" in title:
		title = title.split("@")
		artist = title[0]
		mix_title = [title][1]
	elif title.count(" - ") > 0:
		title = title.split(" - ")
		artist = title[0]
		mix_title = title[1]
	else:
		artist = ""
		mix_title = ""
	return {"original_slug":original_slug, "artist":artist, "mix_title":mix_title}




def scrape_ordered(tracks):
	tracklist = []
	tracks = tracks.find_all("li")
	for track in tracks:
		track = track.text
		tracklist.append(process_line(track))
	return tracklist

def scrape_unordered(tracks):
	tracklist = []
	tracks = tracks.text
	tracks = tracks.splitlines()
	for track in tracks:
		tracklist.append(process_line(track))
	return tracklist


# captures number, artist, title and notes
# regex = r"([\[\d?\]]*)([^\-]*)\-([^\[]*)(.*)"

# regex used only captures number and notes
# slug is then split only if there is either one single dash surrounded by spaces, else, if there is only 1 dash period
def process_line(line):
	match = re.match(r"([\[\d?\]]*)[^\[]*(.*)", line)
	if match:
		number = match.group(1)
		notes = match.group(2)
		notes = notes.rstrip("\n")
		slug = line.replace(notes, "")
		slug = slug.replace(number, "")
		slug = slug.rstrip("\n")
		slug = slug.strip()
		if slug != "?" and slug != "...":
			if slug.count(" -") == 1:
				slug_parts = slug.split(" -")
				artist = slug_parts[0]
				artist = artist.rstrip("\n")
				artist = artist.strip()
				title = slug_parts[1]
				title = title.rstrip("\n")
				title = title.strip()
				#print "slug: "+slug +"\nArtist: "+artist +"\nTitle: " + title + "\nNotes: " + notes +"\n"
			elif slug.count("-") ==1:
				slug_parts = slug.split("-")
				artist = slug_parts[0]
				artist = artist.rstrip("\n")
				artist = artist.strip()
				title = slug_parts[1]
				title = title.rstrip("\n")
				title = title.strip()
				#print "slug: "+slug +"\nArtist: "+artist +"\nTitle: " + title + " \nNotes: " + notes +"\n"
			elif slug.count("-") > 1:
				artist = ""
				title = ""
				#print "Slug: " + slug + "\n unable to determine artist and title, too many dashes"
		return {"artist":artist, "title":title, "original_slug":slug, "Notes":notes}

	#print " Artist: "+match.group(1) +"\n Title:" + match.group(2) + "\n Notes: " + match.group(3) +"\n"
	#return match

for track in tracks:
	process_line(track.text)

for track in unordered_list:
	process_line(track)

unordered_tracks = """<p>[00] ?<br/>
...<br/>
[14] Markus Homm &amp; Philippgonzales - Muuuv [Brise]<br/>
[17] Mark Henning - Stacked [Upon You - UYCD 002]<br/>
[22] Elia Perrone - Bagatelas (Italoboyz Love Klang Remix) [Unclear - 006]<br/>
[27] ?<br/>
...<br/>
[35] Beroshima / Frank Müller &amp; Ulrich Schnauss - Horizon (Pig &amp; Dan Remix) [Tulipa - A 002]<br/>
[40] HD Substance - Wave Carrier [Rez - 018]<br/>
[44] Steve Lorenz - Berghain 5 AM [Tarvisium Electronique - TAEL 004]<br/>
[50] Electric Rescue - Back Home [Soma]<br/>
[58] Tale Of Us - Lost City [Minus - MIN 2]
</p>"""

unordered_tracks = """u'[00]\xa0?\n...\n[14] Markus Homm & Philippgonzales - Muuuv [Brise]\n[17] Mark Henning - Stacked [Upon You - UYCD 002]\n[22] Elia Perrone - Bagatelas (Italoboyz Love Klang Remix) [
Unclear - 006]\n[27]\xa0?\n...\n[35] Beroshima / Frank M\xfcller & Ulrich Schnauss - Horizon (Pig & Dan Remix) [Tulipa - A 002]\n[40] HD Substance - Wave Carrier [Rez - 018]\n[44] S
teve Lorenz - Berghain 5 AM [Tarvisium Electronique - TAEL 004]\n[50] Electric Rescue - Back Home [Soma]\n[58] Tale Of Us - Lost City [Minus - MIN 2]\n'"""

ordered_tacks = """</li>, <li> Digital &amp; Spirit - Phantom Force (Fracture's Astrophonica Edit) [White]
</li>, <li> Sam Binga - 8barr [White]
</li>, <li> Alix Perez Feat. Riko Dan - Warlord [Chroma Chords, Shogun]
</li>, <li> Skeptical - Delusions [White]
</li>, <li> Dub Phizix &amp; Skeptical Feat. Strategy - Marka [Exit]
</li>, <li> Tyler, The Creator - Yonkers [Goblin, Xl]
</li>, <li> Flosstradamus - Roll Up (Baauer Remix) [All Trap Music, Mad Decent]
</li>, <li> Tnght - Higher Ground [Tnght, Warp]
</li>, <li> Alix Perez &amp; Stray - Rip N Dip [Dub]
</li>, <li> Dub Phizix Feat. Skittles - Creator [Exit]
</li>, <li> Stray - Dropping Bombs [White]
</li>, <li> Fracture - Bad Habit (Om Unit VIP) [Astrophonica]
</li>, <li> Rockwell - Back Again [Shogun]
</li>, <li> Icicle - Minimal Funk [Shogun]
</li>, <li> Loxy &amp; Isotone - Ancients (Skeptical Remix) [Cyclon]
</li>, <li> Alix Perez Feat. Strange U - Shadows [Chroma Chords, Shogun]
</li>, <li> Icicle - Dumbstep [Dub]
</li>, <li> Alix Perez Feat. Foreign Beggars - Dark Days (2013 Edit) [Shogun]
</li>, <li> Dom &amp; Roland - Odd Job (Ulterior Motive Remix) [Dom &amp; Roland]
</li>, <li> Alix Perez Feat. Metropolis - Blueprint [Chroma Chords (Deluxe Edition), Shogun]
</li>, <li> Noisia Feat. Joe Seven - Hand Gestures [Split The Atom, Vision]
</li>, <li> Foreign Concept Feat. T Man - Tag Team [Critical]
</li>, <li> Stray - Ginseng Smash [Critical]
</li>, <li> Commix - Justified (Spectrasoul Remix) [Metalheadz]
</li>, <li> Adam F - Metropolis [Metalheadz]
</li>, <li> Ed Rush &amp; Optical - Watermelon [Virus]
</li>, <li> Dillinja - Silver Blade [Prototype]
</li>, <li> Calibre Feat. Chimpo - Start Again [Spill, Signature]
</li>, <li> Calibre Feat. Steo - Wilderness [Spill, Signature]
</li>, <li> SpectraSoul - Guardian [Metalheadz]
</li>, <li> Alix Perez Feat. D.Ablo - Playing Games [Chroma Chords, Shogun]
</li>, <li> Planas Feat. Ed Thomas - Breathtaking (dBridge Soulsteppers Remix) [Exceptional]
</li>, <li> Calibre - Second Sun [Second Sun, Signature]
</li>, <li> Alix Perez - Contradictions [1984, Shogun]
</li>, <li> Alix Perez &amp; Sabre - Solitary Native [Shogun]
</li>, <li> Icicle - Klickstep [Dub]
</li>, <li> Noisia - Facade [Ram]
</li>, <li> Rob F &amp; Impulse - Ultraviolet [Cryptic]
</li>, <li> Alix Perez - I'm Free [Shogun]
</li>, <li> Rockwell - Full Circle [Shogun]
</li>, <li> Skeptical &amp; Chimpo - Bad Acid [White]
</li>, <li> Louis Blaise - Love And Gwalla (Phillip D Kick Remix) [White]
</li>, <li> Stray - Akina [Critical]
</li>, <li> Jubei Feat. Flowdan - Say Nothin' (Rockwell Remix) [Razors Edge]
</li>, <li> Alix Perez Feat. They Call Me Raptor - Villains 1 Heroes 0 [Chroma Chords, Shogun]
</li>, <li> Alix Perez Feat. Sam Wills - Annie's Song [Chroma Chords, Shogun]
</li>, <li> The Bug Feat. Flowdan &amp; Killa P - Skeng [Hyperdub]
</li>, <li> I Am Legion - Warp Speed Thuggin' [Division]
</li>, <li> Aphex Twin - Window Licker [Warp]
</li>, <li> Fela Kuti - Water Get No Enemy [Editions Makossa]
</li>]"""



# real_regex = r"[\[\d\]]*([^\-]*)\-([^\[]*)(.*)"
# regex = 	 r"([\[\d\]]*)([^\-]*)\-([^\[]*)(.*)"


# #matches SPACE AND DASH
# possible_regex = r"[\[\d\]]*([^\-]*)\s\-+([^\[]*)(.*)"

# regex = r'[\[\d\?\]]([^\-])/-([^\[])(.*)'
# #regex = r"[\[\d*?*\]]*([^\s\-\s])[\s\-\s]+"

# "regex = /[\[\d*\]]*([\s\S]+)-+([\s\S]+)\[([\s\S]+)\]/ "



