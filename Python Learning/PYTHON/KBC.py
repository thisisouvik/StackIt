qs = ["Code with _______ fill the blanks", "Mere _____ ne thana thaya"]
op1 = [["Harry", "Maxim", "Jarvis", "Kabir"], ["Mere", "Tumhare", "kaka ke", "Pass"]]
correct_answers = ["Harry", "Tumhare"]
award = [2000, 4000]

for i in range(2):
    print(qs[i])
    print(op1[i])
    ans = input("Answer: ")
    if ans == correct_answers[i]:
        print("You won", award[i], "rupees")
    else:
        print("You are cooked")
        break


