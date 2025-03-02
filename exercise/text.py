def fullJustify(words, max_length):
    letter_count =0
    full_line = []
    return_line = []
    for i in words:
        print(len(i))
        if letter_count + len(i) + len(full_line)> max_length:
            print("In the loop")
            print(letter_count + len(i))
            for j in range(max_length - letter_count):
                print(f'Text count:{j}')
                print(f'Space index:{j%(len(full_line)-1 or 1 )}')
                # print(full_line[i])
                full_line[j%(len(full_line)-1 or 1 )] = full_line[j%(len(full_line)-1 or 1 )] + ' '
            return_line.append(''.join(full_line))
            full_line = []
            letter_count = 0
            # break
        full_line = full_line + [i]
        print(f'full_line :{full_line}')
        print(f'Return Line: {return_line}')
        letter_count = letter_count + len(i)
    print(full_line)
    return return_line +[' '.join(full_line).ljust(max_length)]
x_input = ["This", "is", "an", "example", "of", "text", "justification."]
# x_input = ["What","must","be","acknowledgment","shall","be"]
# x_input = ["This", "is", "an", "example", "of", "text", "justification."]
max_length = 16
a = fullJustify(x_input,max_length)
print(a)