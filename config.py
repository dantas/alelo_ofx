import ConfigParser


section = 'DEFAULT'
filename = 'default.cfg'


def read():
    config = ConfigParser.ConfigParser()
    config.read(filename)
    return config.defaults()


def save(options):
    config = ConfigParser.ConfigParser()
    with open(filename, 'wb') as f:
        for key, value in options.iteritems():
            config.set(section, key, value)
        config.write(f)
