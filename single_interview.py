# single_brainhire_interview.py
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class BrainHireInterviewer:
    def __init__(self):
        self.driver = None
        self.wait = None
        # Путь к папке с аудиоответами (измените при необходимости)
        self.audio_dir = r"C:\Users\Sergio\Desktop\ЗвуковоеИнтервью"
        self.url = "https://bh75.brainhire.tech/interview/personal/64cd9d71-779a-4918-884a-805b89beb140"

    def play_audio(self, filename):
        path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(path):
            print(f"❌ Аудиофайл не найден: {path}")
            return False
        try:
            subprocess.run(f'start "" "{path}"', shell=True)
            print(f"🔊 Воспроизведение: {filename}")
            return True
        except Exception as e:
            print(f"⚠️ Ошибка воспроизведения {filename}: {e}")
            return False

    def setup_browser(self):
        print("🚀 Запускаем браузер...")
        options = Options()
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--autoplay-policy=no-user-gesture-required")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        prefs = {
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Браузер готов. Убедитесь, что OBS и Virtual Audio Cable активны!")

    def click_button_by_text(self, text, description=""):
        """Надёжный клик по кнопке с текстом."""
        try:
            xpath = f"//button[contains(normalize-space(.), '{text}')]"
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(0.5)

            if not btn.is_displayed() or not btn.is_enabled():
                print(f"⚠️ Кнопка '{text}' не видна или не активна")
                return False

            try:
                btn.click()
                print(f"✅ {description or f'Нажата кнопка: {text}'}")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠️ Обычный клик не сработал: {e}")

            from selenium.webdriver.common.action_chains import ActionChains
            try:
                ActionChains(self.driver).move_to_element(btn).click().perform()
                print(f"✅ ActionChains клик: '{text}'")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠️ ActionChains не сработал: {e}")

            try:
                self.driver.execute_script("arguments[0].click();", btn)
                print(f"✅ JavaScript клик: '{text}'")
                time.sleep(2)
                return True
            except Exception as e:
                print(f"⚠️ JavaScript клик не сработал: {e}")

            return False
        except Exception as e:
            print(f"❌ Не удалось нажать кнопку '{text}': {e}")
            return False

    def force_click_next_button(self):
        """Искусственные методы для React-кнопок."""
        print("🎯 ИСКУССТВЕННОЕ НАЖАТИЕ КНОПКИ 'ДАЛЕЕ'...")
        time.sleep(3)

        methods = [
            self._method_direct_function_call,
            self._method_react_props,
            self._method_dom_manipulation,
            self._method_event_bypass,
            self._method_prototype_hack
        ]

        for i, method in enumerate(methods, 1):
            print(f"🔄 Метод {i}/5...")
            if method():
                print(f"✅ Метод {i} сработал!")
                return True
            time.sleep(2)
        return False

    # --- Все 5 методов оставлены без изменений (как в вашем коде) ---
    def _method_direct_function_call(self):
        try:
            script = """
            const buttons = Array.from(document.querySelectorAll('button'));
            const nextBtn = buttons.find(btn => btn.textContent && btn.textContent.includes('Далее'));
            if (nextBtn) {
                if (nextBtn.onclick) nextBtn.onclick(new MouseEvent('click'));
                const reactKey = Object.keys(nextBtn).find(key => key.startsWith('__reactProps'));
                if (reactKey && nextBtn[reactKey].onClick) {
                    nextBtn[reactKey].onClick(new MouseEvent('click'));
                }
                nextBtn.dispatchEvent(new Event('click', { bubbles: true, cancelable: true }));
                nextBtn.focus();
                nextBtn.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
                nextBtn.dispatchEvent(new KeyboardEvent('keyup', { key: 'Enter' }));
                return true;
            }
            return false;
            """
            return self.driver.execute_script(script)
        except:
            return False

    def _method_react_props(self):
        try:
            script = """
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent && btn.textContent.includes('Далее')) {
                    const reactKey = Object.keys(btn).find(key =>
                        key.startsWith('__reactProps') || key.startsWith('__reactEventHandlers')
                    );
                    if (reactKey) {
                        const props = btn[reactKey];
                        if (props.onClick) props.onClick({ preventDefault: () => {} });
                        if (props.onMouseDown) props.onMouseDown({ preventDefault: () => {} });
                        if (props.onMouseUp) props.onMouseUp({ preventDefault: () => {} });
                        if (props.onTouchEnd) props.onTouchEnd({ preventDefault: () => {} });
                        btn.click();
                        return true;
                    }
                }
            }
            return false;
            """
            return self.driver.execute_script(script)
        except:
            return False

    def _method_dom_manipulation(self):
        try:
            script = """
            const originalBtn = document.querySelector('button.chakra-button.css-1s89inu');
            if (!originalBtn) return false;
            originalBtn.outerHTML = originalBtn.outerHTML;
            const newBtn = document.querySelector('button.chakra-button.css-1s89inu');
            if (newBtn) {
                newBtn.onclick = () => console.log('✅ Искусственный клик');
                newBtn.click();
                return true;
            }
            return false;
            """
            return self.driver.execute_script(script)
        except:
            return False

    def _method_event_bypass(self):
        try:
            script = """
            const btn = document.querySelector('button.chakra-button.css-1s89inu');
            if (!btn) return false;
            const originalAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function() {
                if (this === btn && (arguments[0] === 'click' || arguments[0] === 'mousedown')) {
                    return;
                }
                return originalAddEventListener.apply(this, arguments);
            };
            btn.click();
            EventTarget.prototype.addEventListener = originalAddEventListener;
            return true;
            """
            return self.driver.execute_script(script)
        except:
            return False

    def _method_prototype_hack(self):
        try:
            script = """
            const btn = document.querySelector('button.chakra-button.css-1s89inu');
            if (!btn) return false;
            const originalClick = HTMLElement.prototype.click;
            HTMLElement.prototype.click = function() {
                if (this === btn) {
                    originalClick.call(this);
                    return;
                }
                return originalClick.apply(this, arguments);
            };
            btn.click();
            HTMLElement.prototype.click = originalClick;
            return true;
            """
            return self.driver.execute_script(script)
        except:
            return False

    def check_checkboxes(self):
        try:
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, "svg[data-state='unchecked']")
            for i, svg in enumerate(checkboxes):
                try:
                    parent = svg.find_element(By.XPATH, "./ancestor::*[contains(@class, 'chakra-checkbox')]")
                    self.driver.execute_script("arguments[0].click();", parent)
                except:
                    self.driver.execute_script("arguments[0].click();", svg)
                print(f"✅ Чекбокс {i + 1} отмечен")
                time.sleep(0.5)
            return True
        except Exception as e:
            print(f"⚠️ Ошибка при отметке чекбоксов: {e}")
            return False

    def handle_questions(self):
        """Обработка 5 вопросов с голосовыми ответами."""
        print("❓ Начинаем ответы на 5 вопросов...")
        time.sleep(5)

        for q_num in range(1, 6):
            print(f"\n🎯 Вопрос {q_num}/5")

            # Пауза "на размышление"
            time.sleep(3)

            # Воспроизведение аудио
            self.play_audio(f"q{q_num}.mp3")

            # Ожидание ответа (~25 сек)
            time.sleep(27)

            # Переход к следующему вопросу или завершение
            if q_num < 5:
                success = self.click_button_by_text("Перейти к следующему вопросу", f"Вопрос {q_num} → далее")
                if not success:
                    print("⚠️ Пробуем force_click...")
                    self.force_click_next_button()
            else:
                self.click_button_by_text("Завершить", "Завершение интервью")

            time.sleep(2)

    def run(self):
        try:
            self.setup_browser()
            print("\n" + "=" * 60)
            print("🎬 НАЧИНАЕМ ИНТЕРВЬЮ")
            print("=" * 60)

            # 1. Согласие
            self.driver.get(self.url)
            time.sleep(4)
            self.check_checkboxes()
            self.click_button_by_text("Продолжить", "Согласие")

            # 2. Начало интервью
            self.click_button_by_text("Начать интервью", "Начало интервью")

            # 3. Speed Test
            self.click_button_by_text("Начать проверку скорости Интернета", "Speed test")
            time.sleep(12)
            self.click_button_by_text("Отлично, идем дальше", "Завершение Speed Test")

            # 4. Камера
            self.click_button_by_text("Проверить камеру", "Камера")
            time.sleep(6)

            # Ждём активации камеры
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Камера в порядке')]")))
                print("✅ Камера активна!")
            except:
                print("⚠️ Камера не распознана — продолжаем...")

            # 5. Переход от камеры
            success = self.force_click_next_button()
            if success:
                print("🎉 Успешно перешли к микрофону!")
            else:
                print("⚠️ Не удалось нажать 'Далее' после камеры")

            # 6. Микрофон
            self.click_button_by_text("Начать запись", "Начало записи")
            time.sleep(2)

            # Воспроизводим тест микрофона (опционально)
            mic_test = os.path.join(self.audio_dir, "mic_test.mp3")
            if os.path.exists(mic_test):
                subprocess.run(f'start "" "{mic_test}"', shell=True)
                print("🔊 Тест микрофона запущен")

            time.sleep(7)
            self.click_button_by_text("Остановить запись", "Остановка записи")
            time.sleep(3)
            self.click_button_by_text("Далее", "После микрофона")

            # 7. Инструкции
            self.click_button_by_text("Все понятно", "Инструкция")
            self.click_button_by_text("Перейти к вопросам", "К вопросам")

            # 8. Вопросы
            self.handle_questions()

            print("\n🎉 ИНТЕРВЬЮ ЗАВЕРШЕНО!")
            time.sleep(15)

        except Exception as e:
            print(f"💥 Критическая ошибка: {e}")
            time.sleep(20)
        finally:
            self.driver.quit()
            print("🔚 Браузер закрыт")


if __name__ == "__main__":
    print("🎯 BRAINHIRE — Интервью с 5 вопросами и голосовыми ответами")
    bot = BrainHireInterviewer()
    bot.run()