import json


FILENAME = "contacts.json"

def show_menu():
    """Показать меню и получить от пользователя номер команды."""
    menu =  """
    1. Открыть файл
    2. Сохранить файл
    3. Показать все контакты
    4. Добавить контакт
    5. Найти контакт
    6. Изменить контакт
    7. Удалить контакт
    8. Выйти
    """
    print("-" * 30)
    print("Вас приветствует программа 'Телефонный справочник'.")
    print(menu)
    command = input("Введите команду (1-8): ")
    return command


def process_command(contacts, key):
    """Обработка команды пользователя."""
    match key:
        case '1':
            contacts = load_contacts(FILENAME)
        case '2':
            save_contacts(FILENAME, contacts)
        case '3':
            show_contacts(contacts)
        case '4':
            add_contact(contacts)
        case '5':
            text = input("Введите id контакта либо его имя, либо телефон или комментарий: ")
            find_contact(contacts, text)
        case '6':
            edit_contact(contacts)
        case '7':
            delete_contact(contacts)
        case '8':
            answer = input("Несохранённые контакты будут удалены. Вы уверены, что хотите выйти? Да/Нет: ")
            if answer == 'Да':
                return contacts, False
        case _:
            print("Нет такой команды.")
    return contacts, True


def load_contacts(filename):
    """Открываем файл."""
    try:
        with open(filename, encoding='utf-8') as file:
            print("Файл контактов открыт.")
            return json.load(file)
    except FileNotFoundError:
        print("Фойла контактов нет.")
        return []


def save_contacts(filename, contacts):
    """Сохраняем файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(
            contacts,
            file,
            ensure_ascii=False,
            indent=4
        )
    print("Файл сохранён.")


def show_contacts(contacts):
    """Показываем контакты."""
    if not contacts:
        print("Списка контактов нет.")
        return

    for contact in contacts:
        print('-' * 20)
        print_contact(contact)


def add_contact(contacts):
    """Добавляем новый контакт."""
    name = input("Введите имя: ")
    phone = input("Введите номер телефона: ")
    comment = input("Введите комментарий: ")
    if contacts:
        new_id = max(contact["id_user"] for contact in contacts) + 1
    else:
        new_id = 1

    new_contact = {
        "id_user": new_id,
        "name": name,
        "phone": phone,
        "comment": comment
    }
    contacts.append(new_contact)
    print("Новый контакт добавлен.")


def find_contact(contacts, search_text):
    """Ищем контакт."""
    if not contacts:
        print("Списка контактов нет.")
        return

    search_text = search_text.lower()
    found = False

    for contact in contacts:
        name = str(contact.get("name", "")).lower()
        phone = str(contact.get("phone", "")).lower()
        comment = str(contact.get("comment", "")).lower()

        if (
            search_text in name
            or search_text in phone
            or search_text in comment
        ):
            print("Найден контакт: ")
            print_contact(contact)
            found = True

    if not found:
        print("Такого контакта нет.")


def edit_contact(contacts):
    """Изменяем контакт."""
    if not contacts:
        print("Списка контактов нет.")
        return

    try:
        find_id = int(input("Введите ID: "))
    except ValueError:
        print("ID должен быть числом")
        return

    flag = False
    for contact in contacts:
        if find_id == contact["id_user"]:
            print("Найден контакт: ")
            print_contact(contact)
            contact["name"] = input("Введите новое имя: ")
            contact["phone"] = input("Введите новый номер телефона: ")
            contact["comment"] = input("Введите новый комментарий: ")
            print("Данные обновлены.")
            flag = True
            break

    if not flag:
        print("Контакт не найден.")


def delete_contact(contacts):
    """Удаляем контакт."""
    if not contacts:
        print("Списка контактов нет.")
        return

    try:
        find_id = int(input("Введите ID: "))
    except ValueError:
        print("ID должен быть числом")
        return
    for contact in contacts:
        if find_id == contact["id_user"]:
            contacts.remove(contact)
    else:
        print("Контакт не найден.")


def print_contact(contact):
    """Печать одного контакта."""
    print(
        f"ID: {contact['id_user']}\n"
        f"Имя: {contact['name']}\n"
        f"Телефон: {contact['phone']}\n"
        f"Комментарий: {contact['comment']}"
    )


def main():
    """Главный цикл работы приложения."""
    contacts = []
    is_running = True

    while is_running:
        choice = show_menu()
        contacts, is_running = process_command(contacts, choice)

        if not is_running:
            break
    print("Завершаю работу. До свидания.")


main()