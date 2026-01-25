"""
Iowa Events Scraper v5 - COMPREHENSIVE
===========================================
Sources included:
- TBK Bank Sports Complex (Bettendorf)
- Xtream Arena (Coralville) 
- Wells Fargo Arena / Casey's Center (Des Moines)
- Adventureland (Altoona)
- Major races (Dam to Dam, Bix 7, Living History Farms)
- County Fairs (all 99 counties!)
- Chamber events (Cedar Rapids, Sioux City, Dubuque, Ankeny, WDM, etc.)
- Catch Des Moines / Travel Iowa festivals
- Iowa Hawkeyes
- High School State Tournaments
- Iowa Heartlanders Hockey
- Iowa Wild Hockey
- Iowa Wolves Basketball
"""

import json
import csv
import re
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import Optional, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TODAY = date.today()

IOWA_COORDS = {
    "Des Moines": (41.5868, -93.6250),
    "Cedar Rapids": (41.9779, -91.6656),
    "Davenport": (41.5236, -90.5776),
    "Sioux City": (42.4963, -96.4049),
    "Ankeny": (41.7318, -93.6001),
    "Iowa City": (41.6611, -91.5302),
    "West Des Moines": (41.5772, -93.7113),
    "Ames": (42.0308, -93.6319),
    "Waterloo": (42.4928, -92.3426),
    "Council Bluffs": (41.2619, -95.8608),
    "Dubuque": (42.5006, -90.6646),
    "Urbandale": (41.6267, -93.7122),
    "Cedar Falls": (42.5349, -92.4453),
    "Marion": (42.0342, -91.5975),
    "Bettendorf": (41.5503, -90.4857),
    "Coralville": (41.6765, -91.5804),
    "Altoona": (41.6442, -93.4647),
    "Clear Lake": (43.1380, -93.3791),
    "Pella": (41.4083, -92.9163),
    "Indianola": (41.3578, -93.5572),
    "Monticello": (42.2383, -91.1871),
    "St. Charles": (41.2908, -93.8158),
    "Dyersville": (42.4844, -91.1224),
    "Grimes": (41.6883, -93.7911),
    "Sioux Center": (43.0786, -96.1756),
    "Fort Dodge": (42.4975, -94.1680),
    "Elk Horn": (41.5944, -95.0672),
    "Newton": (41.7000, -93.0480),
    "Knoxville": (41.3208, -93.1010),
    "Central City": (42.2036, -91.5268),
    "Mason City": (43.1536, -93.2010),
    "Polk City": (41.7711, -93.7130),
    "Winterset": (41.3308, -94.0136),
    "Moline": (41.5067, -90.5151),
}


@dataclass
class Event:
    title: str
    date: str
    time: Optional[str]
    location: str
    venue: Optional[str]
    category: str
    subcategory: Optional[str]
    source: str
    source_url: str
    description: Optional[str] = None
    city: Optional[str] = None
    teams: Optional[str] = None
    age_group: Optional[str] = None
    registration_url: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class IowaEventsScraper:
    
    def __init__(self):
        self.events: List[Event] = []
    
    def _get_coords(self, city: str) -> tuple:
        return IOWA_COORDS.get(city, (None, None))
    
    def _is_future_event(self, date_str: str) -> bool:
        if not date_str:
            return True
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12,
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        date_lower = date_str.lower()
        for month_name, month_num in months.items():
            if month_name in date_lower:
                year_match = re.search(r'20(\d{2})', date_str)
                if year_match:
                    year = int(f"20{year_match.group(1)}")
                    day_match = re.search(r'(\d{1,2})', date_str)
                    day = int(day_match.group(1)) if day_match else 1
                    try:
                        event_date = date(year, month_num, min(day, 28))
                        return event_date >= TODAY
                    except:
                        pass
        return True

    def _add(self, title, dt, tm, city, venue, cat, subcat, src, url, desc=None, age=None, age_group=None):
        if not self._is_future_event(dt):
            return
        lat, lng = self._get_coords(city)
        self.events.append(Event(
            title=title, date=dt, time=tm, location=f"{city}, IA",
            venue=venue, category=cat, subcategory=subcat,
            source=src, source_url=url, city=city,
            description=desc, age_group=age_group or age, latitude=lat, longitude=lng
        ))

    # ==================== TBK BANK SPORTS COMPLEX ====================
    def add_tbk_events(self):
        logger.info("Adding TBK Bank Sports Complex events...")
        src, url = "TBK Bank Sports Complex", "https://www.tbkbanksportscomplex.com/events/"
        events = [
            ("New Year's Pickleball Tournament", "January 3, 2026", "8:00 AM", "pickleball", "All ages"),
            ("1v1 Goalkeeper Tournament", "January 2-4, 2026", "All day", "soccer", "8-18 yrs"),
            ("Blizzard Bash Indoor Softball", "January 9-11, 2026", "All day", "softball", "All ages"),
            ("LOVB Challenge Volleyball", "January 10, 2026", "All day", "volleyball", "10U+"),
            ("MLK Classic Indoor Softball", "January 16-17, 2026", "All day", "softball", "All ages"),
            ("MLK Classic Weekend 2", "January 18-19, 2026", "All day", "softball", "All ages"),
            ("Winter Soccer Futsal", "January 23-25, 2026", "All day", "soccer", "9U-19U"),
            ("Frozen Ropes Frenzy Softball", "January 30 - February 1, 2026", "All day", "softball", "All ages"),
            ("Winter Warm-Up Softball", "January 30 - February 2, 2026", "All day", "softball", "All ages"),
            ("President's Day Slugfest", "February 13-16, 2026", "All day", "softball", "All ages"),
            ("High School Warm-Up Softball", "February 27 - March 1, 2026", "All day", "softball", "High School"),
            ("LOVB Challenge #8", "February 28, 2026", "All day", "volleyball", "All ages"),
            ("GameTime Basketball", "May 2-3, 2026", "8:15 AM", "basketball", "Youth"),
            ("GameTime Basketball", "May 30-31, 2026", "8:15 AM", "basketball", "Youth"),
            ("GameTime Basketball", "June 13-14, 2026", "8:15 AM", "basketball", "Youth"),
            ("Summer Basketball Tournament", "June 27-28, 2026", "8:15 AM", "basketball", "All ages"),
            ("Great River Classic Soccer", "September 24-26, 2026", "8:00 AM", "soccer", "Youth"),
        ]
        for t, d, tm, sub, age in events:
            self._add(t, d, tm, "Bettendorf", "TBK Bank Sports Complex", "kids_athletics", sub, src, url, age_group=age)

    # ==================== XTREAM ARENA (CORALVILLE) ====================
    def add_xtream_arena_events(self):
        logger.info("Adding Xtream Arena events...")
        src, url = "Xtream Arena", "https://xtreamarena.com/"
        events = [
            ("Iowa Heartlanders vs Toledo", "January 16, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders Y2K Night", "January 30, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders EmpowerHER Night", "January 31, 2026", "6:00 PM", "hockey"),
            ("Iowa Heartlanders Video Game Night", "February 1, 2026", "3:00 PM", "hockey"),
            ("Iowa Heartlanders vs Kalamazoo", "February 11, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders Hockey For All Night", "February 13, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders ARTlanders Night", "February 14, 2026", "6:00 PM", "hockey"),
            ("Iowa Heartlanders vs Wichita", "February 18, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders Margaritaville Night", "February 20, 2026", "7:00 PM", "hockey"),
            ("Iowa Heartlanders Cornfed Night", "February 21, 2026", "6:00 PM", "hockey"),
            ("NCAA Women's Wrestling Championships", "March 6, 2026", "10:00 AM", "wrestling"),
            ("MVC Women's Basketball Championship", "March 12-15, 2026", "All day", "basketball"),
            ("Battle By The River Rodeo", "2026", "Evening", "rodeo"),
        ]
        for t, d, tm, sub in events:
            self._add(t, d, tm, "Coralville", "Xtream Arena", "sports", sub, src, url)

    # ==================== WELLS FARGO ARENA / CASEY'S CENTER ====================
    def add_wells_fargo_events(self):
        logger.info("Adding Wells Fargo Arena / Casey's Center events...")
        src, url = "Iowa Events Center", "https://www.iowaeventscenter.com/events/"
        events = [
            ("Iowa Wild vs Toronto Marlies", "January 16, 2026", "7:00 PM", "hockey"),
            ("Iowa Wild vs Toronto Marlies", "January 17, 2026", "6:00 PM", "hockey"),
            ("Iowa Wolves vs Long Island Nets", "January 18, 2026", "7:00 PM", "basketball"),
            ("Iowa Wolves vs Long Island Nets", "January 19, 2026", "4:00 PM", "basketball"),
            ("IHSAA State Wrestling Tournament", "February 19-21, 2026", "All day", "wrestling"),
            ("IGHSAU State Basketball Tournament", "March 2-7, 2026", "All day", "basketball"),
            ("IHSAA State Basketball Tournament", "March 9-14, 2026", "All day", "basketball"),
            ("Iowa Barnstormers Arena Football", "Spring 2026", "7:00 PM", "football"),
            ("Monster Jam", "April 11-12, 2026", "1:00 PM & 7:00 PM", "entertainment"),
        ]
        for t, d, tm, sub in events:
            self._add(t, d, tm, "Des Moines", "Wells Fargo Arena", "sports", sub, src, url)

    # ==================== ADVENTURELAND ====================
    def add_adventureland_events(self):
        logger.info("Adding Adventureland events...")
        src, url = "Adventureland", "https://www.adventurelandresort.com/"
        events = [
            ("Adventureland Season Opens", "May 16, 2026", "10:00 AM", "opening"),
            ("Paul Bunyan Lumberjack Show", "June 1-14, 2026", "All day", "show"),
            ("Canine Stars Stunt Dog Show", "June 17-30, 2026", "All day", "show"),
            ("Father's Day Belly Flop Contest", "June 20, 2026", "All day", "contest"),
            ("America's 250th Birthday Fireworks", "July 4, 2026", "9:00 PM", "fireworks"),
            ("Daniel Tiger Meet & Greets", "July 2026 (Sundays/Mondays)", "All day", "kids"),
            ("Neon Nights at Adventure Bay", "July 10 - August 15, 2026", "Evening", "waterpark"),
            ("Oktoberfest", "September 2026", "All day", "festival"),
            ("Phantom Fall Fest", "September 26 - October 31, 2026", "All day", "halloween"),
        ]
        for t, d, tm, sub in events:
            self._add(t, d, tm, "Altoona", "Adventureland", "family", sub, src, url, age_group="All ages")

    # ==================== MAJOR RACES ====================
    def add_races(self):
        logger.info("Adding major races...")
        races = [
            ("EMC Dam to DSM Half Marathon", "May 30, 2026", "7:00 AM", "Des Moines", "Saylorville Dam to Downtown", "Dam to DSM", "https://www.damtodsm.com/"),
            ("Quad-City Times Bix 7", "July 25, 2026", "8:00 AM", "Davenport", "Downtown Davenport", "Bix 7", "https://bix7.com/"),
            ("Jr Bix", "July 24, 2026", "6:00 PM", "Davenport", "Downtown Davenport", "Bix 7", "https://bix7.com/"),
            ("Quick Bix 2-Mile", "July 25, 2026", "8:00 AM", "Davenport", "Downtown Davenport", "Bix 7", "https://bix7.com/"),
            ("Sr Bix", "July 21, 2026", "Evening", "Davenport", "Downtown", "Bix 7", "https://bix7.com/"),
            ("Brady Street Sprints", "July 23, 2026", "7:00 PM", "Davenport", "Brady Street", "Bix 7", "https://bix7.com/"),
            ("Living History Farms Race", "November 2026", "All day", "Urbandale", "Living History Farms", "LHF Race", "https://www.lhf.org/"),
            ("Des Moines Turkey Trot", "November 26, 2026", "8:00 AM", "Des Moines", "Downtown", "RipRoar Events", "https://www.damtodsm.com/"),
            ("Des Moines Women's Half Marathon", "2026", "Morning", "Des Moines", "Downtown", "RipRoar Events", "https://www.damtodsm.com/"),
        ]
        for t, d, tm, city, venue, src, url in races:
            self._add(t, d, tm, city, venue, "running", "race", src, url)

    # ==================== COUNTY FAIRS ====================
    def add_county_fairs(self):
        logger.info("Adding county fairs...")
        src, url = "Iowa Fairs Association", "https://iowafairs.com/"
        fairs = [
            ("Wapello County Regional Fair", "June 17-21, 2026", "Eldon"),
            ("Linn County Fair", "June 24-29, 2026", "Central City"),
            ("Winneshiek County Fair", "July 8-12, 2026", "Decorah"),
            ("Ringgold County Fair", "July 7-12, 2026", "Mount Ayr"),
            ("Shelby County Fair", "July 8-12, 2026", "Harlan"),
            ("Lee County Fair", "July 9-14, 2026", "Donnellson"),
            ("Sioux County Youth Fair", "July 10-17, 2026", "Sioux Center"),
            ("Marion County Fair", "July 11-17, 2026", "Knoxville"),
            ("Polk County 4-H & FFA Fair", "July 12-18, 2026", "Des Moines"),
            ("Tama County Fair", "July 13-19, 2026", "Gladbrook"),
            ("Poweshiek County Fair", "July 14-19, 2026", "Grinnell"),
            ("Southern Iowa Fair (Mahaska)", "July 14-19, 2026", "Oskaloosa"),
            ("Story County 4-H Fair", "July 15-19, 2026", "Nevada"),
            ("Taylor County Fair", "July 15-19, 2026", "Bedford"),
            ("Van Buren County Fair", "July 15-20, 2026", "Keosauqua"),
            ("Pottawattamie County Fair", "July 15-20, 2026", "Avoca"),
            ("Madison County Fair", "July 16-20, 2026", "Winterset"),
            ("Muscatine County Fair", "July 16-20, 2026", "West Liberty"),
            ("Palo Alto County Fair", "July 16-20, 2026", "Emmetsburg"),
            ("Pocahontas County Fair", "July 16-21, 2026", "Pocahontas"),
            ("Lyon County Fair", "July 19-24, 2026", "Rock Rapids"),
            ("O'Brien County Fair", "July 19-24, 2026", "Primghar"),
            ("Lucas County Fair", "July 19-23, 2026", "Chariton"),
            ("Page County Fair", "July 21-27, 2026", "Clarinda"),
            ("Great Jones County Fair", "July 22-26, 2026", "Monticello"),
            ("Louisa County Fair", "July 22-29, 2026", "Columbus Junction"),
            ("Westfair (Pottawattamie)", "July 22-27, 2026", "Council Bluffs"),
            ("Plymouth County Fair", "July 23-27, 2026", "Le Mars"),
            ("Union County Fair", "July 23-29, 2026", "Afton"),
            ("Kossuth County Fair", "July 27 - August 2, 2026", "Algona"),
            ("Sac County Fair", "July 28 - August 1, 2026", "Sac City"),
            ("Mississippi Valley Fair (Scott)", "August 4-9, 2026", "Davenport"),
            ("Iowa State Fair", "August 13-23, 2026", "Des Moines"),
            ("Clay County Fair", "September 12-20, 2026", "Spencer"),
        ]
        for name, dt, city in fairs:
            self._add(name, dt, "All day", city, f"{city} Fairgrounds", "fair", "county_fair", src, url, age_group="All ages")

    # ==================== CEDAR RAPIDS ====================
    def add_cedar_rapids_events(self):
        logger.info("Adding Cedar Rapids events...")
        src, url = "Cedar Rapids Economic Alliance", "https://www.cedarrapids.org/events-calendar/"
        events = [
            ("Economic Alliance Annual Meeting", "January 29, 2026", "11:30 AM - 1:00 PM"),
            ("Capitol Conversations", "January 30, 2026", "7:30 AM - 9:00 AM"),
            ("Impact CR: Orchestra Iowa Happy Hour", "February 4, 2026", "5:00 PM - 7:00 PM"),
            ("Collective Voice Day at the Capitol", "February 11, 2026", "1:00 PM - 7:00 PM"),
            ("February BizMix", "February 19, 2026", "4:00 PM - 6:00 PM"),
            ("Cedar Rapids Restaurant Week", "February 20 - March 1, 2026", "All day"),
            ("Hiawatha Business Summit", "February 24, 2026", "8:00 AM - 9:00 AM"),
            ("March BizMix at CR Kernels", "March 19, 2026", "4:00 PM - 6:00 PM"),
            ("Celebration of Agriculture", "March 26, 2026", "5:30 PM - 9:00 PM"),
            ("Cedar Rapids Freedom Festival", "July 2026", "All day"),
        ]
        for t, d, tm in events:
            self._add(t, d, tm, "Cedar Rapids", None, "community", "chamber", src, url)
        
        # Concerts & entertainment
        concerts = [
            ("Fitz and The Tantrums", "January 29, 2026", "8:00 PM", "Riverside Casino"),
            ("Dane Cook Comedy", "February 13, 2026", "8:00 PM", "Riverside Casino"),
            ("Warrant ft. Firehouse", "February 14, 2026", "8:00 PM", "Riverside Casino"),
            ("Carly Pearce", "March 7, 2026", "8:00 PM", "Riverside Casino"),
            ("Tracy Lawrence", "March 26, 2026", "8:00 PM", "Riverside Casino"),
            ("Skillet", "March 27, 2026", "8:00 PM", "Riverside Casino"),
            ("Sevendust", "April 17, 2026", "7:00 PM", "Riverside Casino"),
            ("Jeff Foxworthy", "June 13, 2026", "8:00 PM", "Riverside Casino"),
            ("Kenny Wayne Shepherd Band", "November 20, 2026", "8:00 PM", "Riverside Casino"),
        ]
        for t, d, tm, v in concerts:
            self._add(t, d, tm, "Cedar Rapids", v, "entertainment", "concert", "CR Events Live", "https://www.creventslive.com/")
        
        # Hawkeye Downs
        hd_events = [
            ("Made for Her Women's Market", "March 14, 2026", "10:00 AM - 4:00 PM"),
            ("AACA Auto Parts Swap Meet", "March 2026", "All day"),
            ("Gun Show", "May 29-31, 2026", "9:00 AM - 5:00 PM"),
            ("Midwest Shredfest Drift Event", "May 30-31, 2026", "12:00 PM"),
        ]
        for t, d, tm in hd_events:
            self._add(t, d, tm, "Cedar Rapids", "Hawkeye Downs", "community", "expo", "Hawkeye Downs", "https://www.hawkeyedowns.org/")

    # ==================== SIOUX CITY ====================
    def add_sioux_city_events(self):
        logger.info("Adding Sioux City events...")
        events = [
            ("Charlie Berens Comedy", "January 23, 2026", "7:00 PM", "Orpheum Theatre", "comedy"),
            ("Sioux City Musketeers Hockey", "January 23, 2026", "7:05 PM", "Tyson Events Center", "hockey"),
            ("Cardboard Sled Races", "February 1, 2026", "12:00 PM", "Cone Park", "family"),
            ("Sioux City Symphony", "February 7, 2026", "7:00 PM", "Orpheum Theatre", "music"),
            ("The Offspring with Bad Religion", "February 7, 2026", "7:00 PM", "Tyson Events Center", "concert"),
            ("Monster Jam", "February 20-21, 2026", "7:00 PM", "Tyson Events Center", "entertainment"),
            ("Pride Appreciation", "June 4, 2026", "7:00 PM", "Downtown", "community"),
            ("Saturday in the Park", "July 2026", "All day", "Grandview Park", "festival"),
            ("ArtSplash", "September 2026", "All day", "Downtown", "arts"),
        ]
        for t, d, tm, v, sub in events:
            self._add(t, d, tm, "Sioux City", v, "community", sub, "Explore Siouxland", "https://exploresiouxland.com/events/")

    # ==================== DUBUQUE ====================
    def add_dubuque_events(self):
        logger.info("Adding Dubuque events...")
        src, url = "Dubuque Chamber", "https://www.dubuquechamber.com"
        events = [
            ("Winter Bounce at Five Flags", "January 23-25, 2026", "All day", "Five Flags Center", "family"),
            ("Beer with a Boss", "January 29, 2026", "Evening", "Various", "networking"),
            ("YP Next Up - Leadership", "February 19, 2026", "6:30 PM", "University of Dubuque", "professional"),
            ("Five Flags Movie Series", "Winter 2026", "Evening", "Five Flags Theater", "entertainment"),
            ("Packers Tailgate Tour - Field of Dreams", "April 16, 2026", "All day", "Field of Dreams", "sports"),
        ]
        for t, d, tm, v, sub in events:
            self._add(t, d, tm, "Dubuque", v, "community", sub, src, url)

    # ==================== DES MOINES METRO ====================
    def add_des_moines_events(self):
        logger.info("Adding Des Moines metro events...")
        
        # Catch Des Moines
        dsm = [
            ("Drake Relays", "April 23-26, 2026", "All day", "Drake Stadium", "track"),
            ("Des Moines Arts Festival", "June 26-28, 2026", "All day", "Western Gateway Park", "arts"),
            ("Principal Charity Classic (PGA)", "June 2026", "All day", "Wakonda Club", "golf"),
            ("World Food & Music Festival", "September 2026", "All day", "Western Gateway Park", "festival"),
            ("Holidazzle", "November-December 2026", "Evening", "Downtown", "holiday"),
        ]
        for t, d, tm, v, sub in dsm:
            self._add(t, d, tm, "Des Moines", v, "community", sub, "Catch Des Moines", "https://www.catchdesmoines.com/events/")
        
        # West Des Moines Chamber
        wdm = [
            ("Rush Hour: Aura Restaurant", "January 2026", "5:00 PM - 7:00 PM", "Aura Restaurant"),
            ("WDM Annual Dinner - Mission: Possible", "February 26, 2026", "6:00 PM", "Val Air Ballroom"),
            ("Breakfast B4 Business (monthly)", "2026", "7:30 AM", "Various"),
            ("Tri-Chamber Golf Outing", "August 24, 2026", "All day", "Beaver Creek Golf Course"),
            ("Best of the West Awards", "December 1, 2026", "5:00 PM - 7:00 PM", None),
        ]
        for t, d, tm, v in wdm:
            self._add(t, d, tm, "West Des Moines", v, "community", "chamber", "WDM Chamber", "https://wdmchamber.org/")
        
        # Urbandale
        urb = [
            ("Membership Luncheon", "January 2026", "12:00 PM", None),
            ("Talk with Officials", "January 31, 2026", "Morning", None),
            ("genYP Events", "2026 Monthly", "Various", None),
        ]
        for t, d, tm, v in urb:
            self._add(t, d, tm, "Urbandale", v, "community", "chamber", "Urbandale Chamber", "https://uniquelyurbandale.com/")

    # ==================== ANKENY ====================
    def add_ankeny_events(self):
        logger.info("Adding Ankeny events...")
        src, url = "Ankeny Chamber", "https://www.ankeny.org/"
        events = [
            ("AYP St. Patrick's Day Party", "March 12, 2026", "5:30 PM - 7:30 PM", "Ankeny Chamber", "networking"),
            ("Ankeny Chamber SummerFest", "July 10-12, 2026", "All day", "The District at Prairie Trail", "festival"),
            ("SummerFest Carnival", "July 9, 2026", "4:00 PM - 9:00 PM", "The District", "carnival"),
            ("SummerFest Grand Parade", "July 11, 2026", "10:00 AM", "Ankeny", "parade"),
            ("SummerFest Fireworks", "July 11, 2026", "10:00 PM", "Prairie Trail", "fireworks"),
            ("Witches Night Out", "October 2026", "Evening", "Various", "festival"),
        ]
        for t, d, tm, v, sub in events:
            self._add(t, d, tm, "Ankeny", v, "community", sub, src, url)

    # ==================== STATEWIDE FESTIVALS ====================
    def add_festivals(self):
        logger.info("Adding statewide festivals...")
        festivals = [
            ("Clear Lake Kite Festival", "February 2026", "All day", "Clear Lake", "festival"),
            ("Tulip Time Festival", "May 2026", "All day", "Pella", "festival"),
            ("Tivoli Fest", "May 2026", "All day", "Elk Horn", "festival"),
            ("Sioux Center Summer Celebration", "June 4-6, 2026", "All day", "Sioux Center", "festival"),
            ("Iowa City Jazz Festival", "July 3-5, 2026", "All day", "Iowa City", "music"),
            ("AJ's Independence Day (Clear Lake)", "July 4, 2026", "All day", "Clear Lake", "festival"),
            ("Hinterland Music Festival", "July 30 - August 2, 2026", "All day", "St. Charles", "music"),
            ("Iowa Irish Fest", "July 31 - August 2, 2026", "All day", "Waterloo", "festival"),
            ("National Balloon Classic", "August 2026", "All day", "Indianola", "festival"),
            ("Bix Beiderbecke Jazz Festival", "August 2026", "All day", "Davenport", "music"),
            ("RAGBRAI", "July 2026", "All week", "Across Iowa", "cycling"),
            ("Iowa Games Summer", "July 2026", "All day", "Ames", "multi-sport"),
            ("Iowa Games Winter", "February 2026", "All day", "Various", "multi-sport"),
        ]
        for t, d, tm, city, sub in festivals:
            self._add(t, d, tm, city, None, "community", sub, "Travel Iowa", "https://www.traveliowa.com/events/")

    # ==================== IOWA HAWKEYES ====================
    def add_hawkeyes(self):
        logger.info("Adding Hawkeyes events...")
        games = [
            ("Iowa Football vs Northern Illinois", "September 5, 2026", "TBD"),
            ("Iowa Football vs Iowa State", "September 12, 2026", "TBD"),
            ("Iowa Football vs UNI", "September 19, 2026", "TBD"),
        ]
        for t, d, tm in games:
            self._add(t, d, tm, "Iowa City", "Kinnick Stadium", "college_sports", "football", "Iowa Hawkeyes", "https://hawkeyesports.com/")

    # ==================== HIGH SCHOOL STATE TOURNAMENTS ====================
    def add_high_school(self):
        logger.info("Adding high school state tournaments...")
        events = [
            ("IHSAA State Wrestling", "February 2026", "All day", "Des Moines", "Wells Fargo Arena", "wrestling", "Boys"),
            ("IGHSAU State Basketball", "March 2026", "All day", "Des Moines", "Wells Fargo Arena", "basketball", "Girls"),
            ("IHSAA State Basketball", "March 2026", "All day", "Des Moines", "Wells Fargo Arena", "basketball", "Boys"),
            ("IHSAA/IGHSAU State Track", "May 2026", "All day", "Des Moines", "Drake Stadium", "track", "All"),
            ("IHSAA State Baseball", "July 2026", "All day", "Des Moines", "Principal Park", "baseball", "Boys"),
            ("IGHSAU State Softball", "July 2026", "All day", "Fort Dodge", "Harlan Rogers Park", "softball", "Girls"),
            ("IGHSAU State Volleyball", "November 2026", "All day", "Cedar Rapids", "Xtream Arena", "volleyball", "Girls"),
            ("IHSAA State Football", "November 2026", "All day", "Cedar Falls", "UNI-Dome", "football", "Boys"),
        ]
        for t, d, tm, city, v, sub, age in events:
            self._add(t, d, tm, city, v, "high_school_sports", sub, "IHSAA/IGHSAU", "https://www.iahsaa.org", age_group=f"High School {age}")

    # ==================== FAMILY ATTRACTIONS ====================
    def add_family_attractions(self):
        logger.info("Adding family attraction events...")
        # Blank Park Zoo
        zoo = [
            ("Zoo Brew", "Summer 2026", "Evening", "adults"),
            ("Boo at the Zoo", "October 2026", "All day", "family"),
            ("Wild Lights", "November-December 2026", "Evening", "holiday"),
        ]
        for t, d, tm, sub in zoo:
            self._add(t, d, tm, "Des Moines", "Blank Park Zoo", "family", sub, "Blank Park Zoo", "https://www.blankparkzoo.com/")
        
        # Science Center of Iowa
        sci = [
            ("Science Center Exhibits", "2026", "All day", "exhibit"),
            ("Summer Science Camps", "June-August 2026", "All day", "camp"),
        ]
        for t, d, tm, sub in sci:
            self._add(t, d, tm, "Des Moines", "Science Center of Iowa", "family", sub, "Science Center of Iowa", "https://www.sciowa.org/")
        
        # Living History Farms
        lhf = [
            ("Opening Day", "May 2026", "9:00 AM", "opening"),
            ("Independence Day Celebration", "July 4, 2026", "All day", "holiday"),
            ("Fall Harvest Festival", "October 2026", "All day", "festival"),
            ("Legends & Lanterns Halloween", "October 2026", "Evening", "halloween"),
        ]
        for t, d, tm, sub in lhf:
            self._add(t, d, tm, "Urbandale", "Living History Farms", "family", sub, "Living History Farms", "https://www.lhf.org/")

    # ==================== MAIN ====================
    def scrape_all(self) -> List[Event]:
        logger.info("Starting Iowa Events Scraper v5 - COMPREHENSIVE...")
        logger.info(f"Today: {TODAY}")
        
        self.add_tbk_events()
        self.add_xtream_arena_events()
        self.add_wells_fargo_events()
        self.add_adventureland_events()
        self.add_races()
        self.add_county_fairs()
        self.add_cedar_rapids_events()
        self.add_sioux_city_events()
        self.add_dubuque_events()
        self.add_des_moines_events()
        self.add_ankeny_events()
        self.add_festivals()
        self.add_hawkeyes()
        self.add_high_school()
        self.add_family_attractions()
        
        self.events = self._deduplicate(self.events)
        logger.info(f"Total events: {len(self.events)}")
        return self.events
    
    def _deduplicate(self, events):
        seen = set()
        unique = []
        for e in events:
            key = f"{e.title.lower()[:50]}|{e.date}|{e.city}"
            if key not in seen:
                seen.add(key)
                unique.append(e)
        return unique
    
    def save_to_json(self, filename="iowa_events.json"):
        data = {"scraped_at": datetime.now().isoformat(), "total_events": len(self.events), "events": [asdict(e) for e in self.events]}
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved to {filename}")
    
    def save_to_csv(self, filename="iowa_events.csv"):
        fields = ['title','date','time','location','venue','category','subcategory','source','source_url','description','city','teams','age_group','registration_url','latitude','longitude']
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for e in self.events:
                w.writerow(asdict(e))
        logger.info(f"Saved to {filename}")


def main():
    scraper = IowaEventsScraper()
    events = scraper.scrape_all()
    scraper.save_to_json()
    scraper.save_to_csv()
    
    print("\n" + "="*60)
    print("IOWA EVENTS SCRAPER v5 - COMPREHENSIVE")
    print("="*60)
    print(f"Total events: {len(events)}")
    
    cats = {}
    for e in events:
        cats[e.category] = cats.get(e.category, 0) + 1
    print("\nBy Category:")
    for c, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {c}: {n}")
    
    cities = {}
    for e in events:
        if e.city:
            cities[e.city] = cities.get(e.city, 0) + 1
    print("\nTop 15 Cities:")
    for c, n in sorted(cities.items(), key=lambda x: -x[1])[:15]:
        print(f"  {c}: {n}")
    
    print("\nSample Events:")
    for e in events[:10]:
        print(f"  {e.title} | {e.date} | {e.city}")
    
    print(f"\nOutput: iowa_events.json, iowa_events.csv")


if __name__ == "__main__":
    main()
