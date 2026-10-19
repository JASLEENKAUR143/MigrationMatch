import csv
import math
from pathlib import Path

import numpy as np

np.random.seed(42)

cities = [
    "Ludhiana","Chandigarh","Amritsar","Jalandhar","Mohali","Delhi","Gurugram","Faridabad","Noida","Ghaziabad",
    "Lucknow","Kanpur","Agra","Varanasi","Jaipur","Jodhpur","Ahmedabad","Surat","Vadodara","Mumbai",
    "Pune","Nagpur","Nashik","Indore","Bhopal","Kolkata","Howrah","Durgapur","Siliguri","Bengaluru",
    "Mysuru","Hyderabad","Warangal","Chennai","Coimbatore","Madurai","Kochi","Thiruvananthapuram","Patna","Ranchi",
    "Jamshedpur","Bhubaneswar","Cuttack","Visakhapatnam","Vijayawada"
]

# 20 occupations (blue-collar / relevant)
occupations = [
    "Electrician","Plumber","Mechanic","Painter","Mason","Carpenter","Welder","Driver",
    "AC Technician","Refrigeration Technician","Machine Operator","Factory Worker","Construction Worker",
    "Security Guard","Delivery Executive","Cook","Waiter","Housekeeping Worker","Tailor","Barber"
]

# Base salary per occupation (monthly, INR) - realistic proxies
base_salary_skill = {
    "Electrician": 14000, "Plumber": 13000, "Mechanic": 14000, "Painter": 11000,
    "Mason": 12000, "Carpenter": 12500, "Welder": 13000, "Driver": 13000,
    "AC Technician": 15000, "Refrigeration Technician": 15000, "Machine Operator": 16000,
    "Factory Worker": 12000, "Construction Worker": 11500, "Security Guard": 10000,
    "Delivery Executive": 11000, "Cook": 11000, "Waiter": 9000, "Housekeeping Worker": 9000,
    "Tailor": 8000, "Barber": 8000
}

# City multipliers and rent ratios approximations by city tier
metro_cities = {"Delhi","Mumbai","Bengaluru","Hyderabad","Chennai","Kolkata","Ahmedabad","Pune"}
tier2_cities = {
    "Surat","Vadodara","Lucknow","Kanpur","Nagpur","Indore","Bhopal","Visakhapatnam",
    "Vijayawada","Nashik","Coimbatore","Thiruvananthapuram","Patna","Ranchi","Jamshedpur","Bhubaneswar","Cuttack"
}
# Remaining will be considered smaller Tier-2/3

def city_multiplier(city):
    if city in metro_cities:
        return 1.25
    if city in tier2_cities:
        return 1.05
    return 0.92

def rent_ratio(city):
    # fraction of salary used for 1BHK rent (varies by city)
    if city in metro_cities:
        return 0.35  # metros more expensive
    if city in tier2_cities:
        return 0.22
    return 0.18

def socio_base(city):
    # Base socio scores by type
    if city in metro_cities:
        return {"Healthcare": 70, "Transport": 72, "QoL": 68, "Safety": 60, "Afford": 45}
    if city in tier2_cities:
        return {"Healthcare": 62, "Transport": 60, "QoL": 63, "Safety": 65, "Afford": 60}
    return {"Healthcare": 55, "Transport": 50, "QoL": 55, "Safety": 68, "Afford": 70}

out_path = Path(__file__).resolve().with_name("migrationmatch_dataset.csv")

# Header matching required columns
header = [
    "City","State","Region","Skill","Job_Demand_Score","Job_Availability",
    "Minimum_Salary","Average_Salary","Maximum_Salary",
    "Average_1BHK_Rent","Shared_Rent",
    "Food_Cost","Utilities_Cost","Transport_Cost","Other_Monthly_Cost",
    "Estimated_Monthly_Expenses","Estimated_Monthly_Savings",
    "Healthcare_Score","Transportation_Score","Quality_of_Life_Score","Safety_Score","Affordability_Score"
]

# Simple mapping of city to State and Region (region = North/South/East/West/Central)
city_state_region = {
    "Ludhiana": ("Punjab","North"), "Chandigarh":("Chandigarh","North"), "Amritsar":("Punjab","North"),
    "Jalandhar":("Punjab","North"), "Mohali":("Punjab","North"), "Delhi":("Delhi","North"),
    "Gurugram":("Haryana","North"), "Faridabad":("Haryana","North"), "Noida":("Uttar Pradesh","North"),
    "Ghaziabad":("Uttar Pradesh","North"), "Lucknow":("Uttar Pradesh","North"), "Kanpur":("Uttar Pradesh","North"),
    "Agra":("Uttar Pradesh","North"), "Varanasi":("Uttar Pradesh","North"), "Jaipur":("Rajasthan","North"),
    "Jodhpur":("Rajasthan","North"), "Ahmedabad":("Gujarat","West"), "Surat":("Gujarat","West"),
    "Vadodara":("Gujarat","West"), "Mumbai":("Maharashtra","West"), "Pune":("Maharashtra","West"),
    "Nagpur":("Maharashtra","Central"), "Nashik":("Maharashtra","West"), "Indore":("Madhya Pradesh","Central"),
    "Bhopal":("Madhya Pradesh","Central"), "Kolkata":("West Bengal","East"), "Howrah":("West Bengal","East"),
    "Durgapur":("West Bengal","East"), "Siliguri":("West Bengal","East"), "Bengaluru":("Karnataka","South"),
    "Mysuru":("Karnataka","South"), "Hyderabad":("Telangana","South"), "Warangal":("Telangana","South"),
    "Chennai":("Tamil Nadu","South"), "Coimbatore":("Tamil Nadu","South"), "Madurai":("Tamil Nadu","South"),
    "Kochi":("Kerala","South"), "Thiruvananthapuram":("Kerala","South"), "Patna":("Bihar","East"),
    "Ranchi":("Jharkhand","East"), "Jamshedpur":("Jharkhand","East"), "Bhubaneswar":("Odisha","East"),
    "Cuttack":("Odisha","East"), "Visakhapatnam":("Andhra Pradesh","South"), "Vijayawada":("Andhra Pradesh","South")
}

rows = []

for city in cities:
    state, region = city_state_region.get(city, ("Unknown","Unknown"))
    cm = city_multiplier(city)
    rr = rent_ratio(city)
    socio = socio_base(city)

    for skill in occupations:
        # base salary by skill
        base = base_salary_skill.get(skill, 10000)

        # average salary derived from base and city multiplier + small randomness
        avg_salary = int(round(base * cm * (1 + np.random.normal(loc=0.02, scale=0.07))))
        if avg_salary < 6000:
            avg_salary = 6000

        # variation for min and max
        min_salary = int(max(3000, round(avg_salary * (0.70 + np.random.uniform(-0.05, 0.05)))))
        max_salary = int(round(avg_salary * (1.10 + np.random.uniform(0, 0.12))))

        # Job demand influenced by skill and city
        # Skill demand modifiers: some skills more in demand
        skill_demand_bonus = {
            "Driver": 8, "Factory Worker": 7, "Security Guard": 6, "Construction Worker": 5,
            "Delivery Executive": 6, "Machine Operator": 5, "Electrician": 4, "Plumber": 4,
            "Welder": 4, "Carpenter": 3, "Mason": 3, "AC Technician": 3, "Refrigeration Technician":2,
            "Cook": 3, "Waiter": 2, "Housekeeping Worker": 2, "Mechanic":3, "Painter":1, "Tailor":0, "Barber":0
        }.get(skill, 2)

        # City demand factor: smaller cities may have fewer absolute jobs but higher local demand (%) — moderate influence
        city_demand_factor = 5 if cm < 1.0 else 3

        job_demand_score = int(np.clip(50 + skill_demand_bonus * 3 + np.random.randint(-15, 16) + (5 if city in ["Mumbai","Delhi","Bengaluru","Hyderabad","Chennai"] else 0), 20, 98))
        job_availability = int(max(5, job_demand_score * np.random.randint(8, 18)))  # rough proportional

        # Rent & expenses
        avg_rent = int(max(1500, round(avg_salary * rr * (1 + np.random.normal(0, 0.08)))))
        shared_rent = int(round(avg_rent * (0.45 + np.random.uniform(-0.05, 0.05))))

        food_cost = int(round(avg_salary * (0.11 + np.random.uniform(-0.02, 0.03))))
        utilities_cost = int(round(avg_salary * (0.035 + np.random.uniform(-0.01, 0.02))))
        transport_cost = int(round(avg_salary * (0.055 + np.random.uniform(-0.02, 0.03))))
        other_cost = int(round(avg_salary * (0.045 + np.random.uniform(-0.02, 0.02))))

        est_expenses = avg_rent + food_cost + utilities_cost + transport_cost + other_cost
        est_savings = int(avg_salary - est_expenses)

        # Socio scores with small random perturbation
        healthcare = int(np.clip(socio["Healthcare"] + np.random.randint(-8, 9), 10, 98))
        transportation = int(np.clip(socio["Transport"] + np.random.randint(-10, 10), 8, 98))
        qol = int(np.clip(socio["QoL"] + np.random.randint(-10, 10), 10, 98))
        safety = int(np.clip(socio["Safety"] + np.random.randint(-10, 10), 8, 98))
        affordability = int(np.clip(socio["Afford"] + np.random.randint(-10, 10), 8, 98))

        rows.append([
            city, state, region, skill,
            job_demand_score, job_availability,
            min_salary, avg_salary, max_salary,
            avg_rent, shared_rent,
            food_cost, utilities_cost, transport_cost, other_cost,
            est_expenses, est_savings,
            healthcare, transportation, qol, safety, affordability
        ])

# Write CSV
with open(out_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Generated dataset at: {out_path} ({len(rows)} rows)") 