from yaml import load, FullLoader
PATH_YAML_CONFIG = r'./config/config.yml'

def loadParametersYml():
    with open(PATH_YAML_CONFIG) as file:
        parameters = load(file, Loader=FullLoader)
        return parameters


if __name__ == '__main__':
    print(loadParametersYml())
