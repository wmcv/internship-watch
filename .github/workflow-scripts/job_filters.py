"""Shared title / location filters for both watchers.

The target profile is a US-based general software engineering internship:
generic SWE, full-stack, frontend, backend, infrastructure/platform, and
product *engineering*. Product management, data science/ML, hardware, QA,
security, and non-engineering roles are out.

parse_boards.py uses only the location half (the Simplify board already
scopes rows to its Software Engineering section); ats_watcher.py uses both
halves, since an ATS board is one undifferentiated list of every open req.
"""

import json
import re
from pathlib import Path

CONFIG_PATH = Path(__file__).with_name("watcher_config.json")
DEFAULT_CONFIG = {
    "target_countries": ["US"],
    "keep_ambiguous_locations": True,
    "additional_role_patterns": [],
    "additional_exclude_patterns": [],
}


def load_config() -> dict:
    config = DEFAULT_CONFIG.copy()
    if CONFIG_PATH.exists():
        config.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
    config["target_countries"] = {
        str(country).upper() for country in config["target_countries"]
    }
    return config


CONFIG = load_config()


def optional_regex(patterns: list):
    return re.compile("|".join(f"(?:{p})" for p in patterns), re.I) if patterns else None


EXTRA_ROLE_RE = optional_regex(CONFIG["additional_role_patterns"])
EXTRA_EXCLUDE_RE = optional_regex(CONFIG["additional_exclude_patterns"])

INTERN_RE = re.compile(r"\bintern(ship)?\b|\bco[- ]?op\b", re.I)

# Titles that count as in-profile. Generic "Software Engineer Intern" is the
# common case — big companies rarely label the specialization — and EXCLUDE_RE
# below strips the ones that declare an out-of-profile focus.
ROLE_RE = re.compile(
    r"software (engineer|engineering|developer|development)|\bswe\b|"
    r"back[- ]?end|front[- ]?end|full[- ]?stack|"
    r"web (developer|development|engineer)|"
    r"product (engineer|engineering)|application(s)? (engineer|developer)|"
    r"\bdeveloper\b|server|infrastructure|\binfra\b|platform|dev[- ]?ops|"
    r"site reliability|\bsre\b|cloud|distributed",
    re.I,
)

EXCLUDE_RE = re.compile(
    r"mobile|\bios\b|android|"
    r"data scien|data analy|data engineer|analytics|business|"
    r"hardware|electrical|mechanical|manufactur|embedded|firmware|silicon|"
    r"\basic\b|fpga|\brf\b|optic|quality|\bqa\b|\btest\b|security|"
    r"research (scientist|engineer)|designer\b|\bux\b|user experience|"
    r"graphics|\bgame\b|quantitative|\bquant\b|"
    r"product manag|program manag|project manag|technical program|"
    r"marketing|sales|solutions|support|success|recruit|people|legal|"
    r"finance|accounting|supply chain|"
    r"advocate|evangelis|developer relations",
    re.I,
)

# AI/ML terms only disqualify when the title isn't clearly a software
# engineering role — "Software Engineer Intern, AI Platform" is in profile,
# "Machine Learning Intern" is not.
AI_EXCLUDE_RE = re.compile(
    r"machine learning|\bml\b|\bai\b|artificial intelligence|deep learning",
    re.I,
)

SWE_RE = re.compile(
    r"software (engineer|engineering|developer|development)|\bswe\b|"
    r"back[- ]?end|front[- ]?end|full[- ]?stack|product engineer|"
    r"infrastructure|\binfra\b|platform|dev[- ]?ops|site reliability|\bsre\b",
    re.I,
)

US_HINT_RE = re.compile(
    r"united states|\busa?\b|u\.s\.|remote.*(us|america)|"
    r"alabama|alaska|arizona|arkansas|california|colorado|connecticut|"
    r"delaware|florida|georgia|hawaii|idaho|illinois|indiana|iowa|kansas|"
    r"kentucky|louisiana|maine|maryland|massachusetts|michigan|minnesota|"
    r"mississippi|missouri|montana|nebraska|nevada|new hampshire|"
    r"new jersey|new mexico|new york|north carolina|north dakota|ohio|"
    r"oklahoma|oregon|pennsylvania|rhode island|south carolina|"
    r"south dakota|tennessee|texas|utah|vermont|virginia|washington|"
    r"west virginia|wisconsin|wyoming|"
    r"san francisco|\bnyc\b|seattle|austin|boston|chicago|denver|atlanta|"
    r"los angeles|mountain view|palo alto|sunnyvale|san jose|menlo park|"
    r"bellevue|redmond|\bd\.?c\.?\b|miami|dallas|houston|philadelphia|"
    r"pittsburgh|portland|san diego|santa clara|cupertino|irvine|"
    r"nashville|charlotte|phoenix|salt lake|"
    r",\s?(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|"
    r"MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|"
    r"TN|TX|UT|VT|VA|WA|WV|WI|WY)\b",
    re.I,
)

NON_US_RE = re.compile(
    r"canada|ontario|toronto|vancouver|montr[eé]al|quebec|calgary|ottawa|"
    r"waterloo|british columbia|united kingdom|\buk\b|london|ireland|"
    r"dublin|germany|berlin|munich|france|paris|netherlands|amsterdam|"
    r"belgium|spain|madrid|barcelona|portugal|lisbon|italy|milan|"
    r"switzerland|zurich|geneva|austria|vienna|poland|warsaw|krakow|"
    r"czech|prague|sweden|stockholm|norway|oslo|denmark|copenhagen|"
    r"finland|helsinki|estonia|tallinn|romania|bucharest|hungary|"
    r"budapest|israel|tel aviv|\buae\b|dubai|abu dhabi|saudi|riyadh|"
    r"india|bangalore|bengaluru|hyderabad|mumbai|delhi|gurgaon|gurugram|"
    r"chennai|pune|noida|singapore|malaysia|kuala lumpur|indonesia|"
    r"jakarta|vietnam|thailand|bangkok|philippines|manila|china|beijing|"
    r"shanghai|shenzhen|hangzhou|hong kong|taiwan|taipei|japan|tokyo|"
    r"osaka|korea|seoul|australia|sydney|melbourne|brisbane|new zealand|"
    r"auckland|brazil|paulo|mexico|guadalajara|argentina|buenos aires|"
    r"colombia|bogot|chile|santiago|nigeria|lagos|egypt|cairo|kenya|"
    r"nairobi|south africa|turkey|istanbul|ukraine|kyiv|serbia|belgrade|"
    r"bulgaria|sofia|croatia|zagreb|lithuania|vilnius|latvia|riga|"
    r"armenia|yerevan|cyprus|malta|luxembourg|emea|apac|latam|"
    r",\s?(?-i:ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT)\b",
    re.I,
)

CANADA_RE = re.compile(
    r"canada|ontario|toronto|vancouver|montr[eé]al|quebec|calgary|ottawa|"
    r"waterloo|british columbia|halifax|nova scotia|new brunswick|manitoba|"
    r"saskatchewan|newfoundland|prince edward island|"
    r",\s?(?-i:ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b",
    re.I,
)


def wanted_title(title: str) -> bool:
    """True for an in-profile internship title on a raw ATS board."""
    role_match = ROLE_RE.search(title) or (EXTRA_ROLE_RE and EXTRA_ROLE_RE.search(title))
    if not (INTERN_RE.search(title) and role_match):
        return False
    if EXCLUDE_RE.search(title) or (EXTRA_EXCLUDE_RE and EXTRA_EXCLUDE_RE.search(title)):
        return False
    if AI_EXCLUDE_RE.search(title) and not SWE_RE.search(title):
        return False
    return True


def wanted_location(location: str) -> bool:
    """Return true when a location matches a configured target country."""
    if not location:
        return bool(CONFIG["keep_ambiguous_locations"])
    if "US" in CONFIG["target_countries"] and US_HINT_RE.search(location):
        return True
    if "CA" in CONFIG["target_countries"] and CANADA_RE.search(location):
        return True
    if NON_US_RE.search(location):
        return False
    return bool(CONFIG["keep_ambiguous_locations"])


def is_us(location: str) -> bool:
    """Backward-compatible alias for older callers."""
    return wanted_location(location)
