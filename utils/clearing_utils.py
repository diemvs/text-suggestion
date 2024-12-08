from email import message_from_string
import re

def get_message_body(message: str) -> str:
    # Парсим письмо
    email_message = message_from_string(message)
    # Получаем тело письма
    return email_message.get_payload(decode=True).decode(email_message.get_content_charset() or 'utf-8')

def clear_message_body(message: str) -> str:
    # Получаем тело письма
    body = get_message_body(message)

    # Удаляем строки с ключами To:, From:, RE:, и подобными
    meta_info_pattern = r'(To:|From:|Subject:|CC:|BCC:|RE:|Sent:|cc:|RE:).*$'
    body = re.sub(meta_info_pattern, '', body, flags=re.MULTILINE)

    # Удаляем текст, идущий после -----Original Message----- до первой пустой строки
    original_message_pattern = r'-----Original Message-----.*?\n\n'
    body = re.sub(original_message_pattern, '', body, flags=re.DOTALL)

    # Удаляем адреса электронной почты
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    body = re.sub(email_pattern, '', body)

    # Удаляем даты (формат: день, месяц, год, например: 14 May 2001 или 28/11/2001)
    date_pattern = r'\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s+[A-Za-z]{3,9}\s+\d{2,4})\b'
    body = re.sub(date_pattern, '', body)

    # Удаляем время (формат: 14:30, 8:17 AM, 16:39:00)
    time_pattern = r'\b(?:[01]?\d|2[0-3]):([0-5]?\d)(?::([0-5]?\d))?\b|\d{1,2}:\d{2}\s?(AM|PM)?\b'
    body = re.sub(time_pattern, '', body)

    # Удаляем disclaimers (юридические уведомления, например текст после *****)
    disclaimer_pattern = r'\n\*+.*?This e-mail.*?(?:\n\*+|\Z)'
    body = re.sub(disclaimer_pattern, '', body, flags=re.DOTALL)
    
    # Удаляем числа
    number_pattern = r'\b\d+\b'  # Находит числа (одну или более цифр)
    body = re.sub(number_pattern, '', body)

    # Убираем дополнительные пробелы
    body = re.sub(r'\s+', ' ', body).strip()
    
    # Убираем все символы, которые не являются буквами
    body = re.sub(r'[^\w\s]', '', body)

    return body