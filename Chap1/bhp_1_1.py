# bhp_1_1.py

# Codice di esempio utilizzato per illustrare le funzionalita' offerete dal
# editor WingIDE.

def sum(number_one, number_two):
	number_one_int = convert_integer(number_one)
	number_two_int = convert_integer(number_two)

	result = number_one_int + number_two_int

	return result

def convert_integer(number_string):
	converted_integer = int(number_string)
	return converted_integer

answer = sum("1", "2")

# ho aggiunto una istruzione print affinche' il programma mostri qualcosa
# al termine dell'esecuzione.
print answer
