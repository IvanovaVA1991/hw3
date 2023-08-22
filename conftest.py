import pytest
from checkers import checkout, getout
import random, string
import yaml
from datetime import datetime
from pathlib import Path


with open('config.yaml') as f:
	data = yaml.safe_load(f)    # возвращается словарь


@pytest.fixture()
def make_folders():   # фикстура, которая создает каталоги
	file_path = Path(data.get('folder_in'))
	if not file_path.exists():
		return checkout("mkdir {} {} {} {}".format(data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']), "")


@pytest.fixture()
def clear_folders():   #фикстура для очистки каталогов
	return checkout("rm -rf {}/* {}/* {}/* {}/*".format(data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']), "")  # rm -rf - ключи -rf, чтобы рекурсивоно все очищалось

@pytest.fixture()
def make_files():     #фикстура для создания файлов(5шт) с рандомными именами и данными, объемом 1мб
	list_of_files = []
	for i in range(data['count']):
		filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))    # случайные символы из ascii + случайная цифра
		if checkout('cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'], filename), ''):	#	   dd - linux команда для генерации файлов, /dev/urandom - спец файлы линукс со случайными данными
												#of={} - параметр, куда записывать файлы (в filename)
												#bs=1M - размер 1М
												#iflag=fullblock - метода заполнения файла (плотнее)

			list_of_files.append(filename)          # если checkout успешно, то добавляем в список
	return list_of_files

@pytest.fixture()
def make_subfolder():   # создать файл и подкаталог
	testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
	if not checkout('cd {}; mkdir {}'.format(data['folder_in'], subfoldername), ''):         # если каталог не создан, не создается и файл
		return None, None

	if not checkout('cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['folder_in'], subfoldername, testfilename), ''):

		return subfoldername, None

	return subfoldername, testfilename


@pytest.fixture(autouse=True)    #autouse=True - автоматически дописывает фикстуру к каждому тесту
def print_time():   # вывод времени перед стартом и после
	print('Start: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))   # до выполнения теста
	yield print('Stop: {}'.format(datetime.now().strftime('%H:%M:%S.%f')))  # после выполнения теста

@pytest.fixture(autouse=True)
def stat_file():
	yield
	stat = getout('cat /proc/loadavg')
	checkout(f'echo "time: {datetime.now().strftime("%H:%M:%S.%f")} count: {data.get("count")} size: {data.get("bs")} load: {stat}">> stat.txt', '')
