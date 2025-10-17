from jsktoolbox.configtool import Config

file = "/tmp/example.ini"
section = "TEST"

obj = Config(file, section)

# loading file
if obj.file_exists and obj.load():
    # getting 'SUBTEST' variables
    var01 = obj.get("SUBTEST", varname="test01")
    var02 = obj.get("SUBTEST", varname="test02")
    var03 = obj.get("SUBTEST", varname="test03")
    var04 = obj.get("SUBTEST", varname="test04")

    # getting main section variable
    var05 = obj.get(section, varname="test01")

    print(f"var01: {var01}, type: {type(var01)}")
    print(f"var02: {var02}, type: {type(var02)}")
    print(f"var03: {var03}, type: {type(var03)}")
    print(f"var04: {var04}, type: {type(var04)}")
    print(f"var05: {var05}, type: {type(var05)}")

    # getting non existing variable
    print(
        f"If variable not exists, method return: {obj.get('SUBTEST', varname='test05')}"
    )
