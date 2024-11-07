import subprocess
import time

def process(command):
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE
    )

def expect(proc, pattern):
    pattern = pattern.strip("\n")
    buffer = ""
    while True:
        char = proc.stdout.read(1).decode()
        if pattern.endswith(buffer):
            return True

def write(proc, text):
    proc.stdin.write(f'{text}\n'.encode())
    proc.stdin.flush()
    return text

def test():
    print("Launching processes")
    try:
        # Запуск wampus.bas и wampus.py
        py = process(['python', 'wampus.py'])
        bas = process(['vintbas', 'wampus.bas'])  # Замените 'vintbas' на доступный интерпретатор BASIC

        # Проверка вывода приветствия:
        expected_greetings = """
WUMPUS
CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY


INSTRUCTIONS (Y-N)? """
        print("expecting answers...")
        expect(py, expected_greetings)
        expect(bas, expected_greetings)
        print("[+] TEST 1 - PASSED")

        # Добавление задержки перед вводом
        time.sleep(1)

        # Отправка ответа "Y"
        print("sending keys...")
        write(py, 'Y')
        write(bas, 'Y')
        print("[+] KEYS SENT")

        # Проверка вывода инструкции:
        instructions_text = """
WELCOME TO 'HUNT THE WUMPUS'
  THE WUMPUS LIVES IN A CAVE OF 20 ROOMS. EACH ROOM
HAS 3 TUNNELS LEADING TO OTHER ROOMS. (LOOK AT A
DODECAHEDRON TO SEE HOW THIS WORKS-IF YOU DON'T KNOW
WHAT A DODECAHEDRON IS, ASK SOMEONE)

     HAZARDS:
 BOTTOMLESS PITS - TWO ROOMS HAVE BOTTOMLESS PITS IN THEM
     IF YOU GO THERE, YOU FALL INTO THE PIT (& LOSE!)
 SUPER BATS - TWO OTHER ROOMS HAVE SUPER BATS. IF YOU
     GO THERE, A BAT GRABS YOU AND TAKES YOU TO SOME OTHER
     ROOM AT RANDOM. (WHICH MAY BE TROUBLESOME)

     WUMPUS:
 THE WUMPUS IS NOT BOTHERED BY HAZARDS (HE HAS SUCKER
 FEET AND IS TOO BIG FOR A BAT TO LIFT).  USUALLY
 HE IS ASLEEP.  TWO THINGS WAKE HIM UP: YOU SHOOTING AN
ARROW OR YOU ENTERING HIS ROOM.
     IF THE WUMPUS WAKES HE MOVES (P=.75) ONE ROOM
 OR STAYS STILL (P=.25).  AFTER THAT, IF HE IS WHERE YOU
 ARE, HE EATS YOU UP AND YOU LOSE!

     YOU:
 EACH TURN YOU MAY MOVE OR SHOOT A CROOKED ARROW
   MOVING:  YOU CAN MOVE ONE ROOM (THRU ONE TUNNEL)
   ARROWS:  YOU HAVE 5 ARROWS.  YOU LOSE WHEN YOU RUN OUT
   EACH ARROW CAN GO FROM 1 TO 5 ROOMS. YOU AIM BY TELLING
   THE COMPUTER THE ROOM#S YOU WANT THE ARROW TO GO TO.
   IF THE ARROW CAN'T GO THAT WAY (IF NO TUNNEL) IT MOVES
   AT RANDOM TO THE NEXT ROOM.
     IF THE ARROW HITS THE WUMPUS, YOU WINф.
     IF THE ARROW HITS YOU, YOU LOSE.

    WARNINGS:
     WHEN YOU ARE ONE ROOM AWAY FROM A WUMPUS OR HAZARD,
     THE COMPUTER SAYS:
 WUMPUS:  'I SMELL A WUMPUS'
 BAT   :  'BATS NEARBY'
 PIT   :  'I FEEL A DRAFT'
"""
        expect(py, instructions_text)
        expect(bas, instructions_text)
        print("[+] TEST 2 - PASSED")

        # Добавление задержки перед вводом
        time.sleep(1)

        # Отправка команды "M" для перемещения
        print("sending move command...")
        write(py, 'M')
        write(bas, 'M')
        print("[+] MOVE COMMAND SENT")

        # Проверка запроса на перемещение
        move_prompt = "WHERE TO? "
        expect(py, move_prompt)
        expect(bas, move_prompt)
        print("[+] TEST 3 - PASSED")

        # Отправка номера комнаты для перемещения
        write(py, '2')
        write(bas, '2')
        print("[+] ROOM NUMBER SENT")

        # Проверка вывода после перемещения
        location_output = "YOU ARE IN ROOM 2\n"
        expect(py, location_output)
        expect(bas, location_output)
        print("[+] TEST 4 - PASSED")

        # Проверка предупреждений об опасности
        write(py, 'M')
        write(bas, '3')
        hazard_warning = "I FEEL A DRAFT"
        expect(py, hazard_warning)
        expect(bas, hazard_warning)
        print("[+] TEST 5 - Hazard Warning Passed")

        # Добавление задержки перед вводом
        time.sleep(1)

        # Отправка команды "S" для стрельбы
        print("sending shoot command...")
        write(py, 'S')
        write(bas, 'S')
        print("[+] SHOOT COMMAND SENT")

        # Проверка запроса на количество комнат для стрельбы
        shoot_prompt = "NO. OF ROOMS (1-5): "
        expect(py, shoot_prompt)
        expect(bas, shoot_prompt)
        print("[+] TEST 6 - Shoot Prompt Passed")

        # Отправка количества комнат для стрельбы
        write(py, '1')
        write(bas, '1')
        print("[+] NUMBER OF ROOMS SENT")

        # Проверка запроса на номер комнаты для стрельбы
        room_prompt = "ROOM #: "
        expect(py, room_prompt)
        expect(bas, room_prompt)
        print("[+] TEST 7 - Room Prompt for Shooting Passed")

        # Отправка номера комнаты для стрельбы
        write(py, '2')
        write(bas, '2')
        print("[+] ROOM NUMBER FOR SHOOTING SENT")

        # Проверка результата стрельбы
        shoot_result = "MISSED\n"
        expect(py, shoot_result)
        expect(bas, shoot_result)
        print("[+] TEST 8 - Shoot Result Passed")

    except Exception as ex:
        print(ex)

test()
