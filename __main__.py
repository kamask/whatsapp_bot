from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from xpath import *
from config import *


driver = webdriver.Chrome()


def main():
    driver.get('https://web.whatsapp.com')
    wait(driver, 1000).until(EC.presence_of_element_located((By.ID, 'side')))

    numbers = open("numbers.txt", "r")
    sended = open("sended.txt", "w")
    not_whatsapp = open("not_whatsapp.txt", "w")
    error_numbers = open("error_numbers.txt", "w")

    sended_count = 0
    not_sended_count = 0
    error_numbers_count = 0

    for number in numbers.readlines():

        if number[-1] == '\n':
            number = number[:-1]

        if number[0] == '+' and number[1] == '7' and len(number) == 12:
            number = number[1:]

        if number[0] == '8' and len(number) == 11:
            number = '7' + number[1:]

        if number[0] != '7' or len(number) != 11:
            error_numbers.write(number + "\n")
            error_numbers_count += 1
            continue

        if send(number):
            sended.write(number + "\n")
            sended_count += 1
        else:
            not_whatsapp.write(number + "\n")
            not_sended_count += 1

        print(f"Current: {number}, Sended: {sended_count}, Not WhatsApp: {not_sended_count}, All: {sended_count + not_sended_count + error_numbers_count}")

    numbers.close()
    sended.close()
    not_whatsapp.close()
    error_numbers.close()
    driver.quit()

    with open("sended.txt", "r") as file:
        sended = file.read()

    with open("sended.txt", "w") as file:
        file.write(f"Отправлено на {sended_count} номеров\n\n\n")
        file.write(sended)

    with open("not_whatsapp.txt", "r") as file:
        not_whatsapp = file.read()

    with open("not_whatsapp.txt", "w") as file:
        file.write(f"Нет whatsapp у {not_sended_count} номеров\n\n\n")
        file.write(not_whatsapp)

    with open("error_numbers.txt", "r") as file:
        error_numbers = file.read()

    with open("error_numbers.txt", "w") as file:
        file.write(f"Ошибка отправки на {error_numbers_count} номеров\n\n\n")
        file.write(error_numbers)


def send(number):
    driver.get('https://web.whatsapp.com/send?phone=' + number)
    driver.execute_script("window.onbeforeunload = function() {};")

    wait(driver, 1000).until(EC.presence_of_element_located(
        (By.ID, 'side')))

    try:
        wait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, not_number_in_whatsapp_xpath)))
        return False
    except TimeoutException:
        pass

    input_box = wait(driver, 1000).until(
        EC.presence_of_element_located((By.XPATH, input_box_xpath)))
    input_box.send_keys(message)

    input_box.send_keys(Keys.ENTER)

    wait(driver, 1000).until_not(EC.presence_of_element_located(
        (By.CSS_SELECTOR, sending_clock_icon_selector)))

    attach_button = wait(driver, 1000).until(EC.presence_of_element_located(
        (By.XPATH, attach_button_xpath)))
    attach_button.click()

    input_image = wait(driver, 1000).until(EC.presence_of_element_located(
        (By.XPATH, input_image_xpath)))
    input_image.send_keys(file_path)

    image_text_input = wait(driver, 1000).until(EC.presence_of_element_located(
        (By.XPATH, image_text_input_xpath)))
    image_text_input.send_keys(message_for_image)
    image_text_input.send_keys(Keys.ENTER)

    wait(driver, 1000).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, sending_clock_icon_selector)))

    wait(driver, 1000).until_not(EC.presence_of_element_located(
        (By.CSS_SELECTOR, sending_clock_icon_selector)))
    return True


if __name__ == '__main__':
    main()
