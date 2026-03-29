import csv
import random

# Retrieve colours from csv file and put them in a list
file = open("country_flags.csv", "r")
all_flags = list(csv.reader (file, delimiter=","))
file.close()

# remove the first row
all_flags.pop(0)

round_countries = []
round_capitals = []
round_flag_codes = []
flag_images = []

# loop until we have four flags with different names
while len(round_countries) < 4:
    potential_country = random.choice(all_flags)


    if potential_country[1] not in all_flags[1]:
        round_countries.append(potential_country[0])
        round_capitals.append(potential_country[1])
        round_flag_codes.append(potential_country[2])
        flag_images.append(potential_country[3])

print("Round countries", round_countries)
print("Round capitals", round_capitals)
print("Flag codes", round_flag_codes)
print("Flag images", flag_images)