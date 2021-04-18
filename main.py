from yaml import load, FullLoader
path_yaml_config = r'./config/config.yml'

def loadParametersYml():
    with open(path_yaml_config) as file:
        parameters = load(file, Loader=FullLoader)
        return parameters


if __name__ == '__main__':
    print(loadParametersYml())
