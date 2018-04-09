from random import shuffle


def ask_for_file(communicate):
    while True:
        file_name = input(communicate)

        if '.txt' in file_name:
            return file_name
        else:
            print('Bad file name format (.txt), try again!')


def count_letters(what_to_open):
    text_size = 0

    while True:
        try:
            text_file = open(what_to_open, 'r')
        except FileNotFoundError:
            what_to_open = ask_for_file('File not found :(, try again.')
        else:
            for line in text_file:
                splited_line = line.split()
                for word in splited_line:
                    line_length = len(word)
                    text_size += line_length
            text_file.close()
            return text_size


def create_key():
    key_table = {}
    list_of_letters = []

    for encoded_letter_in_ascii in range(65, 91):
        list_of_letters.append(chr(encoded_letter_in_ascii))
    for encoded_letter_in_ascii in range(97, 123):
        list_of_letters.append(chr(encoded_letter_in_ascii))

    for letter in list_of_letters:
        key_table[letter] = None

    shuffle(list_of_letters)

    iterator = 0
    for key in key_table:
        key_table[key] = list_of_letters[iterator]
        iterator += 1

    return key_table


def save_encoded():
    key_dict = create_key()

    decoded_file_name = ask_for_file('Which file would You like to encode? ')
    file_size = count_letters(decoded_file_name)

    list_of_values_counter = 0
    letter_counter = 0
    list_of_values = list(key_dict.values())
    number_of_letters_in_ascii = 52
    step = file_size // number_of_letters_in_ascii

    decoded_text_file = open(decoded_file_name, 'r')

    encoded_file_name = ask_for_file('Where would You like to encode Your text? ')
    encoded_text_file = open(encoded_file_name, 'w')

    for line in decoded_text_file:
        line = line.rstrip('\n')
        encoded_line = []
        for letter in line:
            letter_counter += 1
            if letter_counter % step == 0 and list_of_values_counter < number_of_letters_in_ascii:
                encoded_line.append(list_of_values[list_of_values_counter])
                list_of_values_counter += 1
            for key in key_dict:
                if key == letter:
                    encoded_line.append(key_dict[key])
                    break
                elif letter not in key_dict.keys():
                    encoded_line.append(letter)
                    break
                else:
                    continue

        encoded_line.append('\n')
        ready_line = ''.join(encoded_line)
        encoded_text_file.write(ready_line)

    decoded_text_file.close()
    encoded_text_file.close()


def save_decoded():
    encoded_file_name = ask_for_file('What would You like to decode? ')
    encoded_text_file = open(encoded_file_name, 'r')
    key_dict = obtain_key_form_encoded_file(encoded_file_name)

    decoded_file_name = ask_for_file('Where would You like to save Ur decoded file? ')
    decoded_text_file = open(decoded_file_name, 'w')

    for line in encoded_text_file:
        line = line.rstrip('\n')
        decoded_line = []
        for letter in line:
            for key in key_dict:
                if key_dict[key] == letter:
                    decoded_line.append(key)
                    break
                elif letter not in key_dict.values():
                    decoded_line.append(letter)
                    break
                else:
                    continue

        decoded_line.append('\n')
        ready_line = ''.join(decoded_line)
        decoded_text_file.write(ready_line)

    decoded_text_file.close()
    encoded_text_file.close()


def obtain_key_form_encoded_file(file_name):
    fo = open(file_name, 'r')
    file_size = count_letters(file_name)
    number_of_letters_in_ascii = 52
    step = (file_size-52) // number_of_letters_in_ascii
    key = {}

    list_of_keys = []

    for encoded_letter_in_ascii in range(65, 91):
        list_of_keys.append(chr(encoded_letter_in_ascii))
    for encoded_letter_in_ascii in range(97, 123):
        list_of_keys.append(chr(encoded_letter_in_ascii))

    list_of_values = []
    keys_counter = 0
    letter_counter = 1
    for line in fo:
        line = line.rstrip('\n')
        for letter in line:
            letter_counter += 1
            if letter_counter % (step+1) == 0 and keys_counter < number_of_letters_in_ascii:
                list_of_values.append(letter)
                keys_counter += 1

    i = 0
    for item in list_of_keys:
        key[item] = list_of_values[i]
        i += 1
    fo.close()
    return key


def menu():
    while True:
        option = input('What do You want to do?\n1. Encode file?\n2. Decode file?\n3. Exit?\n')

        if option == '1':
            save_encoded()
        elif option == '2':
            save_decoded()
        elif option == '3':
            exit()
        else:
            print('Bad choice, try again ! ')
            continue


if __name__ == '__main__':
    menu()

