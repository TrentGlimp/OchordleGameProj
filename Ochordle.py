from datetime import date


class Calendar(object):
    def __init__(self):
        self.months = {  # a dictionary of the days in each month
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }

    def days_past(self):  # equation that calculates the amount of days past jan 1st
        todays_date = str(date.today())
        month = todays_date[5:7]
        if month[0] == "0":
            month = month[1]
        day = todays_date[8:]
        if day[0] == 0:
            day = day[1]
        count_month = 1
        total = 0
        while count_month != int(month):
            total += self.months[int(count_month)]
            count_month += 1
        total += int(day) - 1
        return total


class Words(object):
    def __init__(self):
        with open("allWords.txt", "r") as f:  # list of every eight letter word
            data = f.read()
            self.all_words = data.split('\n')
        # list of 365 words that are the answers on their given day
        with open("wordList.txt", "r") as f:
            data = f.read()
            self.daily_words = data.split('\n')

    def word_slice(self, word):  # slices a word into a list of the word's letters
        wordList = []
        for each in word:
            wordList.append(each)
        return wordList

    def daily_word(self):  # determines the answer for Ochordle today
        cal = Calendar()
        daily = self.daily_words[cal.days_past()]
        return daily

    def daily_slice(self):  # slices the daily word into a list of the word's letters
        daily = self.daily_word()
        sliced = self.word_slice(daily)
        return sliced


class Board(object):
    def __init__(self):
        words = Words()
        self.board = {  # the six guesses (visible) + the answer (never visible)
            1: ["_", "_", "_", "_", "_", "_", "_", "_"],
            2: ["_", "_", "_", "_", "_", "_", "_", "_"],
            3: ["_", "_", "_", "_", "_", "_", "_", "_"],
            4: ["_", "_", "_", "_", "_", "_", "_", "_"],
            5: ["_", "_", "_", "_", "_", "_", "_", "_"],
            6: ["_", "_", "_", "_", "_", "_", "_", "_"],
            7: words.daily_slice()
        }

    def print_board(self):  # prints the board
        x = 1
        while x <= 6:
            word = None
            for each in self.board[x]:
                if word == None:
                    word = each
                else:
                    word += each
            print(f"{x}: {word}")
            x += 1

    def guess_num(self):  # determins which guess you are on
        x = 1
        while x <= 6:
            if self.board[x] == ["_", "_", "_", "_", "_", "_", "_", "_"]:
                return x
            x += 1

    def validate_move(self, given):  # makes sure the input is an eight letter word
        words = Words()
        answer = False
        while answer == False:
            if given.isalpha() == True:
                if len(given) == 8:
                    if given in words.all_words:
                        return given
            given = input(
                f"That is not a valid input\nPlease type in an eight letter word: ")

    def format(self, given):  # formats the input into all lowercase letters then does word_slice()
        words = Words()
        lowercase = given.lower()
        sliced = words.word_slice(lowercase)
        return sliced

    # puts letters in their correct places and shows what letters are in the answer that you've guessed
    def correctness(self, given):
        words = Words()
        corrects = []
        word = self.format(given)
        guess = self.guess_num()
        for i in range(8):
            if word[i] == words.daily_slice()[i]:
                self.board[guess][i] = word[i]
        if self.board[guess] == ['_', '_', '_', '_', '_', '_', '_', '_']:
            self.board[guess] = ["N", "o", " ", "C", "o", "r", "r", "e", "c",
                                 "t", " ", "P", "l", "a", "c", "e", "m", "e", "n", "t", "s", "!"]
        for each in word:
            if each in words.daily_slice():
                corrects.append(each)
        corrects = list(dict.fromkeys(corrects))
        corrects = sorted(corrects)
        corrects = ", ".join(corrects)
        return corrects

    def win(self):  # checks if you've won or not
        x = 1
        while x <= 6:
            if self.board[x] == self.board[7]:
                return True
            x += 1

    def over(self):  # checks if all six guesses have been entered
        x = 1
        while x <= 6:
            if self.board[x] == ["_", "_", "_", "_", "_", "_", "_", "_"]:
                return False
            x += 1
        return True


def play():
    b = Board()
    w = Words()
    print("Welcome To Ochordle!:\nThe 8-letter, Wordle Rip-Off Game")
    while True:
        guess = input("What is your guess? ")
        guess = b.validate_move(guess)
        print(f"The correct letters are: {b.correctness(guess)}")
        b.print_board()
        if b.win() == True:
            print(f'''You Win!\nThe Word Was "{w.daily_word()}\nIt Took You {b.guess_num()-1} Guesses!"''')
            quit()
        if b.over() == True:
            print(
                f'''That Was A Tough One!\nThe Word Was "{w.daily_word()}"''')
            quit()


if __name__ == "__main__":
    play()
