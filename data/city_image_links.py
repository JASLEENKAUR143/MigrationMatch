"""Real landmark photo links for MigrationMatch.

The default links point to real photographs hosted on Wikimedia Commons.
Replace any value with another direct image URL if you prefer a different
photograph. If a link is blank, MigrationMatch uses its built-in fallback.
"""

CITY_IMAGE_LINKS = {
    "ludhiana": "https://upload.wikimedia.org/wikipedia/commons/a/af/Pau_museum.jpg",  # Punjab Agricultural University Museum
    "chandigarh": "https://commons.wikimedia.org/wiki/Special:FilePath/Rock%20Garden%20Chandigarh.jpg?width=900",  # Rock Garden
    "amritsar": "https://commons.wikimedia.org/wiki/Special:FilePath/Golden%20Temple%20Amritsar.jpg?width=900",  # Golden Temple
    "jalandhar": "https://commons.wikimedia.org/wiki/Special:FilePath/Devi%20Talab%20Mandir.jpg?width=900",  # Devi Talab Mandir
    "mohali": "https://upload.wikimedia.org/wikipedia/commons/c/cc/PCA_Stadium_Mohali_wide.jpg",  # Cricket Stadium (PCA)
    "delhi": "https://commons.wikimedia.org/wiki/Special:FilePath/India%20Gate%20in%20New%20Delhi.jpg?width=900",  # India Gate
    "gurugram": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Kingdom_of_Dreams%2C_Gurgaon_2.jpg",  # Kingdom of Dreams
    "faridabad": "https://upload.wikimedia.org/wikipedia/commons/8/85/Most_Beautiful_Lake_in_Faridabad.jpg",  # Surajkund Lake
    "noida": "https://upload.wikimedia.org/wikipedia/commons/d/da/Worlds_Of_Wonder_amusement_park.jpg",  # Worlds of Wonder
    "ghaziabad": "https://images.unsplash.com/photo-1448375240586-882707db888b?w=900&auto=format&fit=crop&q=85",  # City Forest
    "lucknow": "https://commons.wikimedia.org/wiki/Special:FilePath/Bara%20Imambara%20Lucknow.jpg?width=900",  # Bara Imambara
    "kanpur": "https://upload.wikimedia.org/wikipedia/commons/2/20/JK_TEMPLE_of_Kanpur.jpg",  # JK Temple
    "agra": "https://commons.wikimedia.org/wiki/Special:FilePath/Taj%20Mahal%2C%20Agra%2C%20India.jpg?width=900",  # Taj Mahal
    "varanasi": "https://commons.wikimedia.org/wiki/Special:FilePath/Kashi%20Vishwanath%20Temple.jpg?width=900",  # Kashi Vishwanath Temple
    "jaipur": "https://commons.wikimedia.org/wiki/Special:FilePath/Hawa%20Mahal%20Jaipur.jpg?width=900",  # Hawa Mahal
    "jodhpur": "https://commons.wikimedia.org/wiki/Special:FilePath/Mehrangarh%20Fort%20Jodhpur.jpg?width=900",  # Mehrangarh Fort
    "ahmedabad": "https://commons.wikimedia.org/wiki/Special:FilePath/Sabarmati%20Ashram.jpg?width=900",  # Sabarmati Ashram
    "surat": "https://commons.wikimedia.org/wiki/Special:FilePath/Dumas%20Beach%20Surat.jpg?width=900",  # Dumas Beach
    "vadodara": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Laxmi_Vilas_Palace_-_Vadodara.jpg",  # Laxmi Vilas Palace
    "mumbai": "https://commons.wikimedia.org/wiki/Special:FilePath/Gateway%20of%20India%20Mumbai.jpg?width=900",  # Gateway of India
    "pune": "https://commons.wikimedia.org/wiki/Special:FilePath/Shaniwar%20Wada%20Pune.jpg?width=900",  # Shaniwar Wada
    "nagpur": "https://commons.wikimedia.org/wiki/Special:FilePath/Deekshabhoomi%20Nagpur.jpg?width=900",  # Deekshabhoomi
    "nashik": "https://commons.wikimedia.org/wiki/Special:FilePath/Trimbakeshwar%20Temple.jpg?width=900",  # Trimbakeshwar Temple
    "indore": "https://upload.wikimedia.org/wikipedia/commons/5/52/Rajwada_Palace%2C_Indore.jpg",  # Rajwada Palace
    "bhopal": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Upper_Lake%2C_Bhopal%2C_M.P.jpg",  # Upper Lake
    "kolkata": "https://commons.wikimedia.org/wiki/Special:FilePath/Victoria%20Memorial%20Kolkata.jpg?width=900",  # Victoria Memorial
    "howrah": "https://commons.wikimedia.org/wiki/Special:FilePath/Howrah%20Bridge%20Kolkata.jpg?width=900",  # Howrah Bridge
    "durgapur": "https://upload.wikimedia.org/wikipedia/commons/5/56/Durgapur_barrage2.jpg",  # Durgapur Barrage
    "siliguri": "https://commons.wikimedia.org/wiki/Special:FilePath/Mahananda%20Wildlife%20Sanctuary.jpg?width=900",  # Mahananda Wildlife Sanctuary
    "bengaluru": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Indian_Independence_day_celebration_216th_flower_show_2024%2C_Lalbagh%2C_Bangalore_129.jpg",  # Lalbagh Botanical Garden
    "mysuru": "https://commons.wikimedia.org/wiki/Special:FilePath/Mysore%20Palace.jpg?width=900",  # Mysore Palace
    "hyderabad": "https://commons.wikimedia.org/wiki/Special:FilePath/Charminar%20Hyderabad.jpg?width=900",  # Charminar
    "warangal": "https://upload.wikimedia.org/wikipedia/commons/c/c8/Nandi_Thousand_Pillar_Temple.jpg",  # Thousand Pillar Temple
    "chennai": "https://commons.wikimedia.org/wiki/Special:FilePath/Marina%20Beach%20Chennai.jpg?width=900",  # Marina Beach
    "coimbatore": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=900&auto=format&fit=crop&q=85",  # Isha Yoga Center
    "madurai": "https://upload.wikimedia.org/wikipedia/commons/3/36/Sri_Meenakshi_Devasthanam_Temple_from_courtyard.jpg",  # Meenakshi Amman Temple
    "kochi": "https://upload.wikimedia.org/wikipedia/commons/d/d2/Fort_Kochi_-_Mural_of_Na%27vi.jpg",  # Fort Kochi
    "thiruvananthapuram": "https://commons.wikimedia.org/wiki/Special:FilePath/Padmanabhaswamy%20Temple.jpg?width=900",  # Padmanabhaswamy Temple
    "patna": "https://commons.wikimedia.org/wiki/Special:FilePath/Takht%20Sri%20Patna%20Sahib.jpg?width=900",  # Takht Sri Patna Sahib
    "ranchi": "https://upload.wikimedia.org/wikipedia/commons/9/91/Hundru_Falls%2C_Jharkhand%2C_India.jpg",  # Hundru Falls
    "jamshedpur": "https://commons.wikimedia.org/wiki/Special:FilePath/Jubilee%20Park%20Jamshedpur.jpg?width=900",  # Jubilee Park
    "bhubaneswar": "https://commons.wikimedia.org/wiki/Special:FilePath/Lingaraj%20Temple%20Bhubaneswar.jpg?width=900",  # Lingaraj Temple
    "cuttack": "https://commons.wikimedia.org/wiki/Special:FilePath/Barabati%20Fort%20Cuttack.jpg?width=900",  # Barabati Fort
    "visakhapatnam": "https://commons.wikimedia.org/wiki/Special:FilePath/RK%20Beach%20Visakhapatnam.jpg?width=900",  # RK Beach
    "vijayawada": "https://commons.wikimedia.org/wiki/Special:FilePath/Kanaka%20Durga%20Temple.jpg?width=900",  # Kanaka Durga Temple
}
