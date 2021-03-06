"""
Created: Nathan Randle aka BlindMan

This program is used to generate A days worth of travel encounters based on
giffyglyphs darker dungeons. I did however take my own liberties in weighting
the different outcomes.

My changes essentially add more weight to the choosen threat level, so at
level 1 you will see hostile encounters far less often, and never see an aggressive
combat. At higher levels you will see more and more hostile encounters vs mundane
and flavor.

In order to ADD possible events:
    First add them to the CSV, with the type and encounter
        Keep in mind the speelling is case sensitive
    If you use a heading


"""


import common
import random as rn
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Configs
generate_encounters = True

playerCharacters = list(pd.read_csv("./characters.csv"))


def value_counts(arr):
	unique_elements, counts_elements = np.unique(arr, return_counts=True)
	return (np.asarray((unique_elements, counts_elements)))

def weightedChoice(d):
	typesWeighted = []

	for i,encType in enumerate(d.keys()):
		for j in range(d[encType]):
			typesWeighted = np.append(typesWeighted,encType)
	return rn.choice(typesWeighted)


df = pd.read_csv("./EncountersTransposed.csv")


try:
	while True:
		print("\n*________________________________________________________________________________________*")

		command = common.get_input("Threat Level (or command, type ? for help): ")
		if not command.isdigit():
			tokens = command.lower().split()
			if len(tokens) <= 0:
				continue
			if tokens[0] == "exit":
				break
			if tokens[0] == "?":
				common.print_help()
			if len(tokens) == 3 and tokens[0] == "gen" and tokens[1] == "encounters":
				if tokens[2] == "on":
					generate_encounters = True
				elif tokens[2] == "off":
					generate_encounters = False
				else:
					print("Invalid setting")
			continue
		danger = max(min(int(command),5),1)

		# Here are the types of events that can be choosen.

		# The idea for hostile events is that at higher threat levels,
		# the more likely an aggressive event will occur
		# the others are just static because they dont matter as much

		hostile = {
			"Skill Check":danger,
			"Hostile Social":danger,
			"Combat (Non-committal)":danger,
			"Combat (Aggressive)":(danger-1)*2
		}

		mund = {
			"Inventory Check":3,
			"Find something mundane in inventory":1,
			"Weather Check":5
		}

		flavor = {
			"Character Encounter":1,
			"Discovery":1
		}



		phases = ["Dawn", 'Morning', 'Noon', 'Afternoon', 'Dusk', 'Night']


		for i in phases:
			print("\n------------------------------------------------\n\n" +
			"*" + i + "*: ")
			# here is where
			'''
			I created a matrix to show the different results based on danger level
			The number indicates how often the option will be choosen out of the
			total for that row.
			(IE at level 1, hostile encounters will occur 2 out of 14)

			Level | Hostile | Mundane | Flavor | Total
			1     |    2    |    7    |    5   |   14
			2     |    3    |    6    |    4   |   13
			3     |    4    |    5    |    3   |   12
			4     |    5    |    4    |    2   |   11
			5     |    6    |    3    |    1   |   10

			(I rounded down so they may not add up to 100% oops)
			Level |  Hostile  |  Mundane  |  Flavor  | Total
			1     |    14%    |    50%    |    35%   |   14
			2     |    23%    |    46%    |    30%   |   13
			3     |    33%    |    41%    |    25%   |   12
			4     |    45%    |    36%    |    18%   |   11
			5     |    60%    |    30%    |    10%   |   10
			to modify how often something comes up, change the math for
			the variable random.

			'''

			random = [hostile]* (danger+1) \
				+ [mund]* abs(danger-8) \
				+ [flavor]* abs(danger-6)

			#Select and print event type
			choice = weightedChoice(rn.choice(random))
			print(choice+"\n")
			#Print specifics of event
			if choice in df["Type"].unique():
				print(df[df["Type"]==choice].sample()["Encounter"].values[0])
			print()
			if choice == "Character Encounter":
				#If character encounter, also print name
				print(": " + rn.choice(playerCharacters))
			elif generate_encounters and choice == "Combat (Aggressive)" or choice == "Combat (Non-committal)":
				#If set to generate encounters, generate and print one
				encounter = common.get_encounter(common.get_encounter_config())
				common.print_encounter(encounter)
except:
	print("Sorry, I just crashed -.-")
