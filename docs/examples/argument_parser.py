import getopt
import sys


class ArgumentParser:
    def __init__(self, **kwargs):
        self._options = {}
        for option, value in kwargs.items():
            if len(option) == 1:
                self._options[option] = (option, True, None)
            else:
                self._options[option] = (option[2:], False, option[0])

    def parse_args(self, argv):
        print(f"{argv} -- {self._options.keys()}")
        print(f"{self._options}")
        options, args = getopt.getopt(argv, self._options.keys())
        for option, value in options:
            self._handle_option(option, value)

    def _handle_option(self, option, value):
        if value is None:
            value = ""
        options = str(self._options)
        key = self._options[option][0]
        if self._options[option][1]:
            self._options[key] = value
        else:
            self._options[key] = True

    def get_option(self, option):
        return self._options.get(option)


class MyApp:
    parser = None

    def __init__(self, **kwargs):
        self.parser = ArgumentParser(**kwargs)
        self.parser.parse_args(sys.argv[1:])
        self.verbose = self.parser.get_option("-v")
        self.file = self.parser.get_option("-f")

    def run(self):
        if self.verbose:
            print("Uruchomiono z opcjami:", self.parser._options)
        if self.file:
            print("Plik:", self.file)


if __name__ == "__main__":
    app = MyApp(verbose=True, file="myfile.txt")
    app.run()
