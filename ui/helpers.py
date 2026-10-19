"""Helper utilities for city images, currency, labels, and sector tags."""
import html
import base64
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import quote
import pandas as pd

from data.city_image_links import CITY_IMAGE_LINKS

# Professional urban skyline and cityscape photos (no religious or sacred sites)
CITY_IMAGES = {
    "bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600&auto=format&fit=crop&q=80",
    "pune": "https://images.unsplash.com/photo-1600100397608-f010f4439c28?w=600&auto=format&fit=crop&q=80",
    "ahmedabad": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "coimbatore": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "hyderabad": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
    "delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80",
    "mumbai": "https://images.unsplash.com/photo-1529253355930-ddbe423a2ac7?w=600&auto=format&fit=crop&q=80",
    "chennai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "kolkata": "https://images.unsplash.com/photo-1558431382-27e303142255?w=600&auto=format&fit=crop&q=80",
    "jaipur": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&auto=format&fit=crop&q=80",
    "chandigarh": "https://images.unsplash.com/photo-1590496793929-36417d3117de?w=600&auto=format&fit=crop&q=80",
    "ludhiana": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600&auto=format&fit=crop&q=80",
    "nagpur": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=600&auto=format&fit=crop&q=80",
    "surat": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "indore": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=600&auto=format&fit=crop&q=80",
    "kochi": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?w=600&auto=format&fit=crop&q=80",
    "amritsar": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "jodhpur": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600&auto=format&fit=crop&q=80",
    "warangal": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
    "varanasi": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=600&auto=format&fit=crop&q=80",
    "gurugram": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80",
    "noida": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80",
    "faridabad": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600&auto=format&fit=crop&q=80",
    "ghaziabad": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600&auto=format&fit=crop&q=80",
    "lucknow": "https://images.unsplash.com/photo-1600100397608-f010f4439c28?w=600&auto=format&fit=crop&q=80",
    "kanpur": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "agra": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=600&auto=format&fit=crop&q=80",
    "vadodara": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "nashik": "https://images.unsplash.com/photo-1600100397608-f010f4439c28?w=600&auto=format&fit=crop&q=80",
    "nasik": "https://images.unsplash.com/photo-1600100397608-f010f4439c28?w=600&auto=format&fit=crop&q=80",
    "bhopal": "https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?w=600&auto=format&fit=crop&q=80",
    "howrah": "https://images.unsplash.com/photo-1558431382-27e303142255?w=600&auto=format&fit=crop&q=80",
    "durgapur": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "siliguri": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "mysuru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600&auto=format&fit=crop&q=80",
    "madurai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "thiruvananthapuram": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "patna": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "ranchi": "https://images.unsplash.com/photo-1600100397608-f010f4439c28?w=600&auto=format&fit=crop&q=80",
    "jamshedpur": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "bhubaneswar": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "cuttack": "https://images.unsplash.com/photo-1588416936097-41850ab3d86d?w=600&auto=format&fit=crop&q=80",
    "visakhapatnam": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600&auto=format&fit=crop&q=80",
    "vijayawada": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
    "vijayvada": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
    "jalandhar": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=600&auto=format&fit=crop&q=80",
    "mohali": "https://images.unsplash.com/photo-1590496793929-36417d3117de?w=600&auto=format&fit=crop&q=80",
    "hydrabad": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
    "chandigrh": "https://images.unsplash.com/photo-1590496793929-36417d3117de?w=600&auto=format&fit=crop&q=80",
    "wranchal": "https://images.unsplash.com/photo-1605007493699-ce65834f8a00?w=600&auto=format&fit=crop&q=80",
}

# Landmark-focused sources for the most frequently explored destinations.
CITY_IMAGES.update({
    "delhi": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=1200&auto=format&fit=crop&q=85",
    "mumbai": "https://images.unsplash.com/photo-1570168007204-dfb528c6958f?w=1200&auto=format&fit=crop&q=85",
    "bengaluru": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=1200&auto=format&fit=crop&q=85",
    "hyderabad": "https://images.unsplash.com/photo-1572449043416-55f4685c9bb7?w=1200&auto=format&fit=crop&q=85",
    "kolkata": "https://images.unsplash.com/photo-1558431382-27e303142255?w=1200&auto=format&fit=crop&q=85",
    "jaipur": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=1200&auto=format&fit=crop&q=85",
    "agra": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=1200&auto=format&fit=crop&q=85",
    "chennai": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=1200&auto=format&fit=crop&q=85",
})

_CITY_IMAGE_DATA_CACHE = {}

# Deterministic city-specific landmark searches provide a distinct image for
# every dataset city while keeping the mapping easy to maintain.
CITY_LANDMARKS = {
    "ludhiana": "Punjab Agricultural University Museum Ludhiana",
    "chandigarh": "Rock Garden Chandigarh",
    "amritsar": "Golden Temple Amritsar",
    "jalandhar": "Devi Talab Mandir Jalandhar",
    "mohali": "PCA Cricket Stadium Mohali",
    "delhi": "India Gate Delhi",
    "gurugram": "Kingdom of Dreams Gurugram",
    "faridabad": "Surajkund Lake Faridabad",
    "noida": "Worlds of Wonder Noida",
    "ghaziabad": "City Forest Ghaziabad",
    "lucknow": "Bara Imambara Lucknow",
    "kanpur": "JK Temple Kanpur",
    "agra": "Taj Mahal Agra",
    "varanasi": "Kashi Vishwanath Temple Varanasi",
    "jaipur": "Hawa Mahal Jaipur",
    "jodhpur": "Mehrangarh Fort Jodhpur",
    "ahmedabad": "Sabarmati Ashram Ahmedabad",
    "surat": "Dumas Beach Surat",
    "vadodara": "Laxmi Vilas Palace Vadodara",
    "mumbai": "Gateway of India Mumbai",
    "pune": "Shaniwar Wada Pune",
    "nagpur": "Deekshabhoomi Nagpur",
    "nashik": "Trimbakeshwar Temple Nashik",
    "indore": "Rajwada Palace Indore",
    "bhopal": "Upper Lake Bhopal",
    "kolkata": "Victoria Memorial Kolkata",
    "howrah": "Howrah Bridge Kolkata",
    "durgapur": "Durgapur Barrage",
    "siliguri": "Mahananda Wildlife Sanctuary Siliguri",
    "bengaluru": "Vidhana Soudha Bengaluru",
    "mysuru": "Mysore Palace Mysuru",
    "hyderabad": "Charminar Hyderabad",
    "warangal": "Thousand Pillar Temple Warangal",
    "chennai": "Marina Beach Chennai",
    "coimbatore": "Isha Yoga Center Coimbatore",
    "madurai": "Meenakshi Amman Temple Madurai",
    "kochi": "Fort Kochi",
    "thiruvananthapuram": "Padmanabhaswamy Temple Thiruvananthapuram",
    "patna": "Takht Sri Patna Sahib",
    "ranchi": "Hundru Falls Ranchi",
    "jamshedpur": "Jubilee Park Jamshedpur",
    "bhubaneswar": "Lingaraj Temple Bhubaneswar",
    "cuttack": "Barabati Fort Cuttack",
    "visakhapatnam": "RK Beach Visakhapatnam",
    "vijayawada": "Kanaka Durga Temple Vijayawada",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600&auto=format&fit=crop&q=80"


def _city_fallback_image(city: str) -> str:
    """Return a reliable illustrated fallback when a remote city photo is unavailable."""
    label = html.escape(str(city).strip() or "India")
    initials = html.escape("".join(word[0] for word in str(city).split()[:2]).upper() or "IN")
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600">
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
        <stop offset="0" stop-color="#063b35"/><stop offset="1" stop-color="#0d7a5f"/>
      </linearGradient></defs>
      <rect width="1200" height="600" fill="url(#g)"/>
      <path d="M0 510h120v-150h90v150h80V270h100v240h90V320h110v190h90V210h120v300h100V285h90v225h100V350h100v160h100v90H0z" fill="#062c2a" opacity=".8"/>
      <text x="70" y="110" fill="#d1fae5" font-family="Arial,sans-serif" font-size="52" font-weight="700">{label}</text>
      <text x="74" y="165" fill="#a7f3d0" font-family="Arial,sans-serif" font-size="26">MigrationMatch city profile</text>
      <text x="1030" y="505" fill="#ffffff" font-family="Arial,sans-serif" font-size="88" font-weight="700" text-anchor="middle">{initials}</text>
    </svg>
    """
    return f"data:image/svg+xml;charset=utf-8,{quote(svg)}"


def _landmark_image(city: str, landmark: str) -> str:
    """Create a guaranteed-visible landmark cover without relying on remote hosts."""
    safe_city = html.escape(city)
    safe_landmark = html.escape(landmark)
    initials = html.escape(
        "".join(word[0] for word in landmark.split()[:2]).upper() or "IN"
    )
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600">
      <defs>
        <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#063b35"/>
          <stop offset="1" stop-color="#159a78"/>
        </linearGradient>
        <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stop-color="#0b5b4b"/>
          <stop offset="1" stop-color="#062c2a"/>
        </linearGradient>
      </defs>
      <rect width="1200" height="600" fill="url(#sky)"/>
      <circle cx="970" cy="120" r="78" fill="#a7f3d0" opacity=".18"/>
      <path d="M0 455 Q180 380 360 455 T720 445 T1200 430 V600 H0Z" fill="url(#ground)"/>
      <g fill="#032e2b" opacity=".92">
        <rect x="110" y="350" width="75" height="160" rx="5"/>
        <rect x="205" y="295" width="95" height="215" rx="5"/>
        <rect x="325" y="375" width="80" height="135" rx="5"/>
        <rect x="430" y="265" width="130" height="245" rx="5"/>
        <rect x="585" y="345" width="95" height="165" rx="5"/>
        <rect x="705" y="300" width="115" height="210" rx="5"/>
        <rect x="845" y="370" width="80" height="140" rx="5"/>
      </g>
      <g fill="#a7f3d0" opacity=".55">
        <rect x="225" y="325" width="10" height="10"/><rect x="255" y="325" width="10" height="10"/>
        <rect x="465" y="300" width="12" height="12"/><rect x="510" y="300" width="12" height="12"/>
        <rect x="740" y="330" width="11" height="11"/><rect x="780" y="330" width="11" height="11"/>
      </g>
      <text x="70" y="95" fill="#d1fae5" font-family="Arial,sans-serif" font-size="28" font-weight="700"
        letter-spacing="4">MIGRATIONMATCH • CITY EXPLORER</text>
      <text x="70" y="175" fill="#ffffff" font-family="Arial,sans-serif" font-size="56" font-weight="800">{safe_landmark}</text>
      <text x="72" y="220" fill="#d1fae5" font-family="Arial,sans-serif" font-size="30">{safe_city}, India</text>
      <circle cx="1080" cy="475" r="66" fill="#10b981"/>
      <text x="1080" y="500" text-anchor="middle" fill="#ffffff" font-family="Arial,sans-serif"
        font-size="50" font-weight="800">{initials}</text>
    </svg>
    """
    return f"data:image/svg+xml;charset=utf-8,{quote(svg)}"

CITY_SECTORS = {
    "ahmedabad": ["Textiles", "Pharmaceuticals", "Automotive"],
    "coimbatore": ["Textiles", "Manufacturing", "IT Services"],
    "pune": ["IT & Tech", "Automotive", "Education"],
    "bengaluru": ["IT & Software", "Aerospace", "Electronics"],
    "hyderabad": ["Pharmaceuticals", "IT & Tech", "Biotechnology"],
    "chennai": ["Automobile", "Hardware", "Healthcare"],
    "mumbai": ["Financial Services", "Logistics", "Media"],
    "delhi": ["Commerce", "Services", "Manufacturing"],
    "ludhiana": ["Textiles", "Light Engineering", "Hosiery"],
    "chandigarh": ["IT Services", "Hospitality", "Education"],
    "varanasi": ["Handicrafts", "Textile Weaving", "Tourism"],
    "surat": ["Diamond Processing", "Textiles", "Petrochemicals"],
    "nagpur": ["Logistics Hub", "Mining", "Food Processing"],
    "indore": ["Food Processing", "Pharma", "Textiles"],
    "kolkata": ["Engineering", "Logistics", "Leather"],
    "jaipur": ["Gems & Jewelry", "Tourism", "Handicrafts"],
    "kochi": ["Marine Logistics", "Shipbuilding", "Tourism"],
    "amritsar": ["Trade & Logistics", "Food Processing", "Textiles"],
    "jodhpur": ["Handicrafts", "Mineral Processing", "Tourism"],
    "warangal": ["Textiles", "Agriculture Tech", "Education"],
    "gurugram": ["Corporate Services", "Tech Startups", "Automotive"],
    "noida": ["IT Infrastructure", "Electronics", "Media"],
    "vadodara": ["Chemicals", "Heavy Engineering", "Pharma"],
    "visakhapatnam": ["Port Logistics", "Steel & Metals", "Pharma"],
    "bhopal": ["Heavy Electricals", "Automobile", "Textiles"],
    "lucknow": ["Aerospace", "Handicrafts", "IT Hub"],
    "kanpur": ["Leather Industry", "Chemicals", "Defense"],
    "agra": ["Leather Goods", "Handicrafts", "Automotive"],
    "nashik": ["Automotive", "Pharma", "Agriculture Tech"],
    "ranchi": ["Mining & Metals", "Engineering", "Forestry"],
    "jamshedpur": ["Steel Manufacturing", "Automotive", "Heavy Machinery"],
    "bhubaneswar": ["IT & Electronics", "Metals", "Tourism"],
    "cuttack": ["Textiles", "Silver Filigree", "Logistics"],
    "vijayawada": ["Automobile Ancillaries", "Agriculture Trade", "Textiles"],
    "jalandhar": ["Sports Goods", "Leather", "Hand Tools"],
    "mohali": ["IT Hub", "Biotechnology", "R&D"],
}


def get_city_image(city: str) -> str:
    if not city:
        return _city_fallback_image("India")
    cleaned = re.sub(r"[^a-z0-9]", "", str(city).strip().lower())
    custom_link = CITY_IMAGE_LINKS.get(cleaned, "").strip()
    if custom_link:
        return custom_link
    normalized_images = {
        re.sub(r"[^a-z0-9]", "", key): value for key, value in CITY_IMAGES.items()
    }
    landmark = CITY_LANDMARKS.get(cleaned)
    if landmark:
        return _landmark_image(str(city).strip(), landmark)
    if cleaned in normalized_images:
        return normalized_images[cleaned]
    landmark = f"{city} India landmark"
    return _landmark_image(str(city).strip(), landmark)


def get_city_image_data_uri(city: str) -> str:
    """Return a browser-safe image URI, embedding remote photos server-side."""
    image_url = get_city_image(city)
    if image_url.startswith("data:"):
        return image_url
    if image_url in _CITY_IMAGE_DATA_CACHE:
        return _CITY_IMAGE_DATA_CACHE[image_url]

    try:
        request = Request(image_url, headers={"User-Agent": "MigrationMatch/1.0"})
        with urlopen(request, timeout=12) as response:
            content_type = response.headers.get_content_type()
            image_bytes = response.read(3 * 1024 * 1024)
        if not content_type.startswith("image/"):
            raise ValueError(f"Expected an image response, got {content_type}")
        data_uri = f"data:{content_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"
    except (HTTPError, URLError, TimeoutError, ValueError):
        # Keep a real custom photo URL as the final fallback; do not replace it
        # with generated artwork when a photo host rate-limits the app server.
        cleaned = re.sub(r"[^a-z0-9]", "", str(city).strip().lower())
        data_uri = image_url if CITY_IMAGE_LINKS.get(cleaned, "").strip() else _landmark_image(
            str(city).strip(),
            CITY_LANDMARKS.get(cleaned, f"{city} India landmark"),
        )
    _CITY_IMAGE_DATA_CACHE[image_url] = data_uri
    return data_uri
def get_city_sectors(city: str) -> list:
    if not city:
        return ["Manufacturing", "Services", "Trade"]
    cleaned = str(city).strip().lower()
    return CITY_SECTORS.get(cleaned, ["Manufacturing", "Services", "Trade"])


def format_inr(value: float) -> str:
    if pd.isna(value):
        return "₹0"
    return f"₹{int(value):,}"


def job_demand_label(score: float) -> str:
    if score >= 70:
        return "High"
    elif score >= 50:
        return "Medium"
    return "Low"


def cost_of_living_label(expense: float) -> str:
    if expense > 8500:
        return "High"
    elif expense >= 5500:
        return "Moderate"
    return "Low"


def why_recommended(row: pd.Series) -> str:
    if "Why_Recommended" in row and pd.notna(row["Why_Recommended"]):
        return str(row["Why_Recommended"])
    return "High employment availability and balanced living expenses."
