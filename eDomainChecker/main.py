import dns.resolver
import re
from typing import List, Dict


def validate_email_format(email: str) -> bool:
    """Проверяет базовый формат email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def extract_domain(email: str) -> str:
    """Извлекает домен из email-адреса"""
    return email.split('@')[1] if '@' in email else ''


def check_mx_records(domain: str) -> Dict[str, any]:
    """Проверяет MX-записи для домена"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return {
            'status': 'valid',
            'mx_count': len(mx_records),
            'mx_servers': [str(mx.exchange) for mx in mx_records]
        }
    except dns.resolver.NXDOMAIN:
        return {'status': 'domain_not_exists', 'error': 'Домен не существует'}
    except dns.resolver.NoAnswer:
        return {'status': 'no_mx', 'error': 'MX-записи отсутствуют'}
    except dns.resolver.NoNameservers:
        return {'status': 'no_mx', 'error': 'DNS серверы недоступны'}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}


def check_emails(email_list: List[str]) -> None:
    """Основная функция проверки списка email"""
    print("=" * 70)
    print("ПРОВЕРКА EMAIL-ДОМЕНОВ")
    print("=" * 70)

    for email in email_list:
        email = email.strip()

        if not email:
            continue

        print(f"\n📧 Email: {email}")

        # Проверка формата
        if not validate_email_format(email):
            print("   ❌ Статус: Некорректный формат email")
            continue

        # Извлечение домена
        domain = extract_domain(email)
        print(f"   🌐 Домен: {domain}")

        # Проверка MX-записей
        result = check_mx_records(domain)

        if result['status'] == 'valid':
            print(f"   ✅ Статус: Домен валиден")
            print(f"   📊 Найдено MX-записей: {result['mx_count']}")
            print(f"   🔧 MX-серверы: {', '.join(result['mx_servers'][:3])}")
        elif result['status'] == 'domain_not_exists':
            print(f"   ❌ Статус: Домен отсутствует")
        elif result['status'] == 'no_mx':
            print(f"   ⚠️  Статус: MX-записи отсутствуют или некорректны")
        else:
            print(f"   ❌ Статус: Ошибка проверки - {result['error']}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Пример 1: Список email прямо в коде
    emails = [
        "test@gmail.com",
        "example@yahoo.com",
        "info@nonexistentdomain12345.com",
        "user@nodns-domain.test",
        "invalid-email",
        "support@outlook.com"
    ]

    print("\n🔍 ВАРИАНТ 1: Проверка встроенного списка")
    check_emails(emails)

    # Пример 2: Чтение из файла
    print("\n\n🔍 ВАРИАНТ 2: Проверка из файла emails.txt")
    print("(Создайте файл emails.txt с email-адресами, по одному на строку)")

    try:
        with open('emails.txt', 'r', encoding='utf-8') as f:
            file_emails = f.readlines()
        check_emails(file_emails)
    except FileNotFoundError:
        print("⚠️  Файл emails.txt не найден. Создайте его для проверки.")

    # Пример 3: Ввод вручную
    print("\n\n🔍 ВАРИАНТ 3: Ручной ввод")
    print("Введите email-адреса (по одному на строку, пустая строка для завершения):")
    manual_emails = []
    while True:
        email = input("Email: ").strip()
        if not email:
            break
        manual_emails.append(email)

    if manual_emails:
        check_emails(manual_emails)