from requests import get
from time import sleep
from googletrans import Translator
from threading import Timer

settings = {"answer_occurs_time": 5, 'amount of questions': 5,'time_to_answer': 10, 'players': 2, 'correct_languages': ['pl','en']}
translator = Translator()

def play_game():

    """Function which makes a call to api,
    asks the question to players and keep track of the players scores
    :returns int score of the players"""

    language = input('choose language: (pl or en):> ').lower()
    while language not in settings['correct_languages']:
        language = input('language: pl, en').lower()
    current_player, waiting_player = input('Player1: '), input('Player2: ')
    current_player_score, waiting_player_score = 0, 0

    amount_of_questions = settings['amount of questions']
    for x in range(amount_of_questions):
        t = Timer(settings['time_to_answer'], print, '\nTime passed! press ENTER to continue')
        print(f'{current_player} is playing now!')
        response_json = get('https://jservice.io/api/random').json()
        question = translator.translate(text=(response_json[0]['question']), dest=language)
        print('You have 5 sec to read the question')
        sleep(1)
        print(question.text)
        sleep(settings['answer_occurs_time'])
        print('You have 10 sec to answer the question')
        t.start()
        player_answer = input('Your answer is:> ').lower()
        t.cancel()
        answer_translated = translator.translate(response_json[0]['answer'], dest=language)
        answer = str(answer_translated.text).lower()

        if player_answer == answer:
            print('*' * 30)
            print('CORRECT!')
            print('*' * 30)
            current_player_score += 1
        else:
            print()
            print('*' * 30)
            print(f'correct answer is: {answer}')
            print('*' * 30)
            print()
            sleep(3)
        current_player, waiting_player = waiting_player, current_player

    return f'player1 score: {current_player_score}, player2 score: {waiting_player_score}'
