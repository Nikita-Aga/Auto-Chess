# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.remote.webdriver import By
# import selenium.webdriver.support.expected_conditions as EC  # noqa
# from selenium.webdriver.support.wait import WebDriverWait
# import pickle
# import undetected_chromedriver as uc
# import pickle
# import time
# driver = uc.Chrome(headless=False,version_main=119)
# driver.get("https://www.chess.com/play")
# print(1)
# time.sleep(180)
# print(2)
# pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# print(3)

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import pickle
import undetected_chromedriver as uc
import pickle
import time
import chess
import chess.engine
import logging
l = [["1" for i in range(8)] for i in range(8)]
logger2 = logging.getLogger(__name__)
logger2.setLevel(logging.DEBUG)

handler2 = logging.FileHandler(f"{__name__}.log", mode='w')
formatter2 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

# добавление форматировщика к обработчику
handler2.setFormatter(formatter2)
# добавление обработчика к логгеру
logger2.addHandler(handler2)
engine = chess.engine.SimpleEngine.popen_uci(r"D:\stockfish\stockfish-windows-x86-64-avx2.exe")

logger2.info("Library done!")

driver = uc.Chrome(headless=False,version_main=119)
logger2.info("Chrome done!")
driver.get("https://www.chess.com/play")
cookies = pickle.load(open(f"cookies.pkl", "rb"))
for cookie in cookies: driver.add_cookie(cookie)
driver.get("https://www.chess.com/play")
logger2.info("Chrome full done!")
w_b = "w"
time.sleep(5)
def ches():
	l = [["1" for i in range(8)] for i in range(8)]
	print("start")
	for i in range(8):
		for j in range(8):
			try:
				x = driver.find_elements(By.CLASS_NAME, f"square-{i+1}{j+1}")[-1].get_attribute("class")
				logger2.debug(x)
				x = x.split(" ")
				if x[0] == "piece":
					z = x[1]
					if z[0] == "w": z = z[1].upper()
					if z[0] == "b": z = z[1]
					l[7-j][i] = z
			except Exception as e:
				pass

	# for i in l:
	# 	logger2.info(str(*i))

	for i in range(len(l)):
		for s in range(len(l[i])):
			if l[i][s] == "1" and s>0 and l[i][s-1].isdigit():
				l[i][s] = str(int(l[i][s-1])+1)
				l[i][s-1] = ""



	f = ""
	for i in l:
		for s in i:
			f = f + s
		f = f + "/"

	f = f[:-1]
	f = f + f" {w_b} KQkq - 0 1"
	logger2.info(f"FEN {f}")
	board = chess.Board(f)
	if board.is_variant_end():
		run = False
		return
	logger2.info(str(board))
	
	result = engine.play(board, chess.engine.Limit(time=0.1))
	print(result.move)
	board.push(result.move)
	m = str(result.move)[:2]
	if m[0]=="a": m = "1"+m[1:]
	if m[0]=="b": m = "2"+m[1:]
	if m[0]=="c": m = "3"+m[1:]
	if m[0]=="d": m = "4"+m[1:]
	if m[0]=="e": m = "5"+m[1:]
	if m[0]=="f": m = "6"+m[1:]
	if m[0]=="g": m = "7"+m[1:]
	if m[0]=="h": m = "8"+m[1:]
	driver.find_element(By.CLASS_NAME, f"square-{m}").click()
	m = str(result.move)[2:]
	if m[0]=="a": m = "1"+m[1:]
	if m[0]=="b": m = "2"+m[1:]
	if m[0]=="c": m = "3"+m[1:]
	if m[0]=="d": m = "4"+m[1:]
	if m[0]=="e": m = "5"+m[1:]
	if m[0]=="f": m = "6"+m[1:]
	if m[0]=="g": m = "7"+m[1:]
	if m[0]=="h": m = "8"+m[1:]
	time.sleep(1)
	if len(m) == 3: 
		time.sleep(10)
		return
	element = driver.find_element(By.CLASS_NAME, f"square-{m}")
	x = element.location["x"]
	y = element.location["y"]
	actionChains = ActionChains(driver)
	actionChains.move_to_element(element).click().perform()

	
	
	logger2.info(str(board))


run = True
input("start??")
w_b = "w" if driver.find_elements(By.CLASS_NAME, "clock-component")[1].get_attribute("class").split(" ")[2] == "clock-white" else "b"
while True:


	if run:
		if len(driver.find_elements(By.CLASS_NAME, "clock-component")[1].get_attribute("class").split(" ")) == 4:
			try:
				time.sleep(0.2)
				ches()
			except Exception as e:
				print(e)
	else:
		input("start??")
		w_b = "w" if driver.find_elements(By.CLASS_NAME, "clock-component")[1].get_attribute("class").split(" ")[2] == "clock-white" else "b"
		run=True


logger2.info("Programm finish!")
time.sleep(10)
driver.quit()