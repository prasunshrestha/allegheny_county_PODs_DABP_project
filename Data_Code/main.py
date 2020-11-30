# -*- coding: utf-8 -*-
"""
Decision Analytics for Business and Policy
Final Project

@author: Team Ruth & Co
"""

title = "Team Ruth & Co Final Project"
course = "94-867 Decision Analytics for Business & Policy Fall 2020"
team = "Florian Cords, Jose Salomon, Prasun Shrestha, Ruth Wang"
print('\n', title, course, team, sep='\n')

welcome = "\"welcome message\""
print("\nWould you like to update the distances")
update = input("Enter Y or N: ")
if update.upper() == "N":
	status = False
elif update.upper() == "Y":
	print("Distances Updated")
	status = False
else:
	print("Invalid selection. Please try again.")
	cont = input("Enter Y or N: ")

instructions = "\"instructions\""
print('\n', welcome, instructions, sep='\n')

choice = input("Enter your value: ")
status = True
while status == True:
	try:
		choice = int(choice)
	except:
		print("Invalid selection. Please try again.")
		choice = input("Enter your value: ")
	else: 
		if choice == 1: print("Formulation 1")
		elif choice == 2: print("Formulation 2")
		elif choice == 3: print("Stochastic")

		print("Would you like to run another model?")
		cont = input("Enter Y or N: ")
		if cont.upper() == "N":
			print("The End", "Have a great day!", sep="\n")
			status = False
		elif cont.upper() == "Y":
			choice = input("Enter your value: ")
		else:
			print("Invalid selection. Please try again.")
			cont = input("Enter Y or N: ")