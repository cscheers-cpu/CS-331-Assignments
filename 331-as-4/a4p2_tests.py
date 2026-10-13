"""Test cases for Problem 2 (nomenclator). Run: python3 a4p2_tests.py

Notes on expected behaviour (taken from the assignment's sample output):
  - A codebook word is decrypted to the codebook key exactly as it is written in the codebook
    ('University' -> 'university', 'winter' -> 'WINTER', 'cat' -> 'Cat' if the key is 'Cat').
  - Words NOT in the codebook keep their original case and punctuation.
  - Encryption picks symbols at random, so cases with several symbols are checked by round trip
    and by symbol validity; cases where every codebook word has one symbol are checked exactly.
"""
import re
import a4p2

K1 = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
cb1 = {'university': ['1', '2', '3'], 'examination': ['4', '5'],
       'examinations': ['6', '7', '8'], 'WINTER': ['9']}


def check(name, key, plain, book, cipher, decrypted, exact):
    # 1. decrypting the stored ciphertext gives the expected text
    got = a4p2.decryptMessage(key, cipher, book)
    assert got == decrypted, f"[{name}] decrypt: expected {decrypted!r}, got {got!r}"
    # 2. encrypt then decrypt returns the same expected text (run several times: symbols are random)
    for _ in range(50):
        enc = a4p2.encryptMessage(key, plain, book)
        back = a4p2.decryptMessage(key, enc, book)
        assert back == decrypted, f"[{name}] round trip: {enc!r} -> {back!r}"
        # every run of digits in the ciphertext is either a symbol from the codebook or a digit run from the message
        allowed = {str(v) for vals in book.values() for v in vals} | set(re.findall(r'\d+', plain))
        assert set(re.findall(r'\d+', enc)) <= allowed, f"[{name}] unexpected symbol in {enc!r}"
        # punctuation and whitespace outside words are untouched
        assert re.sub(r'[A-Za-z0-9]', '', enc) == re.sub(r'[A-Za-z0-9]', '', plain), f"[{name}] punctuation changed: {enc!r}"
        if exact:
            assert enc == cipher, f"[{name}] encrypt: expected {cipher!r}, got {enc!r}"
    print('ok  ', name)


check('assignment example', K1, 'At the University of Alberta, examinations take place in December and April for the Fall and Winter terms.', cb1,
      'Lj jia 2 py Lmfacjl, 7 jlka bmlwa sx Oawanfac lxo Lbcsm ypc jia Ylmm lxo 9 jacnr.',
      'At the university of Alberta, examinations take place in December and April for the Fall and WINTER terms.', False)

check('no codebook words', K1, 'Hello, world! This message has nothing from the codebook.', cb1,
      'Iammp, epcmo! Jisr narrlua ilr xpjisxu ycpn jia wpoafppk.',
      'Hello, world! This message has nothing from the codebook.', True)

check('empty codebook', 'QWERTYUIOPASDFGHJKLZXCVBNM', 'Nothing here is replaced; only letters change.', {},
      'Fgziofu itkt ol kthsqetr; gfsn stzztkl eiqfut.',
      'Nothing here is replaced; only letters change.', True)

check('empty message', K1, '', cb1,
      '',
      '', True)

check('reverse key', 'ZYXWVUTSRQPONMLKJIHGFEDCBA', 'Zebra crossing: a quick test.', {},
      'Avyiz xilhhrmt: z jfrxp gvhg.',
      'Zebra crossing: a quick test.', True)

check('single symbols', K1, 'The cat and the dogs said hello.', {'the': ['10'], 'and': ['11'], 'hello': ['12'], 'Cat': ['13'], 'dogs': ['14']},
      '10 13 11 10 14 rlso 12.',
      'the Cat and the dogs said hello.', True)

check('case-insensitive codebook', K1, 'HELLO Hello hello hElLo', {'hello': ['5']},
      '5 5 5 5',
      'hello hello hello hello', True)

check('punctuation around codebook words', 'QWERTYUIOPASDFGHJKLZXCVBNM', '"hello" hello; (hello) hello... hello?', {'hello': ['1', '2']},
      '"2" 1; (2) 1... 1?',
      '"hello" hello; (hello) hello... hello?', False)

check('mixed case non-codebook', K1, 'HeLLo wOrLD, SoMeThInG StRaNgE', {},
      'IaMMp ePcMO, RpNaJiSxU RjClXuA',
      'HeLLo wOrLD, SoMeThInG StRaNgE', True)

check('codebook key with capitals', K1, 'winter Winter WINTER wInTeR', {'WINTER': ['9']},
      '9 9 9 9',
      'WINTER WINTER WINTER WINTER', True)

check('adjacent punctuation', K1, "Wait... what?! Yes -- really; (maybe), 'sure'.", {'wait': ['0']},
      "0... eilj?! Har -- calmmh; (nlhfa), 'rtca'.",
      "wait... what?! Yes -- really; (maybe), 'sure'.", True)

check('digits in message', 'QWERTYUIOPASDFGHJKLZXCVBNM', 'In 2003 there were 5 cats and 12 dogs.', {'cats': ['40'], 'dogs': ['41']},
      'Of 2003 zitkt vtkt 5 40 qfr 12 41.',
      'In 2003 there were 5 cats and 12 dogs.', True)

check('multi-digit symbols', K1, 'the cat and the dogs', {'the': ['100', '101'], 'cat': ['7'], 'and': ['25'], 'dogs': ['300']},
      '101 7 25 100 300',
      'the cat and the dogs', False)

check('plural vs singular entries', 'ZYXWVUTSRQPONMLKJIHGFEDCBA', 'examination examinations examination', cb1,
      '5 7 4',
      'examination examinations examination', False)

check('long text all words in codebook', K1, 'the and the and', {'the': ['1', '2', '3'], 'and': ['4', '5']},
      '1 4 2 5',
      'the and the and', False)

check('newlines and spacing', K1, 'Line one has the cat.\nLine two,  with  double spaces\tand a tab.', {'cat': ['9']},
      'Msxa pxa ilr jia 9.\nMsxa jep,  esji  optfma rblwar\tlxo l jlf.',
      'Line one has the cat.\nLine two,  with  double spaces\tand a tab.', True)

print('all Problem 2 tests passed')
