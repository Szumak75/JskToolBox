from jsktoolbox.configtool import Config

file = "/tmp/example.ini"
section = "TEST"

obj = Config(file, section)

# main section description
obj.set(section, desc="This is example configuration file,")
obj.set(section, desc="showing how to use the 'Config' class.")

# add subsection description
obj.set("SUBTEST", desc="This is subsection description")

# add a bundle of subsection variables with different types
obj.set("SUBTEST", varname="test01", value=1)
obj.set("SUBTEST", varname="test02", value=3.14, desc="PI number")
obj.set("SUBTEST", varname="test03", value="example string")
obj.set("SUBTEST", varname="test04", value=False)

# add variable to the main section
obj.set(section, varname="test01", value=[1, "a", True], desc="a list value")

# write configuration file
obj.save()
