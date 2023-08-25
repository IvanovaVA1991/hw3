import yaml
from ssh_checkers import ssh_checkout, ssh_getout

with open('config.yaml') as f:
    data = yaml.safe_load(f)  # возвращается словарь


class TestPositive:
    def test_step1(self, make_folders, clear_folders, make_files): 
        # test1
        res1 = ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}/arx",
                                "Everything is Ok")
        res2 = ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"ls {data.get('folder_out')}", "arx.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}/arx2", "Everything is Ok"))
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_out')}; 7z e arx2.7z -o{data.get('folder_ext')} -y", "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"ls {data.get('folder_ext')}"), item))
        assert all(res), "test2 FAIL"  

    def test_step3(self):
        # test3
        assert ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_out')}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"

    def test_step4(self):
        # test4
        assert ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z u arx2.7z", "Everything is Ok"), "test4 FAIL"

    def test_step5(self, clear_folders, make_files):
        # test5
        res = []
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}/arx2", "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_out')}; 7z l arx2.7z", item))
        assert all(res), "test5 FAIL"


    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}/arx", "Everything is Ok"))
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_out')}; 7z x arx.7z -o {data.get('folder_ext2')} -y", "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"ls {data.get('folder_ext2')}", item))
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"ls {data.get('folder_ext2')}", make_subfolder[0]))
        res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"ls {data.get('folder_ext2')}/{make_subfolder[0]}", make_subfolder[1]))
        assert all(res), "test6 FAIL"


    def test_step7(self):
        # test7
        assert ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_out')}; 7z d arx.7z", "Everything is Ok"), "test7 FAIL"


    def test_step8(self, clear_folders, make_files):
        # test8
        res = []
        for item in make_files:
            res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z h {item}", "Everything is Ok"))
            hash = ssh_getout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; crc32 {item}").upper()
            res.append(ssh_checkout(data.get('ip'), data.get('user'), data.get('passwd'), f"cd {data.get('folder_in')}; 7z h {item}", hash))
        assert all(res), "test8 FAIL"
