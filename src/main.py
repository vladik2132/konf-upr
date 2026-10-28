import argparse
import os
import socket
import sys

# Настройка парсера аргументов командной строки для Этапа 2 (Вариант 13)
parser = argparse.ArgumentParser(description="Эмулятор языка оболочки ОС (Этап 2)")
parser.add_argument("vfs", nargs="?", default="", help="Путь к физическому расположению VFS")
parser.add_argument("script", nargs="?", default="", help="Путь к стартовому скрипту")
args = parser.parse_args()

# Требование: отладочный вывод всех заданных параметров при запуске
print("=== Отладка: Параметры запуска эмулятора ===")
print(f"Путь к VFS          : {args.vfs if args.vfs else '[не указан]'}")
print(f"Путь к скрипту      : {args.script if args.script else '[не указан]'}")
print("==============================================")

def execute_command(line):
    """Функция обработки и выполнения отдельной команды."""
    # Раскрытие переменных окружения (например, $HOME)
    expanded_line = os.path.expanduser(line)
    expanded_line = os.path.expandvars(expanded_line)
    parts = expanded_line.split()
    
    if not parts:
        return True, ""
    
    cmd = parts[0]
    cmd_args = parts[1:]
    
    if cmd == "exit":
        return False, "exit"
    elif cmd in ("ls", "cd"):
        output = f"Команда: {cmd}, Аргументы: {cmd_args}"
        print(output)
        return True, output
    else:
        # Сообщение об ошибке выполнения команды
        error_msg = f"Ошибка: неизвестная команда или неверные аргументы: {cmd}"
        print(error_msg, file=sys.stderr)
        return "error", error_msg

# Обработка стартового скрипта (если он передан)
if args.script:
    if os.path.exists(args.script):
        try:
            with open(args.script, "r", encoding="utf-8") as f:
                for line_num, script_line in enumerate(f, 1):
                    script_line = script_line.strip()
                    # Пропуск пустых строк и комментариев (в стиле Python: '#')
                    if not script_line or script_line.startswith("#"):
                        continue
                    
                    # Имитация диалога: отображение ввода (приглашения и команды)
                    prompt = f"{os.getlogin()}@{socket.gethostname()}:~$ "
                    print(f"{prompt}{script_line}")
                    
                    status, _ = execute_command(script_line)
                    
                    if status == False:  к команда exit в скрипте
                        sys.exit(0)
                    elif status == "error":
                        # Требование Варианта 13: останавливается при первой ошибке
                        print(f"Ошибка в стартовом скрипте '{args.script}' на строке {line_num}. Остановка выполнения.", file=sys.stderr)
                        sys.exit(1)
        except Exception as e:
            print(f"Ошибка при чтении стартового скрипта: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"Ошибка: файл стартового скрипта не найден: {args.script}", file=sys.stderr)
        sys.exit(1)

# Основной интерактивный цикл REPL (если скрипт не задан или уже завершился)
while True:
    try:
        prompt = f"{os.getlogin()}@{socket.gethostname()}:~$ "
        line = input(prompt).strip()
        if not line:
            continue
        
        status, _ = execute_command(line)
        if status == False:
            break
    except (KeyboardInterrupt, EOFError):
        print("\nexit")
        break