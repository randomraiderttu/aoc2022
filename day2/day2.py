import os
import fileProcessor as fp

# File variables
fileName = 'inputfile.txt'
fullPathName = os.path.join(os.path.dirname(os.path.realpath(__file__)),fileName)

class rpsRound:
    def __init__(self, roundString: str) -> None:
        self.originalString = roundString
        self.setRoundChoices()
        self.exercise1RoundTotal = self.getMyChoiceScore() + self.scoreExercise1Round()
        self.exercise2RoundTotal = self.scoreExercise2Round()

    def setRoundChoices(self):
        self.opponentChoice = self.originalString[:1]
        self.myChoice = self.originalString[2:]

    def getMyChoiceScore(self):
        match self.myChoice:
            case 'X':
                return 1
            case 'Y':
                return 2
            case 'Z':
                return 3
            case _:
                raise Exception('Invalid myChoice option - could not assign a numeric score for it.')

    def scoreExercise1Round(self):
        # Opponent - My Choice
        # A - Rock      - X
        # B - Paper     - Y
        # C - Scissors  - Z
        match self.opponentChoice + self.myChoice:
            case 'AX':
                return 3
            case 'AY':
                return 6
            case 'AZ':
                return 0
            case 'BX':
                return 0
            case 'BY':
                return 3
            case 'BZ':
                return 6
            case 'CX':
                return 6
            case 'CY':
                return 0
            case 'CZ':
                return 3
            case _:
                raise Exception(f'Invalid scoring combination. OpponentChoice + MyChoice = {self.opponentChoice + self.myChoice}')

    def scoreExercise2Round(self):
        # In this case, the second option wasn't my choice, but rather how the match needs to end so I win the overall. So I need
        #   to see what they played, choose the winning/draw/loser choice based on what it told me to do in that round and then get
        #   the score. I can precalculate the entire score for the round here.
        
        # Opponent Choice (and score for that element)
        # A - Rock (1 point)
        # B - Paper (2 points)
        # C - Scissors (3 points)

        # X - I need to lose (0 points)
        # Y - I need a draw (3 points)
        # Z - I need to win (6 points)
        match self.opponentChoice + self.myChoice:
            case 'AX':
                return 3
            case 'AY':
                return 4
            case 'AZ':
                return 8
            case 'BX':
                return 1
            case 'BY':
                return 5
            case 'BZ':
                return 9
            case 'CX':
                return 2
            case 'CY':
                return 6
            case 'CZ':
                return 7
            case _:
                raise Exception(f'Invalid scoring combination. OpponentChoice + MyChoice = {self.opponentChoice + self.myChoice}')

def processRounds(rounds: list[str]) -> list[rpsRound]:
    roundList = []
    for round in rounds:
        tmpRound = rpsRound(round)
        roundList.append(tmpRound)
    return roundList

def getTotalScores(rounds: list[rpsRound]) -> tuple[int, int]:
    exercise1Total = 0
    exercise2Total = 0
    for round in rounds:
        exercise1Total += round.exercise1RoundTotal
        exercise2Total += round.exercise2RoundTotal

    return exercise1Total, exercise2Total

def getExercise2TotalScore(rounds: list[rpsRound]) -> int:
    total = 0
    for round in rounds:
        total += round.roundTotal

    return total

if __name__ == '__main__':
    recs = fp.ingestFile(fullPathName)

    roundList = processRounds(recs)

    exercise1Total, exercise2Total = getTotalScores(roundList)
    print(f'Exercise 1 Total: {exercise1Total}')
    print(f'Exercise 2 Total: {exercise2Total}')