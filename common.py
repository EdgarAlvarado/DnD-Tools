import json
import requests
import sys
python3 = True
if sys.version_info[0] < 3:
    python3 = False

def get_input(prompt):
	res = None
	if python3:
		res = input(prompt)
	else:
		res = raw_input(prompt)
	return res

def get_encounter_config():
	with open("./encounter.config", 'rb') as json_file:
		return json.load(json_file)

def get_encounter(configs):
	args = []
	for config in configs:
		if isinstance(configs[config], list):
			for value in configs[config]:
				args.append(config+"[]="+str(value))
			continue
		args.append(config+"="+str(configs[config]))
	#Site requires cookies, so a session must be created on the base url
	url_0 = "http://tools.goblinist.com/5enc"
	url_1 = "http://tools.goblinist.com/g/encounter?"+'&'.join(args)

	sesion = requests.session()
	sesion.get(url_0)
	response = sesion.get(url_1)
	encounter = json.loads(response.text)
	return encounter

def print_encounter(encounter):
	print("Encounter")
	print("Metadata:")
	print("Budget [max: " + str(encounter["maxBudget"]) + ", min:" + str(encounter["maxBudget"])+"]")
	print("Experience [Value: " + str(encounter["encounterValue"]) + ", Award: " + str(encounter["awardValue"]) + "]")
	print("Monsters:")
	for monsterName in encounter["monsters"]:
		monster = encounter["monsters"][monsterName]
		print("\tName: " + monster["name"])
		print("\tQty: " + str(monster["qty"]))
		print("\tXP each: " + str(monster["awardValuePH"]))
		print("\tXP total: " + str(monster["awardValue"]))
		print("\t--------------------------\n")
		pass

def print_help():
	print("\nYou can type a threat level from 1 to 5")
	print("A list of events for each time of the day will be printed\n")
	print("If an encounter may or will happen it will be printed")
	print("The encounter is generated with the help of http://tools.goblinist.com/5enc")
	print("There you can find the possible configurations")
	print("The configuration of the encounter can be changed in encounter.config\n")
	print("You can enable or disable the generation of encounters typing: gen encounters [on|off]")
