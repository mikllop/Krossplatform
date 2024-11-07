from flask import Flask, render_template, request, redirect, url_for
import sys
from multiprocessing import Process
from time import sleep
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

app = Flask(__name__)


# 
@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/play", methods = ['GET', 'POST'])
def play():
    if request.method == 'POST':
        # Получение ввода от пользователя через веб-интерфейс
        user_input = request.form.get('user_input')
        if user_input:
            write_f('input.txt', user_input)
            sleep(3)

    # Проверяем существование файла перед чтением
    if not os.path.exists('print.txt'):
        write_f('print.txt', '')  # Создаем пустой файл, если он не существует

    # Чтение текущего вывода игры
    game_output = read_f('print.txt')
    return render_template('play.html', text=game_output)


def background_worker():
    """
    Запускает игру в фоновом режиме. Игра взаимодействует с файлами для получения ввода и вывода.
    """

    def input_handler(prompt):
        write_f('print.txt', prompt + '\n')
        while True:
            sleep(3) 
            if os.path.exists('input.txt'):
                user_input = read_f('input.txt')
                os.remove('input.txt')  # удаляем файл после чтения
                
                return user_input  # возвращаем пользовательский ввод

    # Очищаем файлы перед началом игры
    if os.path.exists('input.txt'):
        os.remove('input.txt')
    if os.path.exists('print.txt'):
        os.remove('print.txt')

    def custom_print(*args, end='\n'):
        # Если нет аргументов, просто выводим новую строку
        if not args:
            message = ''
        else:
            # Соединяем все переданные аргументы через пробел
            message = ' '.join(map(str, args))
        
        # Записываем сообщение и добавляем 'end' (по умолчанию это '\n')
        write_f('print.txt', message + end)

    # Переопределяем стандартные функции ввода и вывода в main
    main.input = input_handler
    main.print = custom_print

    # Запускаем вашу игру (например, функцию в вашем игровом файле)
    main.nachalo()
    main.main()


def read_f(file):
    with open(file, 'r') as f:
        return f.read()


def write_f(file, text):
    with open(file, 'a') as f:
        f.write(text)


if __name__ == '__main__':
    # Создаем файл print.txt, если он не существует, перед запуском сервера
    if not os.path.exists('print.txt'):
        write_f('print.txt', '')

    # Запуск фонового процесса с игрой
    process = Process(target=background_worker)
    process.start()

    # Запуск веб-сервера Flask
    app.run(debug=True)

# flask --app {file} run
